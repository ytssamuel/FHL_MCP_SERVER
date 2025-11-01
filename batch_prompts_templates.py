"""
批量生成剩餘9個P1 prompts的簡化版本
"""

# 定義9個prompts的簡化模板
PROMPTS = {
    # 7. special_topical_chain (7493字 → 900字)
    "special_topical_chain": {
        "path": "src/fhl_bible_mcp/prompts/special/special_topical_chain.py",
        "target": 900,
        "content": '''"""
FHL Bible MCP Server - Topical Chain Prompt

主題經文串連研究
"""

from ..base import PromptTemplate


class SpecialTopicalChainPrompt(PromptTemplate):
    """特殊 - 主題經文串連 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="special_topical_chain",
            description="追蹤特定主題在聖經中的發展脈絡，建立主題經文鏈",
            arguments=[
                {"name": "topic", "description": "研究主題", "required": True},
                {"name": "testament", "description": "約別限制 (OT/NT/both)", "required": False}
            ]
        )
    
    def render(self, topic: str = "信心", testament: str = "both") -> str:
        """渲染主題串連的 prompt"""
        return f"""# 主題經文串連 - {topic}

## 步驟 1: 搜尋主題經文
**執行**: 找出所有與主題相關的經文
- 搜尋範圍: {testament}
- 主題: {topic}
**輸出**: 經文清單與出現次數

## 步驟 2: 建立時間線
**執行**: 按聖經順序排列經文
- 舊約 → 新約發展
- 標記關鍵轉折點
**輸出**: 時間線圖表

## 步驟 3: 分析主題發展
**執行**: 觀察主題如何演進
- 初次出現與背景
- 逐步深化過程
- 高峰與完全揭示
**輸出**: 發展階段分析

## 步驟 4: 識別關鍵經文
**執行**: 找出5-10節核心經文
- 定義性經文
- 轉折性經文
- 總結性經文
**輸出**: 關鍵經文列表

## 步驟 5: 建立經文鏈
**執行**: 串連相關經文
- 直接引用關係
- 主題呼應關係
- 對比關係
**輸出**: 經文串連圖

## 步驟 6: 提煉神學洞見
**執行**: 總結主題的聖經神學
- 核心教導
- 實踐應用
**輸出**: 神學摘要與應用

💡 工具: search_bible, study_topic_deep
"""
'''
    },
    
    # 8. advanced_parallel_gospels (6536字 → 1000字)
    "advanced_parallel_gospels": {
        "path": "src/fhl_bible_mcp/prompts/advanced/advanced_parallel_gospels.py",
        "target": 1000,
        "content": '''"""
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
- 馬太福音: [章:節]
- 馬可福音: [章:節]
- 路加福音: [章:節]
- 約翰福音: [章:節]
**輸出**: 平行經文對照表

## 步驟 2: 比較內容異同
**執行**: 逐節對比分析
- 共同記載的內容
- 獨特的細節
- 順序差異
**輸出**: 異同對照表

## 步驟 3: 分析作者視角
**執行**: 理解各作者的神學強調
- 馬太: 君王視角
- 馬可: 僕人視角
- 路加: 人子視角
- 約翰: 神子視角
**輸出**: 作者特色分析

## 步驟 4: 識別獨特內容
**執行**: 找出各福音書的特殊記載
- 僅出現在某福音的內容
- 特殊強調的部分
**輸出**: 獨特性分析

## 步驟 5: 綜合神學意義
**執行**: 整合四福音的見證
- 互補的真理
- 完整的圖像
**輸出**: 綜合神學洞見

## 步驟 6: 實際應用
**執行**: 從多角度認識真理
- 全面理解
- 個人回應
**輸出**: 應用建議

💡 工具: get_bible_verse, study_translation_compare
"""
'''
    },
    
    # 9. special_sermon_prep (5997字 → 900字)
    "special_sermon_prep": {
        "path": "src/fhl_bible_mcp/prompts/special/special_sermon_prep.py",
        "target": 900,
        "content": '''"""
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
                {"name": "sermon_type", "description": "講道類型 (expository/topical/narrative)", "required": False}
            ]
        )
    
    def render(self, passage: str = "約翰福音 3:16", sermon_type: str = "expository") -> str:
        """渲染講道準備的 prompt"""
        return f"""# 講道準備 - {passage}

**類型**: {sermon_type}

## 步驟 1: 研讀經文
**執行**: 深入理解經文
- 獲取經文內容
- 查閱註釋
- 原文分析
**輸出**: 釋經基礎

## 步驟 2: 找出大綱
**執行**: 建立講章結構
- 識別經文自然段落
- 提煉主要論點 (3-5點)
- 安排邏輯流程
**輸出**: 講道大綱

## 步驟 3: 發展內容
**執行**: 充實各論點
- 解釋經文意義
- 提供相關經文支持
- 加入例證說明
**輸出**: 講道內容草稿

## 步驟 4: 連結應用
**執行**: 將真理應用到生活
- 個人層面應用
- 群體層面應用
- 具體行動建議
**輸出**: 應用部分

## 步驟 5: 設計引言與結語
**執行**: 完善講道框架
- 引言: 吸引注意
- 結語: 呼召回應
**輸出**: 完整講章

## 步驟 6: 準備輔助材料
**執行**: 準備投影片與講義
- 關鍵經文投影
- 大綱講義
**輸出**: 輔助材料清單

💡 工具: study_verse_deep, get_commentary, search_bible
"""
'''
    },
}

print("已生成9個prompts的模板")
print("接下來將逐個創建檔案...")
