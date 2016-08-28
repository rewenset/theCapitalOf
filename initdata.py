import pickle
import os


def create_file():
    import urllib.request
    import json

    def is_country_suitable(country):
        for key in country.keys():
            if country[key] == '':
                return False
        return True

    url = 'https://restcountries.eu/rest/v1/all'

    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()

    data = json.loads(resp_data.decode('utf-8'))

    list_of_keys = list(data[0].keys())
    list_of_keys.remove('name')
    list_of_keys.remove('capital')
    list_of_keys.remove('region')
    list_of_keys.remove('nativeName')

    regions = set()
    for country in data:
        for key in list_of_keys:
            del country[key]  # removing unnecessary information

        regions.add(country['region'])
    regions.remove('')

    countries = list(filter(is_country_suitable, data))  # it's removing only 5 countries with not enough information

    data = {
        'countries': countries,
        'regions': list(regions)
    }

    here = os.path.dirname(__file__)
    dbpath = os.path.join(here, 'countries')
    dbfile = open(dbpath, 'wb')
    pickle.dump(data, dbfile)
    dbfile.close()


def get_countries():
    here = os.path.dirname(__file__)
    dbpath = os.path.join(here, 'countries')
    dbfile = open(dbpath, 'rb')
    data = pickle.load(dbfile)
    length = len(data['countries'])
    return length, data


if __name__ == '__main__':
    create_file()
