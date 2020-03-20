import json
import time
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup


def search_in_rev(search_query):
    """ Uses the search_query to search in rev.com for the transcripts of the speeches
    :param search_query: List of the terms to use in the search

    Output: Saves the responses in html format
    """
    response = requests.get("https://www.rev.com/blog/transcripts?s={}".format('+'.join(search_query)))

    if response.status_code == 200:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rev_search_results', 'responses', 'response{}.html'.format('_'.join(search_query)))

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(response.text)
    else:
        print("For search query: {} Response status: {}".format('_'.join(search_query), response.status_code))

    return file_path


def process_html(html_file):
    """
    Processes the response of the search in rev.com
    :param html_file: File containing the result of the search

    Output: Saves the
    """
    with open(html_file, 'r') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    result_elements = soup.find_all('div', {'class': 'fl-post-grid-text'})
    search_query = (os.path.basename(html_file).replace('response', '')
                                               .replace('.html', '')
                                               .strip())
    rev_result_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rev_search_results')

    if result_elements:
        result = [(elem.a.text.replace('\t', '').replace('\n', ' ') , elem.a.attrs['href'])
                  for elem in result_elements if elem != '\n']

        if len(result) > 1:
            print('process_html: More then one match! Matches: {} File: '.format(len(result)), html_file)
            file_path = os.path.join(rev_result_dir, 'jsons', 'many_results_{}.json'.format(search_query))

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            multiple_res = OrderedDict()
            multiple_res['query'] = search_query
            multiple_res['results'] = [{'index': index, 'title': tup[0], 'url': tup[1]} for index, tup in enumerate(result)]

            with open(file_path, 'w') as f:
                json.dump(multiple_res, f)
        else:
            print("Result Found! For file: ", html_file)
            result_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                       'rev_search_results',
                                       "result_{}.csv".format(time.strftime("%Y%m%d")))

            os.makedirs(os.path.dirname(result_file), exist_ok=True)

            with open(result_file, 'a') as f:
                f.write('\n')
                f.write(', '.join(result[0]))

    else:
        print('process_html: For search_query: {} No results! File: {}'.format(search_query, html_file))


def info_search_in_rev(search_query):
    """ Uses the search_query to search in rev.com for the transcripts of the speeches
    :param search_query: List of the terms to use in the search

    Output: Saves the responses in html format
    """
    response = requests.get("https://www.rev.com/blog/transcripts?s={}".format('+'.join(search_query)))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        result_elements = soup.find_all('div', {'class': 'fl-post-grid-text'})

        if len(result_elements) > 1:
            return len(result_elements)
    else:
        return None


if __name__ == "__main__":
    import os

    file_names = os.listdir('/home/paco/Documents/diplomna/dataset/annotated_transcripts')

    for file_n in file_names:
        query_terms = file_n[8:].replace(".csv", '').split('_')

        query_terms.append(file_n[:4])

        file_path = search_in_rev(query_terms)

        process_html(file_path)
