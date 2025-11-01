"""快速批量重構剩餘8個prompts"""
import os
import shutil

BASE_PATH = "c:/Users/USER/Desktop/develope/FHL_MCP_SERVER/src/fhl_bible_mcp/prompts"

# 8-15號 prompts
PROMPTS = [
    # 8. advanced_parallel_gospels
    ("advanced/advanced_parallel_gospels", '''"""
Advanced Parallel Gospels Prompt

四福音對觀研究
"""

from ..base import PromptTemplate


class AdvancedParallelGospelsPrompt(PromptTemplate):
    """進階 - 四福音對觀研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="advanced_parallel_gospels",
            description="比較四福音書的平行記載，分析異同與神學重點",
            arguments=[
                {"name": "event", "description": "事件名稱", "required": True},
                {"name": "references", "description": "平行經文引用", "required": False}
            ]
        )
    
    def render(self, event: str = "登山寶訓", references: str = "") -> str:
        """渲染四福音對觀的 prompt"""
        return f"""# 四福音對觀 - {event}

## 步驟 1: 找出平行經文
**執行**: 識別四福音中的平行記載
**輸出**: 平行經文對照表

## 步驟 2: 比較內容異同
**執行**: 逐節對比分析
- 共同記載、獨特細節、順序差異
**輸出**: 異同對照表

## 步驟 3: 分析作者視角
**執行**: 理解各作者的神學強調
- 馬太(君王)、馬可(僕人)、路加(人子)、約翰(神子)
**輸出**: 作者特色分析

## 步驟 4: 識別獨特內容
**執行**: 找出各福音書的特殊記載
**輸出**: 獨特性分析

## 步驟 5: 綜合神學意義
**執行**: 整合四福音的見證
**輸出**: 綜合神學洞見

## 步驟 6: 實際應用
**執行**: 從多角度認識真理
**輸出**: 應用建議

💡 工具: get_bible_verse, study_translation_compare
"""
'''
    ),
    
    # 9. special_sermon_prep
    ("special/special_sermon_prep", '''"""
FHL Bible MCP Server - Sermon Prep Prompt

講道準備輔助
"""

from ..base import PromptTemplate


class SpecialSermonPrepPrompt(PromptTemplate):
    """特殊 - 講道準備 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_sermon_prep",
            description="輔助講道準備，從釋經到應用的完整流程",
            arguments=[
                {"name": "passage", "description": "講道經文", "required": True},
                {"name": "sermon_type", "description": "講道類型", "required": False}
            ]
        )
    
    def render(self, passage: str = "約翰福音 3:16", sermon_type: str = "expository") -> str:
        """渲染講道準備的 prompt"""
        return f"""# 講道準備 - {passage} ({sermon_type})

## 步驟 1: 研讀經文
**執行**: 深入理解經文
- 獲取經文、查閱註釋、原文分析
**輸出**: 釋經基礎

## 步驟 2: 找出大綱
**執行**: 建立講章結構 (3-5點)
**輸出**: 講道大綱

## 步驟 3: 發展內容
**執行**: 充實各論點
- 解釋意義、相關經文、例證說明
**輸出**: 講道內容草稿

## 步驟 4: 連結應用
**執行**: 將真理應用到生活
**輸出**: 應用部分

## 步驟 5: 設計引言與結語
**執行**: 完善講道框架
**輸出**: 完整講章

## 步驟 6: 準備輔助材料
**執行**: 準備投影片與講義
**輸出**: 輔助材料清單

💡 工具: study_verse_deep, get_commentary
"""
'''
    ),
    
    # 10. advanced_cross_reference
    ("advanced/advanced_cross_reference", '''"""
Advanced Cross Reference Prompt

交叉引用研究
"""

from ..base import PromptTemplate


class AdvancedCrossReferencePrompt(PromptTemplate):
    """進階 - 交叉引用研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="advanced_cross_reference",
            description="深入研究經文的交叉引用，建立經文網絡",
            arguments=[
                {"name": "reference", "description": "經文引用", "required": True}
            ]
        )
    
    def render(self, reference: str = "約翰福音 3:16") -> str:
        """渲染交叉引用研究的 prompt"""
        return f"""# 交叉引用研究 - {reference}

## 步驟 1: 獲取主經文
**執行**: 取得研究的經文
- 經文: {reference}
**輸出**: 完整經文內容

## 步驟 2: 找直接引用
**執行**: 識別直接引用關係
- 本節引用的舊約經文
- 新約中引用本節的經文
**輸出**: 直接引用清單

## 步驟 3: 找主題相關
**執行**: 搜尋相同主題的經文
- 關鍵字搜尋
- 主題串連
**輸出**: 主題相關經文

## 步驟 4: 找對照經文
**執行**: 找出對比或補充的經文
- 相似教導
- 對立觀點
**輸出**: 對照經文分析

## 步驟 5: 建立經文網絡
**執行**: 繪製經文關係圖
**輸出**: 經文網絡圖

## 步驟 6: 綜合解讀
**執行**: 從多處經文理解真理
**輸出**: 綜合解經

💡 工具: search_bible, get_commentary
"""
'''
    ),
    
    # 11. reading_daily
    ("reading/reading_daily", '''"""
FHL Bible MCP Server - Reading Daily Prompt

每日讀經輔助
"""

from ..base import PromptTemplate


class ReadingDailyPrompt(PromptTemplate):
    """讀經 - 每日讀經輔助 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="reading_daily",
            description="每日靈修讀經指引，包含默想和應用",
            arguments=[
                {"name": "passage", "description": "今日經文", "required": False}
            ]
        )
    
    def render(self, passage: str = None) -> str:
        """渲染每日讀經的 prompt"""
        if not passage:
            passage_text = "取得今日金句 (get_verse_of_day)"
        else:
            passage_text = passage
            
        return f"""# 每日讀經 - {passage_text}

## 步驟 1: 獲取經文
**執行**: 取得今日要讀的經文
**輸出**: 經文內容

## 步驟 2: 初步閱讀
**執行**: 閱讀2-3遍
- 整體印象
- 關鍵字詞
**輸出**: 初步理解

## 步驟 3: 默想經文
**執行**: 深入思考經文意義
- 這段說什麼？
- 對我說什麼？
**輸出**: 個人領受

## 步驟 4: 連結生活
**執行**: 將經文應用到生活
- 今天要學習什麼？
- 今天要做什麼？
**輸出**: 具體行動

## 步驟 5: 禱告回應
**執行**: 用經文禱告
**輸出**: 禱告內容

💡 開始: get_verse_of_day
"""
'''
    ),
    
    # 12. special_bible_trivia
    ("special/special_bible_trivia", '''"""
FHL Bible MCP Server - Bible Trivia Prompt

聖經知識問答
"""

from ..base import PromptTemplate


class SpecialBibleTriviaPrompt(PromptTemplate):
    """特殊 - 聖經知識問答 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_bible_trivia",
            description="生成聖經知識問答題目，適合小組活動或教學",
            arguments=[
                {"name": "category", "description": "問答類別", "required": False},
                {"name": "difficulty", "description": "難度級別", "required": False}
            ]
        )
    
    def render(self, category: str = "all", difficulty: str = "medium") -> str:
        """渲染聖經知識問答的 prompt"""
        return f"""# 聖經知識問答

**類別**: {category}
**難度**: {difficulty}

## 步驟 1: 選擇主題
**執行**: 確定問答範圍
- 人物、地點、事件、教義等
**輸出**: 主題清單

## 步驟 2: 設計問題
**執行**: 創建問答題目 (5-10題)
- 選擇題
- 是非題
- 簡答題
**輸出**: 問題清單

## 步驟 3: 提供答案
**執行**: 給出正確答案及經文依據
**輸出**: 答案與經文引用

## 步驟 4: 加入延伸
**執行**: 提供額外資訊
- 背景說明
- 相關經文
**輸出**: 延伸資料

💡 類別: 人物/地點/事件/教義/書卷
💡 難度: easy/medium/hard
"""
'''
    ),
    
    # 13. special_memory_verse
    ("special/special_memory_verse", '''"""
FHL Bible MCP Server - Memory Verse Prompt

經文背誦輔助
"""

from ..base import PromptTemplate


class SpecialMemoryVersePrompt(PromptTemplate):
    """特殊 - 經文背誦 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_memory_verse",
            description="協助經文背誦，提供記憶技巧和應用提醒",
            arguments=[
                {"name": "verse", "description": "要背誦的經文", "required": True}
            ]
        )
    
    def render(self, verse: str = "約翰福音 3:16") -> str:
        """渲染經文背誦的 prompt"""
        return f"""# 經文背誦 - {verse}

## 步驟 1: 獲取經文
**執行**: 取得完整經文
- 經文: {verse}
**輸出**: 經文內容及引用

## 步驟 2: 理解意義
**執行**: 先理解再背誦
- 經文意思
- 關鍵字詞
**輸出**: 經文解釋

## 步驟 3: 分段記憶
**執行**: 將經文分成小段
- 每段3-5個字
- 逐段記憶
**輸出**: 分段方案

## 步驟 4: 使用技巧
**執行**: 應用記憶法
- 首字記憶法
- 圖像聯想法
- 韻律記憶法
**輸出**: 記憶提示

## 步驟 5: 反覆練習
**執行**: 多次複誦
- 看著背、不看背
- 每日複習
**輸出**: 練習計畫

## 步驟 6: 實際應用
**執行**: 在生活中使用
**輸出**: 應用場景

💡 建議: 每週背誦1-2節
"""
'''
    ),
    
    # 14. special_devotional
    ("special/special_devotional", '''"""
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
'''
    ),
    
    # 15. basic_quick_lookup
    ("basic/basic_quick_lookup", '''"""
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
'''
    ),
]

for path, content in PROMPTS:
    filepath = f"{BASE_PATH}/{path}.py"
    backup = f"{filepath}.bak"
    
    # 備份
    if os.path.exists(filepath):
        shutil.copy(filepath, backup)
    
    # 寫入新內容
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path.split('/')[-1]}")

print(f"\n🎉 完成所有8個prompts的重構！")
