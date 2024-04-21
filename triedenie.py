import pytz
import sys
import csv
import re

povodne_data = sys.argv[1]
nove_data = sys.argv[2]
stav_moznosti = ['active', 'cancelled', 'interrupted', 'new_in_process', '', ['active', 'new_in_process']]
ip = ''
produkt = ''
stav = ''
ticket = ''
username = ''

def nacitanie_parametrov():
    '''nacitanie premennych od usera'''
    global ip, produkt, stav, ticket
    print('\nNastav filtre:\n')
    print('IP/subnet (default=all): ', end='')
    ip = str(input() or '.')
    print('Produkt, ie. homelink (default=all): ', end='')
    produkt = str(input() or '').lower()
    print('Ticket verejna IP (y/n) (default=n): ', end='')
    ticket = str(input() or 'n')
    if ticket.lower() == 'y':
        ticket = ['1','2']
    else:
        ticket = ['', '']
    print('\nMoznosti pre stav zmluvy')
    print('1: active')
    print('2: cancelled')
    print('3: interrupted')
    print('4: new')
    print('5: all')
    print('6: all except cancelled and interrupted')
    print('Stav zmluvy volba: ', end='')
    stav_volba = int(input() or 5)
    if ((stav_volba > 6) or (stav_volba == 5)):
        stav = stav_moznosti
    else:
        stav = stav_moznosti[stav_volba-1]
    print()

def najdi_ip_na_gw(vyraz):
    '''Najdi vyraz v outpute z GW'''
    username = ''
    ip_gw = ''
    with open ('ppp_active.txt', mode='r') as gw_vycuc:
        read_gw_vycuc = csv.reader(gw_vycuc, delimiter=' ')
        #print(f'vo funkcii hladanie parameter vyraz: {vyraz}')
        for riadok in read_gw_vycuc:
            #print(f'riadok {riadok}')
            if (len(riadok) > 6):
                #print(f'riadok[5] vo funkcii {riadok[5]}')
                if (vyraz in riadok):
                    #print(f'vyraz {vyraz} sa rovna {riadok[5]} username je {riadok[2]} gw je {riadok[7]}')
                    username = riadok[2]
                    ip_gw = riadok[7]
    if username == '':
        username = 'nenaslo'
    return username, ip_gw

def filter():
    '''Otvor CSV a vyfiltruj podla parametrov do noveho file'''
    nove_data = sys.argv[2]
    with open(povodne_data, mode='r') as in_file, \
        open(nove_data, mode='w') as out_file, \
        open('for_rucne.txt', mode='w') as for_rucne:
            read_in_file = csv.reader(in_file, delimiter=',')
            line_count = 0
            for row in read_in_file:
                if line_count == 0:
                    line_count += 1
                else:
                    #   filter
                    #   POZOR: ak su viac ako 1 IP na zmluve, prida sa do file "for_rucne.txt" na rucne prekontrolovanie
                    strip_str = '\{\}'
                    if ((ip in row[1]) and (produkt in row[5].lower()) and (row[6] in stav) and (row[13] in ticket)):
                        if len(row[1]) < 17:
                            print(f'{row[1].strip(strip_str)}\t{row[3]}\t{row[5]}\t\t{row[6]}\t\t{row[16]}')
                            out_file.write(f'{row[1].strip(strip_str)}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\t{row[13]}\t{row[16]}\n')
                        else:
                            print(f'*** {row[1]}')
                            for_rucne.write(f'{row[3]}\t{row[1].strip(strip_str)}\t{row[4]}\t{row[5]}\t{row[6]}\t{row[13]}\t{row[16]}\n')
                    line_count += 1
            print(f'Processed {line_count} lines.')

def vytried_podla_active():
    '''vytried vyfiltrovane data podla toho, ci su active pppoe na gw a roztried do suborov'''
    with open ('nove_data.txt', mode='r') as nove_data, \
        open ('active.txt', mode='w') as active_ppp, \
        open ('for_rucne.txt', mode='a+') as for_rucne:
        read_nove_data = csv.reader(nove_data, delimiter='\t')
        active_line = 0
        rucne_line = 0
        sum_lines = 0
        for row in read_nove_data:
            #print(f'v main row[0] {row[0]}')
            username, ip_gw = najdi_ip_na_gw(row[0])
            username = username.replace('...', '')
            username = username.replace('@', '')
            #print(f'{username} {ip_gw} blablabla')
            sum_lines += 1
            if username != 'nenaslo':
                if username in row[6]:
                    active_ppp.write(f'{row[1]}\t{username}\t{row[0]}\t{ip_gw}\t{row[6]}\t{row[2]}\n')
                    active_line += 1
                else:
                    for_rucne.write(f'{row[1]}\t{row[0]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\n')
                    rucne_line += 1
            else:
                for_rucne.write(f'{row[1]}\t{row[0]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\n')
                rucne_line += 1
                
        print(f'{active_line} lines were added to active.txt')
        print(f'{rucne_line} lines were added to for_rucne.txt')
        print(f'{sum_lines} lines were processed')

def pridel_ip():
    '''pridel IP podla zaciatocnej a konciacej IP a pridel k zmluvam, vytvor subory pre sap a radius'''
    print('\n***\n*** Pridelenie IP\n*** Ak uz mas skriptom vytvoreny subor "active.txt" a chces len pridelit subnet\n***')
    print('\nChces pridelit IPcky? (y/N): ', end='')
    odpoved = str(input() or 'n').lower()
    if odpoved == 'y':
        print('\n***\n*** Pouzi adresy patriace do max jedneho /24 subnetu a hlavne platnu IPV4 adresu PLSs #lenivost #totoniejescriptfordummies\n***\n')
        pokracovat = 'y'
        zaciatok, koniec, pokracovat = zadaj_subnet()
        line_count = 0
        #print(f'zaciatok main {zaciatok}')
        #print(f'koniec main {koniec}')
        #print (f'{zaciatok} {koniec} {pokracovat}')
        while pokracovat == 'y':
            with open ('active.txt', mode='r') as active_ppp, \
                open ('for_radius.txt', mode='w') as for_radius, \
                open('for_sap.csv', mode='w') as for_sap, \
                open('for_l2.csv', mode='w') as for_l2:
                read_active_ppp = csv.reader(active_ppp, delimiter='\t')
                print('\n***\n*** TO COPY\n***\n')
                print('Zmluva\t\tPPPoE\t\tNova IP')
                for_sap.write('Zmluva,Nova IP\n')
                for_l2.write('Meno,Zmluva,Stara IP,Nova IP\n')
                for line in read_active_ppp:
                    if (int(zaciatok[3]) + line_count) > (int(koniec[3])):
                        print('\nSubnet skoncil alebo bol nespravne zadany. Chces pokracovat s dalsim subnetom? (y/N): ', end='')
                        odpoved = str(input() or 'n').lower()
                        if odpoved == 'y':
                            print('\n!!! Postaraj sa, aby sa subnety neprekryvali !!! Nech nemusim robit vsetko')
                            line_count = 0
                            zaciatok, koniec, pokracovat = zadaj_subnet()
                            if pokracovat == 'n':
                                break
                        else:
                            pokracovat = 'n'
                            break
                    host = str(int(zaciatok[3]) + line_count)
                    nova_ip = zaciatok[0] + '.' + zaciatok[1] + '.' + zaciatok[2] + '.' + host
                    print(f'{line[0]}\t{line[1]}\t{nova_ip}')
                    for_radius.write(f'ldapuser --user={line[1]} --modify=radiusFramedIPAddress={nova_ip}\n')
                    for_sap.write(f'{line[0]},{nova_ip}\n')
                    for_l2.write(f'{line[0]},{line[2]},{nova_ip},{line[5]}\n')
                    line_count += 1
                pokracovat = 'n'

def zadaj_subnet():
    '''zadaj zaciatok a koniec subnetu, vypluj rozdelene na list'''
    zaciatok = ''
    koniec = ''
    pokracovat = 'n'
    print('Zadaj zaciatocnu IP: ', end='')
    zaciatok = input()
    zaciatok = zaciatok.split('.')
    #print(f'zaciatok {zaciatok[0]}')
    print('Zadaj konecnu IP: ', end='')
    koniec = input()
    koniec = koniec.split('.')
    #print(f'koniec {koniec[3]}')
    if (((zaciatok[0] == koniec[0]) and (zaciatok[1] == koniec[1]) and (zaciatok[2] == koniec[2])) and checkni_adresu(koniec) and (int(zaciatok[3]) <= int(koniec[3]))):
        pokracovat = 'y'
    else:
        print(f'\n*** Instrukcie neboli jasne, prave som pristal na Marse ***\n')
        zaciatok = []
        koniec = []
        pokracovat = 'n'
    return zaciatok, koniec, pokracovat
    
def checkni_adresu(adresa):
    '''checkni ci adresa je platna'''
    for item in adresa:
        #print(f'item {item}')
        if int(item) > 255:
            return False
    return True

def kontrola():
    '''kontrola po restarte pppoe, hladanie IP na GW'''
    with open ('for_l2.csv', mode='r') as kontrola:
        read_kontrola = csv.reader(kontrola, delimiter=',')
        for row in read_kontrola:
            #print(f'v main row[0] {row[0]}')
            username, ip_gw = najdi_ip_na_gw(row[2])
            #print(f'{username} {ip_gw} blablabla')
            print(f'{row[0]}\t{username}\t{row[2]}\t{row[3]}')