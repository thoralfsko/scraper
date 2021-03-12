import pytest
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests

def get_game_links(team, year):
    '''get_game_links(team, year)
        team: team name. Boston Celtics == "BOS"
        year: year of season. this_year(2021) == "2021"

    returns: list of game url extensions for "https://www.basketball-reference.com"'''

    #create the url
    url = 'https://www.basketball-reference.com/teams/' + team + '/' + year + '.html'

    #make request
    page = requests.get(url)

    #create soup
    soup = bs(page.content, 'html.parser')
    results = soup.find(id='timeline_results')
    links = results.find_all('a')

    #create list of links
    result = []
    for i,_ in enumerate(links):
        try:
            result.append(links[i]['href'])
        except KeyError:
            pass

    return result

def get_line_score(game):
    '''get_line_score(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    returns: list of 2 line score rows => [[id, team, q1, q2, q3, q4, total], [id, team, q1, q2, q3, q4, total]]'''

    #create the url
    url = 'https://www.basketball-reference.com' + game

    #make request
    page = requests.get(url)

    #create soup
    soup = bs(page.content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    #find the table in the comments
    for comment in (comment for comment in comments if len(comment) > 2):
        ins = bs(comment, 'html.parser')
        table = ins.find(id='div_line_score')
        if table != None:
            soup = table

    #find game id
    id = game.split('/')[2].split('.')[0]

    #get team names for id
    stats = []
    body = soup.tbody
    teams = body.find_all('a')

    #get the points
    trs = body.find_all('tr')
    for i,tr in enumerate(trs):
        #create temp list for the row
        row = []

        #add the team and id to the row
        row.append(id)
        row.append(teams[i].get_text())

        #add scores to the row
        tds = tr.find_all('td')
        for td in tds:
            row.append(td.get_text())

        #add the row to stats
        stats.append(row)

    return stats

def get_four_factors(game):
    '''get_four_factors(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    returns: list of two four factor rows => [[id, team, pace, efg%, tov%, orb%, ft/fga, ortg], [id, team, pace, efg%, tov%, orb%, ft/fga, ortg]]'''

    #create the url
    url = 'https://www.basketball-reference.com' + game

    #make request
    page = requests.get(url)

    #create soup
    soup = bs(page.content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    #find the table in the comments
    for comment in (comment for comment in comments if len(comment) > 2):
        ins = bs(comment, 'html.parser')
        table = ins.find(id='four_factors')
        if table != None:
            soup = table

    #find game id
    id = game.split('/')[2].split('.')[0]

    #get team names for id
    stats = []
    body = soup.tbody
    teams = body.find_all('a')

    #get the points
    trs = body.find_all('tr')
    for i,tr in enumerate(trs):
        #create temp list for the row
        row = []

        #add the team and id to the row
        row.append(id)
        row.append(teams[i].get_text())

        #add scores to the row
        tds = tr.find_all('td')
        for td in tds:
            row.append(td.get_text())

        #add the row to stats
        stats.append(row)

    return stats

def get_basic_box(game):
    '''get_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    returns: list of basic box score rows => [[id, team, player, mp, fg, fga, fg%, 3p, 3pa, 3p%, ft, fta, ft%, orb, drb, trb, ast, stl, blk, tov, pf, pts, +/-], ...]'''

    #create the url
    url = 'https://www.basketball-reference.com' + game

    #make request
    page = requests.get(url)

    #find teams for soup.find
    #create soup
    soup = bs(page.content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    #find the table in the comments
    for comment in (comment for comment in comments if len(comment) > 2):
        ins = bs(comment, 'html.parser')
        table = ins.find(id='four_factors')
        if table != None:
            soup = table

    #find game id
    gid = game.split('/')[2].split('.')[0]

    #get team names for id
    stats = []
    body = soup.tbody
    teams = body.find_all('a')
    teams = [team.get_text() for team in teams]

    #create div id to search for
    ids = ['box-' + team + '-game-basic' for team in teams]

    #create soup
    s = bs(page.content, 'html.parser')

    #for each team find pasic box score rows
    for i,id in enumerate(ids):
        #find the table
        table = s.find('table', id=id)
        body = table.tbody

        #find table rows
        trs = body.find_all('tr')

        for tr in trs:
            #will hold this rows data
            row = []

            #add id to the row
            row.append(gid)

            #find team and add it to row
            row.append(teams[i])

            #find player name and add it to row
            player = tr.find_all('th')[0].get_text()
            #check that it is not a bogus row
            if player == 'Reserves':
                continue
            row.append(player)

            #find the players stats
            tds = tr.find_all('td')
            for td in tds:
                row.append(td.get_text())

            stats.append(row)

    return stats

#########
##TESTS##
#########
def test_contents_get_basic_box():
    #get the results
    results = get_basic_box('/boxscores/202012230BOS.html')
    #create names list
    names = ['Jrue Holiday', 'Khris Middleton', 'Giannis Antetokounmpo', 'Brook Lopez', 'Donte DiVincenzo', 'Pat Connaughton',
        'Bobby Portis', 'Bryn Forbes', 'D.J. Wilson', 'Sam Merrill', 'Jaylen Adams', 'Thanasis Antetokounmpo',
        'Jordan Nwora', 'Mamadi Diakite', 'Torrey Craig', 'Marcus Smart', 'Jaylen Brown', 'Jayson Tatum', 'Daniel Theis',
        'Tristan Thompson', 'Jeff Teague', 'Semi Ojeleye', 'Grant Williams', 'Payton Pritchard', 'Robert Williams',
        'Carsen Edwards', 'Javonte Green', 'Aaron Nesmith', 'Tremont Waters']
    #create player rows to test
    rows = [['202012230BOS', 'MIL', 'Jrue Holiday', '38:23', '10', '16', '.625', '1', '4', '.250', '4', '4', '1.000', '2', '4', '6', '3', '2', '1', '3', '3', '25', '-5'],
        ['202012230BOS', 'MIL', 'Torrey Craig', 'Did Not Play'],
        ['202012230BOS', 'BOS', 'Marcus Smart', '38:27', '0', '3', '.000', '0', '2', '.000', '3', '4', '.750', '0', '1', '1', '7', '0', '2', '2', '2', '3', '0'],
        ['202012230BOS', 'BOS', 'Tremont Waters', 'Did Not Play']]

    #test players col
    for i,row in enumerate(results):
        assert row[2] == names[i]

    #test rows
    assert results[0] == rows[0]
    assert results[14] == rows[1]
    assert results[15] == rows[2]
    assert results[28] == rows[3]

def test_empty_get_basic_box():
    #get the result
    result = get_basic_box('/boxscores/202012230BOS.html')
    assert [] != result

def test_contents_get_four_factors():
    #get the results
    result = get_four_factors('/boxscores/202012230BOS.html')
    assert result == [['202012230BOS', 'MIL', '99.9', '.589', '14.0', '28.9', '.167', '121.1'],
        ['202012230BOS', 'BOS', '99.9', '.564', '5.4', '19.6', '.079', '122.1']]

def test_empty_get_four_factors():
    #get the results
    result = get_four_factors('/boxscores/202012230BOS.html')
    assert result != []

#@pytest.mark.line
def test_contents_line_score():
    #get the result
    result = get_line_score('/boxscores/202012230BOS.html')
    assert [['202012230BOS', 'MIL', '34', '25', '25', '37', '121'],
        ['202012230BOS', 'BOS', '31', '33', '37', '21', '122']] == result

#@pytest.mark.line
def test_empty_get_line_score():
    #get the result
    result = get_line_score('/boxscores/202012230BOS.html')
    assert [] != result

#@pytest.mark.link
def test_empty_get_game_links():
    #get result
    result = get_game_links('BOS', '2021')
    #print(result)

    #check that the list is not empty
    assert [] != result

#@pytest.mark.link
def test_contents_get_game_links():
    #get result
    result = get_game_links('BOS', '2021')

    #test for correct values
    assert result[0] == '/boxscores/202012230BOS.html'
    assert result[30] == '/boxscores/202102230DAL.html'
    assert result[31] == '/boxscores/202102240ATL.html'
    #print(len(result))
