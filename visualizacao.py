import csv
from sys import argv, exit

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Verifica se o nome do arquivo de saída foi fornecido como argumento
if len(argv) < 2:
    print("Uso: python visualizacao.py <nome_do_arquivo_de_saida>")
    exit(1)

# Extraindo as colunas hora e taxa
df = pd.read_csv('./taxa-cdi.csv')

# Salvando no gráfico
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
grafico.set_xticks(range(len(df['hora'])))
grafico.set_xticklabels(labels=df['hora'], rotation=90)
plt.tight_layout()  # Ajusta o layout para evitar cortes nos rótulos
grafico.get_figure().savefig(f"{argv[1]}.png")
