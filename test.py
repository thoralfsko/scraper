#!/usr/bin/env python3
import os

#run tests and write output to pytest directory
os.system('pytest -vv -s write.py > pytest/write.txt')
os.system('pytest -vv -s scraper.py > pytest/scraper.txt')
