"""
FHL Bible MCP Server - Tool Reference Prompt

提供所有工具的詳細參考手冊
"""

from ..base import PromptTemplate


class BasicToolReferencePrompt(PromptTemplate):
    """基礎 - 工具參考手冊 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="basic_tool_reference",
            description="顯示所有可用工具的詳細參考手冊，包含用法、參數和範例",
            arguments=[
                {
                    "name": "tool_name",
                    "description": "特定工具名稱（可選）",
                    "required": False
                },
                {
                    "name": "category",
                    "description": "工具類別（verse/search/strongs/commentary/info/audio/all）",
                    "required": False
                }
            ]
        )
    
    def render(self, tool_name: str = None, category: str = "all") -> str:
        """渲染工具參考手冊的 prompt"""
        return f"""# 工具參考

## 步驟 1: 列出可用工具
**執行**: 顯示 FHL Bible MCP Server 的所有工具
**輸出**: 工具清單（經文查詢、搜尋、原文、註釋、資訊、音訊類）

## 步驟 2: 查詢工具詳情
**執行**: 根據用戶需求提供具體工具的使用說明
- 工具名稱: {tool_name if tool_name else '所有工具'}
- 類別: {category}
**輸出**: 工具名稱、參數、範例

## 步驟 3: 提供使用範例
**執行**: 展示 1-2 個實際調用範例
**輸出**: 可執行的代碼範例

💡 工具類別: verse/search/strongs/commentary/info/audio
"""
