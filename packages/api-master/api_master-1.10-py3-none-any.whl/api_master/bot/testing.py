import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



import pdb
import asyncio
import aiohttp
from cfg import YOUR_API_KEY, two_years_from_now_str, today_str
import requests
from urllib.parse import urlencode

import pandas as pd
async def get_price_data(ticker: str):
    if ticker.startswith('SPX'):
        ticker = ticker.replace(f"{ticker}", f"I:{ticker}")
    else:
        ticker = ticker
    url = f"https://api.polygon.io/v3/snapshot?ticker.any_of={ticker}&apiKey={YOUR_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return
            data = await resp.json()
            results = data['results'] if 'results' in data else None
            value = results[0]['value']
            return value


async def get_near_the_money_options(ticker: str, lower_strike, upper_strike, date: str = "2027-12-30"):
    if ticker.startswith('SPX'):
        ticker = ticker.replace(f"{ticker}", f"I:{ticker}")
        initial_url = f"https://api.polygon.io/v3/snapshot/options/{ticker}?strike_price.gte={lower_strike}&strike_price.lte={upper_strike}&expiration_date.gte={today_str}&expiration_date.lte=2023-09-30&limit=250&apiKey={YOUR_API_KEY}"

        async with aiohttp.ClientSession() as session:
            async with session.get(initial_url) as resp:
                atm_options = await resp.json()
                results = atm_options['results'] if atm_options['results'] is not None else None
                ticker = [i.get('details').get('ticker') for i in results]

                while 'next_url' in atm_options:
                    next_url = atm_options['next_url']
                    async with aiohttp.ClientSession() as session:
                        async with session.get(next_url + f"&apiKey={YOUR_API_KEY}") as response:
                            atm_options = await response.json()
                            results.extend(atm_options['results'])

                    # Now you have all the results in the `results` list
                    # You can process them in chunks of 250 if needed
                    chunk_size = 250
                    chunks = []
                    for i in range(0, len(results), chunk_size):
                        chunk = results[i:i+chunk_size]
                        symbol = [i.get('details').get('ticker') for i in chunk]
                        chunks.append(symbol)

                    # Construct URLs for each chunk
                    base_url = "https://api.polygon.io/v3/snapshot?ticker.any_of={}&apiKey={}"
                    urls = []
                    for chunk in chunks:
                        # Flatten the chunk list
                        
                        # Join the tickers into a comma-separated string
                        ticker_string = ",".join(chunk)
                        
                        # Construct the URL
                        url = base_url.format(ticker_string, YOUR_API_KEY)
                        
                        urls.append(url)
                    print(urls)
                    return urls

                else:
                    initial_url = f"https://api.polygon.io/v3/snapshot/options/{ticker}?strike_price.gte={lower_strike}&strike_price.lte={upper_strike}&expiration_date.gte={today_str}&expiration_date.lte={date}&limit=250&apiKey={YOUR_API_KEY}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(initial_url) as resp:
                            atm_options = await resp.json()
                            results = atm_options['results']

                            while 'next_url' in atm_options:
                                next_url = atm_options['next_url']
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(next_url + f"&apiKey={YOUR_API_KEY}") as response:
                                        atm_options = await response.json()
                                        results.extend(atm_options['results'])

                        # Now you have all the results in the `results` list
                        # You can process them in chunks of 250 if needed
                        chunk_size = 250
                        chunks = []
                        for i in range(0, len(results), chunk_size):
                            chunk = results[i:i+chunk_size]
                            # Do something with the chunk of results
                            chunks.append(chunk)
                        api_key = YOUR_API_KEY
                        base_url = "https://api.polygon.io/v3/snapshot?ticker.any_of={}&apiKey={}"
                        urls = []
                for chunk in chunks:
                    # Flatten the chunk list
                    flattened_chunk = [ticker for sublist in chunk for ticker in sublist]
                    
                    # Join the tickers into a comma-separated string
                    ticker_string = ",".join(flattened_chunk)
                    
                    # Construct the URL
                    url = base_url.format(ticker_string, api_key)
                    urls.append(url)
                    # Use the URL for further processing (e.g., send requests, etc.)
                print(urls)
                return urls





async def find_lowest_iv(output):
    final_dicts_call = []
    final_dicts_put = []

    async with aiohttp.ClientSession() as session:
        for url in output:
            async with session.get(url) as filtered_resp:
                if filtered_resp.status != 200:
                    print(f"Error")
                    continue
                else:
                    response = await filtered_resp.json()

                    if response is None:
                        print(f"Bad output: {output}")
                        continue

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


                        call_volume = [i.get('session').get('volume') for i in call_data]
                        put_volume = [i.get('session').get('volume') for i in put_data]

                        call_dict = {
                            'Symbol': call_symbols,
                            'Name': call_name,
                            'Strike': call_strikes,
                            'Expiry': call_expiry,
                            'IV': call_ivs,
                            'Volume': call_volume,
                        }

                        put_dict = {
                            'Symbol': put_symbols,
                            'Name': put_name,
                            'Strike': put_strikes,
                            'Expiry': put_expiry,
                            'IV': put_ivs,
                            'Volume': put_volume
                        }

                        call_df = pd.DataFrame(call_dict).sort_values('IV').dropna(how="any")
                        put_df = pd.DataFrame(put_dict).sort_values('IV').dropna(how="any")
                        call_df.to_csv('iv_monitor_calls.csv', index=False)
                        put_df.to_csv('iv_monitor_puts.csv', index=False)

                        def get_lowest_iv(group):
                            return group.sort_values('IV').iloc[0]

                        grouped_call_df = call_df.groupby('Expiry').apply(get_lowest_iv)
                        grouped_put_df = put_df.groupby('Expiry').apply(get_lowest_iv)

                        for index, row in grouped_call_df.iterrows():
                            current_dict = {
                                'symbol': row['Symbol'],
                                'name': row['Name'],
                                'strike': row['Strike'],
                                'expiry': index,  # level 0 index is 'Expiry'
                                'iv': row['IV'],
                                'volume': row['Volume']
                            }
                            final_dicts_call.append(current_dict)

                        for index, row in grouped_put_df.iterrows():
                            current_dict = {
                                'symbol': row['Symbol'],
                                'name': row['Name'],
                                'strike': row['Strike'],
                                'expiry': index,  # level 0 index is 'Expiry'
                                'iv': row['IV'],
                                'volume': row['Volume']
                            }
                            final_dicts_put.append(current_dict)

    return final_dicts_call, final_dicts_put


# async def main():
#     ticker = "SPX"
#     price = await get_price_data(ticker)
#     print(price)
#     lower_strike = 0.99 * price
#     upper_strike = 1.01 * price
#     symbols = await get_near_the_money_options(ticker="SPX", lower_strike=lower_strike, upper_strike=upper_strike)

#     low_iv_data = await find_lowest_iv(symbols)

#     low_iv_expiry = [k['expiry'] if 'expiry' in k else None for k in low_iv_data]


#     for k in low_iv_data[0]:
#         print(f"{k['expiry']} | STRIKE: ${k['strike']} v. PRICE: ${price} | IV: {k['iv']} | ")
#     else:
#         print("No lowest IV data found.")


# asyncio.run(main())