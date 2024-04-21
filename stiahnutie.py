import paramiko
import sys
import csv
from getpass4 import getpass
import re


def stiahni_data():
    '''pripoji sa na GW a ulozi vysledok prikazu do suboru'''
    print('\nZadaj IP GW: ', end='')
    IP_GW = (input() or '')
    print ('Username: ', end='')
    username_gw = (input() or '')
    password_gw = (getpass('Password: ') or '')
    print()
    print(f'Vytvaram subor s outputom z GW:{IP_GW}, prikaz: "ppp active print without-paging"...')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=str(IP_GW), username=str(username_gw), password=str(password_gw), allow_agent=False)
    stdin, stdout, stderr = client.exec_command('ppp active print without-paging ')
    with open('ppp_active.txt', mode='a+') as out_file:
        for line in stdout:
            #if '100.64.' not in line:
            if line.isspace() == False:
                line = re.sub(' +', ' ', line)
                #print(f'{line}')
                line = line.strip()
                line = str(line).rstrip('\n') + ' ' + str(IP_GW)
                #print(f'{line}')
                out_file.write(f'{line}\n')
    client.close()
    print(f'{IP_GW} stiahnute')

def main():
    '''zadaj pocet GW'''
    open('ppp_active.txt', mode='w').close()
    print('Zadaj pocet GW, z ktorych chces vysledok (default=1): ', end='')
    pocet = int(input() or 1)
    rozsah = range(pocet)

    for i in rozsah:
        stiahni_data()

    print('\nHotovo, vysledok je v subore "ppp_active.txt"')
