
# SWAPI Vehicle Management

Este projeto implementa um serviço web para gerenciar veículos da franquia Star Wars. Ele permite listar, adicionar, excluir e buscar veículos,personagens,filmes,naves,planetas,especies e favoritos na base de dados local, bem como buscar veículos,personagens,filmes,naves,planetas e especies diretamente da API SWAPI. Utiliza Flask como framework web e SQLAlchemy para manipulação do banco de dados.

## Requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

- Python (versão 3.6 ou superior)
- pip (gerenciador de pacotes do Python)

## Instalação

Siga os passos abaixo para instalar e configurar o projeto no Windows:

### 1. Clone o Repositório

Abra o Prompt de Comando (cmd) e navegue até o diretório onde deseja clonar o repositório. Em seguida, execute o comando:

```bash
git clone https://github.com/JeremiasONunes/Swapi_api
```

### 2. Navegue até o Diretório do Projeto

Entre no diretório do projeto clonado:

```bash
cd Swapi_api
```

### 3. Crie um Ambiente Virtual

É uma boa prática usar um ambiente virtual para gerenciar as dependências do seu projeto. Execute o comando abaixo para criar um ambiente virtual:

```bash
python -m venv .venv
```

### 4. Ative o Ambiente Virtual

Ative o ambiente virtual que você acabou de criar:

```bash
.venv\Scripts\activate
```

### 5. Instale as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto usando o seguinte comando:

```bash
pip install Flask Flask-SQLAlchemy requests Flask-Migrate
```

### 6. Configure o Banco de Dados

Crie um arquivo chamado `config.py` no diretório do seu projeto e adicione a seguinte configuração:

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 7. Execute as Migrações (se necessário)

Se você estiver usando o Flask-Migrate, inicialize o repositório de migração e crie as tabelas no banco de dados:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 8. Execute o Servidor

Agora, você pode executar o servidor Flask. Certifique-se de que o ambiente virtual ainda está ativado e execute:

```bash
python -m Routes.app
```

O servidor estará em execução em `http://127.0.0.1:5000`.

### 9. Acesse a API

Você pode acessar a API em seu navegador ou usando ferramentas como Postman ou Insomnia. Para listar os veículos, acesse:

```
GET http://127.0.0.1:5000/veiculos
```

## Contribuição

Sinta-se à vontade para contribuir para este projeto. Abra um pull request ou envie um issue se encontrar algum problema.

## Licença

Este projeto é licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.
