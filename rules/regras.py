cardif = {
    "NmSeguradora": "CARDIF",
    "CNPJSeguradora": "0000000000000-00",
    "CanalVenda": "Conseg",
    "CdRamoSusep": False,  
    "data": False,
    "NumeroRecibo": False,
    "NumeroEndosso": False,
    "extensao": '.pdf',
    "nom_arquivo": 'CARDIF',
    "arquivo_extraction": 'cardif.py'  # Arquivo de extração correspondente
}

mitsui = {
    "NmSeguradora": "MITSUI",
    "CNPJSeguradora": "0000000000000-00",
    "CanalVenda": "Conseg",
    "CdRamoSusep": False,  
    "data": False,
    "NumeroRecibo": False,
    "NumeroEndosso": False,
    "extensao": '.xlsx',
    "nom_arquivo": 'MITSUI',
    "arquivo_extraction": 'mitsui.py' 
}

alfa = {
    "NmSeguradora": False,  # Nome da seguradora
    "CNPJSeguradora": False,  # CNPJ pode ser preenchido se necessário
    "CanalVenda": "Conseg",  # Defina o canal de venda específico
    "CdRamoSusep": False,  # Caso não tenha o código do ramo
    "data": False,  # Precisa de data, então mantemos True
    "NumeroRecibo": False,  # Extrai o número do recibo 
    "NumeroEndosso": False,  # Se não extrair o endosso, mantenha como False
    "extensao": '.csv',  # Extensão do arquivo que está sendo processado
    "nom_arquivo": 'ALFA',  # Nome padrão para o arquivo da seguradora Alfa
    "arquivo_extraction": 'alfa.py'  # Arquivo correspondente ao processo de extração da Alfa
}


rules_dict = {
    'cardif': cardif,
    'mitsui': mitsui,
    'alfa': alfa  
}

