import pytz
import sys
import csv
from menu import hlavne_menu
import triedenie
import stiahnutie
import odstranenie

def menu():
    '''print MENU'''
    print()
    print('\n*******************************************')
    print('MENU:')
    print('*******************************************')
    for key, value in hlavne_menu.items():
        print(f'{key}: {value}')
    print('0: EXIT')
    print('\nVolba = ', end='')
    volba = str(input() or '0')
    print('********************************************\n')
    print()
    return volba

def main():
    '''_main_'''
    volba = '*'
    while volba != '0':
        if volba in hlavne_menu:
            print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            if volba == '1':
                triedenie.nacitanie_parametrov()
            elif volba == '2':
                triedenie.filter()
            elif volba == '3':
                stiahnutie.main()
            elif volba == '4':
                triedenie.vytried_podla_active()
            elif volba == '5':
                triedenie.pridel_ip()
            elif volba == '6':
                odstranenie.main()
            elif volba == '7':
                triedenie.kontrola()
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            volba = menu()
        else:
            volba = menu()

main()
