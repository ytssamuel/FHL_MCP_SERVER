"""
FHL Bible MCP Server - Reading Passage Prompt

段落讀經輔助，針對跨章節經文段落的深入研讀
"""

from ..base import PromptTemplate


class ReadingPassagePrompt(PromptTemplate):
    """讀經 - 段落讀經輔助 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="reading_passage",
            description="閱讀和分析一段經文（可能跨越多個章節），包含背景、主題、解經和應用",
            arguments=[
                {
                    "name": "book",
                    "description": "經卷名稱（中文或英文）",
                    "required": True
                },
                {
                    "name": "start_chapter",
                    "description": "起始章",
                    "required": True
                },
                {
                    "name": "start_verse",
                    "description": "起始節",
                    "required": True
                },
                {
                    "name": "end_chapter",
                    "description": "結束章",
                    "required": True
                },
                {
                    "name": "end_verse",
                    "description": "結束節",
                    "required": True
                },
                {
                    "name": "version",
                    "description": "聖經版本代碼（預設：unv）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        book: str = "約翰福音",
        start_chapter: int = 3,
        start_verse: int = 1,
        end_chapter: int = 3,
        end_verse: int = 21,
        version: str = "unv"
    ) -> str:
        """渲染段落讀經的 prompt"""
        passage_ref = f"{book} {start_chapter}:{start_verse}-{end_chapter}:{end_verse}"
        is_cross_chapter = start_chapter != end_chapter
        
        return f"""# 段落讀經 - {passage_ref}

## 步驟 1: 獲取經文
**執行**: 取得段落完整經文
- 範圍: {book} {start_chapter}:{start_verse} 至 {end_chapter}:{end_verse}
- 版本: {version}
- 跨章: {'是' if is_cross_chapter else '否'}
**輸出**: 完整經文內容

## 步驟 2: 分析背景
**執行**: 了解段落的上下文脈絡
- 查詢前後章節內容
- 識別書卷主題與段落位置
**輸出**: 歷史文化背景、寫作目的

## 步驟 3: 識別主題
**執行**: 找出核心與次要主題
- 標記重複出現的關鍵詞
- 搜尋聖經中相關經文
**輸出**: 主要主題及支持經文

## 步驟 4: 解析重點
**執行**: 深入分析3-5節關鍵經文
- 原文字詞分析 (get_word_analysis)
- Strong's 字典查詢 (lookup_strongs)
**輸出**: 關鍵經節的深度解釋

## 步驟 5: 整理結構
**執行**: 建立段落大綱
- 識別文學體裁（敘事/詩歌/書信等）
- 劃分論證或敘事流程
**輸出**: 結構大綱與邏輯流程

## 步驟 6: 實際應用
**執行**: 將真理轉化為行動
- 檢視信仰、品格、關係、服事
- 制定具體 SMART 行動計畫
**輸出**: 本週實踐目標與禱告回應

💡 可查看註釋: get_commentary(book="{book}", chapter={start_chapter}, verse={start_verse})
📖 延伸研讀: study_verse_deep, study_topic_deep
"""
