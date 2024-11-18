import fitz
from architecture.extrategia_extracao import *
from architecture.functions import *
import re
import pandas as pd
from extraction.cardif import * 


class ExtracaoAzul(ExtracaoCardif):

    def processar_dataframe(self, nome_arquivo, texto_alvo="Segurado\nCPF / CNPJ\n"):
        """-------------------------------------------------------------"""
        """-----------------------TABELA PRINCIPAL----------------------"""
        """-------------------------------------------------------------"""
        try:
            """Abstrai de ExtracaoCardif a função extrair texto"""
            texto_extraido = self.extrair_texto(nome_arquivo, texto_alvo)
            
            padrao_nome = r'\b[A-Z]+(?:\s+[A-Z]+)*\b'
            nomes_segurado = re.findall(padrao_nome, texto_extraido)
            del nomes_segurado[-1]

            padrao_nome = r'\b[A-Z]+(?:\s+[A-Z]+)*\b'
            padrao_data = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
            
            nome_match = re.search(padrao_nome, texto_extraido)
            if nome_match is None:
                raise ValueError(f"Nome não encontrado no arquivo: {nome_arquivo}")

            nome_entre_linhas = nome_match.group(0)
            dados = [nome_entre_linhas]
            partes = re.split(padrao_data, texto_extraido)
            dados.extend([parte.strip() for parte in partes[1:] if parte.strip()])

            df1 = pd.DataFrame(dados, columns=["Conteúdo"])
            df1 = df1['Conteúdo'].str.split('\n', expand=True)
            df1 = df1.iloc[:, :10]
            
            # Move o dado da primeira linha da primeira coluna para a coluna 8
            primeira_linha = df1.iloc[0]
            df1.iloc[0, 8] = primeira_linha[0]
            nome = df1[8]
            df1 = df1.iloc[1:].reset_index(drop=True)
            df1['nome'] = nome
            df1['segurado'] = nomes_segurado 

            # Transformação das colunas
            df1 = df1.drop(columns=[9])
            df1 = df1.drop(columns=[3])
            df1 = df1.drop(columns=[7])
            df1 = df1.drop(columns=[5])
            df1 = df1.drop(columns=[8])
            df1 = df1.drop(columns=['nome'])
            df1.columns = ['Apolice', 'Parc', '%', 'Prêmio', 'Comissão', 'Segurado']
            df1['Parc'] = df1['Parc'].str.split('/').str[0]
        except Exception:
            df1 = None


        """-------------------------------------------------------------"""
        """-----------------------TABELA RECUPERAÇÃO----------------------"""
        """-------------------------------------------------------------"""

        try:

            texto_extraido = self.extrair_texto(nome_arquivo, "Descrição")
            padrao_nome = r'\b[A-Z]+(?:\s+[A-Z]+)*\b'
            padrao_data = r'\b\d{2}\.\d{2}\.\d{2}\.\d{6}-\d{3}\b'
            
            nome_match = re.search(padrao_nome, texto_extraido)
            if nome_match is None:
                raise ValueError(f"Nome não encontrado no arquivo: {nome_arquivo}")

            nome_entre_linhas = nome_match.group(0)
            dados = [nome_entre_linhas]
            partes = re.split(padrao_data, texto_extraido)
            dados.extend([parte.strip() for parte in partes[1:] if parte.strip()])

            df2 = pd.DataFrame(dados, columns=["Conteúdo"])
            df2 = df2['Conteúdo'].str.split('\n', expand=True)
            
            # Nova lógica para a coluna nome
            primeira_linha = df2.iloc[0]
            df2.iloc[0, 2] = primeira_linha[0]
            nome = df2[2]
            df2 = df2.iloc[1:].reset_index(drop=True)
            df2['nome'] = nome
            
            # Resto das transformações
            apolice = re.findall(padrao_data, texto_extraido)
            df2 = df2.drop(columns=[0, 2])
            df2['Apolice'] = apolice
            df2['Parc'] = '0'
            df2['%'] = '0,00'
            df2['Prêmio'] = '0,00'
            df2.columns = ['Comissão', 'Segurado', 'Apolice', 'Parc', '%', 'Prêmio']
            df2 = df2[['Apolice', 'Parc', '%', 'Prêmio', 'Comissão', 'Segurado']]
        except Exception:
            df2 = None

        # Concatenar DataFrames, se ambos não são None
        if df1 is not None and df2 is not None:
            df = pd.concat([df1, df2], ignore_index=True)
        elif df1 is not None:
            df = df1
        elif df2 is not None:
            df = df2



        if not df.empty:
            df['Data'] = leitura_data_arquivo(nome_arquivo)
            df['Recibo'] = extrair_data_do_nome_arquivo(nome_arquivo)
            df['Prêmio'] = df['Prêmio'].apply(number_format)
            df['%'] = df['%'].apply(number_format)
            df['Comissão'] = df['Comissão'].apply(number_format)
            df['Apolice'] = df['Apolice'] = df['Apolice'].str.replace(".", "").str.replace("-", "").str.strip()
            df['Cnpj'] = extrair_informacao_pdf(nome_arquivo, 'C.N.P.J. ',  r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')
            df['Cnpj'] = df['Cnpj'].str.replace(".", "").str.replace("-", "").str.replace("/", "")


        return df