import paramiko
import sys
import csv
from getpass4 import getpass


def remove_ppp_user():
    '''pripoji sa na GW a odstrani pppoe session usera zo suboru active.txt'''
    print('Zadaj IP GW: ', end='')
    IP_GW = (input() or '')
    print ('Username: ', end='')
    username_gw = (input() or '')
    password_gw = (getpass('Password: ') or '')
    print()
    print(f'\nOdstranujem userov z GW:{IP_GW}\n')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=str(IP_GW), username=str(username_gw), password=str(password_gw))
    with open('active.txt', mode='r') as in_file:
        #open('active.txt', mode='a+') as out_file:
        read_in_file = csv.reader(in_file, delimiter='\t')
        for line in read_in_file:
            username = line[4]
            print(f'username {username}')
            cmd = 'ppp active remove [find where name="' + username + '"]'
            stdin, stdout, stderr = client.exec_command(cmd)
            #print(f'output \nin {stdin} \nout {stdout} \nerr {stderr}')
            #out_file.write(f'{line}\n')
    client.close()
    print(f'Z {IP_GW} odstranene')


def main():
    '''main v odstranenie'''
    pokracovat = True
    print('\n***\n*** Skript odstrani userov zo suboru "active.txt" zo zadanych GW\n*** Ak si sa zlakol, pouzi CTRL+C\n***\n')
    while pokracovat:
        remove_ppp_user()
        print('Chces pokracovat dalsou GW? (y/N)')
        odpoved = str(input() or 'n').lower()
        pokracovat = (odpoved == 'y')

