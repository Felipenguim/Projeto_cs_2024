import cloudscraper 
import re
from typing import List, Tuple, Dict, Optional
from datetime import datetime
import pytz
import pandas as pd
from bs4 import BeautifulSoup
import time
import csv
import json

def extract_players_info(links: List[str]):  #de uma lista com todos os players pega os nicks e links
    player_links = []
    player_nicks = []
    for link in links:
        match = re.search(r'/player/(\d+)/(\w+)', link)
        if match:
            player_id = match.group(1)
            player_nick = match.group(2)
            player_link = f'/{player_id}/{player_nick}'
            player_links.append(player_link)
            player_nicks.append(player_nick)
    return player_links, player_nicks


def scraper():
    return cloudscraper.create_scraper()

def get_site(url:str):
    scr = scraper()
    return scr.get(url)

# links = [
#     "https://www.hltv.org/player/23750/gothchild",
#     "https://www.hltv.org/player/22884/gr1ks"
# ]

def all_list() -> List[str]:  #preciso passar uma lista dos nicks e não dos links
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

        div_geral_players = soup.find('div', class_='players-archive-grid')
        if div_geral_players is None:
                print(f"Div 'players-archive-grid' não encontrada na página: {url}")
                continue 
        links = div_geral_players.find_all('a', class_='standard-box')

        # Iterar pelos links dos jogadores
        for link in links:
            pais_element = link.find_all('div', class_='players-archive-country')  
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
    return nicks

def top_50_list():   #Posso tornar uma função que pega o top x
    scraper = cloudscraper.create_scraper()
    url = 'https://www.hltv.org/ranking/teams'
    response = scraper.get(url)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    teams = site.findAll('div', attrs={'class': 'ranked-team standard-box'})
    top_50 = []
    for i, team in enumerate(teams):
        if i >= 50:
            break
        players_team = team.findAll('div', attrs={'class': 'rankingNicknames'})
        players_name = [player.text.strip() for player_team in players_team for player in player_team.find_all('span')]
        for player in players_name:
            top_50.append(player)
    return top_50

#Fazer funções de exportação para vários formatos
def do_dataframe():
    pass

def export_to_excel(data, filename="output.xlsx"):
    """Exporta os dados para um arquivo Excel."""
    if data and isinstance(data, list):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Dados exportados para {filename} com sucesso.")
    else:
        print("Dados inválidos para exportação.")

def export_to_json(data, filename="output.json"):
    """Exporta os dados para um arquivo JSON."""
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Dados exportados para {filename} com sucesso.")


# def export_to_csv(data, filename="output.csv"):
#     """Exporta os dados para um arquivo CSV."""
#     if data and isinstance(data, list):
#         with open(filename, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=data[0].keys())
#             writer.writeheader()
#             writer.writerows(data)
#         print(f"Dados exportados para {filename} com sucesso.")
#     else:
#         print("Dados inválidos para exportação.")
#Tenho que adaptar os csvs e nomes das features para os filtros que tenho 
def export_csv(data, filename="output.csv"):
    # Verifica se o dict_players está no formato correto
    df = pd.DataFrame.from_dict({k: v[0] for k, v in data.items()}, orient='index')

    df.index.name = 'Player'
    df.reset_index(inplace=True)
    df.to_csv(filename, index=False)
    return df




def date_filter(filter: str):
    if filter == "":
        return "all"
    filters_list =["choosen_date", "last month", "last 3 months", "last 6 months", "last 12 months", "last 2 years", "last 3 years", "last 5 years", "last 10 years", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012"]
    cet_tz = pytz.timezone('Europe/Paris')

    today_cet = datetime.now(cet_tz)
    
    if filter not in filters_list:
        raise ValueError("Data inválida")
    if filter == "choosen_date":
        print("Digite a data no formato dd/mm/yyyy")
        start_date = input(str("Digite a data no de início dd/mm/yyyy"))
        end_date = input(str("Digite a data no de fim dd/mm/yyyy"))
    elif filter == "2024":
        start_date = "2024-01-01"
        end_date = "2024-12-31"
    elif filter == "2023":
        start_date = "2023-01-01"
        end_date = "2023-12-31"
    elif filter == "2022":
        start_date = "2022-01-01"
        end_date = "2022-12-31"
    elif filter == "2021":
        start_date = "2021-01-01"
        end_date = "2021-12-31"
    elif filter == "2020":
        start_date = "2020-01-01"
        end_date = "2020-12-31"
    elif filter == "2019":
        start_date = "2019-01-01"
        end_date = "2019-12-31"
    elif filter == "2018":
        start_date = "2018-01-01"
        end_date = "2018-12-31"
    elif filter == "2017":
        start_date = "2017-01-01"
        end_date = "2017-12-31"
    elif filter == "2016":
        start_date = "2016-01-01"
        end_date = "2016-12-31"
    elif filter == "2015":
        start_date = "2015-01-01"
        end_date = "2015-12-31"
    elif filter == "2014":
        start_date = "2014-01-01"
        end_date = "2014-12-31"
    elif filter == "2013":
        start_date = "2013-01-01"
        end_date = "2013-12-31"
    elif filter == "2012":
        start_date = "2012-01-01"
        end_date = "2012-12-31"
    elif filter == "last month":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
    elif filter == "last 3 months":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(months=3)).strftime('%Y-%m-%d')
    elif filter == "last 6 months":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(months=6)).strftime('%Y-%m-%d')
    elif filter == "last 12 months":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
    elif filter == "last 2 years":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(years=2)).strftime('%Y-%m-%d')
    elif filter == "last 3 years":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(years=3)).strftime('%Y-%m-%d')
    elif filter == "last 5 years":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(years=5)).strftime('%Y-%m-%d')
    elif filter == "last 10 years":
        end_date = today_cet.strftime('%Y-%m-%d')
        start_date = (today_cet - pd.DateOffset(years=10)).strftime('%Y-%m-%d')
    
    return start_date, end_date

def match_type_filter(filter: str = ""):
    if filter == "":
        return "all"
    filters_list =["Majors", "BigEvents", "Lan", "Online"]
    if filter not in filters_list:
        raise ValueError("Tipo de partida inválido")
    else:
        return filter

def maps_filter(filter: List[str]):
    maps = ["ancient", "cache", "dust2", "inferno", "mirage", "nuke", "overpass", "train", "vertigo", "anubis", "cobblestone"]
    if len(filter) == 0:
        return "all"
    else:
        for i in range(len(filter)):
            if filter[i] in maps:
                filter[i] = f"de_{filter[i]}"
            if filter[i] not in maps:
                print(f"Mapa '{filter[i]}' não existe")
                filter.pop(i)
        if len(filter) == 0:
            raise ValueError("Nenhum mapa válido")
        return filter

def ranking_filter(filter: str):
    if filter == "":
        return "all"
    filters_list =["Top5", "Top10", "Top20", "Top30", "Top50"]
    if filter not in filters_list:
        raise ValueError("Tipo de ranking inválido")
    else:
        return filter


def filters(filters = None) -> str: # Recebe um dicionário de filtros
    no_filter_string = '?startDate=all&matchType=all&maps=all&rankingFilter=all'
    if filters == None:
        return no_filter_string
    if len(filters) == 0:
        return no_filter_string
    
    default_filters = {
        "Date": "",
        "matchType": "",
        "maps": [],
        "rankingFilter": ""
    }
    for key in filters:
        if key in default_filters:
            default_filters[key] = filters[key]
        else:
            raise ValueError(f"Filtro inválido: {key}")
    if default_filters["Date"] == "":
        start_date, end_date = "all"
    else:
        start_date, end_date = date_filter(default_filters["Date"])

    maps = maps_filter(default_filters["maps"])
    ranking = ranking_filter(default_filters["rankingFilter"])
    match_type = match_type_filter(default_filters["matchType"])
    
    filter_url = f'?startDate={start_date}&endDate={end_date}&matchType={match_type}&maps={maps}&rankingFilter={ranking}'
    return filter_url
    #Ta muito mal feito essa passagem de filtros
    
    



    
    

    #Depois posso fazer um "filtro" de país de palyers
def player_country_list(): #Vai pegar os principais players de x país a partir da função que pega em all
    pass