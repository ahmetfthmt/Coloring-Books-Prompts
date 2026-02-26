import json
from pathlib import Path

from toon_prompts import encode_table_to_toon

INPUT_JSON = Path("prompts_full.json")
OUTPUT_TOON = Path("js/prompts_data.toon")
OUTPUT_LEGACY_JS = Path("js/prompts_data.js")


def main():
    if not INPUT_JSON.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_JSON}")

    with INPUT_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    toon_text = encode_table_to_toon(
        data,
        key="prompts",
        fields=("text", "category", "sheet"),
        delimiter="|",
        indent=2,
    )

    OUTPUT_TOON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_TOON.open("w", encoding="utf-8", newline="\n") as f:
        f.write(toon_text)

    # Legacy compatibility output (kept intentionally)
    with OUTPUT_LEGACY_JS.open("w", encoding="utf-8") as f:
        f.write("window.promptsData = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";")

    print(f"✅ Created {OUTPUT_TOON} with {len(data)} prompts (TOON)")
    print(f"✅ Updated legacy file {OUTPUT_LEGACY_JS}")


if __name__ == "__main__":
    main()
