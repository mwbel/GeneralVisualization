from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import os
import json

from .generate_visualization import generate_from_prompt

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
REGISTRY_PATH = os.path.join(BASE_DIR, "app", "modules", "ai_visualizer", "registry", "registry.json")


class ResolveRequest(BaseModel):
    prompt: str
    vizType: str = "自动"
    complexity: str = "中等"


def _load_registry() -> Dict[str, Any]:
    if not os.path.exists(REGISTRY_PATH):
        return {"concepts": []}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_registry(data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _match_concept(prompt: str, concepts: List[Dict[str, Any]]):
    p_low = prompt.lower()
    for c in concepts:
        aliases = [a.lower() for a in c.get("aliases", [])]
        title = str(c.get("title", "")).lower()
        cid = str(c.get("id", "")).lower()
        if any(a in p_low for a in aliases) or (cid in p_low) or (title in p_low):
            return c
    return None


@router.post("/resolve_or_generate")
async def resolve_or_generate(req: ResolveRequest):
    """先查本地注册表，命中则返回现有页面，否则生成并更新注册表。"""
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt 不能为空")

    registry = _load_registry()
    hit = _match_concept(prompt, registry.get("concepts", []))
    if hit:
        url = hit.get("url", "")
        # 如果是 .html.bak，复制为 .html 并返回 .html 以避免下载
        if url.endswith(".html.bak"):
            abs_bak = os.path.join(BASE_DIR, url)
            html_url = url[:-4]  # 去掉 .bak
            abs_html = os.path.join(BASE_DIR, html_url)
            try:
                if os.path.exists(abs_bak) and not os.path.exists(abs_html):
                    os.makedirs(os.path.dirname(abs_html), exist_ok=True)
                    with open(abs_bak, "r", encoding="utf-8") as fr, open(abs_html, "w", encoding="utf-8") as fw:
                        fw.write(fr.read())
                # 更新注册表为 .html
                hit["url"] = html_url
                _save_registry(registry)
                url = html_url
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"现有页面处理失败: {e}")
        return {"kind": "existing", "url": url, "source": "registry"}

    # 未命中 → 调用生成逻辑
    try:
        gen = generate_from_prompt(prompt=prompt, viz_type=req.vizType, complexity=req.complexity)
        # 将生成结果登记
        concepts = registry.get("concepts", [])
        concepts.append({
            "id": gen["id"],
            "aliases": gen.get("aliases", []),
            "module": "ai_visualizer",
            "title": gen.get("title", gen["id"]),
            "url": gen["url"],
            "type": "generated"
        })
        registry["concepts"] = concepts
        _save_registry(registry)
        return {"kind": "generated", "url": gen["url"], "source": "generator"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))