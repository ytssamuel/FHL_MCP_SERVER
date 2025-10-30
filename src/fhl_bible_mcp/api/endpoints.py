"""
FHL Bible API Endpoints

Implements specific API endpoint methods for the FHL Bible API.
Each method corresponds to a specific API endpoint documented in the planning document.
"""

import logging
import hashlib
import json
from typing import Any

from fhl_bible_mcp.api.client import FHLAPIClient
from fhl_bible_mcp.utils.errors import InvalidParameterError
from fhl_bible_mcp.utils.cache import get_cache

logger = logging.getLogger(__name__)


class FHLAPIEndpoints(FHLAPIClient):
    """
    Extended API client with specific endpoint methods.
    
    This class inherits from FHLAPIClient and adds methods for each
    FHL API endpoint. Includes automatic caching for better performance.
    """
    
    def __init__(
        self,
        base_url: str = "https://bible.fhl.net/json/",
        timeout: int = 30,
        max_retries: int = 3,
        use_cache: bool = True,
        cache_dir: str = ".cache"
    ):
        """
        Initialize FHL API Endpoints with caching support.
        
        Args:
            base_url: Base URL of the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            use_cache: Enable caching (default: True)
            cache_dir: Cache directory path (default: ".cache")
        """
        super().__init__(base_url=base_url, timeout=timeout, max_retries=max_retries)
        self.use_cache = use_cache
        self.cache = get_cache(cache_dir=cache_dir) if use_cache else None
        
        if self.use_cache:
            logger.info(f"Cache enabled: {cache_dir}")
    
    def _make_cache_key(self, **kwargs) -> str:
        """
        Generate a cache key from parameters.
        
        Args:
            **kwargs: Parameters to hash
            
        Returns:
            Cache key string
        """
        # 將參數排序後轉成 JSON 字串
        params_str = json.dumps(kwargs, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(params_str.encode()).hexdigest()
    
    async def _cached_request(
        self,
        endpoint: str,
        params: dict[str, Any],
        namespace: str,
        strategy: str
    ) -> Any:
        """
        Make a cached API request.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            namespace: Cache namespace
            strategy: Cache strategy name
            
        Returns:
            API response (from cache or fresh request)
        """
        if not self.use_cache or self.cache is None:
            return await self._make_request(endpoint, params=params)
        
        # 生成快取鍵
        cache_key = self._make_cache_key(endpoint=endpoint, **params)
        
        # 嘗試從快取讀取
        cached_data = self.cache.get(namespace, cache_key, strategy_name=strategy)
        if cached_data is not None:
            logger.debug(f"Cache hit: {namespace}:{cache_key[:8]}...")
            return cached_data
        
        # 快取未命中,發送請求
        logger.debug(f"Cache miss: {namespace}:{cache_key[:8]}...")
        data = await self._make_request(endpoint, params=params)
        
        # 儲存到快取
        self.cache.set(namespace, cache_key, data, strategy_name=strategy)
        
        return data

    # ========================================================================
    # 1. Basic Information APIs
    # ========================================================================

    async def get_bible_versions(self) -> dict[str, Any]:
        """
        List all available Bible versions.
        
        API: ab.php
        Cache: Permanent (versions list rarely changes)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of versions
                - record: List of version objects with fields:
                    - book: Version code
                    - cname: Version name
                    - proc: Special font requirement (0-4)
                    - strong: Has Strong's Number (0/1)
                    - ntonly: New Testament only (0/1)
                    - otonly: Old Testament only (0/1)
                    - candownload: Can download offline (0/1)
                    - version: Last update time
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     versions = await client.get_bible_versions()
            >>>     print(f"Found {versions['record_count']} versions")
        """
        logger.info("Fetching Bible versions list")
        return await self._cached_request(
            endpoint="ab.php",
            params={},
            namespace="versions",
            strategy="permanent"
        )

    async def get_book_list(self) -> str:
        """
        Get list of all Bible books.
        
        API: listall.html
        
        Returns:
            CSV string with format: id,english_abbr,english_full,chinese_abbr,english_short
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     books_csv = await client.get_book_list()
            >>>     # Parse CSV to get book list
        """
        logger.info("Fetching book list")
        return await self._make_request("listall.html")

    # ========================================================================
    # 2. Verse Query APIs
    # ========================================================================

    async def get_verse(
        self,
        book: str,
        chapter: int,
        verse: str | None = None,
        version: str = "unv",
        include_strong: bool = False,
    ) -> dict[str, Any]:
        """
        Query Bible verses.
        
        API: qb.php
        
        Args:
            book: Book name (Chinese or English abbreviation)
            chapter: Chapter number
            verse: Verse(s) - supports formats like "1", "1-5", "1,3,5", "1-2,5,8-10"
                   If None, returns entire chapter
            version: Bible version code (default: "unv" for 和合本)
            include_strong: Include Strong's numbers (default: False)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of verses
                - v_name: Version name
                - version: Version code
                - proc: Special font requirement
                - prev: Previous verse info (chineses, engs, chap, sec)
                - next: Next verse info
                - record: List of verse objects:
                    - engs: English book abbreviation
                    - chineses: Chinese book abbreviation
                    - chap: Chapter number
                    - sec: Verse number
                    - bible_text: Verse text
        
        Raises:
            InvalidParameterError: If parameters are invalid
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     verse = await client.get_verse("約", 3, "16")
            >>>     print(verse['record'][0]['bible_text'])
        """
        params: dict[str, Any] = {
            "chineses": book,
            "chap": chapter,
            "version": version,
            "strong": 1 if include_strong else 0,
        }
        
        if verse is not None:
            params["sec"] = verse
        
        logger.info(
            f"Fetching verse: {book} {chapter}" + (f":{verse}" if verse else "")
        )
        
        return await self._cached_request(
            endpoint="qb.php",
            params=params,
            namespace="verses",
            strategy="verses"  # 7 days TTL
        )

    async def query_verse_citation(
        self,
        citation: str,
        version: str = "unv",
        include_strong: bool = False,
    ) -> dict[str, Any]:
        """
        Query verses using citation format.
        
        API: qsb.php
        
        Args:
            citation: Citation string (e.g., "太 10:1-3", "John 3:16")
            version: Bible version code
            include_strong: Include Strong's numbers
        
        Returns:
            Dictionary with verse data
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     result = await client.query_verse_citation("太 10:1-3")
        """
        params = {
            "qstr": citation,
            "version": version,
            "strong": 1 if include_strong else 0,
        }
        
        logger.info(f"Fetching verses by citation: {citation}")
        return await self._make_request("qsb.php", params)

    # ========================================================================
    # 3. Search APIs
    # ========================================================================

    async def search_bible(
        self,
        query: str,
        search_type: str = "keyword",  # "keyword", "greek_number", "hebrew_number"
        scope: str = "all",  # "all", "ot", "nt", "range"
        version: str = "unv",
        limit: int | None = None,
        offset: int = 0,
        range_start: int | None = None,
        range_end: int | None = None,
        count_only: bool = False,
        index_only: bool = False,
    ) -> dict[str, Any]:
        """
        Search for keywords or Strong's numbers in the Bible.
        
        API: se.php
        
        Args:
            query: Search query (keyword or Strong's number)
            search_type: "keyword", "greek_number", or "hebrew_number"
            scope: "all", "ot" (Old Testament), "nt" (New Testament), or "range"
            version: Bible version code
            limit: Maximum results to return
            offset: Number of results to skip
            range_start: Starting book number (1-66) if scope="range"
            range_end: Ending book number (1-66) if scope="range"
            count_only: Return only the count
            index_only: Return only book index without content
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Total number of results
                - orig: Search type (0=keyword, 1=greek, 2=hebrew)
                - key: Search query
                - record: List of matching verses (if not count_only/index_only)
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     results = await client.search_bible("愛", limit=10)
            >>>     print(f"Found {results['record_count']} verses")
        """
        # Map search type to orig parameter
        search_type_map = {
            "keyword": "0",
            "greek_number": "1",
            "hebrew_number": "2",
        }
        
        if search_type not in search_type_map:
            raise InvalidParameterError(
                "search_type",
                search_type,
                "Must be 'keyword', 'greek_number', or 'hebrew_number'",
            )
        
        # Map scope to RANGE parameter
        scope_map = {"all": "0", "nt": "1", "ot": "2", "range": "3"}
        
        if scope not in scope_map:
            raise InvalidParameterError(
                "scope", scope, "Must be 'all', 'ot', 'nt', or 'range'"
            )
        
        params: dict[str, Any] = {
            "VERSION": version,
            "orig": search_type_map[search_type],
            "q": query,
            "RANGE": scope_map[scope],
            "offset": offset,
            "count_only": 1 if count_only else 0,
            "index_only": 1 if index_only else 0,
        }
        
        if limit is not None:
            params["limit"] = limit
        
        if scope == "range":
            if range_start is None or range_end is None:
                raise InvalidParameterError(
                    "range",
                    None,
                    "range_start and range_end are required when scope='range'",
                )
            params["range_bid"] = range_start
            params["range_eid"] = range_end
        
        logger.info(f"Searching Bible: query='{query}', type={search_type}, scope={scope}")
        return await self._cached_request(
            endpoint="se.php",
            params=params,
            namespace="search",
            strategy="search"  # 1 day TTL
        )

    # ========================================================================
    # 4. Word Analysis APIs
    # ========================================================================

    async def get_word_analysis(
        self, book: str, chapter: int, verse: int
    ) -> dict[str, Any]:
        """
        Get word-by-word analysis of a verse in original language.
        
        API: qp.php
        
        Args:
            book: Book name (English abbreviation preferred)
            chapter: Chapter number
            verse: Verse number
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of words + 1 (for verse summary)
                - N: Testament (0=NT, 1=OT)
                - prev: Previous verse info
                - next: Next verse info
                - record: List of word analysis objects:
                    - For wid=0 (verse summary):
                        - word: Original text
                        - exp: Translation
                        - chineses: Chinese book name
                        - chinesef: Chinese book full name
                    - For wid>0 (individual words):
                        - word: Original word
                        - sn: Strong's number
                        - pro: Part of speech
                        - wform: Morphology
                        - orig: Lemma (dictionary form)
                        - exp: Gloss
                        - remark: Notes
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     analysis = await client.get_word_analysis("John", 3, 16)
            >>>     for word in analysis['record']:
            >>>         if word['wid'] > 0:
            >>>             print(f"{word['word']} - {word['exp']}")
        """
        params = {"engs": book, "chap": chapter, "sec": verse}
        
        logger.info(f"Fetching word analysis: {book} {chapter}:{verse}")
        return await self._make_request("qp.php", params)

    async def get_strongs_dictionary(
        self, number: int, testament: str
    ) -> dict[str, Any]:
        """
        Lookup Strong's Dictionary entry.
        
        API: sd.php
        
        Args:
            number: Strong's number (without leading zeros)
            testament: "nt" for New Testament (Greek) or "ot" for Old Testament (Hebrew)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: 1
                - record: List with one dictionary entry:
                    - sn: Strong's number (with leading zeros)
                    - dic_text: Chinese dictionary text
                    - edic_text: English dictionary text
                    - dic_type: 0 for NT, 1 for OT
                    - orig: Original word
                    - same: List of related words (NT only):
                        - word: Related word
                        - csn: Strong's number
                        - ccnt: Occurrence count
                        - cexp: Chinese explanation
        
        Raises:
            InvalidParameterError: If testament is not "nt" or "ot"
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     entry = await client.get_strongs_dictionary(25, "nt")
            >>>     print(entry['record'][0]['dic_text'])  # Chinese definition
        """
        testament = testament.lower()
        if testament not in ["nt", "ot"]:
            raise InvalidParameterError(
                "testament", testament, "Must be 'nt' or 'ot'"
            )
        
        params = {"N": "0" if testament == "nt" else "1", "k": number}
        
        logger.info(f"Fetching Strong's dictionary: {testament.upper()} #{number}")
        return await self._cached_request(
            endpoint="sd.php",
            params=params,
            namespace="strongs",
            strategy="permanent"  # Strong's dictionary never changes
        )

    # ========================================================================
    # 5. Commentary APIs
    # ========================================================================

    async def list_commentaries(self) -> dict[str, Any]:
        """
        List all available commentaries.
        
        API: sc.php?validbook=1
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of commentaries
                - record: List of commentary info:
                    - id: Commentary ID
                    - name: Commentary name
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     commentaries = await client.list_commentaries()
            >>>     for c in commentaries['record']:
            >>>         print(f"{c['id']}: {c['name']}")
        """
        params = {"validbook": "1"}
        
        logger.info("Fetching commentaries list")
        return await self._make_request("sc.php", params)

    async def get_commentary(
        self,
        book: str,
        chapter: int,
        verse: int,
        commentary_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Get commentary for a specific verse.
        
        API: sc.php
        
        Args:
            book: Book name (English abbreviation)
            chapter: Chapter number
            verse: Verse number
            commentary_id: Commentary ID (optional, use multiple IDs like "1,2,3")
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of commentary entries
                - record: List of commentary entries:
                    - title: Entry title
                    - book_name: Commentary name
                    - com_text: Commentary text
                    - prev: Previous section info
                    - next: Next section info
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     commentary = await client.get_commentary("John", 3, 16)
            >>>     for entry in commentary['record']:
            >>>         print(f"{entry['book_name']}: {entry['com_text']}")
        """
        params: dict[str, Any] = {"engs": book, "chap": chapter, "sec": verse}
        
        if commentary_id is not None:
            params["book"] = commentary_id
        
        logger.info(
            f"Fetching commentary: {book} {chapter}:{verse}"
            + (f" (commentary #{commentary_id})" if commentary_id else "")
        )
        return await self._make_request("sc.php", params)

    async def search_commentary(
        self, keyword: str, commentary_id: int | None = None
    ) -> dict[str, Any]:
        """
        Search within commentaries.
        
        API: ssc.php
        
        Args:
            keyword: Search keyword
            commentary_id: Commentary ID to search in (optional)
        
        Returns:
            Dictionary with search results
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     results = await client.search_commentary("愛")
        """
        params: dict[str, Any] = {"key": keyword}
        
        if commentary_id is not None:
            params["book"] = commentary_id
        
        logger.info(f"Searching commentary: keyword='{keyword}'")
        return await self._make_request("ssc.php", params)

    # ========================================================================
    # 6. Topical Study APIs
    # ========================================================================

    async def get_topic_study(
        self,
        keyword: str | None = None,
        topic_id: int | None = None,
        source: str = "all",  # "all", "torrey_en", "naves_en", "torrey_zh", "naves_zh"
        count_only: bool = False,
    ) -> dict[str, Any]:
        """
        Query topical Bible study resources.
        
        API: st.php
        
        Args:
            keyword: Topic keyword (optional if topic_id provided)
            topic_id: Topic ID (optional if keyword provided)
            source: "all", "torrey_en", "naves_en", "torrey_zh", "naves_zh"
            count_only: Return only count
        
        Returns:
            Dictionary with:
                - record_count: Number of results
                - N: Source type
                - k: Topic ID
                - keyword: Search keyword
                - record: List of topic entries:
                    - book: Source (0-3)
                    - id: Entry ID
                    - topic: Topic name
                    - text: Topic content
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     topics = await client.get_topic_study(keyword="faith")
        """
        source_map = {
            "all": "4",
            "torrey_en": "0",
            "naves_en": "1",
            "torrey_zh": "2",
            "naves_zh": "3",
        }
        
        if source not in source_map:
            raise InvalidParameterError(
                "source",
                source,
                "Must be one of: all, torrey_en, naves_en, torrey_zh, naves_zh",
            )
        
        params: dict[str, Any] = {"N": source_map[source], "count_only": 1 if count_only else 0}
        
        if keyword is not None:
            params["keyword"] = keyword
        if topic_id is not None:
            params["k"] = topic_id
        
        if keyword is None and topic_id is None:
            raise InvalidParameterError(
                "keyword/topic_id", None, "Either keyword or topic_id must be provided"
            )
        
        logger.info(f"Fetching topic study: keyword='{keyword}', source={source}")
        return await self._make_request("st.php", params)

    # ========================================================================
    # 7. Audio Bible APIs
    # ========================================================================

    async def get_audio_bible(
        self, book_id: int, chapter: int, audio_version: int = 0
    ) -> dict[str, Any]:
        """
        Get audio Bible links.
        
        API: au.php
        
        Args:
            book_id: Book ID (1-66)
            chapter: Chapter number
            audio_version: Audio version (0=和合本, 1=台語, etc.)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - name: Audio version name
                - chinesef: Book name
                - engf: English book name
                - chap: Chapter
                - pbid/pchinesef/pchap: Previous chapter info
                - nbid/nchinesef/nchap: Next chapter info
                - ogg: OGG file URL
                - mp3: MP3 file URL
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     audio = await client.get_audio_bible(43, 3, 0)  # John 3
            >>>     print(f"MP3: {audio['mp3']}")
        """
        params = {"version": audio_version, "bid": book_id, "chap": chapter}
        
        logger.info(f"Fetching audio Bible: book_id={book_id}, chapter={chapter}")
        return await self._make_request("au.php", params)
