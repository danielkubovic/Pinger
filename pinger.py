'''
Program slouží ke kontrole stavu elektrické energie.
Při každém spuštění pinguje IP adresu,
která je doufejme není dostupná pouze v případě, že neběží elektřina.
'''
import os
import time
from subprocess import check_output

# Pokud neexistuje výstupní soubor, vytvoří ho a rovnou zapíše nějakou IP adresu
if not os.path.isfile('VYSTUP\\vystup.txt'):
    if not os.path.exists('VYSTUP'):
        os.makedirs('VYSTUP')
    with open('VYSTUP\\vystup.txt', 'w') as f:
        f.write('192.168.21.57\n')

# Přečte IP adresu z prvního řádku souboru
with open('VYSTUP\\vystup.txt', 'r') as f:
    ip_addr = f.readline()[:-1]

cas = time.asctime(time.localtime(time.time()))
vystup = str(check_output(['ping', '-n', '1', ip_addr]))

if 'Destination host unreachable.' in vystup:
    stav = 'Vypnuto'
elif 'Received = 1' in vystup:
    stav = 'Zapnuto'
else:
    stav = f'Nečekaný stav! Vystup: {vystup}'

'''
Porovná odpověď pingu s předchozí odpovědí nacházející se na posledním řádku souboru
pokud se odpověď liší, zapíše změnu na další řádek souboru
pokud se odpověď neliší, přepíše poslední řádek s aktuálním časem
'''
with open('VYSTUP\\vystup.txt', 'rb+') as f:
    try:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    posl_radek = f.readline().decode()
    if stav != posl_radek[25:32]:
        with open('VYSTUP\\vystup.txt', 'a') as f:
            f.write(cas + ' ' + stav + '\n')
    else:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        f.truncate()
        with open('VYSTUP\\vystup.txt', 'a') as f:
            f.write(cas + ' ' + stav + '\n')
