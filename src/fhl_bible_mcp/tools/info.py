"""
資訊查詢 MCP Tools

提供聖經版本列表、註釋書列表、書卷列表等資訊查詢的 MCP 工具函數。
"""

from typing import Optional, Dict, Any, List
from ..api.endpoints import FHLAPIEndpoints
from ..utils.booknames import BookNameConverter


async def list_bible_versions(
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    列出所有可用的聖經版本

    Args:
        use_simplified: 是否使用簡體中文

    Returns:
        版本列表字典
    """
    async with FHLAPIEndpoints() as api:
        response = await api.get_bible_versions()

    versions = []
    for record in response["record"]:
        # 判斷聖經範圍
        testament = "both"
        if record["ntonly"] == 1:
            testament = "nt_only"
        elif record["otonly"] == 1:
            testament = "ot_only"

        # 判斷特殊字型需求
        special_font = "none"
        if record["proc"] == 1:
            special_font = "greek"
        elif record["proc"] == 2:
            special_font = "hebrew"
        elif record["proc"] == 3:
            special_font = "roman"
        elif record["proc"] == 4:
            special_font = "openhan"

        versions.append(
            {
                "code": record["book"],
                "name": record["cname"],
                "has_strongs": record["strong"] == 1,
                "testament": testament,
                "special_font": special_font,
                "can_download": record.get("candownload", 0) == 1,
                "version": record.get("version", "") or "",
            }
        )

    return {
        "total_count": len(versions),
        "versions": versions,
    }


async def get_book_list(
    testament: Optional[str] = None,
) -> Dict[str, Any]:
    """
    取得聖經書卷列表

    Args:
        testament: 指定約別（可選）
            - None: 全部書卷
            - "OT": 僅舊約
            - "NT": 僅新約

    Returns:
        書卷列表字典
    """
    # 從本地資料取得書卷列表
    all_books = BookNameConverter.get_all_books()

    # 根據約別篩選
    if testament:
        testament_upper = testament.upper()
        if testament_upper == "OT":
            books = [book for book in all_books if 1 <= book["id"] <= 39]
        elif testament_upper == "NT":
            books = [book for book in all_books if 40 <= book["id"] <= 66]
        else:
            books = all_books
    else:
        books = all_books

    return {
        "total_count": len(books),
        "testament": testament or "all",
        "books": books,
    }


async def get_book_info(
    book: str,
) -> Dict[str, Any]:
    """
    取得特定書卷的詳細資訊

    Args:
        book: 書卷名稱（支援中文或英文，完整或縮寫）

    Returns:
        書卷資訊字典
    """
    book_id = BookNameConverter.get_book_id(book)
    if not book_id:
        from ..utils.errors import InvalidParameterError
        raise InvalidParameterError(f"找不到書卷: {book}")

    eng_short = BookNameConverter.get_english_short(book)
    eng_full = BookNameConverter.get_english_full(book)
    chi_short = BookNameConverter.get_chinese_short(book)
    chi_full = BookNameConverter.get_chinese_full(book)
    is_ot = BookNameConverter.is_old_testament(book)

    return {
        "id": book_id,
        "testament": "OT" if is_ot else "NT",
        "names": {
            "english": {
                "short": eng_short,
                "full": eng_full,
            },
            "chinese": {
                "short": chi_short,
                "full": chi_full,
            },
        },
    }


async def search_available_versions(
    has_strongs: Optional[bool] = None,
    testament: Optional[str] = None,
    use_simplified: bool = False,
) -> Dict[str, Any]:
    """
    根據條件篩選聖經版本

    Args:
        has_strongs: 是否必須包含 Strong's Number（可選）
        testament: 約別篩選 "OT", "NT", "both"（可選）
        use_simplified: 是否使用簡體中文

    Returns:
        篩選後的版本列表
    """
    # 取得所有版本
    all_versions = await list_bible_versions(use_simplified)

    # 篩選
    filtered_versions = all_versions["versions"]

    if has_strongs is not None:
        filtered_versions = [
            v for v in filtered_versions
            if v["has_strongs"] == has_strongs
        ]

    if testament:
        testament_upper = testament.upper()
        if testament_upper in ["OT", "NT"]:
            filtered_versions = [
                v for v in filtered_versions
                if v["testament"] in ["both", f"{testament_upper.lower()}_only"]
            ]

    return {
        "total_count": len(filtered_versions),
        "filters": {
            "has_strongs": has_strongs,
            "testament": testament,
        },
        "versions": filtered_versions,
    }
