import pandas as pd
import re
from pathlib import Path
import fitz
from typing import Optional
import datetime

def leitura_data_arquivo(nom_arquivo):
    """Extrai o campo DataExtrato do nome do arquivo"""
    ano_atual = datetime.datetime.now().year
    # Usar expressão regular para encontrar a data no nome do arquivo
    match = re.search(r'(\d{2}-\d{2})', nom_arquivo)
    if match:
        # Extrair a data encontrada
        data_str = match.group(1)
        # Dividir a data pelo traço para obter dia e mês
        dia_mes_split = data_str.split('-')
        dia = dia_mes_split[0]
        mes = dia_mes_split[1]

        data_formatada = f"{dia}/{mes}/{ano_atual}"
        return data_formatada
    else:
        return "Data não encontrada no nome do arquivo"


def extrair_data_do_nome_arquivo(nome_arquivo: str) -> str:
    """Extrai a data do nome do arquivo."""
    ano_atual = datetime.datetime.now().year
    padrao_data = r'(\d{2}-\d{2})'
    padrao_numero = r'\((\d+)\)'
    
    match_data = re.search(padrao_data, nome_arquivo)
    match_numero = re.search(padrao_numero, nome_arquivo)
    
    if not match_data:
        return "Data não encontrada no nome do arquivo"
    
    dia, mes = match_data.group(1).split('-')
    data_formatada = f"{ano_atual}{mes}{dia}"
    
    if match_numero:
        data_formatada += match_numero.group(1)
    
    return data_formatada

def extrair_informacao_excel(df: pd.DataFrame, texto_alvo: str, padrao: str) -> Optional[str]:
    """Extrai informação de um DataFrame do Excel."""
    for _, linha in df.iterrows():
        linha_completa = ' '.join(linha.astype(str))
        if texto_alvo in linha_completa:
            correspondencia = re.search(padrao, linha_completa)
            if correspondencia:
                return correspondencia.group()
    return None

def extrair_informacao_pdf(doc: fitz.Document, texto_alvo: str, padrao: str) -> Optional[str]:
    """Extrai informação de um documento PDF."""
    texto_completo = "".join(pagina.get_text() for pagina in doc)
    if texto_alvo in texto_completo:
        indice_texto = texto_completo.find(texto_alvo)
        texto_a_partir_do_alvo = texto_completo[indice_texto:]
        correspondencia = re.search(padrao, texto_a_partir_do_alvo)
        if correspondencia:
            return correspondencia.group()
    return None

def extrai_recibo(texto_alvo: str, padrao: str, nome_arquivo: str) -> Optional[str]:
    """Extrai informações de arquivos Excel ou PDF com base em um padrão específico."""
    arquivo = Path(nome_arquivo)
    
    try:
        if arquivo.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(arquivo)
            return extrair_informacao_excel(df, texto_alvo, padrao)
        elif arquivo.suffix == '.pdf':
            with fitz.open(arquivo) as doc:
                return extrair_informacao_pdf(doc, texto_alvo, padrao)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {arquivo.suffix}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {nome_arquivo}: {str(e)}")
        return extrair_data_do_nome_arquivo(nome_arquivo)