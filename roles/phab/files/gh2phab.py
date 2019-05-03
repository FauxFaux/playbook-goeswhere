import sys
from typing import List, Iterator

import requests


def main():
    # FauxFaux
    gh = sys.argv[1]

    # https://phabricator.goeswhere.com/api
    conduit = sys.argv[2]

    with open('phabricator-api-key') as f:
        phabricator_api_key = f.read().strip()

    resp = requests.post('{}/diffusion.repository.search'.format(conduit), {
        'api.token': phabricator_api_key,
    })
    assert resp.ok
    has = set(phab_has(resp.json()))
    want = set(gh_has(gh))

    print(want - has)


def phab_has(doc) -> Iterator[str]:
    repos = doc['result']['data']
    for repo in repos:
        fields = repo['fields']
        name = fields['name']
        view_policy = fields['policy']['view']
        if 'public' != view_policy:
            print('{}: skipping as .view.policy is {}'.format(name, view_policy))
            continue
        yield name


def gh_has(user: str) -> Iterator[str]:
    resp = requests.get('https://api.github.com/users/{}/repos?per_page=100'.format(user), headers={
        'Accept': 'application/vnd.github.v3+json'
    })
    assert resp.ok

    for repo in resp.json():
        if repo['private']:
            continue
        yield repo['name']


if '__main__' == __name__:
    main()
