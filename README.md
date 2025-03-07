# Airport Manager

O **Airport Manager** é uma aplicação web desenvolvida para gerenciar voos, companhias aéreas, passageiros e avaliações de serviços. A aplicação permite visualizar métricas importantes, como o total de voos, passageiros, médias de notas e muito mais.

## Funcionalidades

- **Gerenciamento de Voos:**
  - Adicionar, editar e excluir voos.
  - Visualizar detalhes de voos, como número do voo, companhia aérea, modelo de aeronave, quantidade de passageiros e horários.

- **Gerenciamento de Companhias Aéreas:**
  - Adicionar, editar e excluir companhias aéreas.
  - Visualizar métricas específicas de cada companhia, como total de voos, passageiros e médias de notas.

- **Dashboard:**
  - Visualizar informações gerais, como total de voos, passageiros e médias de notas.
  - Gráficos e tabelas para análise de dados, como voos por tipo de aeronave, passageiros por companhia e médias de notas.

- **Avaliações:**
  - Registrar avaliações de voos, incluindo notas para objetivo, pontualidade, serviços e pátio.
  - Visualizar médias de avaliações por companhia aérea.

## Tecnologias Utilizadas

- **Front-end:**
  - HTML, CSS, JavaScript
  - Bootstrap para estilização e layout responsivo.
  - Chart.js para gráficos interativos.

- **Back-end:**
  - Python com Flask para desenvolvimento da aplicação web.
  - SQLAlchemy para gerenciamento do banco de dados.

- **Banco de Dados:**
  - SQLite (ou outro banco de dados suportado pelo SQLAlchemy).

## Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior.
- Pip (gerenciador de pacotes do Python).

### Passos para Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/airport-manager.git
   cd airport-manager

2. **Crie um ambiente virtual (opcional, mas recomendado):**

  ```bash
  python -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instale as dependências:**

  ```bash
  pip install -r requirements.txt
