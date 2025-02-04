import os
import streamlit as st
import boto3
from decouple import config
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.output_parsers import StrOutputParser

def initial_parameters() -> tuple:
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return model, parser, client

model, parser, client = initial_parameters() 

st.set_page_config(
    page_title='Stock Sales',
    page_icon='📄',
)
st.header('Assistente de Estoque')

model_options = [
    'Nenhum',
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o',
]
selected_model = st.sidebar.selectbox(
    label='Selecione o modelo LLM',
    options=model_options,
)

st.sidebar.markdown('### Sobre')
st.sidebar.markdown('Este agente consulta um banco de dados de estoque utilizando um modelo de LLM.')

st.write('Faça perguntas sobre o estoque de produtos, preços e reposições.')
user_question = st.text_input('O que deseja saber sobre o estoque?')
database_name = st.text_input('Nome do Banco de Dados')
table_name = st.text_input('Nome da Tabela')
start_date = st.date_input('Data de Início')
end_date = st.date_input('Data de Fim')

model = ChatOpenAI(
    model=selected_model,
)

# Conexão com o Amazon Athena usando boto3
athena_client = boto3.client(
    'athena',
    region_name='your-region',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def query_athena(query: str):
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database_name
        },
        ResultConfiguration={
            'OutputLocation': 's3://your-athena-staging-dir/'
        }
    )
    query_execution_id = response['QueryExecutionId']
    
    # Espera a consulta ser concluída
    status = 'RUNNING'
    while status in ['RUNNING', 'QUEUED']:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']
    
    if status == 'SUCCEEDED':
        result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        return result['ResultSet']['Rows']
    else:
        raise Exception('Query failed')

if st.button('Consultar'):
    if user_question and database_name and table_name and start_date and end_date:
        with st.spinner('Consultando o banco de dados...'):
            query = f"""
            SELECT * FROM {table_name}
            WHERE date >= '{start_date}' AND date <= '{end_date}'
            AND question LIKE '%{user_question}%'
            """
            results = query_athena(query)
            st.write(results)
    else:
        st.warning('Por favor, insira a pergunta, nome do banco de dados, nome da tabela e selecione as datas.')