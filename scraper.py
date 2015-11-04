import requests
from bs4 import BeautifulSoup
import re


base_url = 'http://www.pro-football-reference.com'
url = 'http://www.pro-football-reference.com/teams/phi/2014.htm'


def _strip_html(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))


def parse_game_log(season_url):
    res = requests.get(season_url)
    soup = BeautifulSoup(res.text)
    parsed = soup.findAll(
        'div', {
            'class': 'table_container',
            'id': 'div_team_gamelogs'
        }
    )
    rows = parsed[0].findAll('td')
    # Group the rows into the number of columns
    grouped_rows = [rows[i:i+24] for i in range(0, len(rows), 24)]
    data = []
    for row in grouped_rows:
        # If there is no day of week then it was the bye week
        if _strip_html(row[1]) == '':
            continue
        soup = BeautifulSoup(str(row[3]))
        box_score_uri = soup.find_all('a', href=True)[0]['href']
        row = map(lambda x: _strip_html(x), row)
        row_data = {
            'week': row[0],
            'day': row[1],
            'date': row[2],
            'boxscore_url': '%s%s' % (base_url, box_score_uri),
            'record': row[6]
        }
        data.append(row_data)
    return data


def parse_log_table(html, div_id):
    soup = BeautifulSoup(html)
    parsed = soup.findAll(
        'div', {
            'class': 'table_container',
            'id': div_id
        }
    )
    rows = parsed[0].findAll('td')
    table = map(lambda x: _strip_html(x), rows)
    # The table comes back as a list with keys and values in sequence.
    # [key1, val1, key2, val2, ...] This convert that list into a dict
    return dict(zip(*[iter(table)]*2))


def parse_game_info_log(gamelog_url):
    res = requests.get(gamelog_url)
    return {
        'game_info': parse_log_table(res.text, 'div_game_info'),
        'ref_info': parse_log_table(res.text, 'div_ref_info')
    }