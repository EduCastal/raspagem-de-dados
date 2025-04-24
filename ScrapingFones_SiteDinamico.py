# Módulo para controlar o navegador web - "simular o navegador"
from selenium import webdriver

# Localizador de elementos - Encontra o "CLASSNAME"
from selenium.webdriver.common.by import By

# Serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# Classe que permite executar ações avançadas. Ex. Mover o mouse, o click e arrasta e etc.
from selenium.webdriver.common.action_chains import ActionChains

# Classe que espera de forma explicita até que uma condição seja satisfeita
# Ex.: "Esperar" que um elemento apareça/carregue, não deixa 'encavalar'
from selenium.webdriver.support.ui import WebDriverWait

# Condições esperadas usadas com WebDriverWait - anterior
from selenium.webdriver.support import expected_conditions as ec

# Trabalhar com dataframe
import pandas as pd

# Uso de funções relacionados à tempo
import time

# Uso do tratamento de excessão
from selenium.common.exceptions import TimeoutException

# Definir o caminho do ChromeDriver
# Averiguar a versão do novegador
caminho_driver = 'C:\Program Files\chromedriver-win64\chromedriver.exe'

# Configuração do WebDriver
servico = Service(caminho_driver) #Inicializa o navegador
controle = webdriver.ChromeOptions() #Configurar as opções do navegador
controle.add_argument('--disable-gpu') #Evita possíveis erros gráficos
controle.add_argument('--windowsize=1920,1080') #Define a resolução de tela como fixa

# Inicialização do WebDriver
driver = webdriver.Chrome(service=servico, options=controle)

# URL inicial
url_base = 'https://www.kabum.com.br/perifericos/fone-de-ouvido-gamer'
driver.get(url_base)
time.sleep(5) #Aguarda 5 segundos para que a página carregue

# Criar um dicionário vazio para armazenar a descrição do produto e os preços
dic_produtos = {'desc_produto': [], 'valor': []}

# Inicia na página 1 e incrementa a cada troca de página
pagina = 1

while True:
    print(f'\n COLETANDO DADOS DA PÁGINA {pagina}...')

    try:
        #WebDriverWait(driver, 10): Cria uma espera explicita de até 10 segundos
        #Until: Faça com que a condição espere até ser verdadeira, encontra o "productCard"
        #ec.presence_of_all_elements_located(...): Verifica se todos os elementos "productCard" estão acessíveis
        #By.CLASS_NAME,'productCard': Indica que a busca será feita através 
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME,'productCard'))
    ) 
        print('Elementos encontrados com sucesso!')
    except TimeoutException:
        print('Tempo de espera excedido!')
    
    produtos = driver.find_elements(By.CLASS_NAME, 'productCard')

    for produto in produtos:
        try:
            desc_produto = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            valor = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()
            
            print(f'{desc_produto} - {valor}')

            dic_produtos['desc_produto'].append(desc_produto)
            dic_produtos['valor'].append(valor)

        except Exception:
            print('Erro ao coletar dados:', Exception)

    # Encontrar o botão para a próxima página
    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            driver.execute_script('arguments[0].scrollIntoView()', botao_proximo)
            time.sleep(1)

            driver.execute_script('arguments[0].click();', botao_proximo)
            print(f'Indo para a página {pagina}')
            pagina += 1
            time.sleep(5)
        else:
            print('Chegou na última página!')
            break
    
    except Exception as e:
        print('Erro ao tentar avançar para a próxima página', e)
        break

# Fechar o navegador
driver.quit()

# Cria a base de dados e gera o arquivo (excell)
df = pd.DataFrame(dic_produtos)
df.to_excel('fones.xlsx', index=False)

print(f'Arquivo fones salvo com sucesso! {len(df)} produtos capturados')
