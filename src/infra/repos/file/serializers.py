import json
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

import aiofiles


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


async def save_to_file(path: Path, data: dict) -> None:
    """Save dict as JSON to file."""
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False, indent=2))


async def load_from_file(path: Path) -> dict | None:
    """Load JSON from file, return None if not found."""
    try:
        async with aiofiles.open(path, encoding="utf-8") as f:
            content = await f.read()
        return json.loads(content)
    except FileNotFoundError:
        return None
