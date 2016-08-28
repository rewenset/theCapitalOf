from flask import Flask, render_template, request, redirect, url_for, flash
from random import randrange, shuffle, choice
from initdata import get_countries

app = Flask(__name__)

size, data = get_countries()
countries = data['countries']
shuffle(countries)
# regions = data['regions']
real_answer = ''
counter = 0
score = 0


@app.route('/', methods=['GET', 'POST'])
@app.route('/<answer>', methods=['GET', 'POST'])
def the_capital_of(answer=None):
    global score, real_answer
    if request.method == 'GET':
        if answer:
            pass  # think out smth later

        if request.cookies.get('theCapitalOfScore') is None:
            return redirect(url_for('newgame'))
        else:
            score_cookie = request.cookies.get('theCapitalOfScore')
            score = int(score_cookie)

        real_answer = choice(['left', 'right'])

        global counter
        counter += 1

        if counter == size:
            return redirect(url_for('gameover'))

        # print(real_answer)  # cheating

        context = {
            'country': countries[counter]['name'],
            'capital1': '',
            'capital2': '',
            'score': score
        }

        numbers = list(range(0, counter)) + list(range(counter + 1, size))
        rand_number = choice(numbers)

        if real_answer == 'left':
            context['capital1'] = countries[counter]['capital']
            context['capital2'] = countries[rand_number]['capital']
        else:
            context['capital1'] = countries[rand_number]['capital']
            context['capital2'] = countries[counter]['capital']

        return render_template('theCapitalOf.html', context=context)
    else:
        answer = request.form['value']
        ret = False
        if answer == real_answer:
            score += 1
            ret = True
        response = app.make_response(redirect(url_for('the_capital_of', answer=ret)))
        response.set_cookie('theCapitalOfScore', str(score))
        return response


@app.route('/gameover')
def gameover():
    score_cookie = request.cookies.get('theCapitalOfScore')
    score = int(score_cookie)
    return render_template('gameover.html', score=score)


@app.route('/newgame')
def newgame():
    global countries, counter, score
    shuffle(countries)
    counter = 0
    score = 0
    response = app.make_response(redirect(url_for('the_capital_of')))
    response.set_cookie('theCapitalOfScore', str(score))
    return response


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()
