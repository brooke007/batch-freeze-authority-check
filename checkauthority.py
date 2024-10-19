import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.async_client import AsyncToken
from solders.pubkey import Pubkey
from dotenv import load_dotenv
import os

load_dotenv()

RPC_URL = os.getenv("RPC_URL")

async def check_freeze_authority(token_address):
    async with AsyncClient(RPC_URL) as client:
        try:
            address = Pubkey.from_string(token_address)
            token = AsyncToken(client, address, TOKEN_PROGRAM_ID, None)
            mint_info = await token.get_mint_info()
            
            if mint_info.freeze_authority:
                return f"{token_address}: Freeze authority exists"
            else:
                return f"{token_address}: Freeze authority does not exist"
        except Exception as e:
            return f"{token_address}: Error during check - {str(e)}"

async def main():
    with open('token.txt', 'r') as file:
        token_addresses = file.read().split()
    
    tasks = [check_freeze_authority(address) for address in token_addresses]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
