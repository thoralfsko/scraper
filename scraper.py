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

#########
##TESTS##
#########
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
