import os
import time
import json
from random import random
from datetime import datetime
import csv
from sys import argv, exit

import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'


def extrair_dados():
    for _ in range(10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

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

        if not os.path.exists('./taxa-cdi.csv'):
            with open('./taxa-cdi.csv', 'w', newline='', encoding='utf8') as fp:
                writer = csv.writer(fp)
                writer.writerow(['data', 'hora', 'taxa'])

        with open('./taxa-cdi.csv', 'a', newline='', encoding='utf8') as fp:
            writer = csv.writer(fp)
            writer.writerow([data, hora, cdi])

        time.sleep(2 + (random() - 0.5))

    print("Extração concluída com sucesso.")


def visualizar_dados(nome_grafico):
    df = pd.read_csv('./taxa-cdi.csv')

    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    grafico.set_xticks(range(len(df['hora'])))
    grafico.set_xticklabels(labels=df['hora'], rotation=90)
    plt.tight_layout()
    grafico.get_figure().savefig(f"{nome_grafico}.png")
    print(f"Gráfico salvo como {nome_grafico}.png")


if __name__ == "__main__":
    if len(argv) < 2:
        print("Uso: python analise.py <nome_do_grafico>")
        exit(1)

    extrair_dados()
    visualizar_dados(argv[1])
