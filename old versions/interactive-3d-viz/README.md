# 一图胜千言 - 智能3D可视化平台

一个智能的交互式3D可视化应用，用户可以通过自然语言描述需求，AI自动生成Python代码实现3D可视化，并在前端展示结果。让复杂的数据可视化变得简单直观，真正做到"一图胜千言"。

## 功能特性

- 🤖 AI驱动的代码生成
- 🎨 实时3D可视化渲染
- 💬 自然语言交互界面
- 📦 一键代码和依赖下载
- 🔧 多种可视化库支持（Plotly、Matplotlib、Mayavi）

## 技术栈

### 前端
- React 18
- Three.js
- WebGL
- Material-UI

### 后端
- Python 3.9+
- FastAPI
- OpenAI API
- Plotly/Matplotlib/Mayavi

### AI模型
- GPT-4 (代码生成)
- Claude-3.5 Sonnet (代码优化)
- CodeLlama (代码分析)

## 项目结构

```
interactive-3d-viz/
├── frontend/          # React前端应用
├── backend/           # Python后端API
├── docs/             # 项目文档
├── scripts/          # 构建和部署脚本
└── README.md         # 项目说明
```

## 快速开始

### 环境要求
- Node.js 16+
- Python 3.9+
- npm/yarn

### 安装依赖

```bash
# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

### 运行应用

```bash
# 启动后端服务
cd backend
python main.py

# 启动前端服务
cd frontend
npm start
```

## 开发指南

详细的开发指南请参考 [docs/](./docs/) 目录。

## 许可证

MIT License