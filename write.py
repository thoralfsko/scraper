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

    side effect: writes game line score data to "data/linescore.csv"'''

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

    #append the rows
    for row in data:
        rs = '' #rowstring
        for col in row:
            rs = rs + col + ','

        file.write(rs[0:len(rs) - 1] + '\n')

    #close the file
    file.close()

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

#@pytest.mark.line
def test_write_line_score():
    #clear the file if it exists
    if os.path.isfile(path + 'linescore.csv'):
        os.remove(path + 'linescore.csv')

    #write to the file then read it
    write_line_score('/boxscores/202012230BOS.html')
    table = pd.read_csv(path + 'linescore.csv')
    #print(table['id'])

    assert table['id'][0] == '202012230BOS'
    assert table['team'][0] == 'MIL'
    assert table['team'][1] == 'BOS'
