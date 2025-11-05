# @fhl-mcp 功能測試報告（複雜度加強版）

- 日期：2025-11-05
- 環境：macOS, VS Code（zsh）
- 目標：全面測試並壓力覆蓋 @fhl-mcp 可用端點，記錄成功、異常與建議

## 1) 測試覆蓋清單（已調用）
- 版本/書卷
  - list_bible_versions, search_available_versions(has_strongs)
  - get_book_list(全部/NT), get_book_info(使徒行傳)
- 經文/註腳/註釋
  - get_bible_chapter（Acts 12, Acts 13, John 3/TCV）
  - get_bible_verse（約 3:16 UNV+Strongs；Rom 3:21-26 ASV+Strongs）
  - query_verse_citation（羅 3:21-26）
  - get_bible_footnote（書卷ID=43，註腳#1）
  - list_commentaries, get_commentary（約 3:16；羅 3:24 指定 id=3）
  - search_commentary（關鍵字：稱義）
- 原文/字典/檢索
  - get_word_analysis（約 1:1）
  - lookup_strongs（G3056、H430）
  - search_strongs_occurrences（G1344）
  - search_bible（關鍵字：稱義；NT 範圍）
  - search_bible（greek_number：1344）
  - search_bible_advanced（關鍵字：聖靈；range 40-66）
- 有聲聖經
  - list_audio_versions
  - get_audio_bible（詩 23）
  - get_audio_chapter_with_text（詩 23）
- 次經（Apocrypha）
  - list_apocrypha_books
  - get_apocrypha_verse（智 1:1-5）
  - search_apocrypha（關鍵字：智慧）
- 使徒教父（Apostolic Fathers）
  - list_apostolic_fathers_books
  - get_apostolic_fathers_verse（1Clem 1:1-3）
  - search_apostolic_fathers（關鍵字：信心）
- 主題查經/文章
  - get_topic_study（信心；all）
  - list_fhl_article_columns
  - search_fhl_articles（title=信心, limit=5）

## 2) 關鍵結果摘要
- 正常/成功
  - 版本、書卷清單與 Acts 書卷 metadata（id=44）正確。
  - 註腳（TCV, John 3:16 #1）返回正常。
  - 註釋清單返回多來源（如 信望愛站註釋 等）。
  - Bible keyword 搜尋（稱義, NT）返回預期經文（含 徒 13:39、羅 3、5 等）。
  - 有聲聖經：版本清單、詩篇 23 音檔連結（mp3/ogg）正常。
  - 使徒教父：清單、1Clem 1:1-3 取文、關鍵字搜尋（信心）正常（含長篇內容）。
  - 主題查經（Torrey/Naves, 信心）回傳豐富條目。
  - 文章專欄清單與文章搜尋（title=信心）正常（預覽模式）。

- 部分成功/資料錯置（高優先修正）
  - get_bible_chapter：要求 Acts 12/13，實際返回 Genesis 12/13（中英版本皆然）。
  - get_bible_chapter：要求 John 3（TCV2019），實際返回 Genesis 3。
  - get_audio_chapter_with_text：音訊正常，但「對應文字」錯置到 Genesis 23。
  - get_bible_verse：要求 約 3:16（UNV+Strongs），返回內容為 Genesis 3:16（且為希伯來 WH 標記）。
  - get_apocrypha_verse：要求 智 1:1-5，返回內文實為 瑪加伯上 1:1-5（書卷映射錯置）。
  - lookup_strongs：回傳示例說明（Strong 00000）而非 G3056/H430 正規詞條。
  - search_strongs_occurrences：對 G1344 回傳 0 筆，且附帶 00000 範例結構。

- 失敗/錯誤（可重現）
  - search_bible：search_type='greek' 觸發錯誤。正確值應為 'greek_number'。
  - search_bible_advanced：range_start/range_end 傳入整數觸發 "'int' object has no attribute 'isascii'"（推測後端期望字串型別）。
  - get_commentary：指定（約 3:16；羅 3:24, id=3）皆回傳 0 筆（資料源或索引需確認）。
  - get_bible_verse：徒 13:39（UNV+Strongs）回傳 0 筆（與書卷映射錯置應相關）。
  - get_word_analysis：出現 "錯誤: 'N'"（端點/參數相容性需檢查）。

## 3) 代表性輸出擷取（節錄）
- 版本清單：含 unv/kjv/rcuv（皆標示 has_strongs=true）與多語多譯本。
- 書卷清單：NT 書卷含 Acts（id=44），中英短全名齊備。
- 註腳（TCV John 3:16 #1）：顯示「只有獨子」之古卷差異說明（成功）。
- 有聲聖經：詩篇 23 mp3/ogg 連結可播放（成功）。
- 使徒教父：1Clem 1:1-3 中文段落（成功）。
- 主題查經：Torrey/Naves「信心」條目包含大量交叉經文（成功）。

## 4) 問題歸類與重現步驟
- 書卷映射錯置（最高優先）
  - 現象：Acts/John 請求卻返回 Genesis；詩 23 的文字部分映到 創 23；次經請求 智 卻返回 瑪加伯上。
  - 觸發：get_bible_chapter / get_bible_verse / get_audio_chapter_with_text / get_apocrypha_verse。
  - 猜測：後端書卷代碼對應表（中英/短名/ID）或路由 cache 有錯，導致索引偏移。

- 參數型別/枚舉不符
  - greek 原樣值無效，應用 greek_number（官方枚舉約束）。
  - range_start/range_end 建議用字串（"40"、"66"），以避開 isascii 對 int 的錯誤。

- 原文字典/詞形分析異常
  - lookup_strongs 回傳 00000 範例說明而非真詞條（G3056/H430）。
  - search_strongs_occurrences（G1344）回 0 且附 00000 結構。
  - get_word_analysis 出現錯誤 'N'。
  - 猜測：Strong 資料源或版本綁定（UNV/RCUV/KJV）未正確接線。

- 註釋抓取為 0
  - 可能需改用其他 commentary_id，或該節無資料，或索引鍵（書卷/章節）未對齊。

## 5) 建議修正與繞道方案
- 修正
  - 校正書卷映射表（中/英/短/ID）；加上單元測試覆蓋 Acts/John/Psalms/Apocrypha 交叉驗證。
  - audio+text 組合端點需以相同索引來源生成，避免音/文不同步。
  - Strong 詞典與詞形分析串接源檢查（確保 G/H 前綴、譯本對齊）。
  - search_* 端點驗證參數型別（數字以字串傳入），補強錯誤訊息。
  - commentary 以 list_commentaries 的 id 集合回歸測試熱門經節（約 3:16；羅 3:24-26）。

- 繞道
  - 以 citation 解析（如 "徒 13:39"）再回填 book_id/query，或先用 get_book_info 取得標準代碼後再請求。
  - Greek/Hebrew 檢索：使用 greek_number/hebrew_number 並帶上 G/H 前綴（如 G1344），或於 keyword 模式加上「稱義」等中文關鍵字做交叉驗證。
  - 暫用 audio-only 端點，避免取文錯置。

## 6) 後續回歸測試計畫
- 修正書卷映射後，回歸以下最小集合：
  - Acts 12、Acts 13、John 3、Psalms 23（含 audio+text）
  - Apocrypha：智 1、加上一 1 對照
  - Strong：G3056、H430、G1344 詞典與出現次數
  - Commentary：羅 3:21-26（至少 1 筆）
  - 搜尋：search_bible_advanced（range=NT，以字串型別）

## 7) 附錄：重要原始回應（節錄）
- search_bible(keyword=稱義, scope=nt)：含 徒 13:39、羅 3:20,24,28；4:2,11；5:1,9 等。
- list_audio_versions：列出 19 種語系/版本（含 unv/tcv 等）。
- list_commentaries：共 7+ 個來源（CBOL、信望愛站等）。
- 錯誤樣例：
  - "錯誤: Invalid parameter 'search_type': greek ... 應為 'keyword', 'greek_number', 'hebrew_number'"
  - "錯誤: 'int' object has no attribute 'isascii'"（range_* 型別）。

## 8) API 參數準則與正確範例（精簡）
- search_bible
  - search_type 僅支援：'keyword' / 'greek_number' / 'hebrew_number'
  - 範例：
    - keyword：query="稱義", scope="nt", version="unv", limit=10
    - greek_number：query="G1344", scope="nt", version="unv"
    - hebrew_number：query="H430", scope="ot", version="unv"
  - 提示：use_simplified 預設 false；offset 用於分頁。
- search_bible_advanced
  - range_start / range_end 請以字串傳入（如："40"、"66"）。
  - search_type 同上；建議 version="unv"，query="聖靈"，limit=10 作為健全性檢查。
- get_bible_verse / get_bible_chapter
  - include_strong=true 需搭配 has_strongs 版本（unv / kjv / rcuv）。
  - 推薦流程：先以 get_book_info 取得標準名稱/ID → 再組裝請求參數。
- get_audio_chapter_with_text
  - 先以 get_bible_chapter 驗證文字正確性，再取 audio；目前已知音/文可能不同步，修正前建議暫以 audio-only 端點。
- 命名/識別建議
  - 書卷命名優先序（建議）：book_id（或標準短名） > 英文全名 > 中文全名 > 中文短名；實務上以 get_book_info 的結果為準。
  - 次經/使徒教父：請依 list_* 回傳的名稱/abbr 範圍（Apocrypha 101-115；Apostolic Fathers 201-217）。

## 9) 常見錯誤對照與處置
- Invalid parameter 'search_type': greek → 改用 'greek_number'（或 'hebrew_number'）。
- 'int' object has no attribute 'isascii'（search_bible_advanced）→ 將 range_start/range_end 以字串傳入。
- get_word_analysis 出現「錯誤: 'N'」→ 檢查書卷/章節對應與版本；若持續發生，需檢 Strong/原文資料源綁定與端點相容性。
- lookup_strongs / search_strongs_occurrences 回傳 00000 範例 → 確認版本 has_strongs 並檢查字典資料源的對接（G*/H* 前綴不可省略）。
- get_bible_* 返回 Genesis（書卷錯置）→ 優先修補後端映射；修復前請改走 citation 解析 + 標準 book_id 流程，或暫停該端點回歸測試。
- get_commentary 回 0 筆 → 以 list_commentaries 取得可用 id 後，改試其他來源或熱門經節；同時比對入參鍵（書卷鍵名、章節）。

## 10) 回歸測試用例矩陣（最小集）
- 經文/版本
  - Acts 12、Acts 13（UNV/ASV/TCV2019）→ 預期：不再返回 Genesis；章節節數一致。
  - John 3（TCV2019）→ 預期：正確返回約翰福音 3 章。
- Strong/詞典
  - 詞條：G3056、H430、G1344 → 預期：正規詞條內容（非 00000 範例）。
  - 出現次數：G1344（NT 範圍）→ 預期：返回至少羅馬書/使徒行傳等相關處。
- 註腳/註釋
  - 註腳：John 3:16（TCV #1）→ 預期：持續可用。
  - 註釋：Romans 3:21-26 → 預期：至少 1 筆來源成功返回。
- Audio + Text
  - Psalm 23（unv）→ 預期：音檔可播；文字為詩篇 23（非創 23）。
- 次經/教父
  - Apocrypha：智 1:1-5 與 加上一 1:1-5 → 預期：不再交叉錯置。
  - Apostolic Fathers：1Clem 1:1-3 與 search("信心") → 預期：持續可用。
- 搜尋
  - search_bible_advanced：query="聖靈"、range_start="40"、range_end="66" → 預期：不再出現 isascii 錯誤，且結果集中於新約。

## 11) 自動化測試建議（非程式碼，流程描述）
- 結構驗證：對每次回應斷言版本代碼、書卷/章節、記錄數量、上一/下一章導航皆合理。
- 內容護欄：若請求 Acts/John 卻出現 Genesis，直接標記 P0 並中止後續相依測試。
- 多來源一致性：對相同經節以 2-3 個版本交叉比對節數與大綱標題是否一致。
- Strong/詞典串接：先驗證 has_strongs 版本，再發出 include_strong=true；出現 00000 時直接標記資料源對接故障。
- 搜尋參數健全性：針對 search_type、range_* 型別施作枚舉/型別回歸測試。

## 12) 未決議題與追蹤清單
- 書卷映射表：來源表、快取層、路由層三處需逐一比對；修補後需批量回歸（Acts/John/Psalms/Apocrypha）。
- Strong/詞形分析：資料源與版本（unv/kjv/rcuv）對齊；確保 G/H 前綴路徑一致；端點共同測。
- get_word_analysis 錯誤 'N'：蒐集最小重現範例（書卷/章節/版本/參數），定位觸發點。
- 註釋索引：以熱門經節驗證多來源（id 列表），若持續為 0，檢查鍵名（書卷對映）與資料匯入狀態。
- audio+text 同步：音訊路徑 OK，但文字索引錯置；修復前明示文件採用 audio-only。
