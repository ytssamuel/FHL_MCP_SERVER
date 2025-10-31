"""
FHL Bible MCP Server - Resource Handlers

提供 MCP Resources 處理器，允許 AI 透過 URI 存取聖經資料。

支援的 Resource URI 格式:
- bible://verse/{version}/{book}/{chapter}/{verse}
- bible://chapter/{version}/{book}/{chapter}
- strongs://{testament}/{number}
- commentary://{book}/{chapter}/{verse}
- info://versions
- info://books
- info://commentaries
"""

from typing import Dict, Any
from urllib.parse import urlparse, parse_qs

from ..api.endpoints import FHLAPIEndpoints
from ..tools.verse import get_bible_verse, get_bible_chapter
from ..tools.strongs import lookup_strongs
from ..tools.commentary import get_commentary, list_commentaries
from ..tools.info import list_bible_versions, get_book_list
from ..utils.errors import FHLAPIError


class ResourceError(FHLAPIError):
    """Resource URI 相關錯誤"""
    def __init__(self, message: str):
        super().__init__(message)


class ResourceHandler:
    """MCP Resource 處理器基類"""
    
    def __init__(self, endpoints: FHLAPIEndpoints):
        """
        初始化 Resource Handler
        
        Args:
            endpoints: FHL API endpoints 實例
        """
        self.endpoints = endpoints
    
    def parse_uri(self, uri: str) -> Dict[str, Any]:
        """
        解析 Resource URI
        
        Args:
            uri: Resource URI 字符串
            
        Returns:
            解析後的 URI 組件字典
            
        Raises:
            ResourceError: URI 格式錯誤
        """
        try:
            parsed = urlparse(uri)
            return {
                "scheme": parsed.scheme,
                "path": parsed.path,
                "query": parse_qs(parsed.query)
            }
        except Exception as e:
            raise ResourceError(f"無效的 URI 格式: {uri}") from e


class BibleResourceHandler(ResourceHandler):
    """聖經經文資源處理器 (bible://)"""
    
    async def handle_verse(self, uri: str) -> Dict[str, Any]:
        """
        處理 bible://verse/{version}/{book}/{chapter}/{verse}
        
        Args:
            uri: Resource URI
            
        Returns:
            經文內容字典
            
        Example:
            bible://verse/unv/John/3/16
            bible://verse/unv/John/3/16-18
        """
        parsed = self.parse_uri(uri)
        path_parts = parsed["path"].strip("/").split("/")
        
        # 移除第一個元素 "verse"
        if path_parts[0] == "verse":
            path_parts = path_parts[1:]
        
        if len(path_parts) < 4:
            raise ResourceError(
                f"bible://verse URI 格式錯誤。正確格式: bible://verse/{{version}}/{{book}}/{{chapter}}/{{verse}}"
            )
        
        version = path_parts[0]
        book = path_parts[1]
        chapter = int(path_parts[2])
        verse = path_parts[3]
        
        # 從 query string 獲取可選參數
        query = parsed.get("query", {})
        include_strong = query.get("strong", ["false"])[0].lower() == "true"
        use_simplified = query.get("simplified", ["false"])[0].lower() == "true"
        
        result = await get_bible_verse(
            book=book,
            chapter=chapter,
            verse=verse,
            version=version,
            include_strong=include_strong,
            use_simplified=use_simplified
        )
        
        return {
            "uri": uri,
            "mimeType": "application/json",
            "content": result
        }
    
    async def handle_chapter(self, uri: str) -> Dict[str, Any]:
        """
        處理 bible://chapter/{version}/{book}/{chapter}
        
        Args:
            uri: Resource URI
            
        Returns:
            整章經文字典
            
        Example:
            bible://chapter/unv/Gen/1
        """
        parsed = self.parse_uri(uri)
        path_parts = parsed["path"].strip("/").split("/")
        
        # 移除第一個元素 "chapter"
        if path_parts[0] == "chapter":
            path_parts = path_parts[1:]
        
        if len(path_parts) < 3:
            raise ResourceError(
                f"bible://chapter URI 格式錯誤。正確格式: bible://chapter/{{version}}/{{book}}/{{chapter}}"
            )
        
        version = path_parts[0]
        book = path_parts[1]
        chapter = int(path_parts[2])
        
        # 從 query string 獲取可選參數
        query = parsed.get("query", {})
        use_simplified = query.get("simplified", ["false"])[0].lower() == "true"
        
        result = await get_bible_chapter(
            book=book,
            chapter=chapter,
            version=version,
            use_simplified=use_simplified
        )
        
        return {
            "uri": uri,
            "mimeType": "application/json",
            "content": result
        }


class StrongsResourceHandler(ResourceHandler):
    """Strong's 字典資源處理器 (strongs://)"""
    
    async def handle(self, uri: str) -> Dict[str, Any]:
        """
        處理 strongs://{testament}/{number}
        
        Args:
            uri: Resource URI
            
        Returns:
            Strong's 字典條目字典
            
        Example:
            strongs://nt/25
            strongs://ot/430
        """
        parsed = urlparse(uri)
        # strongs://nt/25 會被解析為 netloc=nt, path=/25
        testament = parsed.netloc.upper()
        number = parsed.path.strip("/")
        
        if not testament or not number:
            raise ResourceError(
                f"strongs:// URI 格式錯誤。正確格式: strongs://{{testament}}/{{number}}"
            )
        
        testament = testament.upper()
        number = number
        
        # 驗證 testament
        if testament not in ["OT", "NT"]:
            raise ResourceError(f"無效的約別: {testament}。必須是 'OT' 或 'NT'")
        
        # 從 query string 獲取可選參數
        query_params = parse_qs(parsed.query)
        use_simplified = query_params.get("simplified", ["false"])[0].lower() == "true"
        
        result = await lookup_strongs(
            number=number,
            testament=testament,
            use_simplified=use_simplified
        )
        
        return {
            "uri": uri,
            "mimeType": "application/json",
            "content": result
        }


class CommentaryResourceHandler(ResourceHandler):
    """註釋資源處理器 (commentary://)"""
    
    async def handle(self, uri: str) -> Dict[str, Any]:
        """
        處理 commentary://{book}/{chapter}/{verse}
        
        Args:
            uri: Resource URI
            
        Returns:
            註釋內容字典
            
        Example:
            commentary://John/3/16
            commentary://John/3/16?commentary_id=1
        """
        parsed = urlparse(uri)
        # commentary://John/3/16 會被解析為 netloc=John, path=/3/16
        book = parsed.netloc
        path_parts = parsed.path.strip("/").split("/")
        
        if not book or len(path_parts) < 2:
            raise ResourceError(
                f"commentary:// URI 格式錯誤。正確格式: commentary://{{book}}/{{chapter}}/{{verse}}"
            )
        
        chapter = int(path_parts[0])
        verse = int(path_parts[1])
        
        # 從 query string 獲取可選參數
        query_params = parse_qs(parsed.query)
        commentary_id = query_params.get("commentary_id", [None])[0]
        if commentary_id:
            commentary_id = int(commentary_id)
        use_simplified = query_params.get("simplified", ["false"])[0].lower() == "true"
        
        result = await get_commentary(
            book=book,
            chapter=chapter,
            verse=verse,
            commentary_id=commentary_id,
            use_simplified=use_simplified
        )
        
        return {
            "uri": uri,
            "mimeType": "application/json",
            "content": result
        }


class InfoResourceHandler(ResourceHandler):
    """資訊資源處理器 (info://)"""
    
    async def handle(self, uri: str) -> Dict[str, Any]:
        """
        處理 info:// 資源
        
        Args:
            uri: Resource URI
            
        Returns:
            資訊內容字典
            
        Example:
            info://versions
            info://books
            info://books?testament=NT
            info://commentaries
        """
        parsed = urlparse(uri)
        # info://versions 會被解析為 netloc=versions, path=''
        path = parsed.netloc or parsed.path.strip("/")
        query_params = parse_qs(parsed.query)
        use_simplified = query_params.get("simplified", ["false"])[0].lower() == "true"
        
        if path == "versions":
            # 列出所有聖經版本
            result = await list_bible_versions(use_simplified=use_simplified)
        elif path == "books":
            # 列出書卷
            testament = query_params.get("testament", [None])[0]
            result = await get_book_list(testament=testament)
        elif path == "commentaries":
            # 列出註釋書
            result = await list_commentaries(use_simplified=use_simplified)
        else:
            raise ResourceError(
                f"不支援的 info:// 路徑: {path}。支援的路徑: versions, books, commentaries"
            )
        
        return {
            "uri": uri,
            "mimeType": "application/json",
            "content": result
        }


class ResourceRouter:
    """Resource URI 路由器"""
    
    def __init__(self, endpoints: FHLAPIEndpoints):
        """
        初始化路由器
        
        Args:
            endpoints: FHL API endpoints 實例
        """
        self.endpoints = endpoints
        self.bible_handler = BibleResourceHandler(endpoints)
        self.strongs_handler = StrongsResourceHandler(endpoints)
        self.commentary_handler = CommentaryResourceHandler(endpoints)
        self.info_handler = InfoResourceHandler(endpoints)
    
    async def handle_resource(self, uri: str) -> Dict[str, Any]:
        """
        根據 URI scheme 路由到對應的處理器
        
        Args:
            uri: Resource URI
            
        Returns:
            資源內容字典
            
        Raises:
            ResourceError: 不支援的 URI scheme
        """
        # 確保 uri 是字串（可能從 MCP SDK 傳入 AnyUrl 物件）
        uri_str = str(uri)
        parsed = urlparse(uri_str)
        scheme = parsed.scheme
        
        if scheme == "bible":
            # urlparse 將 verse/chapter 視為 netloc
            # 所以需要檢查 netloc 而不是 path
            resource_type = parsed.netloc
            if resource_type == "verse":
                return await self.bible_handler.handle_verse(uri_str)
            elif resource_type == "chapter":
                return await self.bible_handler.handle_chapter(uri_str)
            else:
                raise ResourceError(
                    f"不支援的 bible:// 資源類型: {resource_type}。支援的類型: verse, chapter"
                )
        elif scheme == "strongs":
            return await self.strongs_handler.handle(uri_str)
        elif scheme == "commentary":
            return await self.commentary_handler.handle(uri_str)
        elif scheme == "info":
            return await self.info_handler.handle(uri_str)
        else:
            raise ResourceError(
                f"不支援的 URI scheme: {scheme}。支援的 scheme: bible, strongs, commentary, info"
            )
    
    def list_supported_resources(self) -> Dict[str, list]:
        """
        列出所有支援的 Resource URI 格式
        
        Returns:
            按類別分組的 URI 格式列表
        """
        return {
            "bible": [
                {
                    "uri": "bible://verse/{version}/{book}/{chapter}/{verse}",
                    "description": "查詢指定經文",
                    "example": "bible://verse/unv/John/3/16"
                },
                {
                    "uri": "bible://chapter/{version}/{book}/{chapter}",
                    "description": "查詢整章經文",
                    "example": "bible://chapter/unv/Gen/1"
                }
            ],
            "strongs": [
                {
                    "uri": "strongs://{testament}/{number}",
                    "description": "查詢 Strong's 原文字典",
                    "example": "strongs://nt/25"
                }
            ],
            "commentary": [
                {
                    "uri": "commentary://{book}/{chapter}/{verse}",
                    "description": "查詢經文註釋",
                    "example": "commentary://John/3/16"
                }
            ],
            "info": [
                {
                    "uri": "info://versions",
                    "description": "列出所有聖經版本",
                    "example": "info://versions"
                },
                {
                    "uri": "info://books",
                    "description": "列出所有書卷",
                    "example": "info://books"
                },
                {
                    "uri": "info://commentaries",
                    "description": "列出所有註釋書",
                    "example": "info://commentaries"
                }
            ]
        }
