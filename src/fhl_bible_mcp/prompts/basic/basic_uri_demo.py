"""
FHL Bible MCP Server - URI Demo Prompt

提供完整的 URI 使用教學和互動示範
"""

from ..base import PromptTemplate


class BasicURIDemoPrompt(PromptTemplate):
    """基礎 - URI 使用示範 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="basic_uri_demo",
            description="展示和教導如何使用各種 Resource URI，包含互動式範例和最佳實踐",
            arguments=[
                {
                    "name": "uri_type",
                    "description": "URI 類型 (bible/strongs/commentary/info/all)",
                    "required": False
                }
            ]
        )
    
    def render(self, uri_type: str = "all") -> str:
        """渲染 URI 使用示範的 prompt"""
        return f"""# Resource URI 示範 ({uri_type})

## 步驟 1: 解釋 URI
**執行**: 說明 URI 是什麼及其用途
**輸出**: URI 類似網址，用於快速訪問聖經資源

## 步驟 2: 列出 URI 類型
**執行**: 展示4種 URI 格式
- bible://[type]/[version]/[book]/[chapter]/[verse]
- strongs://[testament]/[number]
- commentary://[id]/[book]/[chapter]/[verse]
- info://[type]
**輸出**: URI 格式清單

## 步驟 3: 提供範例
**執行**: 展示實際可用的 URI
- bible://verse/unv/John/3/16
- strongs://nt/26
- commentary://1/John/3/16
- info://versions
**輸出**: 可點擊的 URI 連結

## 步驟 4: 示範應用
**執行**: 展示 URI 的實際使用場景
**輸出**: 組合使用案例
"""
