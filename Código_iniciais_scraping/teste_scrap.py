from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Escolha o navegador: "chrome" ou "firefox"
#browser_choice = input("Digite o navegador ('chrome' ou 'firefox'): ").strip().lower()
browser_choice = "firefox"

if browser_choice == "chrome":
    # Configuração para Chrome
    service = ChromeService(executable_path=r"C:\Users\felip\Desktop\chromedriver-win64\chromedriver.exe")  # Insira o caminho do chromedriver
    driver = webdriver.Chrome(service=service)

elif browser_choice == "firefox":
    # Configuração para Firefox
    service = FirefoxService(executable_path=r"C:\Users\felip\Desktop\geckodriver.exe")  # Insira o caminho do geckodriver
    driver = webdriver.Firefox(service=service)

else:
    print("Navegador inválido. Escolha 'chrome' ou 'firefox'.")
    exit()

try:
    # Acesse o site da HLTV
    driver.get("https://www.hltv.org/")

    # Aguarde 5 segundos para a página carregar completamente
    time.sleep(5)

    # Capture o título da página como um teste básico
    title = driver.title
    print(f"Título da página: {title}")
    print("-------------------")

    page_content = driver.page_source
    refs = driver.find_elements(By.CSS_SELECTOR, 'a.nav-link')
    #print(refs)
    for ref in refs:

        if ref.text == "Players":
            
            ref.click()
            time.sleep(2)
            
            break
    print(driver.current_url)
    print("-------------------")
    print(driver.title)
    #fazer um loop que na lista encontra todos os jogadores brasileiros, daí vai extrair o nome de cada um deles, e o link deles
    # Os players ficam na div de <div class="players-archive-grid">
    div_geral_players = driver.find_element(By.CSS_SELECTOR, 'div.players-archive-grid')
    #print(f'div_playes:{div_geral_players}')
    links = div_geral_players.find_elements(By.CSS_SELECTOR, 'a.standard-box')
    #print(links)
    jogadores_br = []
    link_br = []
    for link in links:
        pais_element = link.find_elements(By.CSS_SELECTOR, 'div.players-archive-country')
        
        # Verificar se o país é o Brasil
        if pais_element:
            pais_text = pais_element[0].text  # Pega o texto do primeiro elemento encontrado
            if pais_text == "Brazil":
                jogadores_br.append(link.text)  # Adiciona o nome do jogador à lista
                time.sleep(0.2)
                link_player = link.get_attribute('href')
                link_br.append(link_player)

    nomes = []
    nicks = []
    for jogador in jogadores_br:
    # Separar a string por '\n'
        partes = jogador.split('\n')
        nick = partes[0]
        nome = partes[1]
        nicks.append(nick)
        nomes.append(nome)


    print(nomes)
    print(nicks)
    print(link_br)

    #clicar em next e fazer um loop até o fim das páginas

    next = driver.find_elements(By.CSS_SELECTOR, 'div.players-pagination')
    buttons = next[0].find_elements(By.CSS_SELECTOR, 'a')
    print(buttons)
    buttons[-1].click()
    #link_next = buttons[-1].get_attribute('href')
    #link_next.click()
    time.sleep(15)

    print("-------------------")
    print(driver.current_url)
    print(driver.title)
    

    site = BeautifulSoup(page_content, 'html.parser')

    #print(site.prettify())


finally:
    # Encerra o navegador
    driver.quit()