#!/usr/bin/env python3
import fileinput
import requests
import sys
from bs4 import BeautifulSoup

def get_proxy():
        api_key = (('0ee89caa-a9f2-4aac-bb60-b448c15b2e5a'))

        url = ('https://gimmeproxy.com/api/getProxy?api_key={}&protocol=http'.format(api_key))

        response = requests.get(url)

        if response.json()['supportsHttps']:
                proxy = {'https':'{}'.format(response.json()['curl'].strip())}
        else:
                proxy = {'http':'{}'.format(response.json()['curl'].strip())}
        return proxy

def consulta_operadora(fone):

        url = 'https://qualoperadora.info/widget/consulta'
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        data = {'tel':'{}'.format(fone)}

        proxy = get_proxy()
        for i in range(10):
                try:
                        response = requests.post(url, headers=header, data=data, proxies=proxy, timeout=15)
                except Exception as e:
                        continue
                if not response.ok:
                        proxy = get_proxy()
                else:
                        break
        if not response.ok:
                return 0

        try:
                operadora = BeautifulSoup(response.text, 'html.parser').find('img', {'class':'o'})['title'].lower()
        except:
                return 6

        if operadora == 'vivo':
                return 1
        elif operadora == 'claro':
                return 2
        elif operadora == 'tim':
                return 3
        elif operadora == 'oi':
                return 5
        else:
                return 6

operadora = consulta_operadora(sys.argv[1])

cod_area = {
        1:'015',
        2:'021',
        3:'041',
        5:'031',
        6:'041'
}

if operadora != 0 and not sys.argv[1].startswith('14'):
        command = 'SET VARIABLE OPERADORA "{}{}"'.format(operadora, cod_area[operadora]).encode(sys.stdout.encoding)
else:
        command = 'SET VARIABLE OPERADORA "{}"'.format(operadora).encode(sys.stdout.encoding)

sys.stdout.write(command.decode())
