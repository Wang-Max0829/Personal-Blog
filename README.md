# 技术笔记 · 个人博客

一个用于记录 **算法 / 深度学习 / 编程 / 学习笔记** 的静态技术博客，使用 Python 静态站点生成器构建，部署于 GitHub Pages。

## 特性

- ✍️ 用 **Markdown** 写文章，零锁定、易迁移
- 🧮 内置 **KaTeX** 数学公式渲染（`$行内$` 与 `$$块级$$`）
- 💻 **highlight.js** 代码高亮（自动识别语言）
- 🌗 明暗主题切换（记忆偏好，跟随系统）
- 🔍 首页客户端搜索 + 分类过滤
- 📱 响应式，手机/电脑都好读
- 🚀 一键部署 GitHub Pages（GitHub Actions 自动构建）

## 目录结构

```
.
├── posts/                 # 文章源文件（按分类分目录）
│   ├── algorithms/        # 算法
│   ├── deep-learning/     # 深度学习
│   ├── programming/       # 编程
│   └── notes/             # 学习笔记
├── templates/             # HTML 模板（base/index/post/category/about）
├── assets/                # CSS / JS 等静态资源
├── public/                # 构建产物（部署用，自动生成，勿手改）
├── build.py               # 静态站点生成器
├── requirements.txt       # Python 依赖
├── about.md               # 关于页内容
└── .github/workflows/     # GitHub Pages 自动部署
```

## 本地预览

```bash
# 1. 安装依赖（建议用虚拟环境）
pip install -r requirements.txt

# 2. 生成站点
python build.py

# 3. 本地预览（任选其一）
python -m http.server 8000 --directory public
# 然后浏览器打开 http://localhost:8000
```

## 写一篇新文章

在对应分类目录下新建一个 `.md` 文件，例如 `posts/algorithms/2026-08-20-binary-search.md`：

```markdown
---
title: 二分查找详解
date: 2026-08-20
category: 算法
tags: [二分, 查找, 复杂度]
summary: 二分查找的核心思想、模板与常见边界坑。
---

正文用 Markdown 书写……

行内公式示例：$O(\log n)$

块级公式：

$$
\mid = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

代码块：

```python
def bisect(arr, x):
    lo, hi = 0, len(arr) - 1
    ...
```
```

写完（或改完）后重新运行 `python build.py` 即可。

> 提示：`date` 决定排序（新的在前）；`category` 应取分类目录名之一：
> `algorithms` / `deep-learning` / `programming` / `notes`。

## 部署到 GitHub Pages

1. 把本项目推到 GitHub 仓库（如 `your-name/tech-blog`）。
2. 仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 以后每次 `git push` 到 `main` 分支，GitHub Actions 会自动构建并发布。
4. 访问 `https://<用户名>.github.io/<仓库名>/` 即可。

> 想用自定义域名？在仓库 Settings → Pages 里填 Custom domain，并添加 `CNAME` 文件到 `public/` 目录（可在 `build.py` 末尾加一行写入）。

## 自定义

- **站点标题 / 导航**：编辑 `templates/base.html`。
- **配色**：编辑 `assets/css/style.css` 顶部的 CSS 变量（`:root` 与 `[data-theme="dark"]`）。
- **新增分类**：在 `build.py` 的 `CATEGORIES`、首页 `templates/index.html` 的 chips、以及 `posts/` 下都加上对应项。
- **关于页**：编辑 `about.md`。
