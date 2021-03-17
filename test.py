#!/usr/bin/env python3
import os

#create pytest directory if it does not exist
if os.path.isdir('pytest/') == False:
    os.mkdir('pytest/')

#run tests and write output to pytest directory
os.system('pytest -vv -s write.py > pytest/write.txt')
os.system('pytest -vv -s scraper.py > pytest/scraper.txt')
