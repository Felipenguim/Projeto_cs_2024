import cloudscraper
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests



scraper = cloudscraper.create_scraper()
df = pd.read_csv('jogadores_cs.csv')


stats_principais = []
for url in df['Link']:
    print(url)
    time.sleep(3)
    response = scraper.get(url)
    #print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    principal_stat_rows = soup.find_all('div', class_='summaryStatBreakdownRow')
    print(principal_stat_rows)
    if len(principal_stat_rows) >= 2:
        first_row = principal_stat_rows[0]
        second_row = principal_stat_rows[1]
        first_row_values = [value.get_text(strip=True) for value in first_row.find_all('div', class_='summaryStatBreakdownDataValue')]
        second_row_values = [value.get_text(strip=True) for value in second_row.find_all('div', class_='summaryStatBreakdownDataValue')]

        
        all_values = first_row_values + second_row_values

        
        dict_values = {'rating 2.0': float(all_values[0]), 'DPR': float(all_values[1]) , 'KAST': all_values[2], 'Impact': float(all_values[3]), 'ADR': float(all_values[4]) , 'KPR': float(all_values[5])}
        stats_principais.append(dict_values)
        print(dict_values)
    

df_stats = pd.DataFrame(stats_principais)
#unir os dataframes
df_final = pd.concat([df, df_stats], axis=1)
#salvar o dataframe
df_final.to_csv('jogadores_stats.csv', index=False)
print(df_final)

