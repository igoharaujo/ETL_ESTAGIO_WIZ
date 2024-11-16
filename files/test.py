import fitz
from architecture.extrategia_extracao import *
from architecture.extracao_data import *
import re
import pandas as pd


class ExtracaoMitsui:
    def extrair_num_extrato(self, mitsui):
        """Extrai o número do extrato a partir de uma célula contendo 'Extrato:'."""
        def extrair_valor(cell):
            if isinstance(cell, str) and 'Extrato: ' in cell:
                posicao_inicial = cell.find('Extrato: ') + len('Extrato: ')
                posicao_final = cell.find(' ', posicao_inicial)
                if posicao_final == -1:
                    posicao_final = len(cell)
                return cell[posicao_inicial:posicao_final].strip()
            return None

        num_extrato = mitsui.applymap(extrair_valor).stack().dropna().iloc[0]
        return num_extrato

    def processar_dataframe(self, nome_arquivo):
        """Processa o arquivo Excel e formata o DataFrame conforme necessário."""
        
        # Lê o arquivo e extrai o número do extrato
        mitsui = pd.read_excel(nome_arquivo)
        num_extrato = self.extrair_num_extrato(mitsui)

        # Releitura do Excel, pulando as primeiras linhas irrelevantes
        mitsui = pd.read_excel(nome_arquivo, skiprows=6, dtype={'Apolice': str})

        # Filtra linhas e colunas necessárias
        mitsui = mitsui.dropna(subset=['Segurado', 'Apolice'])
        mitsui = mitsui.dropna(axis=1, how='all')

        # Extração de dados
        data = leitura_data_arquivo(nome_arquivo)
        parcela = mitsui['Parcela']
        segurado = mitsui['Segurado']
        premio = mitsui['Prêmio (R$)'].apply(lambda x: "{:.2f}".format(x).replace('.', ',').strip())
        perc_comissao = mitsui['%'].apply(lambda x: "{:.2f}".format(x).replace('.', ',').strip())
        comissao = mitsui['Valor Total Comissão (R$)'].apply(lambda x: "{:.2f}".format(x).replace('.', ',').strip())
        apolice = mitsui['Apolice']
        ramo = mitsui['Ramo'].str.split('-').str[0].str.strip()

extracao = ExtracaoMitsui()
df_processado, numero_arquivo = extracao.processar_dataframe('MITSUI 18-09.xlsx')
arquivo_saida = extracao.salvar_arquivo(df_processado, numero_arquivo)
