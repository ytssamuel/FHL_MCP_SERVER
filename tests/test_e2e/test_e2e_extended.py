"""
擴展的 E2E 測試 - 提升覆蓋率

針對以下模組增加覆蓋率:
- server.py: 34% -> 目標 60%+
- resources/handlers.py: 44% -> 目標 60%+
"""

import pytest
from unittest.mock import patch, AsyncMock
from fhl_bible_mcp.server import FHLBibleServer
from fhl_bible_mcp.api.client import FHLAPIClient


@pytest.mark.asyncio
async def test_server_list_resources():
    """測試 Server 列出所有 Resources"""
    server = FHLBibleServer()
    
    # 測試 resource_router 的 list_supported_resources
    resources = server.resource_router.list_supported_resources()
    
    assert resources is not None
    assert "bible" in resources
    assert "strongs" in resources
    assert "commentary" in resources
    assert "info" in resources
    
    # 驗證 bible 資源格式
    assert len(resources["bible"]) >= 2  # verse 和 chapter
    assert any("verse" in str(r["uri"]) for r in resources["bible"])
    assert any("chapter" in str(r["uri"]) for r in resources["bible"])
    
    await server.endpoints._client.aclose()


@pytest.mark.asyncio
async def test_resource_bible_chapter():
    """測試 Resource - 整章經文"""
    from fhl_bible_mcp.resources.handlers import ResourceRouter
    from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 2,
            "version": "unv",
            "v_name": "FHL和合本",
            "record": [
                {"engs": "Gen", "chineses": "創", "chap": 1, "sec": 1, "bible_text": "起初..."},
                {"engs": "Gen", "chineses": "創", "chap": 1, "sec": 2, "bible_text": "地是..."}
            ]
        }
        
        # 測試整章 URI
        result = await router.handle_resource("bible://chapter/unv/Gen/1")
        
        assert result is not None
        assert "content" in result
        assert result["content"]["record_count"] >= 1
    
    await endpoints._client.aclose()


@pytest.mark.skip(reason="lookup_strongs 需要複雜的 mock 設置，已由 API 測試覆蓋")
@pytest.mark.asyncio
async def test_resource_strongs():
    """測試 Resource - Strong's 字典"""
    pass


@pytest.mark.asyncio
async def test_resource_info_versions():
    """測試 Resource - 版本資訊"""
    from fhl_bible_mcp.resources.handlers import ResourceRouter
    from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "datalist": [
                {"chineses": "和合本", "version": "unv"},
                {"chineses": "新譯本", "version": "cnv"}
            ]
        }
        
        # 測試 info:// URI
        result = await router.handle_resource("info://versions")
        
        assert result is not None
        assert "content" in result
        assert "versions" in result["content"]
    
    await endpoints._client.aclose()


@pytest.mark.asyncio
async def test_resource_info_books():
    """測試 Resource - 書卷資訊"""
    from fhl_bible_mcp.resources.handlers import ResourceRouter
    from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "books": [
                {"chinese": "創世記", "english": "Genesis", "short": "創"}
            ]
        }
        
        # 測試書卷列表 URI
        result = await router.handle_resource("info://books")
        
        assert result is not None
        assert "content" in result
    
    await endpoints._client.aclose()


@pytest.mark.asyncio
async def test_resource_error_invalid_scheme():
    """測試 Resource - 無效的 URI scheme"""
    from fhl_bible_mcp.resources.handlers import ResourceRouter, ResourceError
    from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    # 測試無效的 scheme
    with pytest.raises(ResourceError) as exc_info:
        await router.handle_resource("invalid://test")
    
    assert "不支援的 URI scheme" in str(exc_info.value)
    
    await endpoints._client.aclose()


@pytest.mark.asyncio
async def test_resource_error_invalid_bible_type():
    """測試 Resource - 無效的 bible 資源類型"""
    from fhl_bible_mcp.resources.handlers import ResourceRouter, ResourceError
    from fhl_bible_mcp.api.endpoints import FHLAPIEndpoints
    
    endpoints = FHLAPIEndpoints()
    router = ResourceRouter(endpoints)
    
    # 測試無效的 bible 類型
    with pytest.raises(ResourceError) as exc_info:
        await router.handle_resource("bible://invalid/unv/John/3/16")
    
    assert "不支援的 bible:// 資源類型" in str(exc_info.value)
    
    await endpoints._client.aclose()


@pytest.mark.asyncio
async def test_prompts_study_verse():
    """測試 Prompt - 研讀經文"""
    from fhl_bible_mcp.prompts.templates import StudyVersePrompt
    
    prompt = StudyVersePrompt()
    
    # 測試基本渲染 (使用正確的參數類型)
    result = prompt.render(
        book="約翰福音",
        chapter=3,
        verse=16,  # int 而非 str
        version="unv"
    )
    
    assert result is not None
    assert "約翰福音" in result
    assert "3:16" in result or "3章16節" in result


@pytest.mark.asyncio
async def test_prompts_search_topic():
    """測試 Prompt - 主題搜尋"""
    from fhl_bible_mcp.prompts.templates import SearchTopicPrompt
    
    prompt = SearchTopicPrompt()
    
    result = prompt.render(
        topic="愛",
        version="unv",
        max_verses=10
    )
    
    assert result is not None
    assert "愛" in result


@pytest.mark.asyncio
async def test_prompts_compare_translations():
    """測試 Prompt - 版本比較"""
    from fhl_bible_mcp.prompts.templates import CompareTranslationsPrompt
    
    prompt = CompareTranslationsPrompt()
    
    result = prompt.render(
        book="約翰福音",
        chapter=3,
        verse=16,  # int
        versions="unv,cnv"  # 使用版本代碼而非中文名，逗號分隔
    )
    
    assert result is not None
    assert "約翰福音" in result


@pytest.mark.asyncio
async def test_prompts_word_study():
    """測試 Prompt - 原文字詞研究"""
    from fhl_bible_mcp.prompts.templates import WordStudyPrompt
    
    prompt = WordStudyPrompt()
    
    result = prompt.render(
        strongs_number="25",  # Strong's 編號
        testament="nt",
        max_occurrences=20
    )
    
    assert result is not None
    assert "25" in result


@pytest.mark.asyncio
async def test_tool_get_bible_chapter():
    """測試 Tool - 查詢整章"""
    from fhl_bible_mcp.tools.verse import get_bible_chapter
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 6,  # 詩篇 23 篇有 6 節
            "version": "unv",
            "v_name": "FHL和合本",
            "record": [
                {"engs": "Ps", "chineses": "詩", "chap": 23, "sec": i, "bible_text": f"第{i}節"}
                for i in range(1, 7)
            ]
        }
        
        result = await get_bible_chapter(book="Ps", chapter=23)
        
        assert result is not None
        assert result["record_count"] == 6
        assert len(result["verses"]) == 6


@pytest.mark.asyncio
async def test_tool_query_verse_citation():
    """測試 Tool - 經文引用查詢"""
    from fhl_bible_mcp.tools.verse import query_verse_citation
    
    with patch.object(FHLAPIClient, '_make_request', new_callable=AsyncMock) as mock:
        mock.return_value = {
            "status": "success",
            "record_count": 1,
            "version": "unv",
            "v_name": "FHL和合本",
            "record": [{
                "engs": "Matt",
                "chineses": "太",
                "chap": 5,
                "sec": 3,
                "bible_text": "虛心的人有福了"
            }]
        }
        
        result = await query_verse_citation(citation="太 5:3")
        
        assert result is not None
        assert result["verses"][0]["chapter"] == 5
        assert result["verses"][0]["verse"] == 3


@pytest.mark.asyncio
async def test_error_invalid_citation_format():
    """測試錯誤 - 無效的經文引用格式"""
    from fhl_bible_mcp.tools.verse import query_verse_citation
    from fhl_bible_mcp.utils.errors import InvalidParameterError
    
    with pytest.raises(InvalidParameterError):
        await query_verse_citation(citation="invalid format")
