import os
import time
from typing import Any, Dict, List

from backend.config import ALLOWED_CHARTS, ALLOWED_LIBS, GENERATED_DIR

# --- Utilities ---

def _timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def _slugify(text: str) -> str:
    import re
    text = re.sub(r"\s+", "_", text.strip().lower())
    text = re.sub(r"[^a-z0-9_]+", "", text)
    return text or "viz"


# --- Spec extraction ---

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
    def contains(words: List[str]) -> bool:
        return any(w in p for w in words)
    if contains(KEYWORDS["normal_distribution"]):
        return {"concept":"normal_distribution","chart_type":"pdf","library":"plotly","params":{"mu":0,"sigma":1},"title":"标准正态分布"}
    if contains(KEYWORDS["poisson_distribution"]):
        return {"concept":"poisson_distribution","chart_type":"pmf","library":"plotly","params":{"lambda":4},"title":"泊松分布 PMF"}
    if contains(KEYWORDS["binomial_distribution"]):
        return {"concept":"binomial_distribution","chart_type":"pmf","library":"plotly","params":{"n":20,"p":0.4},"title":"二项分布 PMF"}
    if contains(KEYWORDS["beta_distribution"]):
        # Try to capture alpha,beta from text
        import re
        alpha = 2
        beta = 5
        m = re.search(r"alpha\s*=\s*(\d+\.?\d*)", p)
        if m: alpha = float(m.group(1))
        m = re.search(r"beta\s*=\s*(\d+\.?\d*)", p)
        if m: beta = float(m.group(1))
        return {"concept":"beta_distribution","chart_type":"pdf","library":"plotly","params":{"alpha":alpha,"beta":beta},"title":"Beta 分布 PDF"}
    if contains(KEYWORDS["exponential_distribution"]):
        return {"concept":"exponential_distribution","chart_type":"pdf","library":"plotly","params":{"lambda":1.0},"title":"指数分布 PDF"}
    if contains(KEYWORDS["uniform_distribution"]):
        return {"concept":"uniform_distribution","chart_type":"pdf","library":"plotly","params":{"a":0,"b":1},"title":"均匀分布 PDF"}
    if contains(KEYWORDS["matrix_transform"]):
        return {"concept":"matrix_transform","chart_type":"scatter","library":"plotly","params":{"A":[[1,0],[0,1]]},"title":"二维矩阵变换"}
    return None


# --- Validation ---

def _validate_spec(spec: Dict[str, Any]) -> None:
    if not isinstance(spec, dict):
        raise ValueError("规格必须为对象")
    chart = spec.get("chart_type")
    lib = spec.get("library")
    if chart not in ALLOWED_CHARTS:
        raise ValueError(f"不支持的图表类型: {chart}")
    if lib not in ALLOWED_LIBS:
        raise ValueError(f"不支持的库: {lib}")
    if lib == "plotly" and chart == "surface3d":
        # still valid, will create 3d surface
        pass


# --- HTML build ---

def _build_html_from_spec(spec: Dict[str, Any]) -> str:
    """Return a complete HTML file content with CDN imports and Plotly code."""
    title = spec.get("title", spec.get("concept", "可视化"))
    chart = spec["chart_type"]
    params = spec.get("params", {})
    plot_code = ""

    if chart == "pdf" and spec.get("concept") == "normal_distribution":
        mu = params.get("mu", 0)
        sigma = params.get("sigma", 1)
        plot_code = f"""
        const mu = {mu};
        const sigma = {sigma};
        const xs = Array.from({{length:401}}, (_,i)=>-4+ i*0.02);
        const ys = xs.map(x => (1/Math.sqrt(2*Math.PI)/sigma) * Math.exp(-0.5*Math.pow((x-mu)/sigma,2)) );
        Plotly.newPlot('viz', [{{x: xs, y: ys, type: 'scatter', mode:'lines', name:'PDF'}}], {{title: '{title}'}});
        """
    elif spec.get("concept") == "beta_distribution":
        a = params.get("alpha", 2)
        b = params.get("beta", 5)
        plot_code = f"""
        const alpha = {a};
        const beta = {b};
        function betaPDF(x, a, b) {{
          function gamma(z) {{
            // Lanczos approximation
            const g = 7;
            const p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
            if(z < 0.5) return Math.PI / (Math.sin(Math.PI*z) * gamma(1-z));
            z -= 1;
            let x = p[0];
            for(let i=1; i<g+2; i++) x += p[i]/(z+i);
            const t = z + g + 0.5;
            return Math.sqrt(2*Math.PI) * Math.pow(t, z+0.5) * Math.exp(-t) * x;
          }}
          const B = gamma(a)*gamma(b)/gamma(a+b);
          return Math.pow(x, a-1) * Math.pow(1-x, b-1) / B;
        }}
        const xs = Array.from({{length:401}}, (_,i)=> i/400);
        const ys = xs.map(x => betaPDF(x, alpha, beta));
        Plotly.newPlot('viz', [{{x: xs, y: ys, type:'scatter', mode:'lines', name:'PDF'}}], {{title: '{title}'}});
        """
    elif spec.get("concept") == "poisson_distribution":
        lam = params.get("lambda", 4)
        plot_code = f"""
        const lambda = {lam};
        const ks = Array.from({{length:25}}, (_,i)=>i);
        function pmf(k, lam) {{
          function fact(n){{return n<=1?1:n*fact(n-1);}}
          return Math.pow(lam, k) * Math.exp(-lam) / fact(k);
        }}
        const ys = ks.map(k => pmf(k, lambda));
        Plotly.newPlot('viz', [{{x: ks, y: ys, type:'bar', name:'PMF'}}], {{title: '{title}'}});
        """
    else:
        # Generic line placeholder for supported chart types
        plot_code = "Plotly.newPlot('viz', [{y:[0,1,0,1], type:'scatter'}], {title: '可视化'});"

    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.26.0/plotly.min.js"></script>
  <style>
    body {{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto; background:#f7fafc; }}
    #viz {{ width: 100%; height: 90vh; }}
  </style>
</head>
<body>
  <div id="viz"></div>
  <script>
    {plot_code}
  </script>
</body>
</html>
"""
    # Static checks
    if "Plotly.newPlot" not in html or "<div id=\"viz\">" not in html:
        raise ValueError("生成的 HTML 未包含必要元素")
    return html


# --- Main entry ---

def generate_from_prompt(prompt: str, viz_type: str = "自动", complexity: str = "中等") -> Dict[str, Any]:
    spec = _local_spec_from_prompt(prompt)
    if spec is None:
        raise RuntimeError("无法抽取规格：请更换描述或配置生成模型")
    _validate_spec(spec)

    html = _build_html_from_spec(spec)

    os.makedirs(GENERATED_DIR, exist_ok=True)
    cid = spec.get("concept") or _slugify(prompt)
    fname = f"viz_{_slugify(cid)}_{_timestamp()}.html"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

    return {"id": cid, "title": spec.get("title", cid), "url": f"app/modules/ai_visualizer/generated/{fname}", "aliases": [prompt]}