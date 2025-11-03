"""
FHL Bible API Endpoints

Implements specific API endpoint methods for the FHL Bible API.
Each method corresponds to a specific API endpoint documented in the planning document.
"""

import logging
import hashlib
import json
import httpx
from typing import Any, Optional

from fhl_bible_mcp.api.client import FHLAPIClient
from fhl_bible_mcp.config import Config, get_config
from fhl_bible_mcp.utils.errors import InvalidParameterError
from fhl_bible_mcp.utils.cache import get_cache

logger = logging.getLogger(__name__)


class FHLAPIEndpoints(FHLAPIClient):
    """
    Extended API client with specific endpoint methods.
    
    This class inherits from FHLAPIClient and adds methods for each
    FHL API endpoint. Includes automatic caching for better performance.
    
    Configuration Priority:
    1. Explicit constructor parameters (if provided)
    2. Config object (if provided)
    3. Global config instance
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        use_cache: Optional[bool] = None,
        cache_dir: Optional[str] = None,
        config: Optional[Config] = None
    ):
        """
        Initialize FHL API Endpoints with configuration support.
        
        Args:
            base_url: Base URL of the API (if None, use config)
            timeout: Request timeout in seconds (if None, use config)
            max_retries: Maximum number of retries (if None, use config)
            use_cache: Enable caching (if None, use config)
            cache_dir: Cache directory path (if None, use config)
            config: Optional Config object (if None, use global config)
        """
        # 取得設定 (優先順序: 提供的 config > 全域 config)
        self.config = config or get_config()
        
        # 從設定取得預設值
        _base_url = base_url or self.config.api.base_url
        _timeout = timeout if timeout is not None else self.config.api.timeout
        _max_retries = max_retries if max_retries is not None else self.config.api.max_retries
        _use_cache = use_cache if use_cache is not None else self.config.cache.enabled
        _cache_dir = cache_dir or self.config.cache.directory
        
        # 初始化父類別
        super().__init__(base_url=_base_url, timeout=_timeout, max_retries=_max_retries)
        
        # 設定快取
        self.use_cache = _use_cache
        self.cache = get_cache(cache_dir=_cache_dir) if _use_cache else None
        
        if self.use_cache:
            logger.info(f"Cache enabled: {_cache_dir}")
            
            # 如果設定為啟動時清理,則清理過期快取
            if self.config.cache.cleanup_on_start:
                cleanup_count = self.cache.cleanup_expired()
                if cleanup_count > 0:
                    logger.info(f"Cleaned up {cleanup_count} expired cache entries")
    
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

    # ========================================================================
    # 8. Apocrypha (次經) APIs - Books 101-115
    # ========================================================================

    async def get_apocrypha_verse(
        self,
        book: str,
        chapter: int,
        verse: str | None = None,
        include_strong: bool = False,
    ) -> dict[str, Any]:
        """
        Query Apocrypha (次經) verses.
        
        API: qsub.php
        Book Range: 101-115
        Default Version: c1933 (1933年聖公會出版)
        
        Apocrypha Books:
        - 多俾亞傳 (Tobit) - Book 101
        - 友弟德傳 (Judith) - Book 102
        - 瑪加伯上 (1 Maccabees) - Book 103
        - 瑪加伯下 (2 Maccabees) - Book 104
        - 智慧篇 (Wisdom) - Book 105
        - 德訓篇 (Sirach) - Book 106
        - 巴錄書 (Baruch) - Book 107
        - 耶利米書信 (Letter of Jeremiah) - Book 108
        - 但以理補篇 (Additions to Daniel) - Books 109-111
        - 以斯帖補篇 (Additions to Esther) - Book 112
        
        Note: Apocrypha uses c1933 version by default. 
              Do not specify version parameter - it will be ignored.
        
        Args:
            book: Book name (Chinese or English abbreviation)
            chapter: Chapter number
            verse: Verse(s) - supports formats like "1", "1-5", "1,3,5", "1-2,5,8-10"
                   If None, returns entire chapter
            include_strong: Include Strong's numbers (default: False)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of verses
                - v_name: Version name (1933年聖公會出版)
                - version: Version code (c1933)
                - bid: Book ID (101-115)
                - record: List of verse objects
        
        Raises:
            InvalidParameterError: If parameters are invalid
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     # Query Tobit 1:1 (uses c1933 by default)
            >>>     verse = await client.get_apocrypha_verse("多", 1, "1")
            >>>     print(verse['record'][0]['bible_text'])
        """
        params: dict[str, Any] = {
            "chineses": book,
            "chap": chapter,
            "strong": 1 if include_strong else 0,
        }
        
        if verse is not None:
            params["sec"] = verse
        
        logger.info(
            f"Fetching apocrypha verse: {book} {chapter}" + (f":{verse}" if verse else "")
        )
        
        return await self._cached_request(
            endpoint="qsub.php",
            params=params,
            namespace="apocrypha",
            strategy="verses"  # 7 days TTL
        )

    async def search_apocrypha(
        self,
        query: str,
        limit: int | None = None,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Search for keywords in Apocrypha (次經).
        
        API: sesub.php
        Book Range: 101-115
        Default Version: c1933 (1933年聖公會出版)
        
        Note: Do NOT specify VERSION parameter - it causes API to return empty response.
              The API uses c1933 by default.
        
        Args:
            query: Search keyword
            limit: Maximum results to return
            offset: Number of results to skip
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Total number of results
                - key: Search query
                - record: List of matching verses with bid field (book ID 101-115)
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     # Search in Apocrypha (uses c1933 by default)
            >>>     results = await client.search_apocrypha("智慧", limit=10)
            >>>     print(f"Found {results['record_count']} verses")
        """
        params: dict[str, Any] = {
            "q": query,
            "offset": offset,
        }
        
        if limit is not None:
            params["limit"] = limit
        
        logger.info(f"Searching apocrypha: query='{query}'")
        return await self._cached_request(
            endpoint="sesub.php",
            params=params,
            namespace="apocrypha_search",
            strategy="search"  # 1 day TTL
        )

    # ========================================================================
    # 9. Apostolic Fathers (使徒教父) APIs - Books 201-217
    # ========================================================================

    async def get_apostolic_fathers_verse(
        self,
        book: str,
        chapter: int,
        verse: str | None = None,
        include_strong: bool = False,
    ) -> dict[str, Any]:
        """
        Query Apostolic Fathers (使徒教父) verses.
        
        API: qaf.php
        Book Range: 201-217
        Default Version: afhuang (黃錫木主編《使徒教父著作》)
        
        Apostolic Fathers Books:
        - 革利免前書 (1 Clement) - Book 201
        - 革利免後書 (2 Clement) - Book 202
        - 伊格那丟書信 (Ignatius) - Book 203
        - 坡旅甲書信 (Polycarp) - Book 204
        - 黑馬牧人書 (Shepherd of Hermas) - Book 205
        - 巴拿巴書 (Barnabas) - Book 206
        - 十二使徒遺訓 (Didache) - Book 207
        - 帕皮亞殘篇 (Papias Fragments) - Book 216
        
        Note: Apostolic Fathers uses afhuang version by default.
              Do not specify version parameter - it will be ignored.
        
        Args:
            book: Book name (Chinese or English abbreviation)
            chapter: Chapter number
            verse: Verse(s) - supports formats like "1", "1-5", "1,3,5", "1-2,5,8-10"
                   If None, returns entire chapter
            include_strong: Include Strong's numbers (default: False)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of verses
                - v_name: Version name (黃錫木主編《使徒教父著作》)
                - version: Version code (afhuang)
                - bid: Book ID (201-217)
                - record: List of verse objects
        
        Raises:
            InvalidParameterError: If parameters are invalid
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     # Query 1 Clement 1:1 (uses afhuang by default)
            >>>     verse = await client.get_apostolic_fathers_verse("革", 1, "1")
            >>>     print(verse['record'][0]['bible_text'])
        """
        params: dict[str, Any] = {
            "chineses": book,
            "chap": chapter,
            "strong": 1 if include_strong else 0,
        }
        
        if verse is not None:
            params["sec"] = verse
        
        logger.info(
            f"Fetching apostolic fathers verse: {book} {chapter}" + (f":{verse}" if verse else "")
        )
        
        return await self._cached_request(
            endpoint="qaf.php",
            params=params,
            namespace="apostolic_fathers",
            strategy="verses"  # 7 days TTL
        )

    async def search_apostolic_fathers(
        self,
        query: str,
        limit: int | None = None,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Search for keywords in Apostolic Fathers (使徒教父).
        
        API: seaf.php
        Book Range: 201-217
        Default Version: afhuang (黃錫木主編《使徒教父著作》)
        
        Note: Do NOT specify VERSION parameter - it causes API to return empty response.
              The API uses afhuang by default.
        
        Args:
            query: Search keyword
            limit: Maximum results to return
            offset: Number of results to skip
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Total number of results
                - key: Search query
                - record: List of matching verses with bid field (book ID 201-217)
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     # Search in Apostolic Fathers (uses afhuang by default)
            >>>     results = await client.search_apostolic_fathers("教會", limit=10)
            >>>     print(f"Found {results['record_count']} verses")
        """
        params: dict[str, Any] = {
            "q": query,
            "offset": offset,
        }
        
        if limit is not None:
            params["limit"] = limit
        
        logger.info(f"Searching apostolic fathers: query='{query}'")
        return await self._cached_request(
            endpoint="seaf.php",
            params=params,
            namespace="apostolic_fathers_search",
            strategy="search"  # 1 day TTL
        )

    # ========================================================================
    # 10. Footnotes (註腳) API
    # ========================================================================

    async def get_footnote(
        self,
        book_id: int,
        footnote_id: int,
        version: str = "tcv",
        use_simplified: bool = False,
    ) -> dict[str, Any]:
        """
        Query Bible verse footnotes (註腳).
        
        API: rt.php
        Version: tcv only (台灣聖經公會現代中文譯本)
        
        **Important**: Only TCV version has footnotes. Other versions will return
        empty results (record_count = 0).
        
        Args:
            book_id: Book ID number (1-66)
                     1=Genesis, 43=John, 45=Romans, etc.
            footnote_id: Footnote ID number
                        Each book has its own footnote numbering system.
                        Start from 1 and increment to find available footnotes.
            version: Bible version (default: "tcv")
                    **Only "tcv" has footnotes**
            use_simplified: Use simplified Chinese (default: False)
        
        Returns:
            Dictionary with:
                - status: "success" or "error"
                - record_count: Number of footnotes found (0 or 1)
                - version: Version code ("tcv")
                - engs: English book abbreviation
                - record: List with footnote data (if found)
                    - id: Footnote ID
                    - text: Footnote content
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     # Query Genesis footnote #1
            >>>     result = await client.get_footnote(book_id=1, footnote_id=1)
            >>>     print(result["record"][0]["text"])
            >>>     # Output: 「太初，上帝創造天地。」或譯「太初，上帝創造天地的時候。」...
            >>>     
            >>>     # Query John footnote #10
            >>>     result = await client.get_footnote(book_id=43, footnote_id=10)
            >>>     print(result["record"][0]["text"])
            >>>     # Output: 有些古卷沒有括弧內這一段；另有些古卷...
        
        Note:
            - Footnote IDs are specific to each book
            - No API exists to list all footnote IDs for a book
            - If footnote_id doesn't exist, returns record_count: 0
            - TCV version provides translation alternatives and manuscript variations
        """
        params = {
            "bid": book_id,
            "id": footnote_id,
            "version": version,
            "gb": 1 if use_simplified else 0,
        }
        
        logger.info(
            f"Fetching footnote: book_id={book_id}, footnote_id={footnote_id}, version={version}"
        )
        
        return await self._cached_request(
            endpoint="rt.php",
            params=params,
            namespace="footnotes",
            strategy="verses"  # 7 days TTL
        )
    
    # =============================================================================
    # Section 11: Articles (文章查詢)
    # =============================================================================
    
    async def search_articles(
        self,
        title: str | None = None,
        author: str | None = None,
        content: str | None = None,
        abstract: str | None = None,
        column: str | None = None,
        pub_date: str | None = None,
        use_simplified: bool = False,
        limit: int = 50
    ) -> dict[str, Any]:
        """
        Search Faith Hope Love (信望愛) articles.
        
        API: www.fhl.net/api/json.php
        
        ⚠️ **Important Constraints**:
        - **Must provide at least ONE search parameter** (API returns error otherwise)
        - No pagination support (all results returned at once)
        - Client-side limit applied to prevent overwhelming results
        
        Args:
            title: Title keywords to search for
            author: Author name to search for
            content: Content keywords to search for
            abstract: Abstract keywords to search for
            column: Column code (ptab) to filter by
                    Use list_article_columns() to see available columns
            pub_date: Publication date in YYYY.MM.DD format (e.g., "2025.10.19")
            use_simplified: Use simplified Chinese (default: False)
            limit: Maximum number of results to return (client-side limit)
                   Range: 1-200, Default: 50
        
        Returns:
            Dictionary with:
                - status: 1 for success, 0 for error
                - record_count: Number of articles found
                - record: List of articles (each containing):
                    - id: Article ID
                    - column: Column name (Chinese)
                    - ptab: Column code (English)
                    - aid: Article aid
                    - title: Article title
                    - author: Author name
                    - pubtime: Publication date (YYYY.MM.DD)
                    - abst: Abstract/summary
                    - txt: Full article content (HTML format)
                - limited: True if results were limited (added by client)
        
        Raises:
            InvalidParameterError: If no search parameters provided
        
        Example:
            >>> async with FHLAPIEndpoints() as client:
            >>>     # Search by title
            >>>     result = await client.search_articles(title="愛")
            >>>     print(f"Found {result['record_count']} articles")
            >>>     
            >>>     # Search by author
            >>>     result = await client.search_articles(author="陳鳳翔")
            >>>     for article in result["record"]:
            >>>         print(article["title"])
            >>>     
            >>>     # Search specific column
            >>>     result = await client.search_articles(column="women3")
            >>>     
            >>>     # Combined search with limit
            >>>     result = await client.search_articles(
            >>>         title="信心",
            >>>         author="李",
            >>>         limit=10
            >>>     )
        
        Note:
            - Article content (txt field) is in HTML format
            - Contains tags like <pic>filename.jpg</pic>, <br/>, etc.
            - No sorting control (API returns in its own order)
            - Results are cached for 1 day (articles update weekly)
        """
        # Validate: at least one search parameter required
        if not any([title, author, content, abstract, column, pub_date]):
            raise InvalidParameterError(
                "search_params",
                None,
                "Must provide at least one search parameter (title, author, content, abstract, column, or pub_date)"
            )
        
        # Build parameters
        params: dict[str, str | int] = {
            "gb": 1 if use_simplified else 0
        }
        
        if title:
            params["title"] = title
        if author:
            params["author"] = author
        if content:
            params["txt"] = content
        if abstract:
            params["abst"] = abstract
        if column:
            params["ptab"] = column
        if pub_date:
            params["pubtime"] = pub_date
        
        logger.info(
            f"Searching articles: title={title}, author={author}, "
            f"content={content}, column={column}, limit={limit}"
        )
        
        # Make request to www.fhl.net/api/ (different base URL)
        # Articles API is on www.fhl.net, not bible.fhl.net
        url = "https://www.fhl.net/api/json.php"
        
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Apply client-side limit
        if data.get("status") == 1 and "record" in data:
            if isinstance(data["record"], list) and len(data["record"]) > limit:
                data["record"] = data["record"][:limit]
                data["record_count"] = limit
                data["limited"] = True  # Flag to indicate results were limited
        
        return data
    
    def list_article_columns(self) -> list[dict[str, str]]:
        """
        List available article columns.
        
        Since the API doesn't provide a column listing endpoint,
        this method returns a maintained list of known columns.
        
        Returns:
            List of dictionaries, each containing:
                - code: Column code (use in search_articles)
                - name: Column name (Chinese)
                - description: Column description
        
        Example:
            >>> api = FHLAPIEndpoints()
            >>> columns = api.list_article_columns()
            >>> for col in columns:
            >>>     print(f"{col['code']}: {col['name']} - {col['description']}")
            >>> 
            >>> # Output:
            >>> # women3: 麻辣姊妹 - 女性信仰生活分享
            >>> # sunday: 主日學 - 主日學教材與資源
            >>> # ...
        
        Note:
            - This list is maintained manually
            - May not include all columns
            - Use column codes in search_articles(column=...)
        """
        return [
            {
                "code": "women3",
                "name": "麻辣姊妹",
                "description": "女性信仰生活分享"
            },
            {
                "code": "sunday",
                "name": "主日學",
                "description": "主日學教材與資源"
            },
            {
                "code": "youth",
                "name": "青少年",
                "description": "青少年信仰與生活"
            },
            {
                "code": "family",
                "name": "家庭",
                "description": "家庭生活與信仰"
            },
            {
                "code": "theology",
                "name": "神學",
                "description": "神學探討與研究"
            },
            {
                "code": "bible_study",
                "name": "查經",
                "description": "聖經研究與分享"
            },
            {
                "code": "devotion",
                "name": "靈修",
                "description": "靈修心得與見證"
            },
            {
                "code": "mission",
                "name": "宣教",
                "description": "宣教事工與分享"
            },
            {
                "code": "church",
                "name": "教會",
                "description": "教會生活與事奉"
            },
            {
                "code": "culture",
                "name": "文化",
                "description": "信仰與文化對話"
            },
            {
                "code": "history",
                "name": "歷史",
                "description": "教會歷史與傳統"
            },
            {
                "code": "counseling",
                "name": "輔導",
                "description": "心理輔導與關懷"
            }
        ]
    
    async def get_article_content(
        self,
        article_id: str,
        article_aid: str,
        use_simplified: bool = False
    ) -> dict[str, Any]:
        """
        Get full content of a specific article by ID and AID.
        
        ⚠️ **IMPORTANT LIMITATION**: 
        The FHL API does NOT support direct article lookup by ID/AID.
        This method is designed to work with cached article data from search results.
        
        **Recommended Usage Pattern**:
        1. Use search_articles() to get a list of articles (with full content)
        2. Store the complete article data (including txt field)
        3. Use this method only for re-fetching if needed
        
        Since the API doesn't support ID-based lookup, this method will:
        - Return error with helpful message directing users to search_articles
        
        Args:
            article_id: Article ID (from search results)
            article_aid: Article AID (from search results)
            use_simplified: Use simplified Chinese (default: False)
        
        Returns:
            Dictionary with:
                - status: 0 (not supported)
                - result: Error message explaining the limitation
        
        Example:
            >>> # INCORRECT: Don't use get_article_content alone
            >>> article = await client.get_article_content("8984", "515")
            >>> 
            >>> # CORRECT: Use search results directly
            >>> results = await client.search_articles(title="愛")
            >>> article = results["record"][0]  # Has full content!
            >>> full_content = article["txt"]  # Complete HTML
        
        Note:
            - FHL API does NOT support direct article retrieval
            - Article content is ONLY available through search_articles()
            - The search results already contain full HTML content
            - This method exists for API completeness but returns an error
        """
        if not article_id or not article_aid:
            raise InvalidParameterError(
                "article_id/article_aid",
                f"id={article_id}, aid={article_aid}",
                "Both article_id and article_aid are required"
            )
        
        logger.warning(
            f"get_article_content called for ID={article_id}, AID={article_aid}. "
            f"Note: FHL API does not support direct article lookup."
        )
        
        # The FHL API does NOT support getting articles by ID/AID
        # It only supports search, and the search results already contain full content
        return {
            "status": 0,
            "result": (
                "FHL API does not support direct article retrieval by ID. "
                "Please use search_articles() which returns complete article content "
                "including the full HTML text in the 'txt' field. "
                "The search results already contain everything you need!"
            ),
            "error_code": "API_LIMITATION",
            "recommendation": "Use search_articles() and cache the results"
        }
