import json
import requests
import hashlib


class WikiCountry:
    URL = 'https://en.wikipedia.org/wiki/'

    def __init__(self, filename_in, filename_out):
        self.outfile = filename_out
        with open(filename_in, 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            self.countries_list = [country['name']['common']
                                   for country in metadata]
            self.end = len(self.countries_list)
        with open(self.outfile, 'w', encoding='utf-8') as file:
            file.write('[    \n')

    def __iter__(self):
        self.cursor = 0
        return self

    def __next__(self):
        if self.cursor == self.end:
            with open(self.outfile, 'a', encoding='utf-8') as file:
                file.truncate(file.tell() - 3)
                file.write('\n]')
            raise StopIteration

        country = self.countries_list[self.cursor]
        link = self.URL + country
        req = requests.get(link)
        self.cursor += 1

        if req.ok:
            with open(self.outfile, 'a', encoding='utf-8') as file:
                file.write('    {"country":' + '"' + country + '"' +
                           ',\n     "url": ' + '"' + link + '"' + '\n    },\n')
                return (f"{country} and its wiki_link"
                        f" write to {self.outfile} file"
                        )
        else:
            return f"info about {country} not in wiki"


def md5_hash(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield hashlib.md5(line.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    countries = WikiCountry('countries.json', 'output.json')

    for item in countries:
        print(item)

    for i in md5_hash('output.json'):
        print(i)
