from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from airflow.models import Variable
import time

# Variaveis
twitter = Variable.get("t_id")
email = Variable.get("t_email")
password = Variable.get("t_password")
list_followers = []

class User:
    def __init__(self, name, id):
        self.user_name = name
        self.user_id = id
        
        
class Principal():
    def __init__(self):
        # # Para teste, remove caracteres não reconhecidos das variaveis
        # import sys
        # sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
        # #
        
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from webdriver_manager.core.utils import ChromeType

        options = ChromeOptions()
        prefs = {
            'profile.managed_default_content_settinfs.images': 2,
            'intl.accept_languages': 'en, en_US'
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')

        self._driver = webdriver.Chrome(
            service = ChromeService(
                ChromeDriverManager(
                    chrome_type = ChromeType.CHROMIUM
                ).install()
            ),
            options = options
        )
        self._driver.implicitly_wait(5)
            
    def login(self):
        # import pandas as pd
    
        self._driver.get("https://twitter.com/i/flow/login")
        email_box = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label')))
        submit = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')))
        
        email_box.send_keys(email)
        submit.click()
        time.sleep(2)
        try:
            security = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label')))
            security.send_keys(twitter)
            submit = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')))
            submit.click()
            time.sleep(3)
        except:
          print('Não pediu ID')
        password_box = WebDriverWait(self._driver, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label')))
        password_box.send_keys(password)
    
        submit = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')))
        submit.click()
        time.sleep(3)
        
    def recover_data(self):
        self._driver.get("https://twitter.com/"+twitter+"/followers")
        
        for i in range(1, 100):
            try:
                user_name = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div['+str(i)+']/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]'))).text
                user_id = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div['+str(i)+']/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/a/div/div/span'))).text
                # Retornando vazio - Corrigir
                user = User(user_name, user_id)
                print(user_name)
                list_followers.append(user)
                # rolar pagina para carregar mais
            except:
                break
            
            
    def add_to_data_base(self):
        from airflow.hooks.base import BaseHook
        import psycopg2
        
        connection = BaseHook.get_connection("projeto_final")

        # Usar as informações da conexão
        conn = psycopg2.connect(
            host = connection.host,
            port = connection.port,
            user = connection.login,
            password = connection.password
        )
        
        cursor = conn.cursor()
        
        for user in list_followers:
            sql = f"""INSERT INTO FOLLOWERS_LIST (user_name, user_id) values ('{user.user_name}', '{user.user_id}')"""
            cursor.execute(sql)
            
        conn.commit()
        cursor.close()
        conn.close()
            
from datetime import datetime, timedelta

dag_args = {
    'owner': '',
    'retries': 0,
    'retry_delay': timedelta(minutes = 1)
}

start_date = datetime(2023,5,8)

with DAG(
    dag_id = 'pegar_dados',
    description = '', 
    default_args = dag_args,
    start_date = start_date,
    schedule = timedelta(hours=5),
    catchup = False
) as dag:    
    logar = PythonOperator(
        task_id = 'entrar',
        python_callable =  Principal().login,
    )
    
    recuperar_dados = PythonOperator(
        task_id = 'recuperar_dados',
        python_callable =  Principal().recover_data,
    )
    
    criar_tabela = PostgresOperator(
        task_id='criar_tabela',
        postgres_conn_id='projeto_final',
        sql = """
            CREATE TABLE IF NOT EXISTS FOLLOWERS_LIST(
                ID INT GENERATED BY DEFAULT AS IDENTITY,
                user_name VARCHAR NOT NULL,
                user_id VARCHAR NOT NULL
            )
            """
    )

    inserir_dados = PythonOperator(
        task_id = 'inserir_dados',
        python_callable =  Principal().add_to_data_base,
    )
    
logar >> recuperar_dados >> criar_tabela >> inserir_dados 
#  Comparar dados // outra dag