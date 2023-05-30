from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Pessoa:
    def __init__(self, f_name, f_id):
        self.folower_name = f_name
        self.follower_id = f_id
        
class Principal(webdriver.Chrome):
    def __init__(self):
        # Para teste, remove caracteres não reconhecidos das variaveis
        import sys
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
        #
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        super(Principal, self).__init__(service=service,options=options)
        self.maximize_window()

    def login(self):
        email = ""
        password = ""
        twitter = ""
        self.get("https://twitter.com/i/flow/login")
        email_box = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label')))
        submit = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')))
        
        email_box.send_keys(email)
        time.sleep(2)
        submit.click()
        try:
            security = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label')))
            security.send_keys(twitter)
            submit = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')))
            time.sleep(3)
            submit.click()
        except:
          print('Não pediu ID')
        password_box = WebDriverWait(self, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label')))
        password_box.send_keys(password)
        time.sleep(3)
    
        submit = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')))
        submit.click()
        time.sleep(3)
    
    def pegar_dados(self):
        twitter = ""
        self.get("https://twitter.com/"+twitter+"/followers")
        
        list_followers = []
        for i in range(1, 100):
            try:
                follower_name = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div['+str(i)+']/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]'))).text
                follower_id = WebDriverWait(self, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div['+str(i)+']/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/a/div/div/span'))).text
                user = Pessoa(follower_name, follower_id)
                list_followers.append(user)
                # rolar pagina para carregar mais
            except:
                break
        print(list_followers)
        
if __name__ == "__main__":
    bot = Principal()
    bot.login()
    bot.pegar_dados()
    
    
# Salvar uam tabela com o nome dia/mes e quando comparar, comparar com a tabela do dia anterior, sempre salvar os dados em uma nova tabela