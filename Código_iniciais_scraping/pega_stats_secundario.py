import cloudscraper
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

statistics = [
    "Kills per round",
    "Rounds with a kill",
    "Kills per round win",
    "Rating 2.0",
    "Damage per round",
    "Rounds with a multi-kill",
    "Damage per round win",
    "Pistol round rating",
    "Saved by teammate per round",
    "Traded deaths per round",
    "Traded deaths percentage",
    "Opening deaths traded percentage",
    "Assists per round",
    "Support rounds",
    "Saved teammate per round",
    "Trade kills per round",
    "Trade kills percentage",
    "Assisted kills percentage",
    "Damage per kill",
    "Opening kills per round",
    "Opening deaths per round",
    "Opening attempts",
    "Opening success",
    "Win% after opening kill",
    "Attacks per round",
    "Clutch points per round",
    "Last alive percentage",
    "1on1 win percentage",
    "Time alive per round",
    "Saves per round loss",
    "Sniper kills per round",
    "Sniper kills percentage",
    "Rounds with sniper kills percentage",
    "Sniper multi-kill rounds",
    "Sniper opening kills per round",
    "Utility damage per round",
    "Utility kills per 100 rounds",
    "Flashes thrown per round",
    "Flash assists per round",
    "Time opponent flashed per round",
]

scraper = cloudscraper.create_scraper()
df = pd.read_csv('jogadores_cs.csv')

todos_stats = []

for url in df['Link']:
    time.sleep(2)
    print(url)
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    stat_rows = soup.find_all('div', class_='role-stats-top') 
    all_values = []
    
    for row in stat_rows:
        inter = row.find_all('div', class_='role-stats-data')  
        values = [value.get_text(strip=True) for value in inter] 
        all_values.append(values[0]) 
        
    statistics_dict = {}
    index = 0

    for stat in statistics:
        statistics_dict[stat] = all_values[index]
        statistics_dict[f"{stat}_ct"] = all_values[index + 1]
        statistics_dict[f"{stat}_tr"] = all_values[index + 2]
        index += 3

    print(statistics_dict)
    todos_stats.append(statistics_dict)

    
df_stats = pd.read_csv('jogadores_stats.csv')
df_stats_sec = pd.DataFrame(todos_stats)
#unir os dataframes
df_final = pd.concat([df, df_stats, df_stats_sec], axis=1)
#salvar o dataframe
df_final.to_csv('jogadores_stats_totais.csv', index=False)
print(df_final)

        
  