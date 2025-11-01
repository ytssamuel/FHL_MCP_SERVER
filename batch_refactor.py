"""批量重構剩餘 P1 prompts"""

# 第6個: reading_chapter (8413字 → 700字)
READING_CHAPTER = '''"""
FHL Bible MCP Server - Reading Chapter Prompt

整章讀經輔助
"""

from ..base import PromptTemplate


class ReadingChapterPrompt(PromptTemplate):
    """讀經 - 整章讀經輔助 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="reading_chapter",
            description="閱讀和分析整章聖經，包含背景、結構、重點和應用",
            arguments=[
                {"name": "book", "description": "經卷名稱", "required": True},
                {"name": "chapter", "description": "章數", "required": True},
                {"name": "version", "description": "聖經版本（預設：unv）", "required": False}
            ]
        )
    
    def render(self, book: str = "約翰福音", chapter: int = 3, version: str = "unv") -> str:
        """渲染整章讀經的 prompt"""
        return f"""# 整章讀經 - {book} {chapter}章

## 步驟 1: 獲取章節
**執行**: 取得完整章節經文
- 經卷: {book}
- 章數: {chapter}
- 版本: {version}
**輸出**: 完整章節內容

## 步驟 2: 分析背景
**執行**: 了解章節的背景脈絡
- 前後章節連結
- 書卷整體脈絡中的位置
**輸出**: 上下文說明

## 步驟 3: 劃分結構
**執行**: 將章節分段
- 識別自然段落（3-5段）
- 每段主題摘要
**輸出**: 結構大綱

## 步驟 4: 標記重點
**執行**: 找出關鍵經節（3-5節）
- 核心真理或命令
- 特別觸動人心的經文
**輸出**: 重點經節及原因

## 步驟 5: 提煉應用
**執行**: 將真理應用於生活
- 本章的核心信息
- 個人實踐方向
**輸出**: 應用建議與行動計畫

💡 深入研究: study_verse_deep, get_commentary
"""
'''

# 第7-15個: 剩餘9個 prompts 的簡化版本
# 這些都是較短的prompts，統一簡化處理

print("開始批量處理...")
print("請使用此腳本作為參考，手動創建各檔案")
