#!/usr/bin/env python3
import os
from scraper import *
from write import *

#create the directory if it doesnt exist
if os.path.isdir('docs/') == False:
    os.mkdir('docs/')

#create a list of methods in scraper.py
methods = [get_game_links, get_line_score, get_four_factors, get_basic_box,
    get_team_info, get_basic_table, get_basic_box_q1, get_basic_box_q2,
    get_basic_box_q3, get_basic_box_q4, get_basic_box_h1, get_basic_box_h2]

#create scraper docs
file = open('docs/scraper.txt', 'w+')
for i,method in enumerate(methods):
    file.write(method.__doc__)
    if len(methods) - 1 != i:
        file.write('\n\n########################################\n')

file.close()

#create a list of methods from write.py
methods = [write_line_score, create_directory, clean_directory, write_four_factors,
    write_basic_box, write_basic_box_util, write_basic_box_q1, write_basic_box_q2,
    write_basic_box_q3, write_basic_box_q4, write_basic_box_h1, write_basic_box_h2,
    write_line_score_ot]

#create write docs
file = open('docs/write.txt', 'w+')
for i,method in enumerate(methods):
    file.write(method.__doc__)
    if len(methods) - 1 != i:
        file.write('\n\n########################################\n')

file.close()
