from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.api.registry_ops import lookup, upsert, load_registry
from backend.api.generate_visualization import generate_from_prompt

router = APIRouter()


class ResolveRequest(BaseModel):
    prompt: str = Field(..., min_length=4)
    vizType: Optional[str] = None
    complexity: Optional[str] = None


@router.post("/api/resolve_or_generate")
def resolve_or_generate(req: ResolveRequest) -> Dict[str, Any]:
    p = req.prompt.strip()
    if len(p) < 4:
        raise HTTPException(status_code=400, detail="prompt 太短")

    hit = lookup(p)
    if hit:
        return {"kind": "existing", "url": hit["url"], "source": "registry"}

    try:
        result = generate_from_prompt(p, req.vizType or "自动", req.complexity or "中等")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    upsert({
        "id": result["id"],
        "aliases": result.get("aliases", [p]),
        "module": "ai_visualizer",
        "title": result.get("title", result["id"]),
        "url": result["url"],
        "type": "generated",
    })
    return {"kind": "generated", "url": result["url"], "source": "generator"}


@router.get("/api/registry")
def get_registry(q: Optional[str] = None) -> Dict[str, Any]:
    reg = load_registry()
    if q:
        from backend.api.registry_ops import _normalize
        nq = _normalize(q)
        concepts = [c for c in reg.get("concepts", []) if nq in _normalize(c.get("title", "")) or any(nq in _normalize(a) for a in c.get("aliases", []))]
        return {"concepts": concepts}
    return reg