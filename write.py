#!/usr/bin/env python3
import os
import pytest
import shutil
import pandas as pd
from scraper import *

path = 'data/'

def write_line_score(game):
    '''write_line_score(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes game line score data to "data/linescore.csv"
    returns: the number of overtime periods played'''

    #filename
    filename = 'linescore.csv'

    #labels
    labels = 'id,team,q1,q2,q3,q4,total\n'

    #open the file
    file = open(path + filename, 'a+')

    #add labels if the file is empty
    if os.path.getsize(path + filename) == 0:
        file.write(labels)

    #get the games line linescore
    data = get_line_score(game)

    #check if the game went into overtime
    if len(data[0]) > 7:
        file.close()
        return write_line_score_ot(data)


    #append the rows
    for row in data:
        rs = '' #rowstring
        for col in row:
            rs = rs + col + ','

        file.write(rs[0:len(rs) - 1] + '\n')

    #close the file
    file.close()
    return 0

def create_directory():
    '''create_directory()

    side effect: creates the data directory if it doesnt exist'''

    #create the full path of the data directory
    fullpath = os.getcwd() + path

    try:
        os.mkdir(path)
    except OSError:
        pass

def clean_directory():
    '''clean_directory()

    side effect: deletes the data directory and its contents and creates the data
        directory again'''

    #remove directory and its files if it exists
    if os.path.isdir(path):
        shutil.rmtree(path)

    #create the directory
    create_directory()

def write_four_factors(game):
    '''write_four_factors(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes four factors data to "data/fourfactors.csv"'''

    #filename
    filename = 'fourfactors.csv'

    #labels
    labels = 'id,team,pace,efg%,tov%,orb%,ft/fga,ortg\n'

    #open the file
    file = open(path + filename, 'a+')

    #add labels if the file is empty
    if os.path.getsize(path + filename) == 0:
        file.write(labels)

    #get the data for the game
    data = get_four_factors(game)

    #append the rows
    for row in data:
        rs = '' #rowstring
        for col in row:
            rs = rs + col + ','

        file.write(rs[0:len(rs) - 1] + '\n')

    #close the file
    file.close()

def write_basic_box(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicbox.csv"'''

    #filename
    filename = 'basicbox.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box)

def write_basic_box_util(filename, game, grab):
    '''write_basic_box_util(filename, game)
        filename: name of the file to write to
        game: url extention. game == "/boxscores/202012230BOS.html"
        grab: function used to pull stats from the web

    side effect: writes box score stats of the given game to the file named filename'''

    labels = 'id,team,player,mp,fg,fga,fg%,3p,3pa,3p%,ft,fta,ft%,orb,drb,trb,ast,stl,blk,tov,pf,pts,+/-\n'

    #open the file
    file = open(path + filename, 'a+')

    #add labels if the file is empty
    if os.path.getsize(path + filename) == 0:
        file.write(labels)

    #get the data for the game
    data = grab(game)

    #append the rows
    for row in data:
        rs = '' #rowstring

        if len(row) > 4:
            for col in row:
                rs = rs + col + ','

            file.write(rs[0:len(rs) - 1] + '\n')

    #close the file
    file.close()

def write_basic_box_q1(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicboxq1.csv"'''

    #filename
    filename = 'basicboxq1.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box_q1)

def write_basic_box_q2(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicboxq2.csv"'''

    #filename
    filename = 'basicboxq2.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box_q2)

def write_basic_box_q3(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicboxq3.csv"'''

    #filename
    filename = 'basicboxq3.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box_q3)

def write_basic_box_q4(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicboxq4.csv"'''

    #filename
    filename = 'basicboxq4.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box_q4)

def write_basic_box_h1(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicboxh1.csv"'''

    #filename
    filename = 'basicboxh1.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box_h1)

def write_basic_box_h2(game):
    '''write_basic_box(game)
        game: url extention. game == "/boxscores/202012230BOS.html"

    side effect: writes basic box stats to "data/basicboxh2.csv"'''

    #filename
    filename = 'basicboxh2.csv'

    #write to the file
    write_basic_box_util(filename, game, get_basic_box_h2)

def write_line_score_ot(data):
    '''write_line_score_ot(data)
        data: linescores for the two teams => [[id, team, q1, q2, q3, q4, total], [id, team, q1, q2, q3, q4, total]]

    side effect: writes line scores to linescore<x>ot.csv where x is the number of overtime periods if x > 1 or "" when x == 1
    returns: number of overtime periods played'''

    #find the number of ots
    ots = len(data[0]) - 7

    #create the labels string
    labels = 'id,team,q1,q2,q3,q4,'
    for i in range(ots):
        if i == 0:
            labels = labels + 'ot,'
        else:
            labels = labels + str(i + 1) + 'ot,'
    labels = labels + 'total\n'

    #create the documents filename
    filename = ''
    if ots == 1:
        filename = 'linescoreot.csv'
    else:
        filename = 'linescore' + str(ots) + 'ot.csv'

    #write to the file and close it
    file = open(path + filename, 'a+')
    if os.path.getsize(path + filename) == 0:
        file.write(labels)

    for row in data:
        rs = '' #rowstring
        for col in row:
            rs = rs + col + ','

        file.write(rs[0:len(rs) - 1] + '\n')

    #close the file
    file.close()

    #return the number of ots ????????????????
    return ots
#########
##TESTS##
#########

def test_create_directory():
    #remove the directory and all its files if it exists
    if os.path.isdir(path):
        shutil.rmtree(path)

    #create the directory
    create_directory()

    assert os.path.isdir(path) == True

def test_clean_directory():
    #clean the directory
    clean_directory()

    assert len(os.listdir(path)) == 0

#######################
##add new tests below##
#######################
def test_write_line_score_ot():
    if os.path.isfile(path + 'linescoreot.csv'):
        os.remove(path + 'linescoreot.csv')

    ots = write_line_score('/boxscores/202102210NOP.html')
    table = pd.read_csv(path + 'linescoreot.csv')

    assert table['ot'][0] == 7
    assert table['ot'][1] == 12
    assert ots == 1

def test_write_line_score_2ot():
    if os.path.isfile(path + 'linescore2ot.csv'):
        os.remove(path + 'linescore2ot.csv')

    ots = write_line_score('/boxscores/202101230PHO.html')
    table = pd.read_csv(path + 'linescore2ot.csv')

    assert table['2ot'][0] == 14
    assert table['2ot'][1] == 6
    assert ots == 2

def test_write_basic_box_q1():
    #clear the file if it exists
    if os.path.isfile(path + 'basicboxq1.csv'):
        os.remove(path + 'basicboxq1.csv')

    #write file then read it
    write_basic_box_q1('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicboxq1.csv')

    assert len(table['player']) == 19

def test_write_basic_box_q2():
    #clear the file if it exists
    if os.path.isfile(path + 'basicboxq2.csv'):
        os.remove(path + 'basicboxq2.csv')

    #write file then read it
    write_basic_box_q2('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicboxq2.csv')

    assert len(table['player']) == 20

def test_write_basic_box_q3():
    #clear the file if it exists
    if os.path.isfile(path + 'basicboxq3.csv'):
        os.remove(path + 'basicboxq3.csv')

    #write file then read it
    write_basic_box_q3('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicboxq3.csv')

    assert len(table['player']) == 18

def test_write_basic_box_q4():
    #clear the file if it exists
    if os.path.isfile(path + 'basicboxq4.csv'):
        os.remove(path + 'basicboxq4.csv')

    #write file then read it
    write_basic_box_q4('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicboxq4.csv')

    assert len(table['player']) == 17

def test_write_basic_box_h1():
    #clear the file if it exists
    if os.path.isfile(path + 'basicboxh1.csv'):
        os.remove(path + 'basicboxh1.csv')

    #write file then read it
    write_basic_box_h1('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicboxh1.csv')

    assert len(table['player']) == 20

def test_write_basic_box_h2():
    #clear the file if it exists
    if os.path.isfile(path + 'basicboxh2.csv'):
        os.remove(path + 'basicboxh2.csv')

    #write file then read it
    write_basic_box_h2('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicboxh2.csv')

    assert len(table['player']) == 19

def test_write_basic_box():
    #clear the file if it exists
    if os.path.isfile(path + 'basicbox.csv'):
        os.remove(path + 'basicbox.csv')

    #write file then read it
    write_basic_box('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'basicbox.csv')

    assert len(table['player']) == 20
    assert table['player'][0] == 'Jrue Holiday'
    assert table['player'][10] == 'Marcus Smart'
    assert table['mp'][2] == '36:24'

def test_write_four_factors():
    #clear the file if it exists
    if os.path.isfile(path + 'fourfactors.csv'):
        os.remove(path + 'fourfactors.csv')

    #write file then read it
    write_four_factors('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'fourfactors.csv')

    assert len(table['id']) == 2
    assert table['id'][1] == '202012230BOS'
    assert table['pace'][0] == 99.9
    assert table['ortg'][1] == 122.1

#@pytest.mark.line
def test_write_line_score():
    #clear the file if it exists
    if os.path.isfile(path + 'linescore.csv'):
        os.remove(path + 'linescore.csv')

    #write to the file then read it
    ots = write_line_score('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'linescore.csv')
    #print(table['id'])

    assert table['id'][0] == '202012230BOS'
    assert table['team'][0] == 'MIL'
    assert table['team'][1] == 'BOS'
    assert ots == 0
