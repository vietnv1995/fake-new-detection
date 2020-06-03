from typing import List, Tuple
from pprint import pprint

import requests
import pandas as pd
from bs4 import BeautifulSoup


def _get_triples(tr):
    if tr == None:
        return []
    
    left = tr.td
    right = left.next_sibling
    
    objects = []
    predicate = left.text.split(':')[1].split(' ')[0].split('/')[-1]
    predicate = predicate.strip()

    for li in right.find_all('li'):
        if li.small:
            li.small.extract()
        objects.append(li.text)

    objects = [obj.strip(':') for obj in objects]
    objects = [obj.strip() for obj in objects]

    return [(predicate, obj) for obj in objects]


def get_triples(subject: str) -> List[Tuple[str, str, str]]:
    """Return a tuple include subject-predicate-object
    """

    url = f'http://dbpedia.org/page/{subject}'
    response = requests.get(url)

    result = []

    soup = BeautifulSoup(response.text, 'html.parser')
    for tr in soup.find_all('tr', 'odd'):
        result += _get_triples(tr)
    for tr in soup.find_all('tr', 'even'):
        result += _get_triples(tr)

    result = [(subject, r[0], r[1]) for r in result]
    result = [t for t in (set(tuple(i) for i in result))]
    result = sorted(result)

    return result


def save_triple_to_file(subject):
    triples = get_triples(subject)
    df = pd.DataFrame(triples, columns=['subject', 'predicate', 'object'])
    df.to_csv(f'{subject}.csv', encoding='utf-8')


if __name__ == '__main__':
    save_triple_to_file('Bill_Gates')
