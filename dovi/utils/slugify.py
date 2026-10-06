import re
import unicodedata


def slugify(value: str, max_length: int = 64) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    value = re.sub(r"[-\s]+", "-", value).strip("-_")
    return value[:max_length] or "document"
