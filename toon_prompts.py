import re
from typing import Iterable, Sequence


def _escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def _unescape(value: str) -> str:
    out = []
    i = 0
    while i < len(value):
        ch = value[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue

        if i + 1 >= len(value):
            raise ValueError("Geçersiz escape dizisi: sondaki tek ters slash")

        nxt = value[i + 1]
        mapping = {"\\": "\\", '"': '"', "n": "\n", "r": "\r", "t": "\t"}
        if nxt not in mapping:
            raise ValueError(f"Geçersiz escape dizisi: \\{nxt}")
        out.append(mapping[nxt])
        i += 2

    return "".join(out)


def _needs_quote(value: str, delimiter: str) -> bool:
    if value == "":
        return True
    if value != value.strip():
        return True

    lowered = value.lower()
    if lowered in {"true", "false", "null"}:
        return True

    if re.fullmatch(r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?", value, re.IGNORECASE):
        return True
    if re.fullmatch(r"-?0\d+", value):
        return True

    structural_chars = {":", '"', "\\", "[", "]", "{", "}", "\n", "\r", "\t", delimiter}
    if any(ch in value for ch in structural_chars):
        return True

    if value == "-" or value.startswith("-"):
        return True

    return False


def _encode_cell(value: str, delimiter: str) -> str:
    text = "" if value is None else str(value)
    if _needs_quote(text, delimiter):
        return f'"{_escape(text)}"'
    return text


def _decode_cell(token: str) -> str:
    token = token.strip()
    if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
        return _unescape(token[1:-1])
    if token.startswith('"') and not token.endswith('"'):
        raise ValueError("Kapanmayan tırnaklı değer")
    return token


def _split_row(line: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    in_quotes = False
    i = 0

    while i < len(line):
        ch = line[i]
        if ch == '"':
            current.append(ch)
            in_quotes = not in_quotes
            i += 1
            continue

        if ch == "\\" and in_quotes:
            if i + 1 >= len(line):
                raise ValueError("Geçersiz escape dizisi")
            current.append(ch)
            current.append(line[i + 1])
            i += 2
            continue

        if ch == delimiter and not in_quotes:
            parts.append("".join(current).strip())
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    if in_quotes:
        raise ValueError("Kapanmayan tırnaklı değer")

    parts.append("".join(current).strip())
    return parts


def encode_table_to_toon(
    rows: Iterable[dict],
    key: str,
    fields: Sequence[str],
    delimiter: str = "|",
    indent: int = 2,
) -> str:
    rows = list(rows)
    if delimiter not in {"|", "\t", ","}:
        raise ValueError("Delimiter sadece '|', '\\t' veya ',' olabilir")

    delim_suffix = "" if delimiter == "," else delimiter
    delim_for_fields = delimiter

    field_text = delim_for_fields.join(fields)
    header = f"{key}[{len(rows)}{delim_suffix}]{{{field_text}}}:"

    lines = [header]
    prefix = " " * indent

    for row in rows:
        encoded = [_encode_cell(row.get(field, ""), delimiter) for field in fields]
        lines.append(f"{prefix}{delimiter.join(encoded)}")

    return "\n".join(lines)


def parse_table_toon(
    text: str,
    expected_key: str,
    expected_fields: Sequence[str],
    strict: bool = True,
) -> list[dict]:
    lines = [ln for ln in text.splitlines() if ln.strip() != ""]
    if not lines:
        return []

    header = lines[0].strip()
    match = re.fullmatch(rf"{re.escape(expected_key)}\[(\d+)([|\t]?)\]\{{(.+)\}}:", header)
    if not match:
        raise ValueError("TOON header beklenen formatta değil")

    declared_count = int(match.group(1))
    delimiter_symbol = match.group(2)
    delimiter = delimiter_symbol if delimiter_symbol else ","

    raw_fields = match.group(3)
    fields = _split_row(raw_fields, delimiter)
    parsed_fields = [_decode_cell(token) for token in fields]
    if list(parsed_fields) != list(expected_fields):
        raise ValueError(f"Beklenen alanlar {list(expected_fields)}, gelen {parsed_fields}")

    data_lines = lines[1:]
    if strict and len(data_lines) != declared_count:
        raise ValueError(f"Satır sayısı uyuşmuyor. Beklenen {declared_count}, gelen {len(data_lines)}")

    output: list[dict] = []
    for raw in data_lines:
        if strict:
            if raw.startswith("\t"):
                raise ValueError("Strict mode: girinti tab olamaz")
            if len(raw) - len(raw.lstrip(" ")) != 2:
                raise ValueError("Strict mode: satır girintisi 2 boşluk olmalı")

        row_text = raw.lstrip(" ")
        parts = _split_row(row_text, delimiter)
        if strict and len(parts) != len(expected_fields):
            raise ValueError(
                f"Satır kolon sayısı uyuşmuyor. Beklenen {len(expected_fields)}, gelen {len(parts)}"
            )

        values = [_decode_cell(token) for token in parts]
        item = {expected_fields[i]: values[i] if i < len(values) else "" for i in range(len(expected_fields))}
        output.append(item)

    return output
