import logging
from importlib import import_module
from rules.regras import rules_dict
from extraction import *
from architecture.path import *
import pandas as pd

logging.basicConfig(level=logging.INFO)

class DataExtractor:
    def __init__(self, seguradora):
        self.configs = rules_dict[seguradora]
        self.seguradora = seguradora
        self.classe_extracao = self.carregar_extracao()

    def carregar_extracao(self):
        try:
            arquivo_extraction = self.configs['arquivo_extraction'].replace('.py', '')
            nome_classe = f'Extracao{self.seguradora.capitalize()}'
            modulo = f'extraction.{arquivo_extraction.lower()}'
            mod = import_module(modulo)
            return getattr(mod, nome_classe)
        except (ModuleNotFoundError, AttributeError) as e:
            logging.error(f"Erro ao carregar a classe para {self.seguradora}: {e}")
            return None

    def extrair_dados(self):
        if self.classe_extracao:
            logging.info(f"Iniciando extração para {self.seguradora}")
            # Modificação aqui: não passamos mais o texto_alvo
            estrategia = DataExtractorStrategy(
                self.configs['nom_arquivo'], 
                self.configs['extensao'], 
                self.configs, 
                self.classe_extracao
            )
            resultado = estrategia.processar_arquivos()
            # Verifica se o resultado é um DataFrame
            if isinstance(resultado, pd.DataFrame):
                return resultado
            else:
                logging.error(f"Resultado da extração não é um DataFrame: {resultado}")
                return None
        else:
            logging.error(f"Classe de extração não encontrada para {self.seguradora}")
            return None

    def start(self):
        logging.info(f"Processando seguradora: {self.seguradora}")
        resultado = self.extrair_dados()
        # Verificação do resultado
        if resultado is not None and isinstance(resultado, pd.DataFrame) and not resultado.empty:
            logging.info(f"Extração concluída para {self.seguradora}")
            return resultado
        else:
            logging.error(f"Falha na extração de dados para {self.seguradora} ou DataFrame vazio")
            return None

# Lista de seguradoras a serem processadas
seguradoras = [
'azul'
,'alfa'
,'mitsui'
,'cardif'
]

if __name__ == "__main__":
    dfs_resultados = []
    
    for seguradora in seguradoras:
        extractor = DataExtractor(seguradora)
        resultado = extractor.start()
        if resultado is not None:  
            dfs_resultados.append(resultado)

    # Exibe os DataFrames
    for df in dfs_resultados:
        if isinstance(df, pd.DataFrame):
            print(df)
        else:
            logging.warning("Resultado não é um DataFrame.")
