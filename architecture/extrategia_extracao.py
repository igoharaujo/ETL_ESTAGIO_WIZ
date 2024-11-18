from abc import ABC, abstractmethod

# Interface para as estratégias de extração
class EstrategiaExtracao(ABC):
    @abstractmethod
    def extrair_texto(self, nome_arquivo, texto_alvo):
        """Método abstrato para extrair o texto do PDF."""
        pass

    @abstractmethod
    def processar_dataframe(self, nome_arquivo, texto_alvo):
        """Método abstrato para processar o texto extraído em um DataFrame."""
        pass
