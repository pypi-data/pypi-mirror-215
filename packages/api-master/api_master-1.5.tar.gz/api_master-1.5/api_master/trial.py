from sdks.stocksera_sdk.sdk import StockeraSDK
from cfg import YOUR_STOCKSERA_KEY, today_str, thirty_days_from_now_str, five_days_ago_str
import stocksera
import pandas as pd
import disnake
from urllib.parse import urlencode
from tabulate import tabulate
sdk = StockeraSDK()
from cfg import YOUR_API_KEY
import aiohttp
import asyncio
client = stocksera.Client(YOUR_STOCKSERA_KEY)


async def get_price_data(ticker: str):
    if ticker != "SPX":
        url = f"https://api.polygon.io/v3/snapshot?ticker.any_of={ticker}&apiKey=Hu_4qFYQSp53uz4sZRX1vmiGyNvTbvxz"
        print(url)
    else:
        ticker = f"I:{ticker}"
        url = f"https://api.polygon.io/v3/snapshot?ticker.any_of={ticker}&apiKey=Hu_4qFYQSp53uz4sZRX1vmiGyNvTbvxz"
        print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return
            data = await resp.json()
            results = data['results'] if 'results' in data else None
            if results:
                if 'value' in results[0]:
                    value = results[0]['value']
                elif 'session' in results[0]:
                    value = results[0]['underlying_asset']['price']
                else:
                    value = None
                print(value)
                return value
            else:
                return None

async def get_near_the_money(ticker,lower_strike, upper_strike, today_str):

    url = f"https://api.polygon.io/v3/snapshot/options/{ticker}?strike_price.gte={lower_strike}&strike_price.lte={upper_strike}&expiration_date.gte={today_str}&expiration_date.lte=2023-08-30&limit=250&apiKey={YOUR_API_KEY}"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return
            data = await resp.json()
            results = data['results'] if data['results'] is not None else None
            details = [i['details'] if i['details'] is not None else None for i in results]
            ticker = [i['ticker'] if i['ticker'] is not None else None for i in details]


                ###code to fetch all of the results until exhausted

            all_results = ','.join(ticker)  # holds all the option symbols
            return all_results
            


async def get_near_the_money2(ticker, lower_strike, upper_strike, today_str):
    date = "2023-08-30"
    url = f"https://api.polygon.io/v3/snapshot/options/{ticker}?strike_price.gte={lower_strike}&strike_price.lte={upper_strike}&expiration_date.gte={today_str}&expiration_date.lte={date}&limit=250&apiKey={YOUR_API_KEY}"
    print(url)
    async with aiohttp.ClientSession() as session:
        all_ticker = []  # to hold all the option symbols
        
        while url:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return
                data = await resp.json()
                results = data['results'] if 'results' in data else []
                details = [i['details'] if 'details' in i else None for i in results]
                ticker = [i['ticker'] if 'ticker' in i else None for i in details]
                all_ticker.extend(ticker)
                
                url = data.get('next_url')  # get the next page URL
                if url and YOUR_API_KEY not in url:
                    url += f"&apiKey={YOUR_API_KEY}"  # append the API key to the URL
                
                if len(all_ticker) >= 250:
                    return ','.join(all_ticker[:250])  # yield the current batch of tickers
                     # keep the remaining tickers for the next batch
                
            # yield any remaining tickers that didn't make up a full batch of 250
            if all_ticker:
                return ','.join(all_ticker)

async def find_lowest_iv(output):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.polygon.io/v3/snapshot?ticker.any_of={output}&apiKey={YOUR_API_KEY}"
        async with session.get(url) as filtered_resp:
            if filtered_resp.status != 200:
                print(f"Error")
            else:
                response = await filtered_resp.json()

                if response is None:
                    print(f"Bad output: {output}")
                filtered_results = response['results'] if 'results' in response else None
                if filtered_results is not None:
                    call_data = []
                    put_data = []
                    for result in filtered_results:
                        contract_type = result.get('details').get('contract_type')
                        if contract_type == 'call':
                            call_data.append(result)
                        elif contract_type == 'put':
                            put_data.append(result)
                        else:
                            continue
                    call_changep = [i.get('session', None).get('change_percent') for i in call_data]
                    put_changep = [i.get('session', None).get('change_percent') for i in put_data]
                    
                    call_symbols = [i.get('ticker', None) for i in call_data]
                    call_ivs = [i.get('implied_volatility', None) for i in call_data]
                    call_strikes = [i.get('details').get('strike_price', None) for i in call_data]
                    call_expiry = [i.get('details').get('expiration_date', None) for i in call_data]
                    call_name = [i.get('name', None) for i in call_data]
                    put_symbols = [i.get('ticker', None) for i in put_data]
                    put_ivs = [i.get('implied_volatility', None) for i in put_data]
                    put_strikes = [i.get('details').get('strike_price', None) for i in put_data]
                    put_expiry = [i.get('details').get('expiration_date', None) for i in put_data]
                    put_name = [i.get('name', None) for i in put_data]

                    call_volume = [i.get('session', None).get('volume', None) for i in call_data]
                    put_volume = [i.get('session', None).get('volume', None) for i in call_data]

                    call_mid = [i.get('last_quote', None).get('midpoint') for i in call_data]
                    put_mid = [i.get('last_quote', None).get('midpoint') for i in put_data]

                    call_oi = [i.get('open_interest', None) for i in call_data]
                    put_oi = [i.get('open_interest', None) for i in call_data]

                    def equalize_dict_lists(input_dict):
                        max_len = max(len(lst) for lst in input_dict.values())
                        return {k: v + [None]*(max_len-len(v)) for k, v in input_dict.items()}
                    call_dict = {
                        'Symbol': call_symbols,
                        'Name': call_name,
                        'Strike': call_strikes,
                        'Expiry': call_expiry,
                        'IV': call_ivs,
                        'Change Percent': call_changep,
                        'Volume': call_volume,
                        'OI': call_oi,
                        'mid': call_mid
                        

                    }

                    put_dict = {
                        'Symbol': put_symbols,
                        'Name': put_name,
                        'Strike': put_strikes,
                        'Expiry': put_expiry,
                        'IV': put_ivs,
                        'Change Percent': put_changep,
                        'Volume': put_volume,
                        'OI': put_oi,
                        'mid': put_mid,

                    }
                    put_dict = equalize_dict_lists(put_dict)
                    call_dict = equalize_dict_lists(call_dict)

                    # Now you should be able to create your DataFrames without errors
                    put_df = pd.DataFrame(put_dict).sort_values('IV').dropna(how="any")
                    call_df = pd.DataFrame(call_dict).sort_values('IV').dropna(how="any")
                    call_df = pd.DataFrame(call_dict).sort_values('IV').dropna(how="any")
                    put_df = pd.DataFrame(put_dict).sort_values('IV').dropna(how="any")
                    call_df.to_csv('iv_monitor_calls.csv')
                    put_df.to_csv('iv_monitor_puts.csv')
                    def get_lowest_iv(group):
                        return group.sort_values('IV').iloc[0]

                    grouped_call_df = call_df.groupby('Expiry').apply(get_lowest_iv)
                    grouped_put_df = put_df.groupby('Expiry').apply(get_lowest_iv)
                    #print(grouped_call_df)
                    final_dicts_call = []
                    #print(grouped_put_df)
                    for index, row in grouped_call_df.iterrows():
                        current_dict = {
                            'symbol': row['Symbol'],
                            'name': row['Name'],
                            'strike': row['Strike'],
                            'expiry': index,  # level 0 index is 'Expiry'
                            'iv': row['IV'],
                            'percent_change': row['Change Percent'],
                            'volume': row['Volume'],
                            'oi': row['OI'],
                            'mid': row['mid']

                        }
                        final_dicts_call.append(current_dict)

                    final_dicts_put = []
                    for index, row in grouped_put_df.iterrows():
                        current_dict = {
                            'symbol': row['Symbol'],
                            'name': row['Name'],
                            'strike': row['Strike'],
                            'expiry': index,  # level 0 index is 'Expiry'
                            'iv': row['IV'],
                            'percent_change': row['Change Percent'],
                            'volume': row['Volume'],
                            'oi': row['OI'],
                            'mid': row['mid']

                        }
                        final_dicts_put.append(current_dict)
                    
    return final_dicts_call, final_dicts_put 
# async def main():
#     ticker = "SPX"
#     price = await get_price_data(ticker=ticker)

#     lower_strike = 0.99 * price
#     upper_stike = 1.01 * price

#     atm_options= await get_near_the_money2(ticker=ticker,lower_strike=lower_strike,upper_strike=upper_stike, today_str="2023-06-19")
#     print(atm_options)
#     while True:
#         low_iv_data = await find_lowest_iv(atm_options)
#         for k in low_iv_data:
#             print(f"{k[0]['expiry']} {k[0]['name']} |  | LOW STRIKE: {k[0]['strike']} vs. ${price} | IV: {k[0]['iv']}")
#             print(f"{k[1]['expiry']} {k[1]['name']} |  | LOW STRIKE: {k[1]['strike']} vs. ${price} | IV: {k[1]['iv']}")
#             print(f"{k[2]['expiry']} {k[2]['name']} |  | LOW STRIKE: {k[2]['strike']} vs. ${price} | IV: {k[2]['iv']}")
#             print(f"{k[3]['expiry']} {k[3]['name']} |  | LOW STRIKE: {k[3]['strike']} vs. ${price} | IV: {k[3]['iv']}")
#             print(f"{k[4]['expiry']} {k[4]['name']} |  | LOW STRIKE: {k[4]['strike']} vs. ${price} | IV: {k[4]['iv']}")
#             print(f"{k[5]['expiry']} {k[5]['name']} |  | LOW STRIKE: {k[5]['strike']} vs. ${price} | IV: {k[5]['iv']}")
#             print(f"{k[6]['expiry']} {k[6]['name']} |  | LOW STRIKE: {k[6]['strike']} vs. ${price} | IV: {k[6]['iv']}")


# asyncio.run(main())