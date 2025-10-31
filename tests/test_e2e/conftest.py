"""
E2E 測試的 pytest fixtures 和設定
"""
import sys
import pytest
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, 'src')

from fhl_bible_mcp.server import FHLBibleServer


@pytest.fixture
async def mcp_server():
    """創建 MCP Server 實例用於測試"""
    # 創建 server 實例
    server = FHLBibleServer()
    yield server
    
    # 清理
    if hasattr(server, 'endpoints') and hasattr(server.endpoints, 'client'):
        await server.endpoints.client.close()


@pytest.fixture
def mock_api_response():
    """創建模擬的 API 響應"""
    def _create_response(data: dict[str, Any], status_code: int = 200):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = data
        mock_response.text = str(data)
        return mock_response
    
    return _create_response


@pytest.fixture
def sample_verse_response():
    """範例經文 API 響應"""
    return {
        "status": "success",
        "record_count": 1,
        "v_name": "FHL和合本",
        "version": "unv",
        "proc": 0,
        "record": [{
            "engs": "John",
            "chineses": "約",
            "chap": 3,
            "sec": 16,
            "bible_text": "「　神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不致滅亡，反得永生。"
        }],
        "prev": {"chineses": "約", "engs": "John", "chap": 3, "sec": 15},
        "next": {"chineses": "約", "engs": "John", "chap": 3, "sec": 17}
    }


@pytest.fixture
def sample_search_response():
    """範例搜尋 API 響應"""
    return {
        "status": "success",
        "record_count": 3,
        "orig": 0,
        "key": "愛",
        "record": [
            {
                "id": 1,
                "engs": "Gen",
                "chineses": "創",
                "chap": 22,
                "sec": 2,
                "bible_text": "　神說：「你帶著你的兒子，就是你獨生的兒子，你所愛的以撒..."
            },
            {
                "id": 2,
                "engs": "Gen",
                "chineses": "創",
                "chap": 24,
                "sec": 67,
                "bible_text": "以撒便領利百加進了他母親撒拉的帳棚，娶了她為妻，並且愛她..."
            },
            {
                "id": 3,
                "engs": "John",
                "chineses": "約",
                "chap": 3,
                "sec": 16,
                "bible_text": "「　神愛世人，甚至將他的獨生子賜給他們..."
            }
        ]
    }


@pytest.fixture
def sample_versions_response():
    """範例版本列表 API 響應"""
    return {
        "status": "success",
        "record_count": 3,
        "record": [
            {
                "book": "unv",
                "cname": "FHL和合本",
                "proc": 0,
                "strong": 1,
                "ntonly": 0,
                "otonly": 0,
                "candownload": 1,
                "version": "20231201"
            },
            {
                "book": "nstrunv",
                "cname": "新標點和合本",
                "proc": 0,
                "strong": 1,
                "ntonly": 0,
                "otonly": 0,
                "candownload": 1,
                "version": "20231201"
            },
            {
                "book": "kjv",
                "cname": "KJV",
                "proc": 0,
                "strong": 0,
                "ntonly": 0,
                "otonly": 0,
                "candownload": 0,
                "version": "20231201"
            }
        ]
    }


@pytest.fixture
def sample_strongs_response():
    """範例 Strong's 字典 API 響應"""
    return {
        "status": "success",
        "record_count": 1,
        "record": [{
            "sn": "00025",
            "dic_text": "25 agapao {ag-ap-ah'-o}\n\n可能源自 agan (多)；TDNT - 1:21,5；動詞\n\nAV - love 135, beloved 7; 142\n\n1) 屬神聖性質的愛，是無條件的愛",
            "edic_text": "25 agapao {ag-ap-ah'-o}\n\nperhaps from agan (much)...",
            "dic_type": 0,
            "orig": "ἀγαπάω",
            "same": [
                {
                    "word": "ἀγαπάω",
                    "csn": "00025",
                    "ccnt": "143",
                    "cexp": "愛；表明或證明一個人的愛"
                }
            ]
        }]
    }
