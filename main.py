#!/usr/bin/env python3
from write import *

#list of all teams
teams = '''BOS MIL IND PHI BRK CLE ORL CHO ATL NYK MIA TOR
    CHI WAS DET LAL LAC UTA PHO POR DAL SAS DEN OKC GSW MEM
    SAC NOP HOU MIN'''.split()
#set of gids that have been scraped
links_processed = set()

def main():
    #clean the directory
    clean_directory()

    #pull game data for every team
    for team in teams:

        #get game lins for team. only 2021 for now
        links = get_game_links(team, '2021')

        #process each game link
        for link in links:
            #check if link has been processed
            if link not in links_processed:
                #write linescore
                #get number of ot periods
                ots = write_line_score(link)

                #write fourfactors
                write_four_factors(link)

                #write basic box boxscore
                write_basic_box(link)

                #write bosxcore quarters
                write_basic_box_q1(link)
                write_basic_box_q2(link)
                write_basic_box_q3(link)
                write_basic_box_q4(link)

                #write box score halfs
                write_basic_box_h1(link)
                write_basic_box_h2(link)

                #handle writing overtime if there was one
                for ot in range(ots):
                    write_basic_box_ot(link, ot + 1)

                #add link to proccessed set
                links_processed.add(link)


if __name__ == '__main__':
    main()
