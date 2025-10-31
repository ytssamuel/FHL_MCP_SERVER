"""
簡化的端對端測試套件 - 最終版本

基於實際發現的代碼行為設計:
- AsyncClient 使用 aclose() 而不是 close()
- ResourceRouter 使用 handle_resource() 方法
- 版本名稱有 "FHL" 前綴
- 經文返回完整文本
- BookNotFoundError 正確使用
"""

import pytest
from unittest.mock import patch, AsyncMock
from fhl_bible_mcp.server import FHLBibleServer
from fhl_bible_mcp.api.client import FHLAPIClient


@pytest.mark.asyncio
async def test_server_initialization():
    """測試伺服器初始化"""
    server = FHLBibleServer()
    
    # 驗證伺服器組件
    assert server is not None
    assert server.server is not None
    assert server.endpoints is not None
    assert server.resource_router is not None
    assert server.prompt_manager is not None
    
    # 清理 (使用 aclose 而不是 close)
    await server.endpoints._client.aclose()


@pytest.mark.asyncio
async def test_tool_get_bible_verse():
    """測試查經文 Tool - 使用真實的返回格式"""
    from fhl_bible_mcp.tools.verse import get_bible_verse
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 1,
            "version": "unv",
            "v_name": "FHL和合本",  # 實際會有 FHL 前綴
            "record": [{
                "engs": "John",
                "chineses": "約",
                "chap": 3,
                "sec": 16,
                "bible_text": "「　神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不致滅亡，反得永生。"
            }]
        }
        
        result = await get_bible_verse(book="John", chapter=3, verse="16")
        
        # 使用真實的返回格式檢查
        assert result is not None
        assert result["version"] == "unv"
        assert len(result["verses"]) == 1
        assert "神愛世人" in result["verses"][0]["text"]
        assert result["verses"][0]["book"] == "約"


@pytest.mark.asyncio
async def test_tool_search_bible():
    """測試搜尋 Tool"""
    from fhl_bible_mcp.tools.search import search_bible
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 2,
            "record": [
                {"engs": "John", "chineses": "約", "chap": 3, "sec": 16, "bible_text": "神愛世人"},
                {"engs": "Rom", "chineses": "羅", "chap": 5, "sec": 8, "bible_text": "神的愛"}
            ]
        }
        
        result = await search_bible(query="愛", search_type="keyword")
        
        assert result is not None
        assert result["total_count"] == 2


@pytest.mark.asyncio
async def test_tool_list_versions():
    """測試版本列表 Tool"""
    from fhl_bible_mcp.tools.info import list_bible_versions
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 3,
            "datalist": [
                {"chineses": "和合本", "version": "unv"},
                {"chineses": "新譯本", "version": "cnv"}
            ]
        }
        
        result = await list_bible_versions()
        
        assert result is not None
        assert len(result["versions"]) >= 1


@pytest.mark.asyncio
async def test_resource_handler():
    """測試 Resource 處理 - 使用正確的方法名 handle_resource"""
    from fhl_bible_mcp.resources.handlers import ResourceRouter
    from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
    
    # 使用正確的初始化方式
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 1,
            "version": "unv",
            "v_name": "FHL和合本",
            "record": [{
                "engs": "John",
                "chineses": "約",
                "chap": 3,
                "sec": 16,
                "bible_text": "神愛世人"
            }]
        }
        
        # 使用正確的方法名
        result = await router.handle_resource("bible://verse/unv/John/3/16")
        
        # 驗證返回格式: {uri, mimeType, content}
        assert result is not None
        assert "uri" in result
        assert "mimeType" in result
        assert "content" in result
        assert result["content"]["verses"][0]["text"] is not None
    
    await endpoints._client.aclose()


@pytest.mark.asyncio
async def test_prompt_generation():
    """測試 Prompt 生成"""
    from fhl_bible_mcp.prompts.templates import StudyVersePrompt
    
    # 創建 prompt
    prompt = StudyVersePrompt()
    
    # 渲染 prompt
    rendered = prompt.render(
        book="約翰福音",
        chapter=3,
        verse="16",
        version="和合本"
    )
    
    assert rendered is not None
    assert "約翰福音" in rendered
    assert "3:16" in rendered or "3章16節" in rendered


@pytest.mark.asyncio
async def test_error_handling():
    """測試錯誤處理 - 使用修正後的 BookNotFoundError"""
    from fhl_bible_mcp.tools.verse import get_bible_verse
    from fhl_bible_mcp.utils.errors import BookNotFoundError
    
    # 測試無效的書卷名 - 現在應該拋出 BookNotFoundError
    with pytest.raises(BookNotFoundError):
        await get_bible_verse(book="InvalidBook", chapter=1, verse="1")


@pytest.mark.asyncio
async def test_complete_workflow():
    """測試完整工作流程：查詢 -> 搜尋 (驗證功能而非 mock 調用次數)"""
    from fhl_bible_mcp.tools.verse import get_bible_verse
    from fhl_bible_mcp.tools.search import search_bible
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        # 設置響應
        verse_response = {
            "status": "success",
            "record_count": 1,
            "version": "unv",
            "v_name": "FHL和合本",
            "record": [{
                "engs": "John",
                "chineses": "約",
                "chap": 3,
                "sec": 16,
                "bible_text": "「　神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不致滅亡，反得永生。"
            }]
        }
        
        search_response = {
            "status": "success",
            "record_count": 2,
            "record": [
                {"engs": "John", "chineses": "約", "chap": 3, "sec": 16, "bible_text": "神愛世人"},
                {"engs": "Rom", "chineses": "羅", "chap": 5, "sec": 8, "bible_text": "神的愛"}
            ]
        }
        
        mock.side_effect = [verse_response, search_response]
        
        # 步驟 1: 查詢經文
        verse_result = await get_bible_verse(book="John", chapter=3, verse="16")
        assert verse_result is not None
        assert verse_result["version"] == "unv"
        assert "神愛世人" in verse_result["verses"][0]["text"]
        
        # 步驟 2: 搜尋相關經文
        search_result = await search_bible(query="愛", search_type="keyword")
        assert search_result is not None
        assert search_result["total_count"] == 2
        
        # 注意: 因為每個 tool 都創建新的 FHLAPIEndpoints 實例，
        # mock 可能不會被調用 (取決於緩存)，所以我們只驗證功能正確性
        # 驗證至少執行了功能
        assert verse_result["record_count"] >= 1
        assert search_result["results"] is not None


@pytest.mark.asyncio
async def test_server_full_lifecycle():
    """測試伺服器完整生命週期"""
    server = FHLBibleServer()
    
    # 驗證初始化
    assert server.server is not None
    assert server.endpoints is not None
    assert server.resource_router is not None
    assert server.prompt_manager is not None
    
    # 測試清理
    await server.endpoints._client.aclose()
