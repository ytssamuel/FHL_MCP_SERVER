"""
Test script for FHL API client.

Run this to test the API client functionality.
"""

import asyncio
import logging

from fhl_bible_mcp.api import FHLAPIEndpoints

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_api_client() -> None:
    """Test various API endpoints."""
    
    async with FHLAPIEndpoints() as client:
        logger.info("=" * 60)
        logger.info("Testing FHL API Client")
        logger.info("=" * 60)
        
        # Test 1: Get Bible versions
        logger.info("\n[Test 1] Fetching Bible versions...")
        try:
            versions = await client.get_bible_versions()
            logger.info(f"✓ Found {versions['record_count']} Bible versions")
            logger.info(f"  First version: {versions['record'][0]['cname']}")
        except Exception as e:
            logger.error(f"✗ Failed to fetch versions: {e}")
        
        # Test 2: Get a verse (John 3:16)
        logger.info("\n[Test 2] Fetching John 3:16...")
        try:
            verse = await client.get_verse("約", 3, "16", version="unv")
            logger.info(f"✓ Fetched verse successfully")
            logger.info(f"  Text: {verse['record'][0]['bible_text']}")
        except Exception as e:
            logger.error(f"✗ Failed to fetch verse: {e}")
        
        # Test 3: Search for keyword
        logger.info("\n[Test 3] Searching for '愛' (love)...")
        try:
            results = await client.search_bible("愛", limit=5)
            logger.info(f"✓ Found {results['record_count']} results (showing 5)")
            for i, result in enumerate(results['record'][:3], 1):
                logger.info(
                    f"  {i}. {result['chineses']} {result['chap']}:{result['sec']}"
                )
        except Exception as e:
            logger.error(f"✗ Failed to search: {e}")
        
        # Test 4: Get word analysis
        logger.info("\n[Test 4] Getting word analysis for John 3:16...")
        try:
            analysis = await client.get_word_analysis("John", 3, 16)
            logger.info(f"✓ Found {analysis['record_count']} words")
            # Show first 3 words
            for word in analysis['record'][1:4]:  # Skip wid=0 (summary)
                logger.info(
                    f"  {word['word']} - {word['exp']} (Strong's #{word['sn']})"
                )
        except Exception as e:
            logger.error(f"✗ Failed to get word analysis: {e}")
        
        # Test 5: Get Strong's dictionary entry
        logger.info("\n[Test 5] Looking up Strong's #25 (agapao - love)...")
        try:
            entry = await client.get_strongs_dictionary(25, "nt")
            logger.info(f"✓ Found dictionary entry")
            logger.info(f"  Original word: {entry['record'][0]['orig']}")
            logger.info(f"  Related words: {len(entry['record'][0].get('same', []))}")
        except Exception as e:
            logger.error(f"✗ Failed to get Strong's entry: {e}")
        
        # Test 6: List commentaries
        logger.info("\n[Test 6] Listing available commentaries...")
        try:
            commentaries = await client.list_commentaries()
            logger.info(f"✓ Found {commentaries['record_count']} commentaries")
            for c in commentaries['record'][:3]:
                logger.info(f"  {c['id']}: {c['name']}")
        except Exception as e:
            logger.error(f"✗ Failed to list commentaries: {e}")
        
        logger.info("\n" + "=" * 60)
        logger.info("API Client Tests Completed!")
        logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_api_client())
