"""
FHL Bible MCP Server - Prompt Templates

提供預設的對話範本，幫助使用者快速開始聖經研讀。

支援的 Prompts:
- study_verse: 深入研讀經文
- search_topic: 主題研究
- compare_translations: 版本比較
- word_study: 原文字詞研究
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """Prompt 範本基類"""
    name: str
    description: str
    arguments: List[Dict[str, Any]]
    
    def render(self, **kwargs) -> str:
        """
        渲染 prompt 模板
        
        Args:
            **kwargs: 模板參數
            
        Returns:
            渲染後的 prompt 字符串
        """
        raise NotImplementedError


class StudyVersePrompt(PromptTemplate):
    """深入研讀經文 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="study_verse",
            description="深入研讀一節經文，包含經文內容、原文分析、註釋等",
            arguments=[
                {
                    "name": "book",
                    "description": "經卷名稱（中文或英文縮寫）",
                    "required": True
                },
                {
                    "name": "chapter",
                    "description": "章數",
                    "required": True
                },
                {
                    "name": "verse",
                    "description": "節數",
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
        book: str,
        chapter: int,
        verse: int,
        version: str = "unv"
    ) -> str:
        """
        渲染深入研讀經文的 prompt
        
        Args:
            book: 經卷名稱
            chapter: 章數
            verse: 節數
            version: 聖經版本代碼
            
        Returns:
            渲染後的 prompt
        """
        return f"""請幫我深入研讀 {book} {chapter}:{verse}。

請按照以下步驟進行研讀：

1. **經文內容**
   - 使用 get_bible_verse 查詢 {book} {chapter}:{verse} ({version} 版本)
   - 同時獲取包含 Strong's Number 的版本以便原文分析

2. **原文字彙分析**
   - 使用 get_word_analysis 取得該節經文的希臘文/希伯來文分析
   - 列出每個重要字詞的原文、詞性、字型變化

3. **關鍵字詞研究**
   - 針對經文中的關鍵字，使用 lookup_strongs 查詢 Strong's 字典
   - 解釋重要字詞的原文意義、用法、神學含義
   - 列出同源字及其在聖經中的使用

4. **註釋與解經**
   - 使用 get_commentary 查詢該節經文的註釋
   - 綜合不同註釋書的觀點
   - 提供解經要點和應用建議

5. **相關經文連結**
   - 使用 search_bible 搜尋相關主題或關鍵字
   - 列出 3-5 處相關經文供交叉參考

6. **研讀總結**
   - 綜合以上資訊，提供該節經文的：
     * 核心信息
     * 神學意義
     * 實際應用
     * 思考問題

請以結構化、易讀的方式呈現研讀結果。"""


class SearchTopicPrompt(PromptTemplate):
    """主題研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="search_topic",
            description="研究聖經中的特定主題",
            arguments=[
                {
                    "name": "topic",
                    "description": "要研究的主題關鍵字",
                    "required": True
                },
                {
                    "name": "version",
                    "description": "聖經版本代碼（預設：unv）",
                    "required": False
                },
                {
                    "name": "max_verses",
                    "description": "最多顯示的經文數量（預設：10）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        topic: str,
        version: str = "unv",
        max_verses: int = 10
    ) -> str:
        """
        渲染主題研究的 prompt
        
        Args:
            topic: 研究主題
            version: 聖經版本
            max_verses: 最多顯示經文數
            
        Returns:
            渲染後的 prompt
        """
        return f"""請幫我研究聖經中關於「{topic}」的教導。

請按照以下步驟進行主題研究：

1. **經文搜尋**
   - 使用 search_bible 在 {version} 版本中搜尋「{topic}」
   - 先用 count_only=True 查看總共有多少相關經文
   - 列出最相關的 {max_verses} 處經文（包含上下文）

2. **主題查經資料**
   - 使用 get_topic_study 查詢「{topic}」的主題查經資料
   - 涵蓋 Torrey 和 Naves 主題聖經的相關條目
   - 整理出該主題的聖經神學架構

3. **註釋中的討論**
   - 使用 search_commentary 在註釋書中搜尋「{topic}」
   - 摘要重要註釋家對該主題的見解
   - 列出不同神學傳統的觀點

4. **舊約與新約的教導**
   - 分別搜尋舊約和新約中的相關經文
   - 比較兩約對該主題的教導有何異同
   - 觀察該主題在救恩歷史中的發展

5. **原文洞察**（如適用）
   - 找出該主題相關的關鍵希伯來文/希臘文字詞
   - 使用 lookup_strongs 研究原文字義
   - 解釋原文如何豐富我們對該主題的理解

6. **綜合分析與應用**
   - 總結聖經對「{topic}」的整體教導
   - 歸納出 3-5 個核心真理
   - 提供實際生活應用建議
   - 列出進深研讀的方向

請以清晰的結構呈現研究成果，並引用具體經文支持論點。"""


class CompareTranslationsPrompt(PromptTemplate):
    """版本比較 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="compare_translations",
            description="比較不同聖經譯本的翻譯",
            arguments=[
                {
                    "name": "book",
                    "description": "經卷名稱",
                    "required": True
                },
                {
                    "name": "chapter",
                    "description": "章數",
                    "required": True
                },
                {
                    "name": "verse",
                    "description": "節數",
                    "required": True
                },
                {
                    "name": "versions",
                    "description": "要比較的版本代碼列表（逗號分隔）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        book: str,
        chapter: int,
        verse: int,
        versions: str = "unv,nstrunv,kjv,niv"
    ) -> str:
        """
        渲染版本比較的 prompt
        
        Args:
            book: 經卷名稱
            chapter: 章數
            verse: 節數
            versions: 版本代碼（逗號分隔）
            
        Returns:
            渲染後的 prompt
        """
        version_list = [v.strip() for v in versions.split(",")]
        version_bullets = "\n".join([f"   - {v}" for v in version_list])
        
        return f"""請幫我比較 {book} {chapter}:{verse} 在不同譯本中的翻譯。

請按照以下步驟進行版本比較：

1. **各版本經文**
   - 使用 get_bible_verse 查詢以下版本的經文：
{version_bullets}
   - 並列顯示各版本的翻譯

2. **版本資訊**
   - 使用 list_bible_versions 查詢這些版本的詳細資訊
   - 說明各版本的特色（直譯/意譯、目標讀者、出版年代等）

3. **原文分析**
   - 使用 get_word_analysis 取得該節經文的原文分析
   - 列出關鍵字詞的希臘文/希伯來文及其基本意義
   - 使用 lookup_strongs 查詢重要字詞的 Strong's 字典定義

4. **翻譯差異分析**
   - 比較各版本在以下方面的差異：
     * 字詞選擇（特別是神學關鍵詞）
     * 句子結構
     * 語氣和風格
     * 是否添加解釋性詞語
   - 分析這些差異的原因和影響

5. **原文對照**
   - 將各版本的翻譯與原文進行對照
   - 評估各版本如何處理原文的特殊語法或修辭
   - 指出哪些版本更貼近原文字面意義
   - 指出哪些版本更清楚傳達原文意圖

6. **翻譯評估與建議**
   - 總結各版本的優缺點
   - 針對不同研讀目的推薦合適的版本：
     * 深度研經
     * 靈修默想
     * 初信者閱讀
     * 公開講道引用
   - 建議如何綜合使用多個版本以獲得更全面的理解

請提供詳細的分析，並用表格或對照方式清楚呈現比較結果。"""


class WordStudyPrompt(PromptTemplate):
    """原文字詞研究 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="word_study",
            description="深入研究希臘文或希伯來文單字",
            arguments=[
                {
                    "name": "strongs_number",
                    "description": "Strong's 編號",
                    "required": True
                },
                {
                    "name": "testament",
                    "description": "約別（OT 或 NT）",
                    "required": True
                },
                {
                    "name": "max_occurrences",
                    "description": "最多顯示的出現次數（預設：20）",
                    "required": False
                }
            ]
        )
    
    def render(
        self,
        strongs_number: str,
        testament: str,
        max_occurrences: int = 20
    ) -> str:
        """
        渲染原文字詞研究的 prompt
        
        Args:
            strongs_number: Strong's 編號
            testament: 約別（OT/NT）
            max_occurrences: 最多顯示出現次數
            
        Returns:
            渲染後的 prompt
        """
        testament_name = "新約希臘文" if testament.upper() == "NT" else "舊約希伯來文"
        
        return f"""請幫我研究 Strong's #{strongs_number} ({testament_name}) 這個原文字。

請按照以下步驟進行字詞研究：

1. **字典定義**
   - 使用 lookup_strongs 查詢 Strong's #{strongs_number} 的字典條目
   - 提供：
     * 原文拼寫（含發音）
     * 字根來源
     * 基本字義
     * 英文和中文的詳細定義

2. **同源字分析**（僅適用於新約）
   - 列出所有同源字（來自同一字根的相關字詞）
   - 說明各同源字的：
     * Strong's 編號
     * 原文拼寫
     * 中文意義
     * 在聖經中出現的次數
   - 分析這些同源字的語義關係

3. **聖經出現位置**
   - 使用 search_strongs_occurrences 找出該字在聖經中的所有出現位置
   - 列出前 {max_occurrences} 處具代表性的經文
   - 按書卷順序或主題分類整理

4. **語境中的字義變化**
   - 分析該字在不同語境中的用法：
     * 文學體裁（敘事、詩歌、律法、書信等）
     * 作者風格（保羅、約翰、路加等）
     * 時代背景（舊約時期、福音書、早期教會等）
   - 觀察字義的範圍和強調的不同面向
   - 特別注意是否有比喻或象徵用法

5. **神學意義**
   - 探討該字的神學重要性：
     * 在救恩歷史中的角色
     * 與核心教義的關聯
     * 對理解神的屬性或作為的貢獻
   - 引用重要經文說明其神學用法
   - 參考註釋書對該字的神學討論

6. **跨約比較**（如適用）
   - 比較舊約希伯來文與新約希臘文的對應字詞
   - 觀察七十士譯本（LXX）的翻譯選擇
   - 分析新約如何引用或重新詮釋舊約的概念

7. **研究總結與應用**
   - 總結該字的核心意涵
   - 說明正確理解該字如何幫助我們：
     * 更準確理解相關經文
     * 避免常見的誤解
     * 在生活中活出該字的真理
   - 推薦進深研讀的資源或經文

請提供詳盡的分析，並引用具體經文和學術資源。"""


class PromptManager:
    """Prompt 管理器"""
    
    def __init__(self):
        """初始化 Prompt 管理器"""
        self.prompts: Dict[str, PromptTemplate] = {
            "study_verse": StudyVersePrompt(),
            "search_topic": SearchTopicPrompt(),
            "compare_translations": CompareTranslationsPrompt(),
            "word_study": WordStudyPrompt()
        }
    
    def get_prompt(self, name: str) -> Optional[PromptTemplate]:
        """
        根據名稱獲取 prompt 模板
        
        Args:
            name: Prompt 名稱
            
        Returns:
            PromptTemplate 對象，如果不存在則返回 None
        """
        return self.prompts.get(name)
    
    def list_prompts(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的 prompts
        
        Returns:
            Prompt 資訊列表
        """
        return [
            {
                "name": prompt.name,
                "description": prompt.description,
                "arguments": prompt.arguments
            }
            for prompt in self.prompts.values()
        ]
    
    def render_prompt(self, name: str, **kwargs) -> Optional[str]:
        """
        渲染指定的 prompt
        
        Args:
            name: Prompt 名稱
            **kwargs: Prompt 參數
            
        Returns:
            渲染後的 prompt 字符串，如果 prompt 不存在則返回 None
        """
        prompt = self.get_prompt(name)
        if prompt:
            return prompt.render(**kwargs)
        return None
