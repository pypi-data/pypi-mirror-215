
from sdks.polygon_sdk.async_polygon_sdk import AsyncPolygonSDK
from sdks.polygon_sdk.async_options_sdk import PolygonOptionsSDK
from cfg import YOUR_API_KEY, today_str
import asyncio
poly = AsyncPolygonSDK(YOUR_API_KEY)
poly_opts = PolygonOptionsSDK(YOUR_API_KEY)
import aiohttp

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
                all_results=[]
                while 'next_url' in atm_options:
                    next_url = atm_options['next_url']
                    async with aiohttp.ClientSession() as session:
                        async with session.get(next_url + f"&apiKey={YOUR_API_KEY}") as response:
                            atm_options = await response.json()
                            all_results.extend(atm_options['results'])

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



async def main():
    ticker="SPX"
    price = await poly.get_price(ticker)

    upper_strike = price * 1.05
    lower_strike = price * 0.95
    ticker= await get_near_the_money_options(ticker=ticker, upper_strike=upper_strike, lower_strike=lower_strike)
    low_ivs = await poly_opts.find_lowest_iv(ticker)
    print(low_ivs)
asyncio.run(main())