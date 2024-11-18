
![Imagem do projeto](img/arquitetura.png)

# Sobre o projeto:

Este projeto foi desenvolvido de forma independente durante o meu estágio na wiz co. Ele surgiu com o objetivo de automatizar um processo que exigia intervenção manual. Ele extrai informações de mais de 20 extratos provenientes de diferentes seguradoras, incluindo formatos como PDF, TXT, CSV e Excel, realiza a limpeza e transformação desses dados de acordo com a regra de cada seguradora, deixando-os prontos para serem carregados no datalake e, posteriormente, inseridos no banco de dados da empresa.

OBs: Esta é a estrutura do projeto após a refatoração. Não seguirei incluindo edições ou novas implementações nessa versão pública, com o objetivo de mantê-lo acessível e sem informações sensíveis.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `architecture/`: Contém as classes base e interfaces para a extração de dados, e funções.
- `extraction/`: Implementações específicas para cada seguradora.
- `rules/`: Regras e configurações para cada seguradora.
- `main.py`: Ponto de entrada principal do programa.

## Configuração do Ambiente

### Passo 1: Clonar o Repositório

Clone o repositório do projeto para o seu ambiente local e navegue até o diretório do projeto.

### Passo 2: Criar e Ativar o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto e ative-o. No macOS/Linux, use o comando `source` para ativar o ambiente. No Windows, use o comando `.\venv\Scripts\activate`.

### Passo 3: Instalar Dependências

Instale todas as dependências necessárias listadas no arquivo `requirements.txt` usando o comando `pip install -r requirements.txt`.


## Uso

1. Coloque os arquivos das seguradoras na pasta `files/`.
2. Adicione ou atualize as regras de extração de dados no arquivo `rules/regras.py`.
3. Implemente transformação ou atualize as classes de extração específicas para cada seguradora na pasta `extraction/`.
4. Execute o `main.py` para processar os arquivos e gerar os resultados.

O sistema extrairá automaticamente todos os dados dos arquivos na pasta e os salvará em um arquivo Excel consolidado.

## Adicionando Novas Seguradoras

Para adicionar suporte a uma nova seguradora:

1. Crie uma nova classe de extração em `extraction/` que herde de `EstrategiaExtracao`.
2. Implemente os métodos `extrair_texto` e `processar_dataframe` para a nova seguradora.
3. Adicione as regras e configurações da nova seguradora em `rules/regras.py`.
4. Atualize a lista de seguradoras em `main.py` para incluir a nova seguradora.

