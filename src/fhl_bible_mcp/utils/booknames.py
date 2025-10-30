"""
書卷名稱轉換工具模組

提供聖經書卷的中英文名稱轉換、書卷編號查詢、繁簡轉換、容錯查找等功能。
"""

from typing import Dict, Optional, Tuple, List
import re


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

# 繁簡體對照表
SIMPLIFIED_TO_TRADITIONAL = {
    # 常見繁簡對照
    "创": "創", "记": "記", "出": "出", "埃": "埃", "及": "及",
    "利": "利", "未": "未", "民": "民", "数": "數", "申": "申",
    "命": "命", "书": "書", "约": "約", "亚": "亞", "士": "士",
    "师": "師", "得": "得", "撒": "撒", "母": "母", "耳": "耳",
    "上": "上", "下": "下", "王": "王", "列": "列", "纪": "紀",
    "代": "代", "历": "歷", "志": "志", "拉": "拉", "斯": "斯",
    "尼": "尼", "希": "希", "米": "米", "以": "以", "帖": "帖",
    "伯": "伯", "诗": "詩", "篇": "篇", "箴": "箴", "言": "言",
    "传": "傳", "道": "道", "雅": "雅", "歌": "歌", "赛": "賽",
    "耶": "耶", "利": "利", "哀": "哀", "结": "結", "但": "但",
    "理": "理", "何": "何", "西": "西", "阿": "阿", "珥": "珥",
    "摩": "摩", "俄": "俄", "巴": "巴", "底": "底", "拿": "拿",
    "弥": "彌", "迦": "迦", "鸿": "鴻", "那": "那", "哈": "哈",
    "谷": "谷", "番": "番", "该": "該", "撒": "撒", "加": "加",
    "玛": "瑪", "太": "太", "福": "福", "音": "音", "可": "可",
    "路": "路", "徒": "徒", "行": "行", "罗": "羅", "马": "馬",
    "林": "林", "前": "前", "后": "後", "弗": "弗", "所": "所",
    "腓": "腓", "立": "立", "比": "比", "西": "西", "帖": "帖",
    "撒": "撒", "罗": "羅", "尼": "尼", "提": "提", "多": "多",
    "门": "門", "来": "來", "伯": "伯", "彼": "彼", "壹": "壹",
    "贰": "貳", "叁": "參", "犹": "猶", "大": "大", "启": "啟",
    "示": "示", "录": "錄", "歌": "歌", "罗": "羅", "哥": "哥",
}

TRADITIONAL_TO_SIMPLIFIED = {v: k for k, v in SIMPLIFIED_TO_TRADITIONAL.items()}

# 書卷別名和縮寫
BOOK_ALIASES = {
    # 創世記
    "创": "創", "创世": "創", "创世记": "創世記",
    # 出埃及記
    "出埃及": "出", "出埃及记": "出埃及記",
    # 利未記
    "利未记": "利未記",
    # 民數記
    "民数": "民", "民数记": "民數記",
    # 申命記
    "申命": "申", "申命记": "申命記",
    # 約書亞記
    "约书亚": "書", "约书亚记": "約書亞記", "书亚记": "約書亞記",
    # 士師記
    "士师": "士", "士师记": "士師記",
    # 路得記
    "路得": "得", "路得记": "路得記",
    # 撒母耳記上
    "撒上": "撒上", "撒母耳上": "撒上", "撒母耳记上": "撒母耳記上",
    "sam1": "撒上", "1sam": "撒上", "1 sam": "撒上",
    # 撒母耳記下
    "撒下": "撒下", "撒母耳下": "撒下", "撒母耳记下": "撒母耳記下",
    "sam2": "撒下", "2sam": "撒下", "2 sam": "撒下",
    # 列王紀上
    "王上": "王上", "列王记上": "列王紀上", "kings1": "王上", "1kings": "王上",
    # 列王紀下
    "王下": "王下", "列王记下": "列王紀下", "kings2": "王下", "2kings": "王下",
    # 歷代志上
    "代上": "代上", "历代志上": "歷代志上", "chron1": "代上", "1chron": "代上",
    # 歷代志下
    "代下": "代下", "历代志下": "歷代志下", "chron2": "代下", "2chron": "代下",
    # 以斯拉記
    "以斯拉": "拉", "以斯拉记": "以斯拉記",
    # 尼希米記
    "尼希米": "尼", "尼希米记": "尼希米記",
    # 以斯帖記
    "以斯帖": "斯", "以斯帖记": "以斯帖記",
    # 約伯記
    "约伯": "伯", "约伯记": "約伯記",
    # 詩篇
    "诗": "詩", "诗篇": "詩篇",
    # 箴言
    "箴": "箴", "箴言": "箴言",
    # 傳道書
    "传": "傳", "传道": "傳", "传道书": "傳道書",
    # 雅歌
    "雅": "歌", "雅歌": "雅歌", "歌中歌": "雅歌",
    # 以賽亞書
    "以赛亚": "賽", "以赛亚书": "以賽亞書", "赛亚书": "以賽亞書",
    # 耶利米書
    "耶利米": "耶", "耶利米书": "耶利米書",
    # 耶利米哀歌
    "哀": "哀", "哀歌": "哀", "耶利米哀歌": "耶利米哀歌",
    # 以西結書
    "以西结": "結", "以西结书": "以西結書", "结书": "以西結書",
    # 但以理書
    "但以理": "但", "但以理书": "但以理書",
    # 何西阿書
    "何西阿": "何", "何西阿书": "何西阿書",
    # 約珥書
    "约珥": "珥", "约珥书": "約珥書",
    # 阿摩司書
    "阿摩司": "摩", "阿摩司书": "阿摩司書",
    # 俄巴底亞書
    "俄巴底亚": "俄", "俄巴底亚书": "俄巴底亞書",
    # 約拿書
    "约拿": "拿", "约拿书": "約拿書",
    # 彌迦書
    "弥迦": "彌", "弥迦书": "彌迦書",
    # 那鴻書
    "那鸿": "鴻", "那鸿书": "那鴻書",
    # 哈巴谷書
    "哈巴谷": "哈", "哈巴谷书": "哈巴谷書",
    # 西番雅書
    "西番雅": "番", "西番雅书": "西番雅書",
    # 哈該書
    "哈该": "該", "哈该书": "哈該書",
    # 撒迦利亞書
    "撒迦利亚": "亞", "撒迦利亚书": "撒迦利亞書", "亚书": "撒迦利亞書",
    # 瑪拉基書
    "玛拉基": "瑪", "玛拉基书": "瑪拉基書",
    # 馬太福音
    "马太": "太", "马太福音": "馬太福音", "太福音": "馬太福音",
    "mt": "太", "mat": "太", "matthew": "太",
    # 馬可福音
    "马可": "可", "马可福音": "馬可福音", "可福音": "馬可福音",
    "mk": "可", "mar": "可", "mark": "可",
    # 路加福音
    "路加": "路", "路加福音": "路加福音", "路福音": "路加福音",
    "lk": "路", "luk": "路", "luke": "路",
    # 約翰福音
    "约翰": "約", "约翰福音": "約翰福音", "约福音": "約翰福音",
    "jn": "約", "joh": "約", "john": "約",
    # 使徒行傳
    "使徒": "徒", "使徒行传": "使徒行傳", "行传": "使徒行傳",
    "act": "徒", "acts": "徒",
    # 羅馬書
    "罗马": "羅", "罗马书": "羅馬書",
    "rom": "羅", "romans": "羅",
    # 哥林多前書
    "林前": "林前", "哥林多前": "林前", "哥林多前书": "哥林多前書",
    "cor1": "林前", "1cor": "林前", "1 cor": "林前",
    # 哥林多後書
    "林后": "林後", "哥林多后": "林後", "哥林多后书": "哥林多後書",
    "cor2": "林後", "2cor": "林後", "2 cor": "林後",
    # 加拉太書
    "加拉太": "加", "加拉太书": "加拉太書",
    "gal": "加", "galatians": "加",
    # 以弗所書
    "以弗所": "弗", "以弗所书": "以弗所書", "弗所书": "以弗所書",
    "eph": "弗", "ephesians": "弗",
    # 腓立比書
    "腓立比": "腓", "腓立比书": "腓立比書",
    "phi": "腓", "phil": "腓", "philippians": "腓",
    # 歌羅西書
    "歌罗西": "西", "歌罗西书": "歌羅西書", "西书": "歌羅西書",
    "col": "西", "colossians": "西",
    # 帖撒羅尼迦前書
    "帖前": "帖前", "帖撒罗尼迦前": "帖前", "帖撒罗尼迦前书": "帖撒羅尼迦前書",
    "thes1": "帖前", "1thess": "帖前", "1 thess": "帖前",
    # 帖撒羅尼迦後書
    "帖后": "帖後", "帖撒罗尼迦后": "帖後", "帖撒罗尼迦后书": "帖撒羅尼迦後書",
    "thes2": "帖後", "2thess": "帖後", "2 thess": "帖後",
    # 提摩太前書
    "提前": "提前", "提摩太前": "提前", "提摩太前书": "提摩太前書",
    "tim1": "提前", "1tim": "提前", "1 tim": "提前",
    # 提摩太後書
    "提后": "提後", "提摩太后": "提後", "提摩太后书": "提摩太後書",
    "tim2": "提後", "2tim": "提後", "2 tim": "提後",
    # 提多書
    "提多": "多", "提多书": "提多書",
    "tit": "多", "titus": "多",
    # 腓利門書
    "腓利门": "門", "腓利门书": "腓利門書", "门书": "腓利門書",
    "phm": "門", "philem": "門", "philemon": "門",
    # 希伯來書
    "希伯来": "來", "希伯来书": "希伯來書", "来书": "希伯來書",
    "heb": "來", "hebrews": "來",
    # 雅各書
    "雅各": "雅", "雅各书": "雅各書",
    "jas": "雅", "jam": "雅", "james": "雅",
    # 彼得前書
    "彼前": "彼前", "彼得前": "彼前", "彼得前书": "彼得前書",
    "pet1": "彼前", "1pet": "彼前", "1 pet": "彼前",
    # 彼得後書
    "彼后": "彼後", "彼得后": "彼後", "彼得后书": "彼得後書",
    "pet2": "彼後", "2pet": "彼後", "2 pet": "彼後",
    # 約翰一書
    "约壹": "約壹", "约翰一": "約壹", "约翰一书": "約翰一書", "约翰1书": "約翰一書",
    "joh1": "約壹", "1john": "約壹", "1 john": "約壹",
    # 約翰二書
    "约贰": "約貳", "约翰二": "約貳", "约翰二书": "約翰二書", "约翰2书": "約翰二書",
    "joh2": "約貳", "2john": "約貳", "2 john": "約貳",
    # 約翰三書
    "约叁": "約參", "约翰三": "約參", "约翰三书": "約翰三書", "约翰3书": "約翰三書",
    "joh3": "約參", "3john": "約參", "3 john": "約參",
    # 猶大書
    "犹大": "猶", "犹大书": "猶大書",
    "jud": "猶", "jude": "猶",
    # 啟示錄
    "启": "啟", "启示": "啟", "启示录": "啟示錄",
    "rev": "啟", "revelation": "啟",
}

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
        # 如果是數字字串,直接轉換
        if isinstance(name, str) and name.isdigit():
            book_id = int(name)
            if 1 <= book_id <= 66:
                return 1 <= book_id <= 39
            return None
        
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
        # 如果是數字字串,直接轉換
        if isinstance(name, str) and name.isdigit():
            book_id = int(name)
            if 1 <= book_id <= 66:
                return 40 <= book_id <= 66
            return None
        
        book_id = BookNameConverter.get_book_id(name)
        if book_id is None:
            return None
        return 40 <= book_id <= 66

    @staticmethod
    def simplified_to_traditional(text: str) -> str:
        """
        簡體中文轉繁體中文

        Args:
            text: 簡體中文文字

        Returns:
            繁體中文文字
        """
        result = []
        for char in text:
            result.append(SIMPLIFIED_TO_TRADITIONAL.get(char, char))
        return "".join(result)

    @staticmethod
    def traditional_to_simplified(text: str) -> str:
        """
        繁體中文轉簡體中文

        Args:
            text: 繁體中文文字

        Returns:
            簡體中文文字
        """
        result = []
        for char in text:
            result.append(TRADITIONAL_TO_SIMPLIFIED.get(char, char))
        return "".join(result)

    @staticmethod
    def normalize_book_name(name: str) -> Optional[str]:
        """
        標準化書卷名稱,支援各種別名和縮寫
        
        Args:
            name: 書卷名稱 (可以是別名、縮寫、英文、簡體等)
            
        Returns:
            標準化的中文簡寫,若找不到則返回 None
        """
        if not name:
            return None
            
        # 去除空格並轉小寫 (如果是英文)
        name = name.strip()
        name_lower = name.lower() if name.isascii() else name
        
        # 1. 嘗試直接查找
        result = BookNameConverter.get_chinese_short(name)
        if result:
            return result
        
        # 2. 嘗試從別名表查找
        if name_lower in BOOK_ALIASES:
            alias_target = BOOK_ALIASES[name_lower]
            result = BookNameConverter.get_chinese_short(alias_target)
            if result:
                return result
        
        # 3. 嘗試簡轉繁後查找
        traditional = BookNameConverter.simplified_to_traditional(name)
        result = BookNameConverter.get_chinese_short(traditional)
        if result:
            return result
            
        # 4. 嘗試從別名表查找 (簡轉繁後)
        if traditional in BOOK_ALIASES:
            alias_target = BOOK_ALIASES[traditional]
            result = BookNameConverter.get_chinese_short(alias_target)
            if result:
                return result
        
        # 5. 嘗試移除數字後查找 (如 "1kings" -> "kings")
        if name_lower and name_lower[0].isdigit():
            without_number = name_lower[1:].strip()
            result = BookNameConverter.normalize_book_name(without_number)
            if result:
                return result
        
        return None

    @staticmethod
    def fuzzy_search(query: str, limit: int = 5) -> List[Dict[str, any]]:
        """
        模糊搜尋書卷名稱
        
        Args:
            query: 搜尋關鍵字
            limit: 返回結果數量上限
            
        Returns:
            匹配的書卷列表,按相似度排序
        """
        if not query:
            return []
        
        query = query.strip().lower()
        results = []
        
        # 先嘗試精確匹配
        exact_match = BookNameConverter.normalize_book_name(query)
        if exact_match:
            book_id = BookNameConverter.get_book_id(exact_match)
            if book_id:
                eng_short, eng_full, chi_short, chi_full = _book_id_to_info[book_id]
                return [{
                    "id": book_id,
                    "eng_short": eng_short,
                    "eng_full": eng_full,
                    "chi_short": chi_short,
                    "chi_full": chi_full,
                    "score": 100,
                    "match_type": "exact"
                }]
        
        # 模糊匹配
        for book_id, eng_short, eng_full, chi_short, chi_full in BIBLE_BOOKS:
            score = 0
            match_type = "none"
            
            # 檢查各種匹配
            if query in eng_short.lower():
                score = 80
                match_type = "eng_short_contains"
            elif query in eng_full.lower():
                score = 70
                match_type = "eng_full_contains"
            elif query in chi_short:
                score = 90
                match_type = "chi_short_contains"
            elif query in chi_full:
                score = 85
                match_type = "chi_full_contains"
            # 簡體匹配
            elif query in BookNameConverter.traditional_to_simplified(chi_short):
                score = 85
                match_type = "chi_short_simplified"
            elif query in BookNameConverter.traditional_to_simplified(chi_full):
                score = 80
                match_type = "chi_full_simplified"
            # 開頭匹配
            elif eng_short.lower().startswith(query):
                score = 75
                match_type = "eng_short_starts"
            elif eng_full.lower().startswith(query):
                score = 65
                match_type = "eng_full_starts"
            elif chi_short.startswith(query):
                score = 85
                match_type = "chi_short_starts"
            elif chi_full.startswith(query):
                score = 80
                match_type = "chi_full_starts"
            
            if score > 0:
                results.append({
                    "id": book_id,
                    "eng_short": eng_short,
                    "eng_full": eng_full,
                    "chi_short": chi_short,
                    "chi_full": chi_full,
                    "score": score,
                    "match_type": match_type
                })
        
        # 按分數排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]

    @staticmethod
    def get_book_info(name: str) -> Optional[Dict[str, any]]:
        """
        取得書卷完整資訊
        
        Args:
            name: 書卷名稱或編號
            
        Returns:
            包含完整書卷資訊的字典,若找不到則返回 None
        """
        book_id = None
        
        # 如果是數字,直接當作 ID
        if isinstance(name, int) or (isinstance(name, str) and name.isdigit()):
            book_id = int(name)
        else:
            # 先標準化名稱
            normalized = BookNameConverter.normalize_book_name(name)
            if normalized:
                book_id = BookNameConverter.get_book_id(normalized)
            else:
                # 嘗試直接查找
                book_id = BookNameConverter.get_book_id(name)
        
        if book_id and book_id in _book_id_to_info:
            eng_short, eng_full, chi_short, chi_full = _book_id_to_info[book_id]
            return {
                "id": book_id,
                "eng_short": eng_short,
                "eng_full": eng_full,
                "chi_short": chi_short,
                "chi_full": chi_full,
                "testament": "OT" if book_id <= 39 else "NT",
                "testament_name": "舊約" if book_id <= 39 else "新約"
            }
        
        return None

    @staticmethod
    def parse_reference(reference: str) -> Optional[Dict[str, any]]:
        """
        解析經文引用格式
        
        支援格式:
        - "約3:16"
        - "John 3:16"
        - "創世記 1:1"
        - "Genesis 1:1-5"
        - "太 5:3-10"
        
        Args:
            reference: 經文引用字串
            
        Returns:
            包含 book, chapter, verse_start, verse_end 的字典,若解析失敗則返回 None
        """
        if not reference:
            return None
        
        reference = reference.strip()
        
        # 嘗試匹配 "書卷名 章:節" 或 "書卷名 章:節-節" 格式
        # 支援中英文書卷名
        pattern = r'^(.+?)\s*(\d+):(\d+)(?:-(\d+))?$'
        match = re.match(pattern, reference)
        
        if match:
            book_name = match.group(1).strip()
            chapter = int(match.group(2))
            verse_start = int(match.group(3))
            verse_end = int(match.group(4)) if match.group(4) else verse_start
            
            # 標準化書卷名
            normalized_book = BookNameConverter.normalize_book_name(book_name)
            if not normalized_book:
                # 嘗試模糊搜尋
                fuzzy_results = BookNameConverter.fuzzy_search(book_name, limit=1)
                if fuzzy_results:
                    normalized_book = fuzzy_results[0]["chi_short"]
                else:
                    return None
            
            book_info = BookNameConverter.get_book_info(normalized_book)
            if book_info:
                return {
                    "book": normalized_book,
                    "book_id": book_info["id"],
                    "book_full": book_info["chi_full"],
                    "chapter": chapter,
                    "verse_start": verse_start,
                    "verse_end": verse_end,
                    "original_input": reference
                }
        
        return None
