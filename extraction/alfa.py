import fitz
from architecture.extrategia_extracao import *
from architecture.functions import *
import re
import pandas as pd
import os


# Implementação para extração de dados da seguradora Alfa
class ExtracaoAlfa(EstrategiaExtracao):
    def extrair_texto(self, nome_arquivo):
        """Método placeholder, não necessário para CSVs."""
        pass

    def extrair_num_extrato(self, df):
        """Extrai o número do recibo (extrato) da coluna 'nrrecibo'."""
        return df['nrrecibo'].iloc[0]

    def processar_dataframe(self, nome_arquivo, texto_alvo=None):
        """Processa o arquivo CSV e formata o DataFrame conforme necessário."""
        df = pd.read_csv(nome_arquivo, sep=';')

        # Extração de campos específicos
        df['data'] = df['dtemissao'].str.split().str[0] 
        df['ramo'] = df['documento'].str.split('/').str[1]  
        df['apolice'] = df['documento'].str.replace('/', '') 
        df['parcela'] = df['Pr'].str.split('/').str[0]  
        df['premio'] = df['vlpreliq'] 
        df['perc_comissao'] = '0,00'  
        df['comissao'] = df['vllancamento'] 
        df['segurado'] = df['nmseg']  



        if 'ALFA PREV.' in nome_arquivo:
            df['Cnpj'] = '"0000000000000-00"'
            df['Seguradora'] = 'ALFA PREV'

        elif 'ALFA' in nome_arquivo:
            df['Cnpj'] = '"0000000000000-00"'
            df['Seguradora'] = 'ALFA'

        df['Endosso'] = ""
        df['Segurado'] = df['segurado']
        df['Apolice'] = df['apolice']
        df['Prêmio'] = df['premio']
        df['%'] = df['perc_comissao']
        df['Comissão'] = df['comissao']
        df['Ramo'] = df['ramo']
        df['Data'] = leitura_data_arquivo(nome_arquivo)
        df['Recibo'] = df['nrrecibo']

        colunas = ['Endosso', 'Apolice', 'Segurado', 'Ramo', 'Prêmio', '%', 'Comissão', 'Data', 'Recibo', 'Cnpj', 'Seguradora']
        df = df[colunas]
        df = df.astype(str)

        return df


