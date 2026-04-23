import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Name of the JSON data file.
# It is assumed to be in the same directory as this Python script.
DATA_FILE = Path(__file__).with_name("crops_query.json")


def load_data(path: Path = DATA_FILE) -> Dict[str, Any]:
    """
    Load the JSON dataset and return it as a Python dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_by_id(data: Dict[str, Any], crop_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a single crop by its ID.
    Example: tomato, mint, sugar-cane
    """
    for record in data["records"]:
        if record["id"] == crop_id:
            return record
    return None


def find_by_common_name(data: Dict[str, Any], name: str) -> List[Dict[str, Any]]:
    """
    Find crops by exact match of common_name.
    Example: Tomato, Mint
    """
    q = name.lower().strip()
    return [r for r in data["records"] if r["common_name"].lower() == q]


def find_by_scientific_name(data: Dict[str, Any], scientific_name: str) -> List[Dict[str, Any]]:
    """
    Find crops by exact match of scientific_name.
    Example: Solanum lycopersicum
    """
    q = scientific_name.lower().strip()
    return [r for r in data["records"] if (r["scientific_name"] or "").lower() == q]


def filter_with_gdd(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Return crops that have GDD data.
    """
    return [r for r in data["records"] if r["gdd"]["variants"]]


def filter_without_gdd(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Return crops that do NOT have GDD data.
    """
    return [r for r in data["records"] if not r["gdd"]["variants"]]


def filter_by_gdd_variant(data: Dict[str, Any], variant_name: str) -> List[Dict[str, Any]]:
    """
    Filter crops by a specific GDD variant.
    Example: long_season, market, common, 1st_year
    """
    q = variant_name.lower().strip()
    results = []

    for record in data["records"]:
        for variant in record["gdd"]["variants"]:
            if variant["variant"].lower() == q:
                results.append(record)
                break

    return results


def filter_by_gdd_total_range(
    data: Dict[str, Any],
    min_total: Optional[float] = None,
    max_total: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Filter crops by total GDD range.
    Only matching variants are returned.
    """
    results = []

    for record in data["records"]:
        matched_variants = []

        for variant in record["gdd"]["variants"]:
            total = variant.get("total_c")
            if total is None:
                continue

            if min_total is not None and total < min_total:
                continue
            if max_total is not None and total > max_total:
                continue

            matched_variants.append(variant)

        if matched_variants:
            copied = dict(record)
            copied["gdd"] = {
                "unit": record["gdd"]["unit"],
                "variants": matched_variants
            }
            results.append(copied)

    return results


def search_contains(data: Dict[str, Any], text: str) -> List[Dict[str, Any]]:
    """
    Search for a text inside multiple fields:
    id, slug, common_name, scientific_name, category, subcategory
    """
    q = text.lower().strip()
    results = []

    for record in data["records"]:
        fields = [
            record.get("id", ""),
            record.get("slug", ""),
            record.get("common_name", ""),
            record.get("scientific_name", "") or "",
            record.get("category", ""),
            record.get("subcategory", "")
        ]

        if any(q in str(field).lower() for field in fields):
            results.append(record)

    return results


def print_crop(record: Dict[str, Any]) -> None:
    """
    Print a single crop record in a readable format.
    """
    print(f"\n🌱 {record['common_name']}")
    print(f"ID: {record['id']}")
    print(f"Scientific name: {record['scientific_name']}")
    print(f"Category: {record['category']}")
    print(f"Subcategory: {record['subcategory']}")
    print(f"Temperature base: {record['temperature']['base_c']} °C")
    print(f"Temperature upper: {record['temperature']['upper_c']} °C")

    if record["gdd"]["variants"]:
        print(f"GDD unit: {record['gdd']['unit']}")
        print("GDD variants:")
        for variant in record["gdd"]["variants"]:
            print(f"  - Variant: {variant.get('variant', 'N/A')}")
            print(f"    initial_c: {variant.get('initial_c', 'N/A')}")
            print(f"    develop_c: {variant.get('develop_c', 'N/A')}")
            print(f"    mid_season_c: {variant.get('mid_season_c', 'N/A')}")
            print(f"    harvest_late_c: {variant.get('harvest_late_c', 'N/A')}")
            print(f"    total_c: {variant.get('total_c', 'N/A')}")
            if "note" in variant:
                print(f"    note: {variant['note']}")
    else:
        print("GDD: No data")


def print_results(results: List[Dict[str, Any]]) -> None:
    """
    Print all matched results.
    """
    if not results:
        print("No results found.")
        return

    print(f"\nFound {len(results)} result(s).")
    for record in results:
        print_crop(record)


if __name__ == "__main__":
    data = load_data()

    # If user provides a query argument via CLI
    # Example:
    # python crops_query.py tomato
    if len(sys.argv) > 1:
        query = sys.argv[1]

        # First try exact ID match
        by_id = get_by_id(data, query)
        if by_id:
            print_crop(by_id)
            sys.exit(0)

        # Otherwise perform search
        results = search_contains(data, query)
        print_results(results)

    else:
        # Show usage instructions if no argument is provided
        print("Usage examples:")
        print("  python crops_query.py tomato")
        print("  python crops_query.py mint")
        print("  python crops_query.py sorghum")
        print("  python crops_query.py citrus")
