from utilsF import get_site, extract_players_info, filters
from bs4 import BeautifulSoup
import re
base_url_for_search:str = "https://www.hltv.org/players"
base_url_for_player:str = "https://www.hltv.org/stats/players"

statistics = [
    'rating 2.0', 
    'DPR', 
    'KAST', 
    'Impact', 
    'ADR',
    'KPR',
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

# Criar uma classe acima que será a scraper que fará as coisas mais básicas
class PlayerScraper ():
    def __init__(self, player_nick: str, filters = None):
        self.player_nick = player_nick
        self.filters = filters


    def find_player_link (self):
        player_nick: str = self.player_nick
        filter= self.filters
        if filter is not None:
            url_filter = filters(filter)
            final_base_url = url_filter
        else:
            final_base_url = '?startDate=all&matchType=all&maps=all&rankingFilter=all'
        
        first_letter: str = player_nick[0]
        
        letter_url: str = f"{base_url_for_search}/{first_letter}"
        
        response = get_site(letter_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        players_grid = soup.find('div', class_='players-archive-grid')
        
        links = players_grid.find_all('a', class_='standard-box')
        hrefs = [link['href'] for link in links if 'href' in link.attrs]
        

        player_links, nicks = extract_players_info(hrefs)
        player_nick = re.sub(r'[^a-zA-Z0-9]+$', '', player_nick)
        for i in range(len(nicks)):
            if player_nick.lower() == nicks[i]:
                link_final = f'{base_url_for_player}/{player_links[i]}{final_base_url}'
                print(f'link_final {link_final}')
                return link_final
        
        else:
            other_page = True
            cont = 1
            other_url = "?offset="
            while other_page:
                num_url = 52*cont
                new_page_url = letter_url + other_url + str(num_url)
                print(f'new_page_url: {new_page_url}')
                response = get_site(new_page_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                players_grid = soup.find('div', class_='players-archive-grid')
                links = players_grid.find_all('a', class_='standard-box')
                hrefs = [link['href'] for link in links if 'href' in link.attrs]
                player_links, nicks = extract_players_info(hrefs)
                print(f'player_links: {nicks}')
                for i in range(len(nicks)):
                    if player_nick.lower() == nicks[i]:
                        link_final = f'{base_url_for_player}/{player_links[i]}{final_base_url}'
                        print(f'link_final {link_final}')
                        return link_final
                if len(nicks) == 0:
                    print(f'player_nick: {player_nick} not found')
                    other_page = False
                    return 5
                cont += 1

    def get_player_main_info(self):  
        #player_nick = self.player_nick
        player_link = self.find_player_link()
        if player_link == 5:
            return 5
        response = get_site(player_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        principal_stat_rows = soup.find_all('div', class_='summaryStatBreakdownRow')
        stats_principais = []
        if len(principal_stat_rows) >= 2:
            first_row = principal_stat_rows[0]
            second_row = principal_stat_rows[1]
            first_row_values = [value.get_text(strip=True) for value in first_row.find_all('div', class_='summaryStatBreakdownDataValue')]
            second_row_values = [value.get_text(strip=True) for value in second_row.find_all('div', class_='summaryStatBreakdownDataValue')]

            
            all_values = first_row_values + second_row_values

            
            dict_values = {'rating 2.0': float(all_values[0]), 'DPR': float(all_values[1]) , 'KAST': all_values[2], 'Impact': float(all_values[3]), 'ADR': float(all_values[4]) , 'KPR': float(all_values[5])}
            stats_principais.append(dict_values)
        if len(stats_principais) == 0:
            print(f'player_nick: {self.player_nick} not found')
            return 5    

        return stats_principais[0]


    def get_player_all_info(self):   #ajustar essas funções com mais parâmetros, o de tempo e tal
        all_stats = []
        player_link = self.find_player_link()
        if player_link == 5:
            return 5
        
        response = get_site(player_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        stat_rows = soup.find_all('div', class_='role-stats-top') 
        main_info = self.get_player_main_info()
        if main_info == 5:
            return 5

        all_values = []
        
        for row in stat_rows:
            inter = row.find_all('div', class_='role-stats-data')  
            values = [value.get_text(strip=True) for value in inter] 
            all_values.append(values[0]) 
            
        statistics_dict = {}
        index = 0
        cont = 0
        for stat in statistics:
            if cont <= 5:
                statistics_dict[stat] = main_info[stat]
                cont += 1
                continue
            if index > len(all_values):
                print(f'Warning: index {index} out of range for all_values')
                statistics_dict[stat] = None
            else:
                statistics_dict[stat] = all_values[index]
                statistics_dict[f"{stat}_ct"] = all_values[index + 1]
                statistics_dict[f"{stat}_tr"] = all_values[index + 2]
                index += 3

        
        print(f'statistics_dict final: {statistics_dict}')
        all_stats.append(statistics_dict)
        
        return all_stats
    












