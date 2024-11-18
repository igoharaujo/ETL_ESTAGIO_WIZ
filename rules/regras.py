alfa = {
    "NmSeguradora": False,  # Quando False, ele pega o dado na pasta extraction
    "CNPJSeguradora": False,  
    "NumeroParcela": 'False',
    "CanalVenda": "Conseg",  # Defina o canal de venda específico
    "CdRamoSusep": False,  
    "data": False,  
    "NumeroRecibo": False,  
    "NumeroEndosso": False,  
    "extensao": '.csv',  # Extensão do arquivo que está sendo processado
    "nom_arquivo": 'ALFA',  # Nome padrão para o arquivo da seguradora Alfa
    "arquivo_extraction": 'alfa.py'  # Arquivo correspondente ao processo de extração da Alfa
}

cardif = {
    "NmSeguradora": "CARDIF",
    "CNPJSeguradora": "0000000000000-00",
    "NumeroParcela": False,
    "CanalVenda": "Conseg",
    "CdRamoSusep": False,  
    "data": False,
    "NumeroRecibo": False,
    "NumeroEndosso": False,
    "extensao": '.pdf',
    "nom_arquivo": 'CARDIF',
    "arquivo_extraction": 'cardif.py'  
}

mitsui = {
    "NmSeguradora": "MITSUI",
    "CNPJSeguradora": "0000000000000-00",
    "NumeroParcela":'False',
    "CanalVenda": "Conseg",
    "CdRamoSusep": False,  
    "data": False,
    "NumeroRecibo": False,
    "NumeroEndosso": False,
    "extensao": '.xlsx',
    "nom_arquivo": 'MITSUI',
    "arquivo_extraction": 'mitsui.py' 
}


azul = {
    "NmSeguradora": "AZUL",
    "CNPJSeguradora": False,
    "NumeroParcela":False,
    "CanalVenda": "Conseg",
    "CdRamoSusep": False,  
    "data": False,
    "NumeroRecibo": False,
    "NumeroEndosso": False,
    "extensao": '.pdf',
    "nom_arquivo": 'AZUL',
    "arquivo_extraction": 'azul.py' 
}


ylm = {
    "NmSeguradora": "YLM",
    "CNPJSeguradora": '00000',
    "NumeroParcela":False,
    "CanalVenda": "Conseg",
    "CdRamoSusep": False,  
    "data": False,
    "NumeroRecibo": False,
    "NumeroEndosso": False,
    "extensao": '.csv',
    "nom_arquivo": 'YLM',
    "arquivo_extraction": 'ylm.py' 
}



rules_dict = {
    'cardif': cardif,
    'mitsui': mitsui,
    'alfa': alfa,
    'azul': azul,
    'ylm': ylm  
}

