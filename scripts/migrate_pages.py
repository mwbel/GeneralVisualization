#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迁移旧页面至 modules/pages，修正路径/别名，生成报告。
- 探测源目录：线性代数、概率统计
- 为每个源文件创建 .bak
- 移动到 app/modules/<module>/pages
- 修正 HTML 中样式/脚本路径与别名引用
- 幂等更新配置（保持现有值，如需修正则修正）
- 生成迁移报告到 app/modules/**/build/migrate_report.md
"""
import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # GeneralVisulization 根
LA_SRC = ROOT / "线性代数可视化"
PS_SRC = ROOT / "概率论与数理统计可视化"
LA_DEST = ROOT / "app/modules/linear_algebra/pages"
PS_DEST = ROOT / "app/modules/probability_statistics/pages"
LA_BUILD = ROOT / "app/modules/linear_algebra/build"
PS_BUILD = ROOT / "app/modules/probability_statistics/build"

REPORT_ITEMS = {"la": [], "ps": []}

def ensure_dirs():
    for p in [LA_DEST, PS_DEST, LA_BUILD, PS_BUILD]:
        p.mkdir(parents=True, exist_ok=True)


def list_html_files(src: Path):
    if not src.exists():
        return []
    return sorted([p for p in src.glob("*.html")])


def backup_file(path: Path):
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    return bak


def move_file(src: Path, dest_dir: Path):
    dest = dest_dir / src.name
    # 若已存在则跳过移动（幂等）
    if dest.exists():
        return dest
    src.rename(dest)
    return dest


CSS_GLOBAL = "/app/lib/global-styles.css"

# 简单替换规则：别名与样式路径
REPLACEMENTS = [
    (r"\.{1,2}/\.{1,2}/components/", "@components/"),
    (r"\.{1,2}/\.{1,2}/lib/", "@lib/"),
]

# 样式路径统一：常见写法替换为绝对路径（在本项目根通过Python服务器可用）
STYLE_FIXES = [
    (r"[\./]+/app/lib/global-styles\.css", CSS_GLOBAL),
    (r"[\./]+/lib/global-styles\.css", CSS_GLOBAL),
    (r"global-styles\.css", CSS_GLOBAL),
]


def fix_html_content(text: str):
    new_text = text
    replaced = []
    for pattern, repl in REPLACEMENTS:
        new_text2 = re.sub(pattern, repl, new_text)
        if new_text2 != new_text:
            replaced.append((pattern, repl))
            new_text = new_text2
    for pattern, repl in STYLE_FIXES:
        new_text2 = re.sub(pattern, repl, new_text)
        if new_text2 != new_text:
            replaced.append((pattern, repl))
            new_text = new_text2
    return new_text, replaced


def summarize_dest(dest_dir: Path, report_key: str):
    results = []
    for dest in sorted(dest_dir.glob("*.html")):
        text = dest.read_text(encoding="utf-8", errors="ignore")
        flags = {
            "has_alias_components": "@components/" in text,
            "has_alias_lib": "@lib/" in text,
            "uses_global_styles": "/app/lib/global-styles.css" in text,
        }
        results.append({
            "file": str(dest.relative_to(ROOT)),
            "summary": flags,
        })
    REPORT_ITEMS[report_key] = results


def process_module(src_dir: Path, dest_dir: Path, report_key: str):
    files = list_html_files(src_dir)
    results = []
    for f in files:
        backup_file(f)
        dest = move_file(f, dest_dir)
        text = dest.read_text(encoding="utf-8", errors="ignore")
        fixed_text, replacements = fix_html_content(text)
        if fixed_text != text:
            dest.write_text(fixed_text, encoding="utf-8")
        results.append({
            "file": str(dest.relative_to(ROOT)),
            "replacements": replacements,
        })
    if results:
        REPORT_ITEMS[report_key] = results
    else:
        summarize_dest(dest_dir, report_key)


def update_configs():
    # 幂等检查：trae.config.json 与 package.json 是否匹配既定脚本
    trae_path = ROOT / "trae.config.json"
    pkg_path = ROOT / "package.json"
    changes = {"trae": False, "pkg": False}

    if trae_path.exists():
        try:
            data = json.loads(trae_path.read_text(encoding="utf-8"))
            # 不强制修改，按既定模块root校验
            # 记录发现的workspaces路径（若将来需要修正再写入）
            changes["trae"] = False
        except Exception:
            pass

    if pkg_path.exists():
        try:
            pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            expect = {
                "dev:la": "vite --port 5173 --root app/modules/linear_algebra",
                "dev:ps": "vite --port 5174 --root app/modules/probability_statistics",
                "dev:dg": "vite --port 5175 --root app/modules/differential_geometry",
            }
            updated = False
            for k,v in expect.items():
                if scripts.get(k) != v:
                    scripts[k] = v
                    updated = True
            if updated:
                pkg["scripts"] = scripts
                pkg_path.write_text(json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8")
                changes["pkg"] = True
        except Exception:
            pass
    return changes


def write_report():
    def section(title: str):
        return f"\n## {title}\n\n"

    la_md = ["# 迁移报告 - 线性代数\n"]
    for item in REPORT_ITEMS.get("la", []):
        la_md.append(f"- 搬迁文件: `{item['file']}`")
        if "replacements" in item and item["replacements"]:
            for pat, repl in item["replacements"]:
                la_md.append(f"  - 修正: `{pat}` -> `{repl}`")
        if "summary" in item:
            s = item["summary"]
            la_md.append(f"  - 别名components: {s['has_alias_components']}, 别名lib: {s['has_alias_lib']}, 样式: {s['uses_global_styles']}")
    (LA_BUILD / "migrate_report.md").write_text("\n".join(la_md), encoding="utf-8")

    ps_md = ["# 迁移报告 - 概率与数统\n"]
    for item in REPORT_ITEMS.get("ps", []):
        ps_md.append(f"- 搬迁文件: `{item['file']}`")
        if "replacements" in item and item["replacements"]:
            for pat, repl in item["replacements"]:
                ps_md.append(f"  - 修正: `{pat}` -> `{repl}`")
        if "summary" in item:
            s = item["summary"]
            ps_md.append(f"  - 别名components: {s['has_alias_components']}, 别名lib: {s['has_alias_lib']}, 样式: {s['uses_global_styles']}")
    (PS_BUILD / "migrate_report.md").write_text("\n".join(ps_md), encoding="utf-8")


def main():
    ensure_dirs()
    process_module(LA_SRC, LA_DEST, "la")
    process_module(PS_SRC, PS_DEST, "ps")
    cfg_changes = update_configs()
    write_report()
    print("[migrate] done")
    print("LA files:", len(REPORT_ITEMS.get("la", [])))
    print("PS files:", len(REPORT_ITEMS.get("ps", [])))
    print("Config changes:", cfg_changes)


if __name__ == "__main__":
    main()