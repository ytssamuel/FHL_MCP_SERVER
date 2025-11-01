"""
FHL Bible MCP Server - Devotional Prompt

靈修默想輔助
"""

from ..base import PromptTemplate


class SpecialDevotionalPrompt(PromptTemplate):
    """特殊 - 靈修默想 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_devotional",
            description="引導靈修默想，加深與神的關係",
            arguments=[
                {"name": "passage", "description": "默想經文", "required": False},
                {"name": "theme", "description": "靈修主題", "required": False}
            ]
        )
    
    def render(self, passage: str = None, theme: str = "") -> str:
        """渲染靈修默想的 prompt"""
        passage_text = passage or "今日金句"
        return f"""# 靈修默想 - {passage_text}

**主題**: {theme if theme else '與神相遇'}

## 步驟 1: 安靜預備
**執行**: 預備心靈
- 安靜環境
- 禱告開始
**輸出**: 預備心態

## 步驟 2: 閱讀經文
**執行**: 慢慢讀經文
- 逐字細讀
- 留意感動
**輸出**: 經文印象

## 步驟 3: 默想真理
**執行**: 深入思考
- 神在說什麼？
- 關於神、關於我
**輸出**: 個人領受

## 步驟 4: 省察回應
**執行**: 省察生命
- 需要悔改？
- 需要感恩？
- 需要順服？
**輸出**: 生命回應

## 步驟 5: 禱告交通
**執行**: 與神對話
- 敬拜、認罪、感恩、祈求
**輸出**: 禱告內容

## 步驟 6: 記錄領受
**執行**: 寫下感動
**輸出**: 靈修筆記

💡 建議: 每天15-30分鐘
"""
