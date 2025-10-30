import asyncio
from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints

async def test():
    async with FHLAPIEndpoints() as api:
        r = await api.get_commentary('John', 3, 16, 1)
        print("Keys:", r.keys() if isinstance(r, dict) else 'not dict')
        print("Response:", r)

asyncio.run(test())
