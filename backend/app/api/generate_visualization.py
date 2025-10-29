import os
import json
import time
import re
from typing import Dict, Any

try:
    from openai import OpenAI  # 可选：环境未配置时走本地逻辑
except Exception:
    OpenAI = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
GEN_DIR = os.path.join(BASE_DIR, "app", "modules", "ai_visualizer", "generated")
REGISTRY_PATH = os.path.join(BASE_DIR, "app", "modules", "ai_visualizer", "registry", "registry.json")

SYSTEM_PROMPT_SPEC = (
    "你是交互式可视化工程师。\n"
    "根据以下自然语言描述，输出一个 JSON，字段包含：\n"
    "{concept, chart_type, library, params, title}\n"
    "约束：library 取 plotly 或 three.js，尽量使用 plotly；chart_type 简明如 pdf/pmf/scatter/bar。\n"
    "Few-shot 示例：\n"
    "1) 正态分布 → {\"concept\":\"normal_distribution\",\"chart_type\":\"pdf\",\"library\":\"plotly\",\"params\":{\"mu\":0,\"sigma\":1},\"title\":\"标准正态分布\"}\n"
    "2) 泊松分布 → {\"concept\":\"poisson_distribution\",\"chart_type\":\"pmf\",\"library\":\"plotly\",\"params\":{\"lambda\":4},\"title\":\"泊松分布 PMF\"}\n"
    "3) 矩阵变换 → {\"concept\":\"matrix_transform\",\"chart_type\":\"scatter\",\"library\":\"plotly\",\"params\":{\"A\":[[1,0],[0,1]]},\"title\":\"二维矩阵变换\"}\n"
    "仅输出 JSON，不要解释。"
)

SYSTEM_PROMPT_HTML = (
    "根据以下 JSON 规格，生成一个完整 HTML 文件：\n"
    "- 使用 Plotly 或 Three.js\n"
    "- 页面应可直接在浏览器打开\n"
    "- 必须包含 <title>、<div id=\"viz\"></div>\n"
    "- 样式与万物可视化项目一致"
)


def _timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-]+", "_", text.strip().lower())
    return s.strip("_") or f"concept_{_timestamp()}"


def _load_registry() -> Dict[str, Any]:
    if not os.path.exists(REGISTRY_PATH):
        return {"concepts": []}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_registry(data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _call_openai_for_spec(prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        raise RuntimeError("LLM 未配置，无法抽取规格")
    client = OpenAI(api_key=api_key)
    rsp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_SPEC},
            {"role": "user", "content": prompt},
        ],
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
    )
    content = rsp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", content)
        if m:
            return json.loads(m.group(0))
        raise

def _validate_spec(spec: Dict[str, Any]) -> None:
    required = ["concept", "chart_type", "library", "params", "title"]
    for k in required:
        if spec.get(k) is None:
            raise ValueError(f"规格缺少字段: {k}")
    lib = str(spec.get("library","plotly")).lower()
    if lib not in ("plotly", "three.js", "threejs", "three"):
        raise ValueError("library 必须为 plotly 或 three.js")


def _build_html_from_spec(spec: Dict[str, Any]) -> str:
    title = spec.get("title", "AI Visualization")
    library = spec.get("library", "plotly").lower()

    # 统一样式，嵌入 Plotly/Three.js 代码
    base_head = (
        "<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{title}</title>"
        "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">"
        "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>"
        "<link href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;600;700&display=swap\" rel=\"stylesheet\">"
        "<style>body{font-family:'Noto Sans SC',sans-serif;background:linear-gradient(135deg,#4A65F6,#6C8BFA);margin:0;color:#1f2937;}"
        "#wrap{max-width:980px;margin:24px auto;background:#fff;border-radius:16px;box-shadow:0 12px 24px rgba(0,0,0,.08);padding:16px;}"
        "h1{font-size:20px;margin:0 0 12px;}#viz{height:540px;border:1px dashed #e5e7eb;border-radius:12px;background:#fff}</style>"
        "</head><body><div id=\"wrap\"><h1>" + title + "</h1><div id=\"viz\"></div></div>"
    )

    if library == "plotly":
        js = _plotly_js(spec)
        html = base_head + js + "</body></html>"
    else:
        js = _three_js(spec)
        html = base_head + js + "</body></html>"
    # 静态校验
    if "<title" not in html or "<div id=\"viz\"></div>" not in html:
        raise ValueError("HTML 缺少必要元素")
    if library == "plotly" and "Plotly.newPlot(" not in html:
        raise ValueError("HTML 未包含 Plotly.newPlot 调用")
    return html


def _plotly_js(spec: Dict[str, Any]) -> str:
    chart_type = (spec.get("chart_type") or "line").lower()
    params = spec.get("params", {})
    mu = float(params.get("mu", 0))
    sigma = float(params.get("sigma", 1)) if float(params.get("sigma", 1)) != 0 else 1.0

    if chart_type == "pdf" and spec.get("concept") == "normal_distribution":
        return (
            "<script src=\"https://cdn.plot.ly/plotly-2.31.1.min.js\"></script>"
            "<script>" 
            "function gaussian(x, mu, sigma){return (1/(sigma*Math.sqrt(2*Math.PI)))*Math.exp(-0.5*Math.pow((x-mu)/sigma,2));}"
            "let mu=" + str(mu) + ", sigma=" + str(sigma) + ";"
            "const x=[]; for(let i=-40;i<=40;i++){x.push(i/4);}"
            "function build(){const y=x.map(v=>gaussian(v,mu,sigma));const data=[{x:x,y:y,type:'scatter',mode:'lines',line:{color:'#4A65F6'}}];"
            "const layout={title:'正态分布 PDF',xaxis:{title:'x'},yaxis:{title:'density'},template:'plotly_white'};"
            "Plotly.newPlot('viz',data,layout,{displayModeBar:true});}"
            "build();"
            "</script>"
        )
    # 通用折线图兜底
    return (
        "<script src=\"https://cdn.plot.ly/plotly-2.31.1.min.js\"></script>"
        "<script>const x=[0,1,2,3,4,5,6,7,8,9], y=x.map(v=>Math.sin(v));"
        "Plotly.newPlot('viz',[{x:x,y:y,type:'scatter',mode:'lines',line:{color:'#6C8BFA'}}],{title:'折线图',template:'plotly_white'});" 
        "</script>"
    )


def _three_js(spec: Dict[str, Any]) -> str:
    return (
        "<script src=\"https://unpkg.com/three@0.158.0/build/three.min.js\"></script>"
        "<script>const scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(75,1,0.1,1000);"
        "const renderer=new THREE.WebGLRenderer();renderer.setSize(800,540);document.getElementById('viz').appendChild(renderer.domElement);"
        "const geometry=new THREE.BoxGeometry();const material=new THREE.MeshBasicMaterial({color:0x4A65F6});const cube=new THREE.Mesh(geometry,material);scene.add(cube);"
        "camera.position.z=5;function animate(){requestAnimationFrame(animate);cube.rotation.x+=0.01;cube.rotation.y+=0.01;renderer.render(scene,camera);}animate();" 
        "</script>"
    )

KEYWORDS = {
    "normal_distribution": ["正态", "高斯", "gaussian", "normal"],
    "poisson_distribution": ["泊松", "poisson"],
    "binomial_distribution": ["二项", "binomial"],
    "beta_distribution": ["beta", "贝塔"],
    "exponential_distribution": ["指数", "exponential"],
    "uniform_distribution": ["均匀", "uniform"],
    "matrix_transform": ["矩阵变换", "线性变换", "matrix", "transform"],
}

def _local_spec_from_prompt(prompt: str) -> Dict[str, Any] | None:
    p = prompt.lower()
    def contains(words):
        return any(w in p for w in words)
    if contains(KEYWORDS["normal_distribution"]):
        return {"concept":"normal_distribution","chart_type":"pdf","library":"plotly","params":{"mu":0,"sigma":1},"title":"标准正态分布"}
    if contains(KEYWORDS["poisson_distribution"]):
        return {"concept":"poisson_distribution","chart_type":"pmf","library":"plotly","params":{"lambda":4},"title":"泊松分布 PMF"}
    if contains(KEYWORDS["binomial_distribution"]):
        return {"concept":"binomial_distribution","chart_type":"pmf","library":"plotly","params":{"n":20,"p":0.4},"title":"二项分布 PMF"}
    if contains(KEYWORDS["beta_distribution"]):
        return {"concept":"beta_distribution","chart_type":"pdf","library":"plotly","params":{"alpha":2,"beta":5},"title":"Beta 分布 PDF"}
    if contains(KEYWORDS["exponential_distribution"]):
        return {"concept":"exponential_distribution","chart_type":"pdf","library":"plotly","params":{"lambda":1.0},"title":"指数分布 PDF"}
    if contains(KEYWORDS["uniform_distribution"]):
        return {"concept":"uniform_distribution","chart_type":"pdf","library":"plotly","params":{"a":0,"b":1},"title":"均匀分布 PDF"}
    if contains(KEYWORDS["matrix_transform"]):
        return {"concept":"matrix_transform","chart_type":"scatter","library":"plotly","params":{"A":[[1,0],[0,1]]},"title":"二维矩阵变换"}
    return None

def generate_from_prompt(prompt: str, viz_type: str = "自动", complexity: str = "中等") -> Dict[str, Any]:
    # Step 1: 结构化规格（优先LLM，其次本地规则，不再使用demo）
    try:
        spec = _call_openai_for_spec(prompt)
    except Exception:
        spec = _local_spec_from_prompt(prompt)
        if spec is None:
            raise RuntimeError("无法抽取规格：请更换描述或配置 LLM")
    _validate_spec(spec)

    # Step 2: 生成完整 HTML（模板驱动）并静态校验
    html = _build_html_from_spec(spec)

    # Step 4: 保存文件并写入注册表
    os.makedirs(GEN_DIR, exist_ok=True)
    cid = spec.get("concept") or _slugify(prompt)
    fname = f"viz_{_slugify(cid)}_{_timestamp()}.html"
    fpath = os.path.join(GEN_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

    registry = _load_registry()
    concepts = registry.get("concepts", [])
    aliases = [prompt]
    exists = any(c.get("id") == cid for c in concepts)
    if not exists:
        concepts.append({
            "id": cid,
            "aliases": aliases,
            "module": "ai_visualizer",
            "title": spec.get("title", cid),
            "url": f"app/modules/ai_visualizer/generated/{fname}",
            "type": "generated"
        })
        registry["concepts"] = concepts
        _save_registry(registry)

    return {"id": cid, "title": spec.get("title", cid), "url": f"app/modules/ai_visualizer/generated/{fname}", "aliases": aliases}