#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模块工作区配置自动验证脚本
- 校验 trae.config.json 工作区配置
- 校验 package.json 开发脚本
- 校验共享目录与占位文件
- 校验每个模块的入口页面与脚本
- 对潜在的 TypeScript/浏览器导入问题给出提示
"""
import json
import os
import sys
from typing import List, Dict

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(ROOT, '..'))

OK = 0
WARN = 0
ERR = 0


def exists(path: str) -> bool:
    return os.path.exists(path)


def read_json(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def log_ok(msg: str):
    global OK
    OK += 1
    print(f"[OK] {msg}")


def log_warn(msg: str):
    global WARN
    WARN += 1
    print(f"[WARN] {msg}")


def log_err(msg: str):
    global ERR
    ERR += 1
    print(f"[ERROR] {msg}")


def validate_trae_config():
    path = os.path.join(PROJECT_ROOT, 'trae.config.json')
    if not exists(path):
        log_err('缺少 trae.config.json')
        return
    cfg = read_json(path)
    text = read_text(path)
    expected_names = [
        'Linear Algebra Visualization',
        'Probability & Statistics Visualization',
        'Differential Geometry Visualization',
    ]
    for name in expected_names:
        if name in text:
            log_ok(f'工作区名称存在: {name}')
        else:
            log_err(f'工作区名称缺失: {name}')
    expected_roots = [
        'app/modules/linear_algebra',
        'app/modules/probability_statistics',
        'app/modules/differential_geometry',
    ]
    for root in expected_roots:
        if root in text:
            log_ok(f'工作区根目录配置存在: {root}')
        else:
            log_err(f'工作区根目录配置缺失: {root}')


def validate_package_scripts():
    path = os.path.join(PROJECT_ROOT, 'package.json')
    if not exists(path):
        log_err('缺少 package.json')
        return
    pkg = read_json(path)
    scripts = pkg.get('scripts', {})
    for s in ['dev:la', 'dev:ps', 'dev:dg']:
        if s in scripts:
            log_ok(f'存在开发脚本: {s} -> {scripts[s]}')
        else:
            log_err(f'缺少开发脚本: {s}')


def validate_shared_dirs():
    # components
    comp_dir = os.path.join(PROJECT_ROOT, 'app', 'components')
    if exists(comp_dir):
        log_ok('共享组件目录存在: app/components')
        # 组件文件
        components = ['PlotCanvas.ts', 'ControlPanel.ts', 'ExplainBox.ts',
                      'StatBlock.ts', 'ModuleLayout.ts', 'FormulaRenderer.ts', 'index.ts']
        for f in components:
            p = os.path.join(comp_dir, f)
            if exists(p):
                log_ok(f'组件文件存在: {f}')
            else:
                log_err(f'缺少组件文件: {f}')
    else:
        log_err('缺少共享组件目录: app/components')

    # lib
    lib_dir = os.path.join(PROJECT_ROOT, 'app', 'lib')
    if exists(lib_dir):
        log_ok('共享库目录存在: app/lib')
        libs = ['global-styles.css', 'global-theme.ts', 'mathjax.js', 'autoMath.js', 'responsive-math.js']
        for f in libs:
            p = os.path.join(lib_dir, f)
            if exists(p):
                log_ok(f'共享库文件存在: {f}')
            else:
                log_warn(f'共享库文件缺失: {f}')
    else:
        log_err('缺少共享库目录: app/lib')

    # 视觉标准文档
    std_path = os.path.join(PROJECT_ROOT, 'app', 'global_visual_standards.md')
    if exists(std_path):
        log_ok('视觉标准文档存在: app/global_visual_standards.md')
    else:
        log_warn('视觉标准文档缺失: app/global_visual_standards.md')


def validate_module(module_key: str, rel_dir: str):
    mod_dir = os.path.join(PROJECT_ROOT, rel_dir)
    if not exists(mod_dir):
        log_err(f'模块目录缺失: {rel_dir}')
        return
    log_ok(f'模块目录存在: {rel_dir}')

    index_html = os.path.join(mod_dir, 'index.html')
    main_js = os.path.join(mod_dir, 'main.js')
    if exists(index_html):
        log_ok(f'入口页面存在: {module_key}/index.html')
        content = read_text(index_html)
        if '../../lib/global-styles.css' in content:
            log_ok('入口页面已引入全局样式 global-styles.css')
        else:
            log_warn('入口页面未引入 global-styles.css')
        if 'polyfill.io' in content:
            log_warn('入口页面包含 polyfill.io 引用，可能出现连接关闭报错')
    else:
        log_err(f'缺少入口页面: {module_key}/index.html')

    if exists(main_js):
        log_ok(f'主脚本存在: {module_key}/main.js')
        js_content = read_text(main_js)
        if '.ts' in js_content:
            log_warn('main.js 包含对 .ts 的直接导入，浏览器环境可能无法解析')
    else:
        log_err(f'缺少主脚本: {module_key}/main.js')


def main():
    print('=== 多模块配置自动验证报告 ===')
    validate_trae_config()
    validate_package_scripts()
    validate_shared_dirs()

    validate_module('linear_algebra', 'app/modules/linear_algebra')
    validate_module('probability_statistics', 'app/modules/probability_statistics')
    validate_module('differential_geometry', 'app/modules/differential_geometry')

    print('\n=== 汇总 ===')
    print(f'通过: {OK}, 警告: {WARN}, 错误: {ERR}')

    # 有错误时以非零码退出，便于CI或自动化检测
    sys.exit(1 if ERR > 0 else 0)


if __name__ == '__main__':
    main()