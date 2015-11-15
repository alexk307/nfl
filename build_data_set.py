from scraper import parse_season_log, COL_NAMES


FRANCHISES = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cie', 'dal',
              'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'mia', 'min',
              'nwe', 'nor', 'nyg', 'nyj', 'rai', 'phi', 'pit', 'sdg', 'sfo',
              'sea', 'ram', 'tam', 'oti', 'was']

START_YEAR = 1960
END_YEAR = 2015

FILE_NAME_FORMAT = 'nfl_%s_%s-%s.csv'


def build_team_file(team):
    filename = FILE_NAME_FORMAT % (team, START_YEAR, END_YEAR)
    with open(filename, 'w') as f:
        f.write(','.join(COL_NAMES) + '\n')
        for year in xrange(START_YEAR, END_YEAR+1):
            for season in parse_season_log(team, year, csv=True):
                f.write(season + '\n')