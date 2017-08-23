## Udacity DAND Project 2: Investigate A Dataset
## Eric Jones
## July 2017


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_salaries(show=False):
    '''
    return pandas dataframe from file
    '''
    salaries = pd.read_csv('./data/SalariesEdit.csv')
    if show:
        print salaries.head(3)
        print salaries.tail(3)
    return salaries

def load_team_salaries(show=False):
    '''
    returns dataframe with columns: YearID teamID salary nPlayers
    '''
    player_salaries = load_salaries()

    group_by_team = player_salaries.groupby(['yearID', 'teamID'], as_index=False)
    salaries_by_team = group_by_team[['salary']].sum()
    nplayers_by_team = group_by_team[['salary']].count()
    nplayers_by_team.rename(columns={'salary':'nPlayers'}, inplace=True)

    # Filter out teams with nPlayers < 10
    nplayers_by_team = nplayers_by_team[nplayers_by_team['nPlayers'] >= 10]

    team_salaries_nplayers = salaries_by_team.merge(nplayers_by_team, on=['yearID', 'teamID'], how='inner')

    if show:
        print team_salaries_nplayers.head(3)
        print team_salaries_nplayers.tail(3)
    return team_salaries_nplayers


def player_salaries_by_year(salaries, show=False, save=False):
    '''
    Box plot of player salaries by year
    '''
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(17, 7))

    sns.boxplot(ax=ax, x='yearID', y='salary', data=salaries)
    ax.set_title('MLB Player Salaries')
    ax.set_xlabel('Year')
    ax.set_ylabel('Salary')

    if save:
        fig.savefig('SalaryBoxByYear.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def team_salary_vs_nplayers(show=False, save=False):
    '''
    Scatter plot of team (sum) salaries vs number of players on team
    '''
    salaries = load_team_salaries()

    sns.set_style("whitegrid")
    # sns.lmplot(x='nPlayers', y='salary', hue='yearID', data=salaries, fit_reg=False)
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.regplot(x='nPlayers', y='salary', data=salaries, fit_reg=False)
    plt.ylim(0)
    plt.xlabel('Number of Players')
    plt.ylabel('Team Salary (sum)')
    plt.title('Salary vs. Number of Players')

    if save:
        fig.savefig('TeamSalaryVsTeamSize.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def team_salaries_by_year(show=False, save=False):
    '''
    Box plot of team (sum) salaries by year
    '''
    team_salaries = load_team_salaries()

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(17, 7))

    sns.boxplot(ax=ax, x='yearID', y='salary', data=team_salaries)
    sns.swarmplot(ax=ax, x='yearID', y='salary', data=team_salaries, color="0.25", alpha=0.5)

    ax.set_ylim(bottom=0)
    ax.set_title('MLB Team Salaries')
    ax.set_xlabel('Year')
    ax.set_ylabel('Team Salary')

    if save:
        fig.savefig('TeamSalaryBoxByYear.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def load_teams(show=False):
    '''
    return pandas dataframe from file
    '''
    teams = pd.read_csv('./data/Teams.csv')

    teams = teams[teams['yearID'] >= 1985]

    # restrict columns in output
    teams = teams.loc[:, lambda df: ['yearID', 'teamID', 'lgID', 'divID', 'Rank', 'W', 'L', 'WCWin', 'DivWin', 'LgWin', 'WSWin']]

    # clean for processing
    teams = winners_to_ints(teams)

    if show:
        print teams.head(3)
        print teams.tail(3)
    return teams

def winners_to_ints(teams):
    '''
    Apply YN_to_int function to appropriate columns of the teams dataframe
    '''
    teams['WCWin'] = teams['WCWin'].map(YN_to_int)
    teams['DivWin'] = teams['DivWin'].map(YN_to_int)
    teams['LgWin'] = teams['LgWin'].map(YN_to_int)
    teams['WSWin'] = teams['WSWin'].map(YN_to_int)
    return teams

def YN_to_int(x):
    '''
    Translate 'Y' to 1 and 'N' to 0. Leave ints in place, otherwise return None
    '''
    if isinstance(x, int):
        pass
    if x == 'Y':
        return 1
    elif x == 'N':
        return 0
    else:
        return None

def count_winners_by_year(team_data, show=False, save=False):
    '''
    Line plot: count of post season teams in each year
    '''
    by_year = team_data.groupby('yearID')['WCWin', 'DivWin', 'LgWin', 'WSWin'].sum()

    sns.set_style("whitegrid", {'grid.color':'.9'})
    fig = plt.figure(figsize=(10, 6))

    plt.plot(by_year.index.values, by_year['WCWin'],
             label='Wild Card', linestyle='-', marker='s')
    plt.plot(by_year.index.values, by_year['DivWin'],
             label='Division', linestyle='-', marker='o')
    plt.plot(by_year.index.values, by_year['LgWin'],
             label='League', linestyle='-', marker='^')
    plt.plot(by_year.index.values, by_year['WSWin'],
             label='World Series', linestyle='-', marker='*')

    plt.ylim(0, 7)
    plt.xlim(1983, 2018)
    plt.legend(loc='upper left')
    plt.xlabel('Year')
    plt.ylabel('Number of Teams')
    plt.title('Number of Winners By Year')

    if save:
        fig.savefig('WinnersPerYear.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def rank_hist(show=False, save=False):
    '''
    Historgam of rank for all teams in the dataset
    '''
    teams = load_teams()

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))

    sns.distplot(teams['Rank'], kde=False, bins=range(1, 9))
    plt.xticks(np.arange(1.5, 8, 1), range(1, 9))
    ax.xaxis.grid(False)
    plt.xlabel('End of Season Division Rank')
    plt.ylabel('Number of Teams')
    plt.title('Division Rank')

    if save:
        plt.savefig('RankHist.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def find_missing_teamyear(a, b, show=False):
    '''
    return list of (yearID, teamID) that exist in a or b, and not the other
    '''
    missing = []

    if show:
        print 'Len A: ', len(a)
        print 'Len B: ', len(b)

    a_years = list(a['yearID'])
    a_teams = list(a['teamID'])
    a_zipped = zip(a_years, a_teams)

    b_years = list(b['yearID'])
    b_teams = list(b['teamID'])
    b_zipped = zip(b_years, b_teams)

    for team in b_zipped:
        if team not in a_zipped:
            missing.append(team)
            if show:
                print 'Missing from A: ', team

    for team in a_zipped:
        if team not in b_zipped:
            missing.append(team)
            if show:
                print 'Missing from B: ', team

    return missing

def join_teams_salaries(show=False):
    '''
    returns a dataframe joining team salary info with team W/L and playoff info
    '''
    team_salaries = load_team_salaries()
    team_records = load_teams()

    missing = find_missing_teamyear(team_salaries, team_records, show=show)

    teams_with_salary = team_salaries.merge(team_records, on=['yearID', 'teamID'], how='left')

    # compute a StdSalary by year Column
    salary_by_teamyear = teams_with_salary.pivot(index='teamID', columns='yearID', values='salary')
    std_salary_by_teamyear = standardize(salary_by_teamyear)

    # merge StdSalary Column back to our joined dataframe with proper index.
    std_salaries = std_salary_by_teamyear.stack().reset_index()
    std_salaries.columns = ['teamID', 'yearID', 'StdSalary']
    if show:
        print std_salaries.head()
    teams_with_stdsalary = teams_with_salary.merge(std_salaries, on=['yearID', 'teamID'], how='left')

    # compute a WinPct Column
    teams_with_stdsalary['WinPct'] = teams_with_stdsalary['W'] / (teams_with_stdsalary['W'] + teams_with_stdsalary['L'])

    if show:
        print 'Len teams_with_salary: ', len(teams_with_salary)
        print teams_with_stdsalary.head(3)
        print teams_with_stdsalary.tail(3)

    return teams_with_stdsalary

def standardize(df):
    means = df.mean()
    stds = df.std(ddof=0)
    return (df - means) / stds

def highlight_WS_team_salaries(show=False, save=False):
    '''
    box plot showing WS winner within standardized team salaries per year
    '''
    teams_with_salary = join_teams_salaries()

    WSWin_teams_salaries = teams_with_salary[teams_with_salary['WSWin'] == 1]

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(17, 7))

    sns.boxplot(ax=ax, x='yearID', y='StdSalary', data=teams_with_salary)
    sns.swarmplot(x='yearID', y='StdSalary', data=teams_with_salary, color='.5')

    # overlay WS winners on this boxplot. Need WS salaries, skipping 1994:
    stdsalaries = list(WSWin_teams_salaries['StdSalary'])
    stdsalaries.insert(9, None) #1994

    ax.plot(range(len(stdsalaries)), stdsalaries, label='World Series Champion',
            linestyle='none', marker='*', ms=15, color='red', zorder=10)

    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Standardized Team Salary')
    plt.title('Standardized MLB Team Salaries')

    if save:
        fig.savefig('StandardTeamSalaryBoxWS.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def max_salary_WS(show=False):
    '''
    Calculate number of teams that spent the most and won the World Series
    '''
    teams_with_salary = join_teams_salaries()

    max_salary = teams_with_salary.groupby(['yearID'])['salary'].idxmax()
    teams_with_max_salary = teams_with_salary.loc[max_salary]

    max_winners = teams_with_max_salary['WSWin'].sum()

    if show:
        print 'Teams that won as top spender: ', max_winners
    return max_winners

def expensive_rank(show=False, save=False):
    '''
    histogram of rank for teams with StdSalary > 1.5
    '''
    teams_with_salary = join_teams_salaries()

    expensive_teams = teams_with_salary[teams_with_salary['StdSalary'] >= 1.5]

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))

    sns.distplot(expensive_teams['Rank'], kde=False, bins=range(1, 9))
    plt.xticks(np.arange(1.5, 8, 1), range(1, 9))
    ax.xaxis.grid(False)
    plt.xlabel('End of Season Division Rank')
    plt.ylabel('Number of Teams')
    plt.title('Division Rank of Teams with StdSalary > 1.5 (n=69)')

    if save:
        plt.savefig('ExpensiveTeamRank.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

def highest_salary_in_div_rank(show=False, save=False):
    '''
    Get teams with the highest salary in each division, each league, each year
    Every team on this list could have won their division (Rank == 1). Did they?
    Plot histogram of rank for these teams
    '''
    teams_with_salary = join_teams_salaries()

    teams_with_salary_div = teams_with_salary.groupby(['yearID', 'lgID', 'divID'])
    max_salary_div = teams_with_salary_div['salary'].idxmax()

    teams_with_max_div_salary = teams_with_salary.loc[max_salary_div]

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(9, 5))

    sns.distplot(teams_with_max_div_salary['Rank'], kde=False, bins=range(1, 9))
    plt.xticks(np.arange(1.5, 8, 1), range(1, 9))
    ax.xaxis.grid(False)
    plt.xlabel('End of Season Division Rank')
    plt.ylabel('Number of Teams')
    plt.title('Rank for Teams with Max Salary in Division (n=174)')

    if save:
        plt.savefig('HighestSalaryTeamRank.png', bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    return

if __name__ == '__main__':
    ## Salary Data
    salaries = load_salaries(show=False)
    player_salaries_by_year(salaries, show=False)
    team_salary_vs_nplayers(show=False)
    team_salaries_by_year(show=False)

    ## Team Data
    team_data = load_teams(show=False)
    count_winners_by_year(team_data, show=False)
    rank_hist(show=False)

    ## Join
    join_teams_salaries(show=False)

    ## Does Money Buy Championships
    highlight_WS_team_salaries(show=False)
    max_salary_WS(show=False)
    expensive_rank(show=False)
    highest_salary_in_div_rank(show=False)