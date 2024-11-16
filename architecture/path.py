import os
import pandas as pd
import shutil
from .transformacao import Transformacao

class DataExtractorStrategy:
    def __init__(self, nome_base, extensao, configuracao, estrategia_cls):
        self.nome_base = nome_base
        self.extensao = extensao
        self.configuracao = configuracao
        self.estrategia_cls = estrategia_cls
        self.pasta_arquivos = "files"
        self.pasta_erros = "erro"
        self.dfs_resultados = []

        # Cria a pasta "erro" se não existir
        if not os.path.exists(self.pasta_erros):
            os.makedirs(self.pasta_erros)

    def processar_arquivos(self):
        for arquivo in os.listdir(self.pasta_arquivos):
            if self.nome_base in arquivo and arquivo.endswith(self.extensao):
                try:
                    self._processar_arquivo(arquivo)
                except Exception as e:
                    self._tratar_erro(arquivo, e)

        return self._consolidar_resultados()

    def _processar_arquivo(self, arquivo):
        # Instancia a estratégia de extração e o transformador
        extracao_estrategia = self.estrategia_cls()  # Cria uma instância da classe de estratégia
        extrator = Transformacao(
            extracao_estrategia,
            self.configuracao  # Passa o dicionário completo
        )

        # Extrai e processa os dados do arquivo
        extrator.extrair_e_processar(os.path.join(self.pasta_arquivos, arquivo), "01220213000191")

        # Constrói a tabela a partir dos dados extraídos
        tabela_resultado = extrator.construir_tabela()

        # Adiciona a tabela ao DataFrame de resultados
        self.dfs_resultados.append(tabela_resultado)

    def _tratar_erro(self, arquivo, erro):
        # Move o arquivo com erro para a pasta "erro"
        arquivo_com_erro = os.path.join(self.pasta_arquivos, arquivo)
        destino_erro = os.path.join(self.pasta_erros, arquivo)
        shutil.move(arquivo_com_erro, destino_erro)
        print(f"Erro ao processar {arquivo}: {str(erro)}. Arquivo movido para a pasta 'erro'.")

    def _consolidar_resultados(self):
        # Concatena todos os DataFrames em um único DataFrame
        if self.dfs_resultados:
            df_consolidado = pd.concat(self.dfs_resultados, ignore_index=True)

            # Salva o DataFrame consolidado em um arquivo Excel
            nome_arquivo_saida = f"resultado_consolidado_{self.nome_base}.xlsx"
            df_consolidado.to_excel(nome_arquivo_saida, index=False)
            print(f"Arquivo consolidado salvo como: {nome_arquivo_saida}")

            return df_consolidado
        else:
            print(f"Nenhum arquivo encontrado com o padrão '{self.nome_base}{self.extensao}'")
            return None
