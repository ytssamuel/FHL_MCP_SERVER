"""
FHL Bible MCP Server - Help Guide Prompt

提供完整的使用指南和快速入門教學
"""

from ..base import PromptTemplate


class BasicHelpGuidePrompt(PromptTemplate):
    """基礎 - 使用指南 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="basic_help_guide",
            description="顯示 FHL Bible MCP Server 的完整使用指南，包含快速入門、工具說明和實用技巧",
            arguments=[
                {
                    "name": "section",
                    "description": "指南章節 (all/quickstart/tools/resources/prompts/tips)",
                    "required": False
                }
            ]
        )
    
    def render(self, section: str = "all") -> str:
        """渲染使用指南的 prompt"""
        return f"""# 使用指南 ({section})

## 步驟 1: 介紹功能
**執行**: 說明 FHL Bible MCP Server 主要功能
**輸出**: 經文查詢、原文研究、註釋查閱簡介

## 步驟 2: 列出工具
**執行**: 展示6類工具
- 經文: get_bible_verse, get_bible_chapter
- 搜尋: search_bible
- 原文: lookup_strongs
- 註釋: get_commentary
- 資訊: list_bible_versions
**輸出**: 工具清單

## 步驟 3: 說明 Prompts
**執行**: 介紹提示詞範本
- 基礎/讀經/研經/進階/特殊類
**輸出**: Prompt 類別與用途

## 步驟 4: 提供技巧
**執行**: 分享使用建議
**輸出**: 組合使用、URI 快速訪問

💡 詳情: tool_reference / uri_demo
"""
