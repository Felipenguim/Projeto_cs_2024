import playerScrapper
import utilsF
import time
import playerListScrapper
import pandas as pd


# test1 = playerListScrapper.PlayerListScraper(["fallen", "s1mple"])
# #print(test1.get_players_main_info())
# b = test1.get_players_all_info()
# #print(b)
# test1.export_data(b,"csv")

df = pd.read_csv(r"C:\Users\felip\Programação\projeto_raf\biblioteca\teste.csv")
filters = {
        "Date": "2024",
        "matchType": "",
        "maps": [],
        "rankingFilter": ""
    }
while len(df) < 245:
    print(f'============================================= \n {len(df)} \n ======================================')
    try:
        test2 = playerListScrapper.PlayerListScraper('top50', filters, r"C:\Users\felip\Programação\projeto_raf\biblioteca\teste.csv")
        a = test2.get_players_all_info()

    except Exception as e:
        print(f"An error occurred: {e}")
        continue
    df = pd.read_csv(r"C:\Users\felip\Programação\projeto_raf\biblioteca\teste.csv")
#teste filtro


test2 = playerListScrapper.PlayerListScraper('top50', filters, r"C:\Users\felip\Programação\projeto_raf\biblioteca\teste.csv")
a = test2.get_players_all_info()
test2.export_data(a,"csv", "2024_players_stats.csv")


#testfinal = playerListScrapper.PlayerListScraper("top 50", filters)