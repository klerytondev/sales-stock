# Projeto: Assistente de Estoque

Este projeto utiliza Streamlit para criar uma interface de usuário que interage com um modelo de linguagem (LLM) para consultar um banco de dados de estoque.

## Estrutura de Pastas

```
.
├── projects
│   ├── app-athena.py
│   └── estoque.db
├── .env
├── requirements.txt
└── README.md
```

- `projects/app-athena.py`: Código principal da aplicação.
- `projects/estoque.db`: Banco de dados de estoque.
- `.env`: Arquivo contendo variáveis de ambiente, como a chave da API do OpenAI.
- `requirements.txt`: Lista de dependências do projeto.
- `README.md`: Este arquivo.

## Configurações Necessárias

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar e Ativar um Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API do OpenAI e as credenciais da AWS:

```
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
```

### 5. Executar a Aplicação

```bash
streamlit run projects/app-athena.py
```

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. Certifique-se de instalar todas elas antes de executar a aplicação.

## Sobre

Este projeto foi desenvolvido para fornecer uma interface amigável para consultar um banco de dados de estoque utilizando modelos de linguagem avançados.

