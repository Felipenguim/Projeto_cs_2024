import cloudscraper
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

scraper = cloudscraper.create_scraper()  
jogadores_br = []
link_br = []
nomes = []
nicks = []
links_paginas = ['https://www.hltv.org/players', 'https://www.hltv.org/players?offset=52', 'https://www.hltv.org/players?offset=104', 'https://www.hltv.org/players?offset=156', 'https://www.hltv.org/players?offset=208', 'https://www.hltv.org/players?offset=260', 'https://www.hltv.org/players?offset=312']
for i in range(len(links_paginas)):
    time.sleep(1)
    url = links_paginas[i]
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar o div com a classe 'players-archive-grid'
    div_geral_players = soup.find('div', class_='players-archive-grid')
    if div_geral_players is None:
            print(f"Div 'players-archive-grid' não encontrada na página: {url}")
            continue 

    # Encontrar todos os links dos jogadores
    links = div_geral_players.find_all('a', class_='standard-box')

    # Iterar pelos links dos jogadores
    for link in links:
        pais_element = link.find_all('div', class_='players-archive-country')
        
        # Verificar se o país é o Brasil
        if pais_element:
            pais_text = pais_element[0].text.strip()  # Pega o texto do primeiro elemento encontrado
            
            jogadores_br.append(link.text.strip())  # Adiciona o nome do jogador à lista
            time.sleep(0.2)  # Simula o delay entre requisições
            link_player = link.get('href')  # Pega o link do jogador
            link_br.append(link_player)

    # Separar os nomes e nicks dos jogadores
for jogador in jogadores_br:
    partes = jogador.split('\n')
    if len(partes) > 1:  # Garantir que existem partes separadas por '\n'
        nick = partes[0]
        nome = partes[1]
        nicks.append(nick)
        nomes.append(nome)

completo = "https://www.hltv.org/stats"
for i in range(len(link_br)):
    link_br[i] = completo + link_br[i].replace('/player/', '/players/')
    


df = pd.DataFrame({'Nome': nomes, 'Nick': nicks, 'Link': link_br})

print(df)
df.to_csv('jogadores_cs.csv', index=False)
