"""
FHL Bible MCP Server - Help Guide Prompt

提供完整的使用指南和快速入門教學
"""

from ..base import PromptTemplate


class HelpGuidePrompt(PromptTemplate):
    """使用指南 Prompt"""
    
    def __init__(self):
        super().__init__(
            name="help_guide",
            description="顯示 FHL Bible MCP Server 的完整使用指南，包含快速入門、工具說明和實用技巧",
            arguments=[
                {
                    "name": "section",
                    "description": "指南章節 (all/quickstart/tools/resources/prompts/tips)",
                    "required": False
                }
            ]
        )
    
    def render(self, section: str = "all") -> str:
        """
        渲染使用指南的 prompt
        
        Args:
            section: 要顯示的章節（all/quickstart/tools/resources/prompts/tips）
            
        Returns:
            渲染後的 prompt
        """
        if section == "all":
            return self._render_full_guide()
        elif section == "quickstart":
            return self._render_quickstart()
        elif section == "tools":
            return self._render_tools()
        elif section == "resources":
            return self._render_resources()
        elif section == "prompts":
            return self._render_prompts()
        elif section == "tips":
            return self._render_tips()
        else:
            return self._render_full_guide()
    
    def _render_full_guide(self) -> str:
        """渲染完整使用指南"""
        return """請為我提供 FHL Bible MCP Server 的完整使用指南。

請按照以下結構提供詳細的使用說明：

═══════════════════════════════════════════════════════════════════
  📖 FHL Bible MCP Server - 完整使用指南
═══════════════════════════════════════════════════════════════════

歡迎使用 FHL Bible MCP Server！這是一個功能強大的聖經研讀工具，
提供經文查詢、原文研究、註釋參考等多種功能。

本指南將幫助您快速上手並充分利用所有功能。

───────────────────────────────────────────────────────────────────
🚀 第一章：快速入門
───────────────────────────────────────────────────────────────────

【3 分鐘快速體驗】

步驟 1：查詢一節經文
  最簡單的方式：直接點擊 URI 連結
  
  範例：約翰福音 3:16
  bible://verse/unv/John/3/16
  
  或使用自然語言：
  「請查詢約翰福音 3 章 16 節」

步驟 2：閱讀完整章節
  想看整章？沒問題！
  
  範例：詩篇 23 篇
  bible://chapter/unv/Ps/23
  
  或直接說：
  「請給我看詩篇 23 篇」

步驟 3：查看今日金句
  每天的靈修起點
  
  點擊這裡：
  info://verse_of_day
  
  或說：
  「今天的金句是什麼？」

恭喜！您已經學會最基本的使用方式了！

【您可以做什麼？】

✓ **查詢經文**
  • 單節、多節、整章都可以
  • 支援多種聖經版本
  • 可顯示原文編號
  
✓ **研究原文**
  • 查詢希臘文/希伯來文字義
  • 查看同源字
  • 了解使用頻率
  
✓ **參考註釋**
  • 多本註釋書
  • 專家解經
  • 深入理解
  
✓ **主題搜尋**
  • 關鍵字搜尋
  • 主題研究
  • 串珠查經
  
✓ **版本對照**
  • 多譯本比較
  • 原文對照
  • 理解差異

【適用場景】

📚 個人靈修
  • 每日讀經
  • 經文默想
  • 禱告預備

🎤 講道準備
  • 經文研究
  • 原文查考
  • 註釋參考

👥 小組查經
  • 帶領材料
  • 問題討論
  • 深度分享

🎓 神學研究
  • 字義研究
  • 主題查考
  • 學術寫作

───────────────────────────────────────────────────────────────────
🛠️ 第二章：工具說明
───────────────────────────────────────────────────────────────────

【經文查詢工具】

1. get_bible_text
   功能：取得經文內容
   適用：單節或多節經文
   
   範例：
   • 單節：約翰福音 3:16
   • 多節：約翰福音 3:16-18
   • 跨章：馬太福音 5:1-6:4
   
   參數：
   • version: 版本代碼（如 unv、kjv）
   • book: 書卷名稱
   • chapter: 章數
   • verse: 節數（可選範圍）
   • show_strong: 是否顯示 Strong's Number

2. get_chapter
   功能：取得完整章節
   適用：整章閱讀
   
   範例：
   • 詩篇 23 篇
   • 約翰福音 15 章
   • 啟示錄 21 章
   
   參數：
   • version: 版本代碼
   • book: 書卷名稱
   • chapter: 章數

3. search_bible
   功能：全文搜尋
   適用：找包含特定詞語的經文
   
   範例：
   • 搜尋「愛」
   • 搜尋「信心」
   • 搜尋「平安」
   
   參數：
   • keyword: 搜尋關鍵字
   • version: 版本代碼
   • testament: NT/OT（可選）
   • limit: 結果數量上限

【原文研究工具】

4. lookup_strongs
   功能：查詢 Strong's 原文字典
   適用：研究原文字義
   
   範例：
   • G25 - ἀγαπάω (愛)
   • H430 - אֱלֹהִים (神)
   • G3056 - λόγος (道)
   
   參數：
   • number: Strong's 編號
   • testament: NT/OT

5. get_word_analysis
   功能：經文原文分析
   適用：逐字原文研究
   
   範例：
   • 約翰福音 3:16 的原文分析
   • 創世記 1:1 的字義拆解
   
   參數：
   • book: 書卷
   • chapter: 章
   • verse: 節
   • version: 版本

【註釋參考工具】

6. get_commentary
   功能：取得經文註釋
   適用：深入理解經文
   
   範例：
   • 約翰福音 3:16 的註釋
   • 羅馬書 8:28 的解經
   
   參數：
   • book: 書卷
   • chapter: 章
   • verse: 節
   • commentary_id: 特定註釋書（可選）

【資訊查詢工具】

7. list_versions
   功能：列出所有聖經版本
   適用：選擇適合的版本
   
   傳回：
   • 版本代碼
   • 版本全名
   • 語言
   • 特色說明

8. list_books
   功能：列出聖經書卷
   適用：了解書卷資訊
   
   參數：
   • testament: NT/OT（可選）
   
   傳回：
   • 書卷名稱（中英文）
   • 縮寫
   • 章數

9. list_commentaries
   功能：列出可用註釋書
   適用：選擇註釋參考
   
   傳回：
   • 註釋書名稱
   • 註釋書編號
   • 特色說明

10. get_verse_of_day
    功能：取得今日金句
    適用：每日靈修
    
    傳回：
    • 經文內容
    • 書卷章節
    • 版本資訊

───────────────────────────────────────────────────────────────────
🔗 第三章：Resource URI 使用
───────────────────────────────────────────────────────────────────

【什麼是 Resource URI？】

Resource URI 是快速存取資源的捷徑，就像網址一樣。
您可以點擊 URI 連結，立即取得想要的內容。

優點：
✓ 快速直接 - 一鍵取得
✓ 可分享 - 複製給他人
✓ 可收藏 - 儲存常用經文
✓ 可嵌入 - 用在筆記中

【四種 URI 類型】

1. Bible URI - 經文資源
   格式：bible://verse/{version}/{book}/{chapter}/{verse}
   範例：bible://verse/unv/John/3/16
   
   用途：快速查詢經文

2. Strong's URI - 原文字典
   格式：strongs://{testament}/{number}
   範例：strongs://nt/25
   
   用途：研究原文字義

3. Commentary URI - 註釋資源
   格式：commentary://{book}/{chapter}/{verse}
   範例：commentary://John/3/16
   
   用途：查看專家註釋

4. Info URI - 資訊查詢
   格式：info://{resource_type}
   範例：info://versions
   
   用途：查詢系統資訊

【詳細教學】

想了解更多 URI 使用方式？
請使用 uri_demo prompt 查看完整教學！

或直接詢問：
「請教我如何使用 URI」

───────────────────────────────────────────────────────────────────
💬 第四章：Prompt 模板使用
───────────────────────────────────────────────────────────────────

【什麼是 Prompt？】

Prompt 是預先設計好的對話模板，幫助您更有效地使用本服務。
就像餐廳的套餐，為您配好一系列最佳操作。

【基礎 Prompts】

1. help_guide（就是本指南）
   用途：查看使用說明
   適合：新手入門
   
   使用方式：
   「請顯示使用指南」

2. uri_demo
   用途：學習 URI 使用
   適合：想用 URI 快捷方式的人
   
   使用方式：
   「請教我如何使用 URI」

3. quick_lookup
   用途：快速查經文
   適合：需要快速查詢
   
   使用方式：
   「快速查詢約翰福音 3:16」

4. tool_reference
   用途：工具功能參考
   適合：想了解所有工具
   
   使用方式：
   「顯示工具參考手冊」

【研經 Prompts】

5. study_verse
   用途：深入研讀經文
   適合：個人靈修、講道準備
   
   包含：
   • 經文內容（多版本）
   • 原文分析
   • 註釋參考
   • 相關經文
   • 應用問題
   
   使用方式：
   「請幫我深入研讀約翰福音 3:16」

6. search_topic
   用途：主題式查經
   適合：專題研究
   
   包含：
   • 相關經文搜集
   • 主題分類
   • 經文串連
   • 綜合分析
   
   使用方式：
   「請幫我查考『愛』的主題」

7. compare_translations
   用途：多譯本比較
   適合：了解翻譯差異
   
   包含：
   • 多版本對照
   • 差異說明
   • 原文參考
   • 理解建議
   
   使用方式：
   「請比較約翰福音 3:16 的不同譯本」

8. word_study
   用途：原文字義研究
   適合：深度原文查考
   
   包含：
   • 原文字義
   • 同源字
   • 使用統計
   • 神學意涵
   
   使用方式：
   「請研究『愛』的原文字義」

【如何使用 Prompt？】

方法 1：直接描述
  「請幫我深入研讀約翰福音 3:16」
  
方法 2：指定 Prompt 名稱
  「使用 study_verse 研讀約翰福音 3:16」
  
方法 3：詢問可用 Prompt
  「有什麼 Prompt 可以幫我？」

───────────────────────────────────────────────────────────────────
💡 第五章：實用技巧
───────────────────────────────────────────────────────────────────

【技巧 1：建立個人研經流程】

推薦流程：
  
第一步：快速閱讀
  • 使用 bible://chapter/... 閱讀整章
  • 掌握上下文
  
第二步：深入研讀
  • 使用 study_verse 研讀重點經文
  • 查看原文和註釋
  
第三步：跨譯本比較
  • 使用 compare_translations
  • 理解不同翻譯
  
第四步：主題串連
  • 使用 search_topic
  • 找相關經文
  
第五步：應用反思
  • 默想經文
  • 寫下領受

【技巧 2：講道準備工作流程】

週一：選定經文
  • 使用 bible://chapter/... 閱讀
  • 確定講道範圍
  
週二：原文研究
  • 使用 word_study
  • 查關鍵字原文
  
週三：註釋參考
  • 使用 commentary:// URI
  • 參考多位註釋家
  
週四：相關經文
  • 使用 search_topic
  • 找支持經文
  
週五：整合應用
  • 整理研究成果
  • 撰寫講章大綱

【技巧 3：小組查經帶領】

準備階段：
  • 使用 study_verse 預先研讀
  • 準備討論問題
  
帶領時：
  • 分享 URI 給組員
  • 一起查看經文
  • 使用 compare_translations 比較
  
討論時：
  • 使用 commentary:// 提供參考
  • 使用 search_topic 延伸討論

【技巧 4：建立個人經文庫】

收藏重要經文的 URI：
  
靈修類：
  • bible://verse/unv/Ps/119/105 - 腳前的燈
  • bible://verse/unv/Prov/3/5 - 專心仰賴主
  • bible://chapter/unv/Ps/23 - 牧羊詩篇
  
福音類：
  • bible://verse/unv/John/3/16 - 神愛世人
  • bible://verse/unv/Rom/3/23 - 世人都犯了罪
  • bible://verse/unv/Rom/6/23 - 罪的工價
  
應許類：
  • bible://verse/unv/Rom/8/28 - 萬事互相效力
  • bible://verse/unv/Phil/4/13 - 凡事都能做
  • bible://verse/unv/Jer/29/11 - 平安的計劃

【技巧 5：搜尋進階使用】

精確搜尋：
  • 使用完整詞組
  • 範例：「神愛世人」
  
分類搜尋：
  • 限定新約或舊約
  • testament=NT 或 OT
  
組合搜尋：
  • 先搜主要關鍵字
  • 再從結果中細搜

【技巧 6：版本選擇建議】

中文讀者：
  • 日常：unv（和合本）
  • 研經：nstrunv（新標點和合本）
  
英文讀者：
  • 現代：niv（New International Version）
  • 經典：kjv（King James Version）
  • 學術：esv（English Standard Version）
  
對照研究：
  • 使用 compare_translations
  • 同時查看 2-3 個版本

───────────────────────────────────────────────────────────────────
📚 第六章：常見問題 FAQ
───────────────────────────────────────────────────────────────────

Q1: 我是新手，從哪裡開始？
A: 建議順序：
   1. 閱讀本指南的「快速入門」章節
   2. 嘗試點擊幾個 URI 連結
   3. 使用 uri_demo 學習 URI
   4. 試用 study_verse 研讀一節經文

Q2: URI 和工具有什麼不同？
A: • URI：快速直接，適合單一資源查詢
   • 工具：功能完整，適合複雜操作

Q3: 如何查看所有可用的版本？
A: 方法 1：點擊 info://versions
   方法 2：使用 list_versions 工具
   方法 3：詢問「有哪些聖經版本？」

Q4: Strong's Number 是什麼？
A: Strong's Number 是原文聖經字彙編號系統
   • 希臘文（新約）：G1-G5624
   • 希伯來文（舊約）：H1-H8674
   可用來研究字義、詞源、用法

Q5: 如何找到 Strong's Number？
A: 方法 1：查詢帶原文的經文
          bible://verse/unv/John/3/16?strong=true
   方法 2：使用 get_word_analysis 工具
   方法 3：使用 word_study prompt

Q6: 註釋書可以自己選擇嗎？
A: 可以！
   • 查看所有：info://commentaries
   • 指定註釋書：commentary://John/3/16?commentary_id=1

Q7: 可以搜尋中文關鍵字嗎？
A: 可以！search_bible 支援中文搜尋
   範例：搜尋「愛」、「信心」、「平安」等

Q8: 如何查詢整卷書？
A: 目前需要逐章查詢
   範例：詩篇第 1-150 章
   bible://chapter/unv/Ps/1
   bible://chapter/unv/Ps/2
   ...

Q9: 有沒有行動裝置版本？
A: 本服務是 MCP Server，需要支援 MCP 的客戶端
   如 Claude Desktop、其他 MCP 客戶端

Q10: 如何回報問題或建議？
A: 請透過 GitHub Issues 或專案聯絡方式回報

───────────────────────────────────────────────────────────────────
🎯 快速參考卡
───────────────────────────────────────────────────────────────────

【最常用的 URI】

查經文：
  bible://verse/unv/{書卷}/{章}/{節}
  bible://chapter/unv/{書卷}/{章}

查原文：
  strongs://nt/{編號}  （新約希臘文）
  strongs://ot/{編號}  （舊約希伯來文）

查註釋：
  commentary://{書卷}/{章}/{節}

查資訊：
  info://versions      （版本列表）
  info://books         （書卷列表）
  info://verse_of_day  （今日金句）

【最常用的 Prompt】

新手入門：
  help_guide - 本指南
  uri_demo - URI 教學

快速查詢：
  quick_lookup - 快速查經文

深度研經：
  study_verse - 深入研讀
  word_study - 原文研究
  compare_translations - 譯本比較
  search_topic - 主題查經

【常用版本代碼】

中文：unv, nstrunv, cunp
英文：kjv, niv, esv, nkjv

【常用書卷縮寫】

舊約：Gen, Ex, Ps, Prov, Isa
新約：Matt, John, Rom, 1Cor, Rev

═══════════════════════════════════════════════════════════════════

【立即開始】

現在就試試看吧！

1️⃣ 點擊今日金句：
   info://verse_of_day

2️⃣ 查詢約翰福音 3:16：
   bible://verse/unv/John/3/16

3️⃣ 深入研讀：
   「請幫我深入研讀約翰福音 3:16」

═══════════════════════════════════════════════════════════════════

還有問題嗎？直接問我就對了！

我會盡力幫助您善用這個工具，更好地研讀神的話語。

願神的話語在您生命中發光發熱！
"""

    def _render_quickstart(self) -> str:
        """僅渲染快速入門部分"""
        return """請為我提供 FHL Bible MCP Server 的快速入門指南。

請提供簡潔的快速入門教學，包括：

1. **3 分鐘快速體驗**
   - 第一個操作：查詢單節經文
   - 第二個操作：閱讀完整章節
   - 第三個操作：查看今日金句

2. **您可以做什麼？**
   - 主要功能列表
   - 每個功能的簡短說明

3. **適用場景**
   - 個人靈修
   - 講道準備
   - 小組查經
   - 神學研究

請提供可點擊的實際範例。"""

    def _render_tools(self) -> str:
        """僅渲染工具說明部分"""
        return """請為我提供所有可用工具的詳細說明。

請按類別整理所有工具，包括：

1. **經文查詢工具**
   - get_bible_text
   - get_chapter
   - search_bible

2. **原文研究工具**
   - lookup_strongs
   - get_word_analysis

3. **註釋參考工具**
   - get_commentary

4. **資訊查詢工具**
   - list_versions
   - list_books
   - list_commentaries
   - get_verse_of_day

每個工具請說明：
• 功能描述
• 適用場景
• 使用範例
• 參數說明"""

    def _render_resources(self) -> str:
        """僅渲染 Resource URI 部分"""
        return """請為我說明 Resource URI 的使用方式。

請提供簡潔的 URI 使用說明，包括：

1. **什麼是 Resource URI？**
   - 概念說明
   - 優點列舉

2. **四種 URI 類型**
   - Bible URI（經文）
   - Strong's URI（原文）
   - Commentary URI（註釋）
   - Info URI（資訊）

每種類型請說明：
• 基本格式
• 簡單範例
• 使用場景

詳細教學請參考 uri_demo prompt。"""

    def _render_prompts(self) -> str:
        """僅渲染 Prompt 模板部分"""
        return """請為我介紹所有可用的 Prompt 模板。

請按類別介紹所有 Prompt，包括：

1. **基礎 Prompts**
   - help_guide（本指南）
   - uri_demo（URI 教學）
   - quick_lookup（快速查詢）
   - tool_reference（工具參考）

2. **研經 Prompts**
   - study_verse（深入研讀）
   - search_topic（主題查經）
   - compare_translations（譯本比較）
   - word_study（原文研究）

每個 Prompt 請說明：
• 用途
• 適合對象
• 包含內容
• 使用方式"""

    def _render_tips(self) -> str:
        """僅渲染實用技巧部分"""
        return """請為我提供使用 FHL Bible MCP Server 的實用技巧。

請提供以下實用技巧：

1. **建立個人研經流程**
   - 推薦的研經步驟
   - 每步驟使用的工具

2. **講道準備工作流程**
   - 週間準備計劃
   - 每日重點工作

3. **小組查經帶領**
   - 準備階段
   - 帶領技巧
   - 討論引導

4. **建立個人經文庫**
   - 分類建議
   - 收藏方式
   - 範例 URI

5. **搜尋進階使用**
   - 精確搜尋
   - 分類搜尋
   - 組合搜尋

6. **版本選擇建議**
   - 中文版本推薦
   - 英文版本推薦
   - 對照研究方法"""
