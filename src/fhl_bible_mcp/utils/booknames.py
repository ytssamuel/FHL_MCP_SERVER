"""
書卷名稱轉換工具模組

提供聖經書卷的中英文名稱轉換、書卷編號查詢等功能。
"""

from typing import Dict, Optional, Tuple


# 聖經書卷對照表 (編號, 英文縮寫, 英文全名, 中文簡寫, 中文全名)
BIBLE_BOOKS = [
    # 舊約 (1-39)
    (1, "Gen", "Genesis", "創", "創世記"),
    (2, "Ex", "Exodus", "出", "出埃及記"),
    (3, "Lev", "Leviticus", "利", "利未記"),
    (4, "Num", "Numbers", "民", "民數記"),
    (5, "Deut", "Deuteronomy", "申", "申命記"),
    (6, "Josh", "Joshua", "書", "約書亞記"),
    (7, "Judg", "Judges", "士", "士師記"),
    (8, "Ruth", "Ruth", "得", "路得記"),
    (9, "1Sam", "1 Samuel", "撒上", "撒母耳記上"),
    (10, "2Sam", "2 Samuel", "撒下", "撒母耳記下"),
    (11, "1Kings", "1 Kings", "王上", "列王紀上"),
    (12, "2Kings", "2 Kings", "王下", "列王紀下"),
    (13, "1Chron", "1 Chronicles", "代上", "歷代志上"),
    (14, "2Chron", "2 Chronicles", "代下", "歷代志下"),
    (15, "Ezra", "Ezra", "拉", "以斯拉記"),
    (16, "Neh", "Nehemiah", "尼", "尼希米記"),
    (17, "Esther", "Esther", "斯", "以斯帖記"),
    (18, "Job", "Job", "伯", "約伯記"),
    (19, "Ps", "Psalms", "詩", "詩篇"),
    (20, "Prov", "Proverbs", "箴", "箴言"),
    (21, "Eccl", "Ecclesiastes", "傳", "傳道書"),
    (22, "Song", "Song of Solomon", "歌", "雅歌"),
    (23, "Is", "Isaiah", "賽", "以賽亞書"),
    (24, "Jer", "Jeremiah", "耶", "耶利米書"),
    (25, "Lam", "Lamentations", "哀", "耶利米哀歌"),
    (26, "Ezek", "Ezekiel", "結", "以西結書"),
    (27, "Dan", "Daniel", "但", "但以理書"),
    (28, "Hosea", "Hosea", "何", "何西阿書"),
    (29, "Joel", "Joel", "珥", "約珥書"),
    (30, "Amos", "Amos", "摩", "阿摩司書"),
    (31, "Obad", "Obadiah", "俄", "俄巴底亞書"),
    (32, "Jonah", "Jonah", "拿", "約拿書"),
    (33, "Micah", "Micah", "彌", "彌迦書"),
    (34, "Nahum", "Nahum", "鴻", "那鴻書"),
    (35, "Hab", "Habakkuk", "哈", "哈巴谷書"),
    (36, "Zeph", "Zephaniah", "番", "西番雅書"),
    (37, "Hag", "Haggai", "該", "哈該書"),
    (38, "Zech", "Zechariah", "亞", "撒迦利亞書"),
    (39, "Mal", "Malachi", "瑪", "瑪拉基書"),
    # 新約 (40-66)
    (40, "Matt", "Matthew", "太", "馬太福音"),
    (41, "Mark", "Mark", "可", "馬可福音"),
    (42, "Luke", "Luke", "路", "路加福音"),
    (43, "John", "John", "約", "約翰福音"),
    (44, "Acts", "Acts", "徒", "使徒行傳"),
    (45, "Rom", "Romans", "羅", "羅馬書"),
    (46, "1Cor", "1 Corinthians", "林前", "哥林多前書"),
    (47, "2Cor", "2 Corinthians", "林後", "哥林多後書"),
    (48, "Gal", "Galatians", "加", "加拉太書"),
    (49, "Eph", "Ephesians", "弗", "以弗所書"),
    (50, "Phil", "Philippians", "腓", "腓立比書"),
    (51, "Col", "Colossians", "西", "歌羅西書"),
    (52, "1Thess", "1 Thessalonians", "帖前", "帖撒羅尼迦前書"),
    (53, "2Thess", "2 Thessalonians", "帖後", "帖撒羅尼迦後書"),
    (54, "1Tim", "1 Timothy", "提前", "提摩太前書"),
    (55, "2Tim", "2 Timothy", "提後", "提摩太後書"),
    (56, "Titus", "Titus", "多", "提多書"),
    (57, "Philem", "Philemon", "門", "腓利門書"),
    (58, "Heb", "Hebrews", "來", "希伯來書"),
    (59, "James", "James", "雅", "雅各書"),
    (60, "1Pet", "1 Peter", "彼前", "彼得前書"),
    (61, "2Pet", "2 Peter", "彼後", "彼得後書"),
    (62, "1John", "1 John", "約壹", "約翰一書"),
    (63, "2John", "2 John", "約貳", "約翰二書"),
    (64, "3John", "3 John", "約參", "約翰三書"),
    (65, "Jude", "Jude", "猶", "猶大書"),
    (66, "Rev", "Revelation", "啟", "啟示錄"),
]

# 建立各種索引以加速查詢
_book_id_to_info: Dict[int, Tuple[str, str, str, str]] = {}
_eng_short_to_info: Dict[str, Tuple[int, str, str, str]] = {}
_eng_full_to_info: Dict[str, Tuple[int, str, str, str]] = {}
_chi_short_to_info: Dict[str, Tuple[int, str, str, str]] = {}
_chi_full_to_info: Dict[str, Tuple[int, str, str, str]] = {}

# 初始化索引
for book_id, eng_short, eng_full, chi_short, chi_full in BIBLE_BOOKS:
    _book_id_to_info[book_id] = (eng_short, eng_full, chi_short, chi_full)
    _eng_short_to_info[eng_short.lower()] = (book_id, eng_full, chi_short, chi_full)
    _eng_full_to_info[eng_full.lower()] = (book_id, eng_short, chi_short, chi_full)
    _chi_short_to_info[chi_short] = (book_id, eng_short, eng_full, chi_full)
    _chi_full_to_info[chi_full] = (book_id, eng_short, eng_full, chi_short)


class BookNameConverter:
    """書卷名稱轉換工具類"""

    @staticmethod
    def get_book_id(name: str) -> Optional[int]:
        """
        根據書卷名稱（中文或英文）取得書卷編號

        Args:
            name: 書卷名稱（支援中文簡寫、中文全名、英文縮寫、英文全名）

        Returns:
            書卷編號 (1-66)，若找不到則返回 None
        """
        name_lower = name.lower() if name.isascii() else name

        # 嘗試英文縮寫
        if name_lower in _eng_short_to_info:
            return _eng_short_to_info[name_lower][0]

        # 嘗試英文全名
        if name_lower in _eng_full_to_info:
            return _eng_full_to_info[name_lower][0]

        # 嘗試中文簡寫
        if name in _chi_short_to_info:
            return _chi_short_to_info[name][0]

        # 嘗試中文全名
        if name in _chi_full_to_info:
            return _chi_full_to_info[name][0]

        return None

    @staticmethod
    def get_english_short(name: str) -> Optional[str]:
        """
        根據書卷名稱取得英文縮寫

        Args:
            name: 書卷名稱或編號

        Returns:
            英文縮寫，若找不到則返回 None
        """
        # 如果是數字字串，嘗試當作編號
        if name.isdigit():
            book_id = int(name)
            if book_id in _book_id_to_info:
                return _book_id_to_info[book_id][0]
            return None

        book_id = BookNameConverter.get_book_id(name)
        if book_id and book_id in _book_id_to_info:
            return _book_id_to_info[book_id][0]
        return None

    @staticmethod
    def get_chinese_short(name: str) -> Optional[str]:
        """
        根據書卷名稱取得中文縮寫

        Args:
            name: 書卷名稱或編號

        Returns:
            中文縮寫，若找不到則返回 None
        """
        # 如果是數字字串，嘗試當作編號
        if name.isdigit():
            book_id = int(name)
            if book_id in _book_id_to_info:
                return _book_id_to_info[book_id][2]
            return None

        book_id = BookNameConverter.get_book_id(name)
        if book_id and book_id in _book_id_to_info:
            return _book_id_to_info[book_id][2]
        return None

    @staticmethod
    def get_chinese_full(name: str) -> Optional[str]:
        """
        根據書卷名稱取得中文全名

        Args:
            name: 書卷名稱或編號

        Returns:
            中文全名，若找不到則返回 None
        """
        # 如果是數字字串，嘗試當作編號
        if name.isdigit():
            book_id = int(name)
            if book_id in _book_id_to_info:
                return _book_id_to_info[book_id][3]
            return None

        book_id = BookNameConverter.get_book_id(name)
        if book_id and book_id in _book_id_to_info:
            return _book_id_to_info[book_id][3]
        return None

    @staticmethod
    def get_english_full(name: str) -> Optional[str]:
        """
        根據書卷名稱取得英文全名

        Args:
            name: 書卷名稱或編號

        Returns:
            英文全名，若找不到則返回 None
        """
        # 如果是數字字串，嘗試當作編號
        if name.isdigit():
            book_id = int(name)
            if book_id in _book_id_to_info:
                return _book_id_to_info[book_id][1]
            return None

        book_id = BookNameConverter.get_book_id(name)
        if book_id and book_id in _book_id_to_info:
            return _book_id_to_info[book_id][1]
        return None

    @staticmethod
    def get_all_books() -> list[Dict[str, any]]:
        """
        取得所有書卷的完整資訊

        Returns:
            書卷列表，每個元素包含 id, eng_short, eng_full, chi_short, chi_full
        """
        return [
            {
                "id": book_id,
                "eng_short": eng_short,
                "eng_full": eng_full,
                "chi_short": chi_short,
                "chi_full": chi_full,
            }
            for book_id, eng_short, eng_full, chi_short, chi_full in BIBLE_BOOKS
        ]

    @staticmethod
    def is_old_testament(name: str) -> Optional[bool]:
        """
        判斷是否為舊約書卷

        Args:
            name: 書卷名稱或編號

        Returns:
            True 為舊約，False 為新約，None 表示找不到書卷
        """
        book_id = BookNameConverter.get_book_id(name)
        if book_id is None:
            return None
        return 1 <= book_id <= 39

    @staticmethod
    def is_new_testament(name: str) -> Optional[bool]:
        """
        判斷是否為新約書卷

        Args:
            name: 書卷名稱或編號

        Returns:
            True 為新約，False 為舊約，None 表示找不到書卷
        """
        book_id = BookNameConverter.get_book_id(name)
        if book_id is None:
            return None
        return 40 <= book_id <= 66
