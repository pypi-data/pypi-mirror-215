from api_master.sdks.webull_sdk.webull_sdk import AsyncWebullSDK

webull = AsyncWebullSDK()
import pandas as pd
import asyncio
import requests
rank_type = "volume"
# r = requests.get(f"https://quotes-gw.webullfintech.com/api/wlas/ranking/topActive?regionId=6&rankType={rank_type}&pageIndex=1&pageSize=350").json()
# data  = r['data']
# tickers = [i['tickers'] if 'tickers' in i else None for i in data]

# values = [i['values'] if 'values' in i else None for i in data]
# for i in values:
#     print(i)




async def main():

    ticker= await webull.fifty_two_high_and_lows()


    df = pd.DataFrame(vars(ticker))
    print(df)
asyncio.run(main())