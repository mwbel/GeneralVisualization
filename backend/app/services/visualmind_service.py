import os
import re
import json
import importlib.util
from typing import Dict, Any, Tuple
import plotly.io as pio

# 兼容不同启动方式：优先绝对导入，缺失则提供占位配置
try:
    from core.config import settings  # 目录结构: backend/app/core/config.py
except Exception:
    class _Settings:
        OPENAI_API_KEY = None
        MODEL_NAME = "gpt-4o"
    settings = _Settings()

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # 环境未安装 openai 时的兜底


# === Gemini 适配开始 ===
import os
import google.generativeai as genai

def call_gemini(messages, model_name="gemini-2.5-flash"):
    """
    messages: [{"role":"system","content":"..."},{"role":"user","content":"..."}]
    返回：模型文本输出
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)
    # 把 OpenAI 风格 messages 拼成一条 prompt（Gemini 支持 system + user 但我们简单兼容）
    sys_txt = "\n".join(m["content"] for m in messages if m["role"] == "system")
    usr_txt = "\n".join(m["content"] for m in messages if m["role"] == "user")
    prompt = (sys_txt + "\n\n" + usr_txt).strip()

    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt)
    return resp.text or ""
# === Gemini 适配结束 ===



SAFE_BLOCK_PATTERNS = [
    r"\bsubprocess\b",
    r"\bos\.system\b",
    r"\bopen\(\b",
    r"\bshutil\b",
    r"\burllib\b",
    r"\brequests\b",
    r"\bsocket\b",
    r"\bpathlib\b",
    r"\bos\.remove\b",
]


def classify_kind(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ["行列式", "矩阵", "向量", "线性代数", "determinant", "matrix", "vector", "linear algebra"]):
        return "det"
    if any(k.lower() in low for k in ["分布", "泊松", "poisson", "超几何", "二项", "正态", "distribution", "binomial", "normal", "hypergeometric"]):
        return "dist"
    return "general"


def is_safe(code: str) -> bool:
    low = code.lower()
    if any(re.search(p, low) for p in SAFE_BLOCK_PATTERNS):
        return False
    return True


def scipy_available() -> bool:
    return importlib.util.find_spec("scipy") is not None


def build_system_prompt() -> str:
    return (
        "你是通用可视化引擎 VisualMind。目标：把自然语言需求转为可执行的 "
        "Python/Plotly 代码，并返回变量名为 fig 的 Figure。\n"
        "原则：\n"
        "1) 学科语义匹配：数学/统计/物理/通用 → 选择对应模板与示例。\n"
        "2) 代码必须完整可运行：包含 import ，避免占位符/伪代码。\n"
        "3) 安全与可控：仅使用 numpy、plotly（可选：scipy.stats）。不要使用文件/系统/网络相关库。\n"
        "4) 交互性：优先使用 Plotly；分布/参数类需提供 Slider/Steps。\n"
        "5) 变量约定：最终图对象命名为 fig。\n"
        "输出格式：```python\n# 完整可运行代码（必须包含 import ... 与 fig=...）\n```"
    )


REPAIR_TEMPLATE = (
    "以下Python代码无法按要求生成 Plotly 交互图，请修复并返回完整代码：\n"
    "要求：\n"
    "仅使用 numpy、plotly（可选 scipy.stats）\n"
    "必须创建 fig 变量（plotly.graph_objects.Figure）\n"
    "不使用文件/网络/系统相关库\n"
    "若为分布类，提供 Slider/Steps 参数交互\n"
    "错误信息：\n{error_text}\n"
    "原始代码：\n{bad_code}\n"
)


FALLBACK_POISSON_CODE = '''\
import numpy as np
import plotly.graph_objects as go

lam = 4
x = np.arange(0, 20)
pmf = np.exp(-lam) * np.power(lam, x) / np.array([np.math.factorial(int(v)) for v in x])

fig = go.Figure()
fig.add_bar(x=x, y=pmf, marker_color='teal', name='Poisson PMF')
fig.update_layout(title='环境未安装 scipy：暂以 Poisson 近似展示（安装后支持超几何）',
                  xaxis_title='x', yaxis_title='P(X=x)',
                  template='plotly_white')
'''


class VisualMindService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY and OpenAI is not None:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception:
                self.client = None

    def _llm_generate_code(self, system_prompt: str, user_prompt: str) -> str:
        if not self.client:
            # 无LLM时的最简兜底：生成一个可运行的散点图
            return (
                "import numpy as np\nimport plotly.express as px\n"
                "x = np.linspace(0, 10, 50)\n"
                "y = np.sin(x)\n"
                "fig = px.line(x=x, y=y, title='Fallback Line Chart')\n"
            )

        rsp = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL or "gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"请直接输出完整Python代码（必须创建 fig）。\n用户请求：{user_prompt}",
                },
            ],
            temperature=0,
        )
        content = rsp.choices[0].message.content
        m = re.search(r"```python\n(.*?)\n```", content, re.S | re.I)
        return (m.group(1) if m else content).strip()

    def _execute_to_html(self, code: str) -> Tuple[str, Any]:
        env: Dict[str, Any] = {}
        exec(code, env, env)
        fig = env.get("fig")
        if fig is None:
            raise RuntimeError("代码未创建 fig")
        html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False)
        return html, fig

    def _quality_gate(self, code: str, fig: Any) -> bool:
        if "import plotly" not in code:
            return False
        try:
            traces = getattr(fig, "data", [])
            max_points = 0
            for t in traces:
                # 尝试取 x/y/z 长度
                for key in ("x", "y", "z"):
                    arr = getattr(t, key, None)
                    if arr is not None:
                        try:
                            max_points = max(max_points, len(arr))
                        except Exception:
                            pass
            return max_points > 3
        except Exception:
            return False

    def generate(self, prompt: str) -> Dict[str, Any]:
        kind = classify_kind(prompt)

        # 依赖缺失回退（scipy）
        if (not scipy_available()) and any(k in prompt.lower() for k in ["超几何", "hypergeometric"]):
            code = FALLBACK_POISSON_CODE
            try:
                html, fig = self._execute_to_html(code)
                ok = self._quality_gate(code, fig)
                if not ok:
                    raise RuntimeError("质量门槛未通过")
                return {"status": 200, "html": html, "code": code, "kind": kind}
            except Exception as e:
                # 最终兜底：简单折线
                fallback = (
                    "import numpy as np\nimport plotly.express as px\n"
                    "x = np.arange(0, 10)\n"
                    "y = x\n"
                    "fig = px.line(x=x, y=y, title='Fallback Chart')\n"
                )
                html, _ = self._execute_to_html(fallback)
                return {"status": 200, "html": html, "code": fallback, "kind": kind}

        # 常规路径：LLM生成
        system_prompt = build_system_prompt()
        code = self._llm_generate_code(system_prompt, prompt)

        # 安全检查
        if not is_safe(code):
            return {
                "status": 500,
                "error": "代码包含不安全的API调用",
                "code": code,
                "html": "",
                "kind": kind,
            }

        # 执行并质量门槛
        try:
            html, fig = self._execute_to_html(code)
            if not self._quality_gate(code, fig):
                raise RuntimeError("质量门槛未通过：需包含plotly导入且点数>3")
            return {"status": 200, "html": html, "code": code, "kind": kind}
        except Exception as e:
            # 自愈：带错误与原始代码再次生成
            repair_prompt = REPAIR_TEMPLATE.format(error_text=str(e), bad_code=code)
            repaired = self._llm_generate_code(system_prompt, repair_prompt)
            if not is_safe(repaired):
                repaired = (
                    "import numpy as np\nimport plotly.express as px\n"
                    "x = np.arange(0, 20)\n"
                    "y = np.sin(x)\n"
                    "fig = px.line(x=x, y=y, title='Safe Fallback')\n"
                )
            try:
                html, fig = self._execute_to_html(repaired)
                if not self._quality_gate(repaired, fig):
                    raise RuntimeError("修复后质量门槛未通过")
                return {"status": 200, "html": html, "code": repaired, "kind": kind}
            except Exception:
                # 二次仍失败，最终兜底
                fallback = (
                    "import numpy as np\nimport plotly.express as px\n"
                    "x = np.arange(0, 10)\n"
                    "y = x\n"
                    "fig = px.line(x=x, y=y, title='Fallback Chart')\n"
                )
                html, _ = self._execute_to_html(fallback)
                return {"status": 200, "html": html, "code": fallback, "kind": kind}
