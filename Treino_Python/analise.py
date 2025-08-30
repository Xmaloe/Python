import os
import time
import json
from random import random
from datetime import datetime
import requests
import pandas as pd
import seaborn as sns
from sys import argv


def extrair_dados():
    """Extrai a taxa CDI do BCB e salva em taxa-cdi.csv."""
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.HTTPError:
        print("Dado não encontrado, continuando.")
        dado = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)[-1]['valor']

    for _ in range(0, 10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')
        cdi = float(dado) + (random() - 0.5)

        if not os.path.exists('./taxa-cdi.csv'):
            with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(1)

    print("Extração concluída com sucesso!")


def gerar_grafico(nome_arquivo: str):
    """Lê taxa-cdi.csv e gera um gráfico da taxa CDI."""
    df = pd.read_csv('./taxa-cdi.csv')
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_arquivo}.png")
    print(f"Gráfico salvo como {nome_arquivo}.png")


if __name__ == "__main__":
    if len(argv) < 2:
        print("Uso: python analise.py <nome-do-grafico>")
    else:
        extrair_dados()
        gerar_grafico(argv[1])
