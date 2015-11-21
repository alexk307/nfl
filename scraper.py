import requests
from bs4 import BeautifulSoup
import re


base_url = 'http://www.pro-football-reference.com'
COL_NAMES = ['week', 'day', 'date', 'boxscore_url', 'result', 'OT', 'record',
             'at', 'opponent', 'team_score', 'opp_score', 'off_first_downs',
             'off_total_yds', 'off_pass_yds', 'off_rush_yds',
             'off_turn_overs', 'def_first_downs', 'def_total_yds',
             'def_pass_yds', 'def_rush_yds', 'def_turn_overs']


def _strip_html(text):
    """
    Strips tags from HTML
    :param text: The text to strip from
    :return: Cleaned text
    """
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))


def parse_boxscore_url(url_tag):
    """
    Parses the URL from the boxscore tag
    :param url_tag: The url tag
    :return: The boxscore url
    """
    soup = BeautifulSoup(url_tag)
    return soup.find_all('a', href=True)[0]['href']


def parse_season_log(team, verbose_name, year, csv=False):
    """
    Parses the season log
    :param team: The team abbreviation
    :param verbose_name: The full name of the team
    :param year: The year to fetch
    :param csv: Boolean flag to output in csv or in JSON
    :return: List of data in JSON | csv
    """
    season_url = \
        'http://www.pro-football-reference.com/teams/%s/%s.htm' % (team, year)

    res = requests.get(season_url)
    # PFR will redirect you to a 404 page if not found
    # but still serves you a 200 response
    if '404' in res.url:
        raise Exception('No data found for team %s in year %s' % (team, year))
    soup = BeautifulSoup(res.text)
    parsed = soup.findAll(
        'div', {
            'class': 'table_container',
            'id': 'div_team_gamelogs'
        }
    )
    rows = parsed[0].findAll('td')
    # After 1994, they added 3 more columns
    column_len = 24 if int(year) >= 1994 else 21
    # Group the rows into the number of columns
    grouped_rows = [
        rows[i:i+column_len] for i in range(0, len(rows), column_len)
    ]
    data = []
    for row in grouped_rows:
        # If there is no day of week then it was the bye week
        if _strip_html(row[1]) == '':
            continue
        box_score_uri = parse_boxscore_url(
            str(row[COL_NAMES.index('boxscore_url')]))
        row = map(lambda x: _strip_html(x), row)
        # Add the year into the data
        if csv:
            row.insert(0, str(year))
            row.insert(1, verbose_name)
            row[COL_NAMES.index('boxscore_url') + 1] = box_score_uri
            data.append(','.join(row))
        else:
            row_dict = dict(zip(COL_NAMES, row))
            row_dict['boxscore'] = box_score_uri
            data.append(row_dict)
    return data


def parse_log_table(html, div_id):
    """
    Parses a log table
    :param html: The HTML to parse
    :param div_id: The id of the table div
    :return: List of data
    """
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
    """
    Parses the boxscore gamelogs
    :param gamelog_url: The gamelog URL
    :return: A dict containing game and ref info
    """
    res = requests.get(gamelog_url)
    return {
        'game_info': parse_log_table(res.text, 'div_game_info'),
        'ref_info': parse_log_table(res.text, 'div_ref_info')
    }
