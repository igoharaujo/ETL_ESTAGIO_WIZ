import fitz
from architecture.extrategia_extracao import *
from architecture.functions import *
import re
import pandas as pd
import os


class ExtracaoMitsui(EstrategiaExtracao):
    def extrair_texto(self, nome_arquivo, texto_alvo):
        """Método abstrato implementado sem funcionalidade (placeholder)."""
        pass

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

    def processar_dataframe(self, texto_extraido, nome_arquivo):
        """Processa o arquivo Excel e formata o DataFrame conforme necessário."""
        # Note que adicionei o parâmetro texto_extraido para manter a consistência com a interface
        
        df = pd.read_excel(nome_arquivo)
        num_extrato = self.extrair_num_extrato(df)

        df = pd.read_excel(nome_arquivo, skiprows=6, dtype={'Apolice': str})

        # Filtra linhas e colunas necessárias
        df = df.dropna(subset=['Segurado', 'Apolice'])
        df = df.dropna(axis=1, how='all')
        df = df.drop(columns=['Natureza', 'Valor Comissão Antecipada (R$)', 'Valor Comissão (R$)', 'Data Baixa'])
        df = df.rename(columns={'Prêmio (R$)': 'Prêmio', 'Valor Total Comissão (R$)': 'Comissão'})

        #df.columns = ['Endosso', 'Apolice', 'Segurado', 'Ramo', 'Prêmio', '%', 'Comissão']
        df['Prêmio'] = df['Prêmio'].apply(lambda x: "{:.2f}".format(x).replace('.', ',').strip())
        df['%'] = df['%'].apply(lambda x: "{:.2f}".format(x).replace('.', ',').strip())
        df['Comissão'] = df['Comissão'].apply(lambda x: "{:.2f}".format(x).replace('.', ',').strip())
        df['Ramo'] = df['Ramo'].str.split('-').str[0].str.strip()
        df['Data'] = leitura_data_arquivo(nome_arquivo)
        df['Recibo'] = extrai_recibo('Extrato: ',r"\d{4}", nome_arquivo)
        df = df.astype(str)


        return df




