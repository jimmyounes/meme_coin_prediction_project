import asyncio
import websockets
from datetime import datetime
import you
import base64
import json
import csv
import time
import os 
def generate_sec_websocket_key():
    random_bytes = os.urandom(16)
    key = base64.b64encode(random_bytes).decode('utf-8')
    return key

TYPES = ['pairs', 'latestBlock']

DATA = []
FIELDNAMES = [
  "chain_id", 
  "dex_id", 
  "pair_address", 
  "token_address", 
  "token_name", 
  "token_symbol", 
  "token_m5_buys", 
  "token_m5_sells", 
  "token_h1_buys", 
  "token_h1_sells", 
  "token_h1_to_m5_buys", 
  "token_liquidity", 
  "token_market_cap", 
  "token_created_at", 
  "token_created_since", 
  "token_eti", 
  "token_header", 
  "token_website", 
  "token_twitter", 
  "token_links", 
  "token_img_key", 
  "token_price_usd", 
  "token_price_change_h24", 
  "token_price_change_h6",
  "token_price_change_h1", 
  "token_price_change_m5",
  "information_extracted_at"
]

async def dexscreener_scraper():
   
    headers = {
      "Host": "io.dexscreener.com", 
      "Connection": "Upgrade", 
      "Pragma": "no-cache", 
      "Cache-Control": "no-cache", 
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
      "Upgrade": "websocket", 
      "Origin": "https://dexscreener.com", 
      "Sec-WebSocket-Version": 13, 
      "Accept-Encoding": "gzip, deflate, br, zstd", 
      "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7", 
      "Sec-WebSocket-Key": generate_sec_websocket_key()
    }
    list_token={}
    while True:    
     
     for i in range(1,24): 
      DATA = []
      url =f"wss://io.dexscreener.com/dex/screener/pairs/h24/{i}?rankBy[key]=pairAge&rankBy[order]=asc&rankBy[chainIds]=solana&rankBy[minMarketCap]=40000&rankBy[minLiq]=1000"   
      try:
       async with websockets.connect(url, extra_headers=headers) as websocket:
       
        message_raw = await websocket.recv()
        message = json.loads(message_raw)
        
        _type = message["type"]
        assert _type in TYPES
        if _type == 'pairs' : 

          pairs = message["pairs"]
          
          assert pairs
          for pair in pairs: 

            chain_id = pair["chainId"]
            dex_id = pair["dexId"]
            pair_address = pair["pairAddress"]

            assert pair_address

            token_address = pair["baseToken"]["address"]
            token_name = pair["baseToken"]["name"]
            token_symbol = pair["baseToken"]["symbol"]

            token_txns = pair["txns"]

            token_m5_buys = token_txns["m5"]["buys"]
            token_m5_sells = token_txns["m5"]["sells"]

            token_h1_buys = token_txns["h1"]["buys"]
            token_h1_sells = token_txns["h1"]["sells"]

            token_h1_to_m5_buys = round(token_m5_buys*12/token_h1_buys, 2) if token_m5_buys else None
            if("liquidity" in pair):
                token_liquidity = pair["liquidity"]["usd"]
            else : 
               token_liquidity=0  
            if("marketCap" in pair):
                token_market_cap = pair["marketCap"]
            else :   
               token_market_cap = 0   
           
            token_created_at_raw = pair["pairCreatedAt"]
            token_created_at = token_created_at_raw / 1000
            token_created_at = datetime.utcfromtimestamp(token_created_at)

            now_utc = datetime.utcnow()
            token_created_since = round((now_utc - token_created_at).total_seconds() / 60, 2)
            
            token_eti = pair.get("ear", False)
            token_header = pair.get("profile", {}).get("header", False)
            token_website = pair.get("profile", {}).get("website", False)
            token_twitter = pair.get("profile", {}).get("twitter", False)
            token_links = pair.get("profile", {}).get("linkCount", False)
            token_img_key = pair.get("profile", {}).get("imgKey", False)
            if("priceUsd" in pair ):
                token_price_usd = pair["priceUsd"]
            else :   
               token_price_usd =None  
            token_price_change_h24 = pair["priceChange"]["h24"]
            token_price_change_h6 = pair["priceChange"]["h6"]
            token_price_change_h1 = pair["priceChange"]["h1"]
            token_price_change_m5 = pair["priceChange"]["m5"]
            information_extracted_at= datetime.now()
            VALUES = [
              chain_id, 
              dex_id, 
              pair_address, 
              token_address, 
              token_name, 
              token_symbol, 
              token_m5_buys, 
              token_m5_sells, 
              token_h1_buys, 
              token_h1_sells, 
              token_h1_to_m5_buys, 
              token_liquidity, 
              token_market_cap, 
              token_created_at, 
              token_created_since, 
              token_eti,
              token_header, 
              token_website,
              token_twitter, 
              token_links, 
              token_img_key,
              token_price_usd,
              token_price_change_h24, 
              token_price_change_h6, 
              token_price_change_h1, 
              token_price_change_m5,
              information_extracted_at
            ]

            
            
            row = dict(zip(FIELDNAMES, VALUES))
            
            if(row['dex_id']=='raydium' and  row['token_market_cap']>50000 and row['token_liquidity']>1000 and token_twitter==True ):
                
                print(row)
                DATA.append(row)

          for row in DATA : 
            filename = './database/dexscreener_%s.csv' % row['token_address']
            with open(filename, 'a',encoding='utf-8', newline='') as f: 
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter='\t')
                if f.tell() == 0:
                    writer.writeheader() 
                writer.writerow(row)
      except TimeoutError:
                print("Connection timed out. Retrying...")
                continue
      except Exception as e:
                print(f"An error occurred: {e}")
                continue         
     print('pause 2min :°')
     time.sleep(120)     
    
if __name__ == "__main__":
  asyncio.run(dexscreener_scraper())