"""
Advanced Parallel Gospels Prompt

符類福音對照對話範本
對照四福音書的平行記載，展現異同
"""

from dataclasses import dataclass
from typing import Optional
from ..base import PromptTemplate


@dataclass
class AdvancedParallelGospelsPrompt(PromptTemplate):
    """符類福音對照對話範本
    
    對照馬太、馬可、路加、約翰福音的平行記載。
    展現四福音書在記載同一事件時的異同。
    
    特色：
    - 智能識別福音書事件
    - 四福音並列比較
    - 差異分析和解釋
    - 神學意義探討
    """
    
    def __init__(
        self,
        event: str = "Jesus' Baptism",
        passage: Optional[str] = None,
        version: str = "unv",
        include_john: bool = True
    ):
        """初始化符類福音對照 Prompt
        
        Args:
            event: 事件名稱（如 "Jesus' Baptism", "Feeding 5000"，預設：Jesus' Baptism）
                   或使用常見中文名稱：「耶穌受洗」「五餅二魚」等
            passage: 經文位置（可選，如 "Matthew 3:13-17"，如提供則優先使用）
            version: 聖經版本（預設：unv 和合本）
            include_john: 是否包含約翰福音（預設：True，某些符類福音特有事件可設為 False）
        """
        super().__init__(
            name="advanced_parallel_gospels",
            description="對照四福音書的平行記載，展現異同和神學重點",
            arguments=[
                {"name": "event", "description": "事件名稱", "required": False},
                {"name": "passage", "description": "經文位置（可選）", "required": False},
                {"name": "version", "description": "聖經版本", "required": False},
                {"name": "include_john", "description": "是否包含約翰福音", "required": False}
            ]
        )
        self.event = event
        self.passage = passage
        self.version = version
        self.include_john = include_john
    
    def render(
        self,
        event: str = None,
        passage: str = None,
        version: str = None,
        include_john: bool = None
    ) -> str:
        """渲染符類福音對照指引
        
        Args:
            event: 事件名稱（可選，使用時覆蓋初始化值）
            passage: 經文位置（可選，使用時覆蓋初始化值）
            version: 聖經版本（可選，使用時覆蓋初始化值）
            include_john: 是否包含約翰福音（可選，使用時覆蓋初始化值）
        """
        # 使用傳入的參數或初始化時的值
        if event is not None:
            self.event = event
        if passage is not None:
            self.passage = passage
        if version is not None:
            self.version = version
        if include_john is not None:
            self.include_john = include_john
        
        gospels_to_compare = "四福音" if self.include_john else "符類福音（馬太、馬可、路加）"
        
        prompt = f"""
═══════════════════════════════════════════════════
  📖 符類福音對照 - FHL Bible MCP Server
═══════════════════════════════════════════════════

歡迎使用符類福音對照系統！

🎯 研究事件：**{self.event}**
{"📍 指定經文：**" + self.passage + "**" if self.passage else "📍 將自動搜尋各福音書的記載"}
📚 對照範圍：{gospels_to_compare}
📖 聖經版本：{self.version.upper()}

【符類福音（Synoptic Gospels）說明】
• 馬太福音：強調耶穌是彌賽亞君王，針對猶太人
• 馬可福音：強調耶穌是神的僕人，節奏緊湊
• 路加福音：強調耶穌是完全的人，關懷弱勢
{"• 約翰福音：強調耶穌是神的兒子，神學性最強" if self.include_john else ""}

═══════════════════════════════════════════════════
  步驟 1：定位平行經文 🔍
═══════════════════════════════════════════════════

【如果已提供經文位置】
{"使用指定的經文：" + self.passage if self.passage else ""}
{"需要搜尋其他福音書的平行記載" if self.passage else ""}

【如果僅提供事件名稱】
使用 search_bible 在各福音書中搜尋：

1️⃣ **馬太福音搜尋**
```
使用 search_bible 工具
書卷限制：Matthew（或 Matt, Mt）
關鍵詞：[從事件名稱提取]
例如：「受洗」「五餅二魚」「登山寶訓」等
```

2️⃣ **馬可福音搜尋**
```
使用 search_bible 工具
書卷限制：Mark（或 Mk）
相同關鍵詞搜尋
```

3️⃣ **路加福音搜尋**
```
使用 search_bible 工具
書卷限制：Luke（或 Lk）
相同關鍵詞搜尋
```

{"4️⃣ **約翰福音搜尋**" if self.include_john else ""}
{"```" if self.include_john else ""}
{"使用 search_bible 工具" if self.include_john else ""}
{"書卷限制：John（或 Jn）" if self.include_john else ""}
{"相同關鍵詞搜尋" if self.include_john else ""}
{"```" if self.include_john else ""}

【定位結果整理】

請將找到的經文整理如下：

```
┌─────────────────────────────────────────────┐
│ 事件：{self.event}                           │
│ 平行經文定位                                 │
└─────────────────────────────────────────────┘

📖 馬太福音：[章:節範圍] 或 [無記載]
   URI: bible://verse/{self.version}/Matt/[chapter]/[verse]

📖 馬可福音：[章:節範圍] 或 [無記載]
   URI: bible://verse/{self.version}/Mark/[chapter]/[verse]

📖 路加福音：[章:節範圍] 或 [無記載]
   URI: bible://verse/{self.version}/Luke/[chapter]/[verse]

{"📖 約翰福音：[章:節範圍] 或 [無記載]" if self.include_john else ""}
{"   URI: bible://verse/" + self.version + "/John/[chapter]/[verse]" if self.include_john else ""}
```

💡 **提示**：某些事件可能只在部分福音書中記載

═══════════════════════════════════════════════════
  步驟 2：獲取完整經文 📚
═══════════════════════════════════════════════════

對於每一卷有記載的福音書，使用 get_bible_verses 獲取完整段落：

**馬太福音**
```
使用 get_bible_verses 工具
書卷：Matthew
章節範圍：[從步驟 1 確定]
版本：{self.version}
```

【馬太福音記載】
（在此處顯示完整經文）

---

**馬可福音**
```
使用 get_bible_verses 工具
書卷：Mark
章節範圍：[從步驟 1 確定]
版本：{self.version}
```

【馬可福音記載】
（在此處顯示完整經文）

---

**路加福音**
```
使用 get_bible_verses 工具
書卷：Luke
章節範圍：[從步驟 1 確定]
版本：{self.version}
```

【路加福音記載】
（在此處顯示完整經文）

---

{"**約翰福音**" if self.include_john else ""}
{"```" if self.include_john else ""}
{"使用 get_bible_verses 工具" if self.include_john else ""}
{"書卷：John" if self.include_john else ""}
{"章節範圍：[從步驟 1 確定]" if self.include_john else ""}
{"版本：" + self.version if self.include_john else ""}
{"```" if self.include_john else ""}

{"【約翰福音記載】" if self.include_john else ""}
{"（在此處顯示完整經文）" if self.include_john else ""}

═══════════════════════════════════════════════════
  步驟 3：並列對照表 📊
═══════════════════════════════════════════════════

【經文並列比較】

將四福音的記載並列呈現，便於對照：

```
┌────────────────────────────────────────────────────────────────┐
│ {self.event} - 四福音並列對照                                   │
└────────────────────────────────────────────────────────────────┘

【情節元素】              【太】    【可】    【路】    {"【約】" if self.include_john else ""}
─────────────────────────────────────────────────────────────────
時間地點                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
主要人物                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
事件經過                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
對話內容                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
神蹟細節                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
群眾反應                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
門徒反應                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
教導內容                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}
結論應用                  ✓ __     ✓ __     ✓ __     {"✓ __" if self.include_john else ""}

圖例：✓ 有記載  ✗ 無記載  ~ 簡略提及
─────────────────────────────────────────────────────────────────
```

請針對每個情節元素，列出各福音書的具體內容

═══════════════════════════════════════════════════
  步驟 4：相同點分析 🤝
═══════════════════════════════════════════════════

【共同記載的核心內容】

分析所有福音書都記載的要點：

1. **核心事實**（所有福音書一致的部分）
   
   • 事件本身：[描述核心事件]
   • 主要人物：[列出所有福音都提到的人物]
   • 關鍵行動：[描述一致的動作或行為]
   • 結果影響：[說明一致記載的結果]

2. **相同的措辭**（逐字相同或非常接近）
   
   對比原文或譯文，找出相同的句子或短語：
   ```
   相同措辭 1：「[引用經文]」
   出現於：太 __:__ / 可 __:__ / 路 __:__
   
   相同措辭 2：「[引用經文]」
   出現於：太 __:__ / 可 __:__ / 路 __:__
   ```

3. **共同神學重點**
   
   • 啟示的真理：[所有福音都強調的真理]
   • 對耶穌的描繪：[共同呈現的耶穌形象]
   • 對門徒的教導：[一致的教導內容]

═══════════════════════════════════════════════════
  步驟 5：差異點分析 🔍
═══════════════════════════════════════════════════

【各福音書的獨特記載】

分析每卷福音書特有的內容：

📖 **馬太福音的獨特之處**
```
✨ 獨有細節：
   • [列出只有馬太記載的細節]
   • [例如：舊約引用、數字、猶太背景等]

✨ 強調重點：
   • [馬太特別強調的方面]
   • [符合其「君王」主題的元素]

✨ 獨特措辭：
   • 「[引用馬太特有的詞句]」
```

📖 **馬可福音的獨特之處**
```
✨ 獨有細節：
   • [列出只有馬可記載的細節]
   • [例如：生動的描述、情感表達等]

✨ 強調重點：
   • [馬可特別強調的方面]
   • [符合其「僕人」主題的元素]

✨ 獨特措辭：
   • 「[引用馬可特有的詞句]」
```

📖 **路加福音的獨特之處**
```
✨ 獨有細節：
   • [列出只有路加記載的細節]
   • [例如：對弱勢群體的關注、醫學細節等]

✨ 強調重點：
   • [路加特別強調的方面]
   • [符合其「完全的人」主題的元素]

✨ 獨特措辭：
   • 「[引用路加特有的詞句]」
```

{"📖 **約翰福音的獨特之處**" if self.include_john else ""}
{"```" if self.include_john else ""}
{"✨ 獨有細節：" if self.include_john else ""}
{"   • [列出只有約翰記載的細節]" if self.include_john else ""}
{"   • [例如：神學性對話、「我是」宣告等]" if self.include_john else ""}
{"" if self.include_john else ""}
{"✨ 強調重點：" if self.include_john else ""}
{"   • [約翰特別強調的方面]" if self.include_john else ""}
{"   • [符合其「神的兒子」主題的元素]" if self.include_john else ""}
{"" if self.include_john else ""}
{"✨ 獨特措辭：" if self.include_john else ""}
{"   • 「[引用約翰特有的詞句]」" if self.include_john else ""}
{"```" if self.include_john else ""}

【差異的可能原因】

1. **作者背景不同**
   • 馬太：稅吏，熟悉猶太傳統
   • 馬可：可能是彼得的傳譯，記錄彼得的見證
   • 路加：外邦醫生，細心的歷史學家
   {"• 約翰：使徒，耶穌所愛的門徒，晚年寫作" if self.include_john else ""}

2. **目標讀者不同**
   • 馬太：猶太基督徒
   • 馬可：羅馬信徒（外邦人）
   • 路加：提阿非羅大人（外邦官員）
   {"• 約翰：第二代基督徒，面對異端挑戰" if self.include_john else ""}

3. **寫作目的不同**
   • 馬太：證明耶穌是彌賽亞
   • 馬可：展現耶穌的大能行動
   • 路加：有次序地述說，使人確信
   {"• 約翰：使人信耶穌是基督、是神的兒子" if self.include_john else ""}

4. **記憶與見證角度**
   • 不同目擊者可能注意到不同細節
   • 聖靈啟示作者記錄特定內容
   • 補充性而非矛盾性的差異

═══════════════════════════════════════════════════
  步驟 6：神學意義綜合 🎓
═══════════════════════════════════════════════════

【從四福音看事件的完整意義】

結合所有福音書的記載，歸納事件的神學意義：

1. **對耶穌身份的啟示**
   
   • 君王（馬太角度）：[從馬太的記載看到的君王特質]
   • 僕人（馬可角度）：[從馬可的記載看到的僕人特質]
   • 完全的人（路加角度）：[從路加的記載看到的人性]
   {"• 神的兒子（約翰角度）：[從約翰的記載看到的神性]" if self.include_john else ""}
   
   綜合結論：[四重身份如何在這事件中彰顯]

2. **對門徒的教導**
   
   • 從各福音書綜合看到的教導：
     - [教導 1]
     - [教導 2]
     - [教導 3]
   
   • 這些教導在救恩歷史中的位置

3. **對今日信徒的意義**
   
   • 認識基督：[如何更深認識耶穌]
   • 跟隨基督：[如何實踐門徒生活]
   • 見證基督：[如何向他人見證]

═══════════════════════════════════════════════════
  步驟 7：解經應用指引 💡
═══════════════════════════════════════════════════

【使用本對照研究的建議】

1. **講道/教學使用**
   
   ✅ **主題講道**
   ```
   題目建議：「從四福音看 {self.event}」
   
   大綱建議：
   I. 事件概述（共同記載）
   II. 從不同角度認識耶穌
       A. 君王的威嚴（馬太）
       B. 僕人的服事（馬可）
       C. 完全的人性（路加）
       {"D. 神的榮耀（約翰）" if self.include_john else ""}
   III. 對我們的啟示與挑戰
   ```
   
   ✅ **系列講道**
   ```
   第一講：馬太的視角
   第二講：馬可的視角
   第三講：路加的視角
   {"第四講：約翰的視角" if self.include_john else ""}
   第{"四" if not self.include_john else "五"}講：綜合應用
   ```

2. **小組查經使用**
   
   ✅ **討論問題**
   ```
   1. 各福音書記載的相同點有哪些？為什麼這些是核心？
   2. 各福音書記載的不同點呢？這些差異教導我們什麼？
   3. 哪一個福音書的記載最打動你？為什麼？
   4. 從四個角度綜合來看，你對耶穌有什麼新的認識？
   5. 這個事件對你的信仰生活有什麼啟發？
   ```

3. **個人靈修使用**
   
   ✅ **默想步驟**
   ```
   第 1 天：讀馬太的記載，默想君王的威嚴
   第 2 天：讀馬可的記載，默想僕人的服事
   第 3 天：讀路加的記載，默想完全的人性
   {"第 4 天：讀約翰的記載，默想神的榮耀" if self.include_john else ""}
   第 {"4" if not self.include_john else "5"} 天：綜合默想，回應主的話語
   ```

4. **進深研究建議**
   
   • 使用 study_verse_deep 深入研讀關鍵經節
   • 使用 study_translation_compare 比較不同譯本
   • 使用 study_word_original 研究關鍵字詞原文
   • 使用 advanced_cross_reference 找出更多相關經文

═══════════════════════════════════════════════════
  完成！✅
═══════════════════════════════════════════════════

【本次對照摘要】

🎯 研究事件：{self.event}
📖 對照範圍：{gospels_to_compare}
📊 找到記載：__ 卷福音書有記載
⏱️ 完成時間：[記錄完成時間]

【關鍵發現】

• 共同點：__ 個核心要素
• 差異點：各福音書各有 __ 個獨特記載
• 神學重點：[簡要總結]

【延伸閱讀建議】

• 研究其他相關事件
• 追蹤同一主題在各福音的發展
• 比較福音書作者的寫作特色

【需要幫助？】
• 使用 help_guide 查看完整功能
• 使用 tool_reference 查看工具說明

═══════════════════════════════════════════════════
"""
        return prompt.strip()
