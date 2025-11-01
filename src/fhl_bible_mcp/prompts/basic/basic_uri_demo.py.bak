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
        """
        渲染 URI 使用示範的 prompt
        
        Args:
            uri_type: URI 類型（all/bible/strongs/commentary/info）
            
        Returns:
            渲染後的 prompt
        """
        # 根據 uri_type 決定顯示哪些內容
        if uri_type == "all":
            return self._render_all()
        elif uri_type == "bible":
            return self._render_bible_uri()
        elif uri_type == "strongs":
            return self._render_strongs_uri()
        elif uri_type == "commentary":
            return self._render_commentary_uri()
        elif uri_type == "info":
            return self._render_info_uri()
        else:
            return self._render_all()
    
    def _render_all(self) -> str:
        """渲染完整的 URI 教學"""
        return """請為我展示 FHL Bible MCP Server 的所有 Resource URI 使用方式。

請按照以下結構提供完整的 URI 使用教學：

═══════════════════════════════════════════════════════════════════
  📚 FHL Bible MCP Server - Resource URI 完整使用指南
═══════════════════════════════════════════════════════════════════

【什麼是 Resource URI？】

Resource URI 是一種快速訪問聖經資源的方式，類似於網址 (URL)。
您可以直接點擊 URI 連結，或在對話中使用它們來存取聖經內容。

就像網址一樣：
  • http://example.com/page → 訪問網頁
  • bible://verse/unv/John/3/16 → 訪問經文

優點：
  ✓ 快速直接 - 一鍵取得資源
  ✓ 可分享 - 複製 URI 給其他人
  ✓ 可收藏 - 儲存常用經文的 URI
  ✓ 可組合 - 配合其他工具使用

───────────────────────────────────────────────────────────────────
📖 第一部分：Bible URI - 聖經經文資源
───────────────────────────────────────────────────────────────────

【基本格式】

1. 查詢單節經文：
   bible://verse/{version}/{book}/{chapter}/{verse}
   
2. 查詢整章經文：
   bible://chapter/{version}/{book}/{chapter}

【實用範例】

▸ 範例 1：約翰福音 3:16（和合本）
  URI: bible://verse/unv/John/3/16
  
  說明：這是最常用的格式
  • unv = 和合本
  • John = 約翰福音
  • 3 = 第 3 章
  • 16 = 第 16 節
  
  請點擊此 URI 查看結果 ↓
  bible://verse/unv/John/3/16

▸ 範例 2：詩篇 23 篇完整內容
  URI: bible://chapter/unv/Ps/23
  
  說明：取得整章經文（詩篇 23 篇共 6 節）
  • Ps = 詩篇 (Psalm)
  • 23 = 第 23 章
  
  請點擊此 URI 查看結果 ↓
  bible://chapter/unv/Ps/23

▸ 範例 3：創世記 1:1（中文書卷名稱也可以）
  URI: bible://verse/unv/創世記/1/1
  
  說明：支援中文書卷名稱
  
  請點擊此 URI 查看結果 ↓
  bible://verse/unv/創世記/1/1

▸ 範例 4：約翰福音 3:16（含 Strong's Number）
  URI: bible://verse/unv/John/3/16?strong=true
  
  說明：加上 ?strong=true 參數可顯示原文編號
  適合：想研究原文字義時使用
  
  請點擊此 URI 查看結果 ↓
  bible://verse/unv/John/3/16?strong=true

▸ 範例 5：羅馬書 8:28（英文 NIV 版本）
  URI: bible://verse/niv/Rom/8/28
  
  說明：更換版本代碼即可查看不同譯本
  • niv = New International Version
  
  請點擊此 URI 查看結果 ↓
  bible://verse/niv/Rom/8/28

【支援的聖經版本代碼】

常用中文版本：
  • unv - 和合本（預設推薦）
  • nstrunv - 新標點和合本
  • cunp - 和合本（簡體）
  
常用英文版本：
  • kjv - King James Version
  • niv - New International Version
  • nkjv - New King James Version
  • esv - English Standard Version
  
查看完整版本列表：
  info://versions

【書卷名稱對照】

中文名稱：創世記、出埃及記、詩篇、約翰福音...
英文全名：Genesis, Exodus, Psalm, John...
英文縮寫：Gen, Ex, Ps, John...（推薦使用）

查看完整書卷列表：
  info://books

【使用技巧】

1. 書卷名稱不分大小寫：
   • John = john = JOHN ✓
   • Psalm = psalm = PSALM ✓

2. 支援多種書卷格式：
   • 約翰福音 = John = Jhn = Jn ✓
   • 詩篇 = Psalm = Ps ✓
   
3. 查詢參數可組合：
   • ?strong=true - 顯示 Strong's Number
   • ?simplified=true - 簡體中文（部分版本支援）

───────────────────────────────────────────────────────────────────
📚 第二部分：Strong's URI - 原文字典資源
───────────────────────────────────────────────────────────────────

【基本格式】

strongs://{testament}/{number}

• testament: nt (新約希臘文) 或 ot (舊約希伯來文)
• number: Strong's 編號（不含 G/H 前綴）

【實用範例】

▸ 範例 1：希臘文「愛」(ἀγαπάω)
  URI: strongs://nt/25
  
  說明：G25 是新約中「愛」的重要字
  • nt = 新約 (New Testament)
  • 25 = Strong's Number
  
  內容包含：
  • 原文拼寫和發音
  • 中英文定義
  • 同源字列表
  • 使用頻率
  
  請點擊此 URI 查看結果 ↓
  strongs://nt/25

▸ 範例 2：希伯來文「神」(אֱלֹהִים)
  URI: strongs://ot/430
  
  說明：H430 是舊約中「神」的常用字
  • ot = 舊約 (Old Testament)
  • 430 = Strong's Number
  
  請點擊此 URI 查看結果 ↓
  strongs://ot/430

▸ 範例 3：希臘文「恩典」(χάρις)
  URI: strongs://nt/5485
  
  說明：G5485 - 新約神學關鍵詞
  
  請點擊此 URI 查看結果 ↓
  strongs://nt/5485

▸ 範例 4：希伯來文「平安」(שָׁלוֹם)
  URI: strongs://ot/7965
  
  說明：H7965 - 著名的希伯來文祝福語
  
  請點擊此 URI 查看結果 ↓
  strongs://ot/7965

【如何找到 Strong's Number？】

方法 1：從經文中查找
  1. 使用 bible://verse/unv/John/3/16?strong=true
  2. 經文會顯示每個字的 Strong's Number
  3. 點擊編號或使用 strongs:// URI 查詢

方法 2：使用搜尋功能
  • 使用 search_bible 工具搜尋關鍵字
  • 使用 get_word_analysis 取得經文的原文分析
  • 得到 Strong's Number 後使用 strongs:// 查詢

方法 3：直接查詢工具
  • 使用 lookup_strongs 工具
  • 參數：number=25, testament="NT"

【新約 vs 舊約】

新約（nt）：
  • 希臘文（Greek）
  • Strong's Number: 1-5624
  • 範例：G25 (ἀγαπάω - 愛)

舊約（ot）：
  • 希伯來文/亞蘭文（Hebrew/Aramaic）
  • Strong's Number: 1-8674
  • 範例：H430 (אֱלֹהִים - 神)

───────────────────────────────────────────────────────────────────
💬 第三部分：Commentary URI - 註釋資源
───────────────────────────────────────────────────────────────────

【基本格式】

1. 查詢經文註釋（所有註釋書）：
   commentary://{book}/{chapter}/{verse}
   
2. 查詢特定註釋書：
   commentary://{book}/{chapter}/{verse}?commentary_id={id}

【實用範例】

▸ 範例 1：約翰福音 3:16 的所有註釋
  URI: commentary://John/3/16
  
  說明：取得所有可用註釋書對該節的註解
  內容包含多位註釋家的觀點
  
  請點擊此 URI 查看結果 ↓
  commentary://John/3/16

▸ 範例 2：羅馬書 8:28 的註釋
  URI: commentary://Rom/8/28
  
  說明：綜合多本註釋書的解經
  
  請點擊此 URI 查看結果 ↓
  commentary://Rom/8/28

▸ 範例 3：詩篇 23:1 的註釋
  URI: commentary://Ps/23/1
  
  說明：智慧文學的註釋通常包含文學分析
  
  請點擊此 URI 查看結果 ↓
  commentary://Ps/23/1

▸ 範例 4：指定特定註釋書
  URI: commentary://John/3/16?commentary_id=1
  
  說明：僅查看特定註釋書的內容
  • commentary_id=1 指定註釋書編號
  
  請點擊此 URI 查看結果 ↓
  commentary://John/3/16?commentary_id=1

【可用的註釋書】

查看所有註釋書列表：
  info://commentaries

註釋書類型：
  • 解經註釋 - 逐節解釋
  • 講道註釋 - 應用導向
  • 學術註釋 - 原文語法
  • 靈修註釋 - 屬靈操練

【使用場景】

✓ 難解經文 - 需要專家解釋
✓ 講道準備 - 參考多位註釋家
✓ 查經帶領 - 提供深度內容
✓ 個人研經 - 避免錯誤理解

───────────────────────────────────────────────────────────────────
ℹ️ 第四部分：Info URI - 資訊查詢資源
───────────────────────────────────────────────────────────────────

【基本格式】

info://{resource_type}

可查詢的資源類型：
  • versions - 聖經版本列表
  • books - 書卷列表
  • commentaries - 註釋書列表
  • verse_of_day - 今日金句

【實用範例】

▸ 範例 1：查看所有聖經版本
  URI: info://versions
  
  說明：列出所有可用的聖經譯本
  包含：版本代碼、全名、語言、特色
  
  請點擊此 URI 查看結果 ↓
  info://versions

▸ 範例 2：查看所有書卷
  URI: info://books
  
  說明：列出聖經 66 卷書
  包含：中英文名稱、縮寫、章數
  
  請點擊此 URI 查看結果 ↓
  info://books

▸ 範例 3：僅查看新約書卷
  URI: info://books?testament=NT
  
  說明：篩選新約 27 卷
  • testament=NT 指定新約
  • testament=OT 指定舊約
  
  請點擊此 URI 查看結果 ↓
  info://books?testament=NT

▸ 範例 4：僅查看舊約書卷
  URI: info://books?testament=OT
  
  說明：篩選舊約 39 卷
  
  請點擊此 URI 查看結果 ↓
  info://books?testament=OT

▸ 範例 5：查看所有註釋書
  URI: info://commentaries
  
  說明：列出可用的註釋書
  包含：註釋書名稱、編號、特色
  
  請點擊此 URI 查看結果 ↓
  info://commentaries

▸ 範例 6：取得今日金句
  URI: info://verse_of_day
  
  說明：每日更新的靈修經文
  包含：經文內容、書卷章節
  適合：每日靈修、社群分享
  
  請點擊此 URI 查看結果 ↓
  info://verse_of_day

【查詢參數】

books 資源支援的參數：
  • ?testament=NT - 僅新約
  • ?testament=OT - 僅舊約
  
其他資源目前不需要參數。

───────────────────────────────────────────────────────────────────
💡 第五部分：實用技巧與最佳實踐
───────────────────────────────────────────────────────────────────

【技巧 1：組合使用 URI】

流程：資訊查詢 → 經文閱讀 → 深入研究

步驟 1：查看書卷列表
  info://books
  
步驟 2：選擇書卷閱讀
  bible://chapter/unv/John/1
  
步驟 3：深入研究某節
  bible://verse/unv/John/1/1?strong=true
  
步驟 4：查詢原文
  strongs://nt/3056 (λόγος - 道)
  
步驟 5：查看註釋
  commentary://John/1/1

【技巧 2：建立常用 URI 收藏】

靈修常用：
  • info://verse_of_day - 每日金句
  • bible://chapter/unv/Ps/119 - 詩篇 119（最長詩篇）
  • bible://chapter/unv/Ps/23 - 詩篇 23（牧羊詩）
  
研經常用：
  • info://versions - 版本對照
  • info://commentaries - 註釋參考
  
原文研究：
  • strongs://nt/25 - 愛 (ἀγαπάω)
  • strongs://nt/26 - 愛 (ἀγάπη)
  • strongs://ot/430 - 神 (אֱלֹהִים)

【技巧 3：錯誤排查】

如果 URI 無效，檢查：
  ✓ 書卷名稱拼寫正確
  ✓ 章節號碼存在（如詩篇沒有第 200 章）
  ✓ 版本代碼正確（用 info://versions 確認）
  ✓ 格式符合規範（注意 :// 和 /）

常見錯誤：
  ✗ bible:/verse/... （少一個 /）
  ✓ bible://verse/...
  
  ✗ strongs://25 （缺少 testament）
  ✓ strongs://nt/25
  
  ✗ commentary:/John/3/16 （少一個 /）
  ✓ commentary://John/3/16

【技巧 4：配合 Prompts 使用】

URI + Prompts = 強大研經工具

範例組合：
  • 先用 quick_lookup 找經文
  • 得到 URI 後點擊查看
  • 使用 study_verse 深入研讀
  • 使用 compare_translations 比較譯本

工作流程：
  1. "查約翰福音 3:16" → quick_lookup
  2. 點擊 bible://verse/unv/John/3/16
  3. "深入研讀這節" → study_verse
  4. 點擊 strongs://nt/25 研究「愛」

【技巧 5：分享與協作】

URI 可以輕鬆分享：
  • 複製 URI 給小組成員
  • 在筆記中記錄 URI
  • 在查經材料中嵌入 URI
  
範例：
  "今天我們查考 bible://chapter/unv/John/15
   重點經文是 bible://verse/unv/John/15/5
   請查看 commentary://John/15/5 的註釋"

───────────────────────────────────────────────────────────────────
🎯 第六部分：快速參考卡
───────────────────────────────────────────────────────────────────

【經文查詢】
  單節：bible://verse/{version}/{book}/{chapter}/{verse}
  整章：bible://chapter/{version}/{book}/{chapter}
  範例：bible://verse/unv/John/3/16

【原文字典】
  格式：strongs://{testament}/{number}
  新約：strongs://nt/25
  舊約：strongs://ot/430

【註釋查詢】
  格式：commentary://{book}/{chapter}/{verse}
  範例：commentary://John/3/16

【資訊查詢】
  版本：info://versions
  書卷：info://books
  新約書卷：info://books?testament=NT
  舊約書卷：info://books?testament=OT
  註釋書：info://commentaries
  今日金句：info://verse_of_day

【常用版本代碼】
  unv - 和合本 (推薦)
  nstrunv - 新標點和合本
  kjv - King James Version
  niv - New International Version

【常用書卷縮寫】
  Gen - 創世記    Ex - 出埃及記   Lev - 利未記
  Num - 民數記    Deut - 申命記   Josh - 約書亞記
  Ps - 詩篇       Prov - 箴言     Isa - 以賽亞書
  Jer - 耶利米書  Ezek - 以西結書  Dan - 但以理書
  Matt - 馬太福音 John - 約翰福音 Acts - 使徒行傳
  Rom - 羅馬書    1Cor - 哥林多前書 Eph - 以弗所書
  Phil - 腓立比書 Col - 歌羅西書   Rev - 啟示錄

═══════════════════════════════════════════════════════════════════

【互動練習】

現在請您嘗試以下操作，我會協助您：

1️⃣ 查看約翰福音 3:16
   請點擊或告訴我您想查看這個 URI：
   bible://verse/unv/John/3/16

2️⃣ 閱讀詩篇 23 篇完整內容
   請點擊或告訴我您想查看這個 URI：
   bible://chapter/unv/Ps/23

3️⃣ 研究希臘文「愛」字
   請點擊或告訴我您想查看這個 URI：
   strongs://nt/25

4️⃣ 查看約翰福音 3:16 的註釋
   請點擊或告訴我您想查看這個 URI：
   commentary://John/3/16

5️⃣ 查看今日金句
   請點擊或告訴我您想查看這個 URI：
   info://verse_of_day

═══════════════════════════════════════════════════════════════════

【需要更多幫助？】

• 使用 help_guide 查看完整使用指南
• 使用 tool_reference 查看所有工具說明
• 使用 quick_lookup 快速查詢經文
• 直接詢問我任何問題！

═══════════════════════════════════════════════════════════════════

祝您使用愉快！願神的話語成為您腳前的燈，路上的光。"""

    def _render_bible_uri(self) -> str:
        """僅渲染 Bible URI 教學"""
        return """請為我展示 Bible URI 的詳細使用方式。

請提供完整的 Bible URI 使用教學，包括：

1. **基本格式**
   - 單節經文格式
   - 整章經文格式
   - 參數使用方式

2. **實用範例**（至少 5 個）
   - 約翰福音 3:16
   - 詩篇 23 篇
   - 含 Strong's Number 的經文
   - 不同版本對照

3. **版本代碼列表**
   - 常用中文版本
   - 常用英文版本
   - 如何查看完整列表

4. **書卷名稱對照**
   - 中文、英文全名、英文縮寫
   - 如何查看完整列表

5. **使用技巧**
   - 注意事項
   - 常見錯誤
   - 最佳實踐

請提供可點擊的實際 URI 範例。"""

    def _render_strongs_uri(self) -> str:
        """僅渲染 Strong's URI 教學"""
        return """請為我展示 Strong's URI 的詳細使用方式。

請提供完整的 Strong's URI 使用教學，包括：

1. **基本格式**
   - URI 結構說明
   - Testament 代碼（nt/ot）
   - Strong's Number 格式

2. **實用範例**（至少 5 個）
   - 新約常用字（如「愛」G25）
   - 舊約常用字（如「神」H430）
   - 神學關鍵詞

3. **如何找到 Strong's Number**
   - 從經文中查找
   - 使用搜尋工具
   - 使用查詢工具

4. **新約 vs 舊約**
   - 希臘文 vs 希伯來文
   - 編號範圍
   - 使用差異

請提供可點擊的實際 URI 範例。"""

    def _render_commentary_uri(self) -> str:
        """僅渲染 Commentary URI 教學"""
        return """請為我展示 Commentary URI 的詳細使用方式。

請提供完整的 Commentary URI 使用教學，包括：

1. **基本格式**
   - 查詢所有註釋
   - 查詢特定註釋書
   - 參數使用方式

2. **實用範例**（至少 5 個）
   - 福音書經文註釋
   - 書信經文註釋
   - 詩篇經文註釋
   - 指定註釋書

3. **可用的註釋書**
   - 註釋書類型
   - 如何查看列表
   - 選擇建議

4. **使用場景**
   - 什麼時候需要註釋
   - 如何善用註釋
   - 注意事項

請提供可點擊的實際 URI 範例。"""

    def _render_info_uri(self) -> str:
        """僅渲染 Info URI 教學"""
        return """請為我展示 Info URI 的詳細使用方式。

請提供完整的 Info URI 使用教學，包括：

1. **基本格式**
   - URI 結構說明
   - 可用的資源類型

2. **所有資源類型**
   - versions - 版本列表
   - books - 書卷列表
   - commentaries - 註釋書列表
   - verse_of_day - 今日金句

3. **實用範例**（每種類型至少 1 個）
   - 查看版本
   - 查看書卷（含篩選）
   - 查看註釋書
   - 取得今日金句

4. **查詢參數**
   - books 的 testament 參數
   - 其他參數

5. **使用場景**
   - 什麼時候使用 info URI
   - 與其他 URI 的組合使用

請提供可點擊的實際 URI 範例。"""
