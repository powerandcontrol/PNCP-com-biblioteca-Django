# Portal Nacional de Contratações Públicas - PNCP

Este projeto é um portal para consultar contratos públicos vigentes, contratações por data de publicação e outras funcionalidades relacionadas às contratações públicas.

## Tecnologias Utilizadas

- Python
- Django
- HTML
- CSS
- JavaScript

## Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

- [Git](https://git-scm.com)
- [Python](https://www.python.org/downloads/)
- [Virtualenv](https://pypi.org/project/virtualenv/)

Além disso, é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/).

## Clonando o Repositório

```bash
# Clone este repositório
$ git clone https://github.com/powerandcontrol/contratos-pncp.git

# Acesse a pasta do projeto no terminal/cmd
$ cd contratos-pncp

# Crie um ambiente virtual
$ python -m venv venv

# Ative o ambiente virtual
# No Windows
$ venv\Scripts\activate
# No Linux/Mac
$ source venv/bin/activate

# Instale as dependências
$ pip install -r Django requests tqdm

# Faça as migrações
$ python manage.py migrate

# Crie um superusuário
$ python manage.py createsuperuser

# Execute a aplicação
$ python manage.py runserver

A aplicação estará disponível no endereço http://127.0.0.1:8000.

Funcionalidades
Consulta de contratos vigentes
Consulta de contratações por data de publicação
Filtros por data, município, modalidade de contratação e esfera
