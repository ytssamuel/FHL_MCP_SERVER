"""
Advanced Character Study Prompt

聖經人物研究對話範本
全面研究聖經中的人物，包含生平、性格、事蹟、屬靈教訓
"""

from dataclasses import dataclass
from typing import Optional
from ..base import PromptTemplate


@dataclass
class AdvancedCharacterStudyPrompt(PromptTemplate):
    """聖經人物研究對話範本
    
    全面研究聖經人物的生平、性格、事蹟和屬靈教訓。
    適用於個人靈修、主日學教學、講道準備。
    """
    
    def __init__(
        self,
        character: str = "Peter",
        focus: str = "all",
        testament: str = "both",
        version: str = "unv"
    ):
        """初始化聖經人物研究 Prompt
        
        Args:
            character: 人物名稱（如 "Peter", "Paul", "David"）
            focus: 研究焦點 (all/biography/character/lessons)
            testament: 約別限制 (OT/NT/both)
            version: 聖經版本（預設：unv）
        """
        super().__init__(
            name="advanced_character_study",
            description="全面研究聖經人物，包含生平、性格、事蹟、屬靈教訓",
            arguments=[
                {"name": "character", "description": "人物名稱", "required": False},
                {"name": "focus", "description": "研究焦點 (all/biography/character/lessons)", "required": False},
                {"name": "testament", "description": "約別限制 (OT/NT/both)", "required": False},
                {"name": "version", "description": "聖經版本", "required": False}
            ]
        )
        self.character = character
        self.focus = focus
        self.testament = testament
        self.version = version
    
    def render(
        self,
        character: str = None,
        focus: str = None,
        testament: str = None,
        version: str = None
    ) -> str:
        """渲染聖經人物研究指引"""
        # 使用傳入的參數或初始化時的值
        char = character or self.character
        foc = focus or self.focus
        test = testament or self.testament
        ver = version or self.version
        
        focus_map = {
            "all": "全面研究", "biography": "生平事蹟",
            "character": "性格分析", "lessons": "屬靈教訓"
        }
        testament_map = {"OT": "舊約", "NT": "新約", "both": "新舊約"}
        
        return f"""# 聖經人物研究 - {char}

**研究焦點**: {focus_map.get(foc, '全面研究')}
**範圍**: {testament_map.get(test, '新舊約')}
**版本**: {ver}

## 步驟 1: 搜尋人物經文
**執行**: 找出所有與此人物相關的經文
- 搜尋人物名稱 (search_bible)
- 記錄出現章節
**輸出**: 經文位置清單及主要事件

## 步驟 2: 建立生平時間線
**執行**: 按時間順序整理重要事件
- 出生背景與家庭
- 關鍵轉折點（3-5個）
- 主要成就與失敗
**輸出**: 時間線圖表與事件摘要

## 步驟 3: 分析性格特質
**執行**: 從經文中觀察人物性格
- 優點（信心、勇氣、智慧等）
- 缺點（軟弱、驕傲、懷疑等）
- 成長軌跡
**輸出**: 性格優缺點及經文依據

## 步驟 4: 識別關係網絡
**執行**: 分析人物的重要關係
- 與神的關係
- 與家人的關係
- 與同工的關係
**輸出**: 關係圖與互動模式

## 步驟 5: 提煉屬靈教訓
**執行**: 從人物生命中學習功課
- 正面榜樣（值得效法）
- 負面警戒（應當避免）
- 神的工作（恩典與管教）
**輸出**: 3-5個核心教訓

## 步驟 6: 應用於今日
**執行**: 將教訓應用到現代生活
- 信仰層面的啟發
- 品格塑造的方向
- 具體實踐的行動
**輸出**: 個人應用計畫

## 步驟 7: 深入原文研究（可選）
**執行**: 研究關鍵經文的原文
- 重要事件經文的原文分析 (get_word_analysis)
- 關鍵字詞的 Strong's 研究 (lookup_strongs)
**輸出**: 原文洞見與更深理解

💡 **研究提示**:
- biography焦點: 著重步驟1、2、4
- character焦點: 著重步驟3、5
- lessons焦點: 著重步驟5、6

📚 **延伸工具**: 
- get_commentary: 查看註釋家的分析
- search_topic: 研究相關主題
- study_verse_deep: 深入關鍵經節
"""
