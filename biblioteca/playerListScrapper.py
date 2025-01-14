from playerScrapper import PlayerScraper
from utilsF import get_site, extract_players_info, all_list, top_50_list, export_csv, export_to_json, export_to_excel
from bs4 import BeautifulSoup
from typing import List
import time 
import pandas as pd


class PlayerListScraper ():
    def __init__(self, player_nicks, filters = None, csv_path = None):
        
        self.csv_path = csv_path
        self.filters = filters
        if player_nicks == "all":
            self.player_nicks = all_list()
        elif player_nicks == "top50" or player_nicks == "top 50":
            self.player_nicks = top_50_list()
        else:
            self.player_nicks = player_nicks
        if not self.player_nicks:
            raise ValueError('No players to scrape')  
    
    def get_players_main_info(self):
        dict_players = {}
        players = self.player_nicks
        print(players)
        for player in players:
            time.sleep(2)
            player_scrapper = PlayerScraper(player, self.filters)
            dict_players[player] = player_scrapper.get_player_main_info()
        return dict_players


    def get_players_all_info(self):
        if self.csv_path:
            df = pd.read_csv(self.csv_path)
            dict_players = {}
            players = self.player_nicks
            print(players)
            for player in players:
                player = player.lower()
                df = pd.read_csv(self.csv_path)
                if player in df['Player'].values:
                    print(f'{player} already in csv')
                    continue
                time.sleep(2.5)
                player_scrapper = PlayerScraper(player, self.filters)
                dict_players[player] = player_scrapper.get_player_all_info()
                if dict_players[player] == 5:
                    del dict_players[player]
                    continue
                print(f' aaaaa: {dict_players[player]}')
                dict_players[player][0]['Player'] = player
                print(f' aaaaa222: {dict_players[player][0]}')
                df_player = pd.DataFrame.from_dict(dict_players[player][0], orient='index').T
                df_player.index.name = 'Player'
                

                df = pd.concat([df, df_player], ignore_index=True)
                df.to_csv(self.csv_path, index=False)
        else:
            dict_players = {}
            players = self.player_nicks
            print(players)
            for player in players:
                time.sleep(2.5)
                player_scrapper = PlayerScraper(player, self.filters)
                dict_players[player] = player_scrapper.get_player_all_info()
                if dict_players[player] == 5:
                    del dict_players[player]
                    continue
            
        
        return dict_players
        
   
    def export_data(self, data, format, filename = None):
        if format == 'csv':
            export_csv(data, filename)
        elif format == 'json':
            export_to_json(data, filename)
        elif format == 'excel':
            export_to_excel(data, filename)
        else:
            raise ValueError('Format not supported')
        



        #Fazer um paremtro que recebe um csv para ser complementado, se ele for true vai, ou seja um csv for passado,
        #O nick vai ser checado para ver se ele já está no csv, se estiver, ele não vai ser adicionado, se não estiver,
        #ele vai ser adicionado, ajuda com bugs e tal e não ter que ficar rodando o código inteiro
        #Além de poder fazer essa adição a dados já existentes e complementar a tabela com players faltantes






        #Se der c