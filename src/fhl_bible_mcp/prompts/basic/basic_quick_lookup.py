"""
FHL Bible MCP Server - Quick Lookup Prompt

快速經文查詢
"""

from ..base import PromptTemplate


class BasicQuickLookupPrompt(PromptTemplate):
    """基礎 - 快速查詢 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="basic_quick_lookup",
            description="快速查詢聖經經文，簡單直接",
            arguments=[
                {"name": "query", "description": "查詢內容", "required": True}
            ]
        )
    
    def render(self, query: str = "約翰福音 3:16") -> str:
        """渲染快速查詢的 prompt"""
        return f"""# 快速查詢

**查詢**: {query}

## 步驟 1: 解析查詢
**執行**: 理解查詢意圖
- 經文引用？關鍵字？主題？
**輸出**: 查詢類型

## 步驟 2: 執行查詢
**執行**: 使用適當工具
- 經文: get_bible_verse
- 關鍵字: search_bible
- 主題: 組合搜尋
**輸出**: 查詢結果

## 步驟 3: 顯示結果
**執行**: 清晰呈現結果
**輸出**: 經文內容或搜尋結果

💡 支援: 經文引用、關鍵字搜尋、主題查詢
"""
