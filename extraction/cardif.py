import fitz
from architecture.extrategia_extracao import *
from architecture.functions import *
import re
import pandas as pd

class ExtracaoCardif(EstrategiaExtracao):
    def extrair_texto(self, nome_arquivo, texto_alvo="01220213000191"):
        """Extrai o texto de um PDF com um formato específico."""
        try:
            doc = fitz.open(nome_arquivo)
            texto_extraido = ""

            for page_num in range(len(doc)):
                pagina = doc[page_num]
                texto = pagina.get_text("text")
                indice = texto.find(texto_alvo)
                
                if indice != -1:
                    texto_extraido += texto[indice + len(texto_alvo):] + "\n"
            
            doc.close()
            if not texto_extraido:
                raise ValueError(f"Texto alvo não encontrado no arquivo: {nome_arquivo}")
            return texto_extraido
            
        except fitz.FileDataError:
            print(f"Erro ao abrir o arquivo PDF: {nome_arquivo}")
        except Exception as e:
            print(f"Erro inesperado ao processar o arquivo {nome_arquivo}: {str(e)}")
        return ""

    def processar_dataframe(self, nome_arquivo, texto_alvo="01220213000191"):
        """Processa o texto extraído em um DataFrame formatado."""
        texto_extraido = self.extrair_texto(nome_arquivo, texto_alvo)
        
        padrao_data = r'\b\d{2}/\d{2}/\d{4}\b'
        partes = re.split(padrao_data, texto_extraido)

        dados = [parte.strip() for parte in partes if parte.strip()]
        df = pd.DataFrame(dados, columns=["Conteúdo"])
        df = df['Conteúdo'].str.split('\n', expand=True)
        df = df.iloc[:, :8]

        """-----------------Transformação das colunas-----------------------"""
        df = df.applymap(lambda x: ' '.join([word for word in str(x).split() if not re.search(r'[a-z]', word)]))
        df = df.drop(columns=[3])
        df[2] = df[2].str.replace('-', '')
        
        df.columns = ['Endosso', 'Apolice', 'Segurado', 'Ramo', 'Prêmio', '%', 'Comissão']
        df = df.drop(df.index[-1])  # Remover a última linha, se necessário
        df['Prêmio'] = df['Prêmio'].apply(number_format)
        df['Recibo'] = extrai_recibo('No. Recibo\n',r"\d{7}",nome_arquivo)
        df['Data'] = leitura_data_arquivo(nome_arquivo)
        df['Parc'] = '0'

        return df