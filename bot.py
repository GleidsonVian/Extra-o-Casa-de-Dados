# Importação das bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tkinter import *
from tkinter import ttk
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Função para separar os dados extraídos por caractere específico
def separar_por_caractere(listaDeLeadsNaoTratados):
    nova_lista = []
    # Para cada item na lista
    for item in listaDeLeadsNaoTratados:
        # Divida o item pelo caractere ' - ' e adicione à nova lista
        separado = item.split(' - ')
        nova_lista.append(separado)
    return nova_lista

# Inicialização do navegador Chrome
driver = webdriver.Chrome()
driver.maximize_window()

# Acesso ao site desejado
driver.get("https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada")

# Encontrar o campo de entrada para a atividade principal e preenchê-lo com "atividades de contabilidade"
atividadePrincipal = driver.find_element(By.XPATH, '//input[@placeholder="Código ou nome da atividade"]')
atividadePrincipal.send_keys('atividades de contabilidade')
time.sleep(3)

driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

def botaoPesquisar():
   # Clicar no botão de pesquisa
  botaoPesquisar = driver.find_element(By.XPATH, "//a[@class='button is-success is-medium']")
  botaoPesquisar.click()
  time.sleep(3)
   
try:
  botaoPesquisar()
except Exception :
  print('Ocorreu um erro no botão pesquisar')
        
finally:
  botaoPesquisar()



# Lista para armazenar os CNPJs extraídos
listaDeCNPJs = []


# Loop para percorrer as páginas de resultados (neste caso, apenas 4 páginas)
for i in range(4):
    # Encontrar todos os elementos de div com a classe 'box' que contêm os dados da empresa
    dadosParaPesquisarAEmpresa = driver.find_elements(By.XPATH, "//div[@class='box']")
    # Encontrar o botão para ir para a próxima página de resultados
    proximaGuia = driver.find_element(By.XPATH, "//a[@class='pagination-link pagination-next pagination-next']")

    # Adicionar os textos das empresas à lista de CNPJs
    listaDeCNPJs.extend([empresa.text for empresa in dadosParaPesquisarAEmpresa])
    # Clicar no botão para ir para a próxima página
    proximaGuia.click()
    time.sleep(3)

# Imprimir os CNPJs
# for item in listaDeCNPJs:
#     print(item)

# Tempo de espera antes de fechar o navegador
time.sleep(3)
# Fechar o navegador
driver.quit()

# Chamar a função para separar os CNPJs por caractere específico (' - ')
itens_separados = separar_por_caractere(listaDeCNPJs)
# Imprimir os CNPJs separados

dataFrameItensSeparados = pd.DataFrame(itens_separados)

dataFrameItensSeparados.to_excel(r'C:\pasta4\Python\Casa dos Dados\leadsNaoTratadas.xlsx', index=False)

for item in itens_separados:
    print(item)
