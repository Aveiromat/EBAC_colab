import os
import time
import json
from random import random
from datetime import datetime

import requests

URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

# Criando a variável data e hora 

for _ in range(0, 10):

    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    # Captando a taxa CDI do site da B3

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.ConnectionError as exc:
        print(f"Erro de conexão: {exc}")
        cdi = None
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        cdi = None
    except Exception as exc:
        print("Erro inesperado, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)
        cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

    # Verificando se o arquivo "taxa-cdi.csv" existe

    if not os.path.exists('./taxa-cdi.csv'):
        with open('./taxa-cdi.csv', 'w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    # Salvando dados no arquivo "taxa-cdi.csv"

    with open('./taxa-cdi.csv', 'a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

    time.sleep(2 + (random() - 0.5))

print("Sucesso")
