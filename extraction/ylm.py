import fitz
from architecture.extrategia_extracao import *
from architecture.functions import *
import re
import pandas as pd
from extraction.cardif import * 


class ExtracaoYlm(EstrategiaExtracao):

    def extrair_texto(self, nome_arquivo):
        """Método abstrato implementado sem funcionalidade (placeholder)."""
        pass

    def processar_dataframe(self, nome_arquivo, texto_alvo=None):
        df_recibo = pd.read_csv(nome_arquivo, sep=';', skiprows=9, nrows=1)

        desconto = pd.read_csv(nome_arquivo, sep=';', skiprows=13, nrows=1)

        df1 = pd.read_csv(nome_arquivo, sep=';', skiprows=15)


        """--------------------Tabela Principal----------------"""
        if 'Endosso / Fatura' in df1.columns:
            df1 = pd.read_csv(nome_arquivo, sep=';', skiprows=15,)
        else: 
            df1 = pd.read_csv(nome_arquivo, sep=';', skiprows=16)

        df1['Endosso / Fatura'] = df1['Endosso / Fatura']
        df1['Apolice'] = df1['Apolice'].astype(str)
        df1['Segurado'] = df1['Segurado'].str.strip()
        df1['Premio'] = df1['Premio']
        df1['% Comissao'] = df1['% Comissao'] 
        df1['Valor Comissao'] = df1['Valor Comissao'] 
        df1['Parcela'] = df1['Parcela'].str.split('/').str[0].str.replace("'", "")
        #Ranomeando as colunas:
        df1 = df1.drop(columns=['Marca', 'Lancamento'])
        colunas = ['Segurado', 'Apolice', 'Endosso','Parc', 'Prêmio', '%', 'Comissão']
        df1.columns = colunas
        df1 = df1.astype(str)

        if len(df1.columns) >= len(colunas):
            df1.columns = colunas
        df1 = df1.astype(str)
        """-------------------------------------------------------"""



        """---------------------Tabela Desconto-------------------"""
        df_desconto = pd.DataFrame()
        desc = desconto['Desc. de Adiantamento - R$'].iloc[0]
        vlr_desconto = number_format(desc)
        if vlr_desconto != '0,00' and vlr_desconto != 0:
            df_desconto['Segurado'] = ['Desc. de Adiantamento - R$']
            df_desconto['apolice'] = ['0']
            df_desconto['Endosso'] = ['0']
            df_desconto['Parcela'] = ['0']
            df_desconto['Premio'] = ['0,00']
            df_desconto['% Comissao'] = ['0,00']
            df_desconto['Valor Comissao'] = ('-' + desconto['Desc. de Adiantamento - R$'].astype(str)).str.replace(' ', '')
            ## Renomeando as colunas
            colunas = ['Segurado', 'Apolice', 'Endosso', 'Parc', 'Prêmio', '%', 'Comissão']
            df_desconto.columns = colunas
            df = pd.concat([df1, df_desconto], ignore_index=True)
        else:
            df = df1
        """-------------------------------------------------------"""



        recibo = ' '.join(df_recibo['Nr. Demonstrativo'].astype(str).tolist())
        #df['Data'] = leitura_data_arquivo(nome_arquivo)
        df['Recibo'] = recibo
        df['Data'] = leitura_data_arquivo(nome_arquivo)
        df['Prêmio'] = df['Prêmio'].apply(number_format)
        df['%'] = df['%'].apply(number_format)
        df['Comissão'] = df['Comissão'].apply(number_format)

        return df