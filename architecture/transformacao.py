from .extrategia_extracao import *
import pandas as pd


class Transformacao:
    def __init__(self, estrategia: EstrategiaExtracao, configuracao):
        """Inicializa o extrator com a estratégia apropriada e os dados do dicionário de configuração."""
        self.estrategia = estrategia
        self.configuracao = configuracao  # Armazena o dicionário de configuração
        self.df = None  # DataFrame que será preenchido após a extração e processamento

    def extrair_e_processar(self, nome_arquivo):
        """Executa a extração e processamento de dados."""
        self.df = self.estrategia.processar_dataframe(nome_arquivo)

    def construir_tabela(self):
        """Constrói a tabela final com os dados extraídos."""
        resultados = []
        
        for index, row in self.df.iterrows():
            resposta = {
                'NumeroRecibo': row.get('Recibo') if self.configuracao.get("NumeroRecibo") is False else self.configuracao["NumeroRecibo"],
                'DataExtrato': row['Data'] if self.configuracao.get("data") is False else self.configuracao["data"],  
                'NumeroApolice': row['Apolice'],
                'NumeroProposta': '',
                'NumeroEndosso': row.get('Endosso') if self.configuracao.get("NumeroEndosso") is False else self.configuracao["NumeroEndosso"],
                'NumeroParcela': row.get('Parc') if self.configuracao.get("NumeroParcela") is False else self.configuracao["NumeroParcela"],
                'DataVencimento': '',
                'Dataextrato': row['Data'] if self.configuracao.get("data") is False else self.configuracao["data"],    
                'dataExtrato': row['Data'] if self.configuracao.get("data") is False else self.configuracao["data"],  
                'VlBase': row['Prêmio'],
                'PercComissao': row['%'],
                'VlComissao': row['Comissão'],
                'CdRamoSusep': row.get('Ramo') if self.configuracao.get("CdRamoSusep") is False else self.configuracao["CdRamoSusep"],
                'NmRamoSusep': '',
                'CdProduto': '',
                'NmProduto': '',
                'CNPJSegurado': '',
                'NmSegurado': row['Segurado'],
                'CNPJTomador': '',
                'NmTomador': '',
                'CanalVenda': self.configuracao["CanalVenda"],
                'CdFilial': '',
                'CNPJSeguradora': row['Cnpj'] if self.configuracao.get("CNPJSeguradora") is False else self.configuracao["CNPJSeguradora"],
                'NmSeguradora': row['Seguradora'] if self.configuracao.get("NmSeguradora") is False else self.configuracao["NmSeguradora"],  
            }

            resultados.append(resposta)

        tabela_final = pd.DataFrame(resultados)
        tabela_final['NmSegurado'] = tabela_final['NmSegurado'].str.strip()
        return tabela_final

