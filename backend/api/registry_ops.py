import json
import os
import re
from typing import Any, Dict, List, Optional

from backend.config import REGISTRY_PATH

# Ensure parent directory exists
os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)

DEFAULT_REGISTRY: Dict[str, Any] = {
    "concepts": []
}


def load_registry() -> Dict[str, Any]:
    if not os.path.exists(REGISTRY_PATH):
        return DEFAULT_REGISTRY.copy()
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return DEFAULT_REGISTRY.copy()


def save_registry(registry: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def lookup(prompt: str) -> Optional[Dict[str, Any]]:
    """Simple alias/keyword lookup. Returns matching concept entry or None."""
    p = _normalize(prompt)
    registry = load_registry()
    for entry in registry.get("concepts", []):
        title = _normalize(entry.get("title", ""))
        if entry.get("aliases"):
            for alias in entry["aliases"]:
                if _normalize(alias) in p or p in _normalize(alias):
                    return entry
        if title and (title in p or p in title):
            return entry
        # also check id
        if _normalize(entry.get("id", "")) in p:
            return entry
    return None


def upsert(entry: Dict[str, Any]) -> Dict[str, Any]:
    registry = load_registry()
    concepts: List[Dict[str, Any]] = registry.get("concepts", [])
    existing_idx = next((i for i, c in enumerate(concepts) if c.get("id") == entry.get("id")), None)
    if existing_idx is not None:
        concepts[existing_idx] = {**concepts[existing_idx], **entry}
    else:
        concepts.append(entry)
    registry["concepts"] = concepts
    save_registry(registry)
    return entry