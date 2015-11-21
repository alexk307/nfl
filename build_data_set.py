from scraper import parse_season_log, COL_NAMES


FRANCHISES = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal',
              'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'mia', 'min',
              'nwe', 'nor', 'nyg', 'nyj', 'rai', 'phi', 'pit', 'sdg', 'sfo',
              'sea', 'ram', 'tam', 'oti', 'was']

FRANCHISE_NAMES = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens',
                   'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears',
                   'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys',
                   'Denver Broncos', 'Detroit Lions', 'Green Bay Packers',
                   'Houston Texans', 'Indianapolis Colts',
                   'Jacksonville Jaguars', 'Kansas City Chiefs',
                   'Miami Dolphins', 'Minnesota Vikings',
                   'New England Patriots', 'New Orleans Saints',
                   'New York Giants', 'New York Jets', 'Oakland Raiders',
                   'Philadelphia Eagles', 'Pittsburgh Steelers',
                   'San Diego Chargers', 'San Francisco 49ers',
                   'St. Loutis Rams', 'Tampa Bay Buccaneers',
                   'Tennessee Titans', 'Washington Redskins']

FRANCHISE_DICT = dict(zip(FRANCHISES, FRANCHISE_NAMES))

START_YEAR = 1960
END_YEAR = 2015

FILE_NAME_FORMAT = 'nfl_%s_%s-%s.csv'


def build_team_file(team):
    filename = FILE_NAME_FORMAT % (team, START_YEAR, END_YEAR)
    with open(filename, 'w') as f:
        f.write('year,' + ','.join(COL_NAMES) + '\n')
        for year in xrange(START_YEAR, END_YEAR+1):
            for season in parse_season_log(team, year, csv=True):
                f.write(season + '\n')


def build_master_file():
    filename = 'nfl_masterfile_%s-%s.csv' % (START_YEAR, END_YEAR)
    game_set = set()
    with open(filename, 'w') as f:
        f.write('year,team,' + ','.join(COL_NAMES) + '\n')
        for team, verbose_name in FRANCHISE_DICT.iteritems():
            for year in xrange(START_YEAR, END_YEAR+1):
                try:
                    for season in parse_season_log(
                            team, verbose_name, year, csv=True):
                        print '%s - %s' % (verbose_name, year)
                        f.write(season + '\n')
                except Exception as e:
                    print e
                    pass


if __name__ == '__main__':
    build_master_file()
