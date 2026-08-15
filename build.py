#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""个人技术博客静态站点生成器 (SSG)

读取 posts/<分类>/*.md 与 about.md，渲染为静态 HTML 输出到 public/，
可直接用 GitHub Pages 部署（推荐配合 .github/workflows/deploy.yml）。

依赖: pip install -r requirements.txt
用法: python build.py
"""
import os
import re
import json
import glob
import shutil
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(ROOT, "posts")
TEMPLATES_DIR = os.path.join(ROOT, "templates")
ASSETS_DIR = os.path.join(ROOT, "assets")
OUT_DIR = os.path.join(ROOT, "public")
ABOUT_SRC = os.path.join(ROOT, "about.md")

# 分类目录 -> 中文名
CATEGORIES = {
    "algorithms": "算法",
    "deep-learning": "深度学习",
    "programming": "编程",
    "notes": "学习笔记",
}

BASE = open(os.path.join(TEMPLATES_DIR, "base.html"), encoding="utf-8").read()


def load_template(name):
    return open(os.path.join(TEMPLATES_DIR, name), encoding="utf-8").read()


def parse_frontmatter(text):
    """极简 frontmatter 解析: 支持 title/date/category/tags/summary。

    tags 形如 [a, b, c]。"""
    fm, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if m:
        fm_text, body = m.group(1), m.group(2)
        for line in fm_text.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            fm[k] = v
    return fm, body


def protect_math(body):
    """在 Markdown 渲染前保护 $...$ 与 $$...$$，避免被 Markdown 破坏。"""
    store = []

    def rep(m):
        store.append(m.group(0))
        return "\u0000%d\u0000" % (len(store) - 1)

    body = re.sub(r"\$\$(.+?)\$\$", rep, body, flags=re.DOTALL)
    body = re.sub(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)", rep, body)
    return body, store


def restore_math(html, store):
    for i, m in enumerate(store):
        html = html.replace("\u0000%d\u0000" % i, m)
    return html


def render_markdown(body):
    body, store = protect_math(body)
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    html = md.convert(body)
    return restore_math(html, store)


def reading_time(body):
    chars = len(re.sub(r"\s", "", body))
    return max(1, round(chars / 400))


def load_posts():
    posts = []
    for cat in CATEGORIES:
        d = os.path.join(POSTS_DIR, cat)
        if not os.path.isdir(d):
            continue
        for path in sorted(glob.glob(os.path.join(d, "*.md")), reverse=True):
            text = open(path, encoding="utf-8").read()
            fm, body = parse_frontmatter(text)
            html = render_markdown(body)
            slug = os.path.splitext(os.path.basename(path))[0]
            tags = fm.get("tags", [])
            if not isinstance(tags, list):
                tags = []
            posts.append({
                "title": fm.get("title", slug),
                "date": str(fm.get("date", "")),
                "category": cat,
                "category_cn": CATEGORIES[cat],
                "tags": tags,
                "summary": fm.get("summary", ""),
                "slug": slug,
                "html": html,
                "reading_min": reading_time(body),
            })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def card_html(p, prefix):
    tags = "".join('<span class="tag">%s</span>' % t for t in p["tags"])
    return (
        '<article class="post-card">'
        '<h2 class="post-title"><a href="%sposts/%s.html">%s</a></h2>'
        '<div class="post-meta"><span>%s</span><span class="dot">·</span>'
        '<span class="cat">%s</span><span class="dot">·</span>'
        '<span>%s 分钟</span></div>'
        '<p class="post-summary">%s</p>'
        '<div class="tags">%s</div>'
        "</article>"
    ) % (prefix, p["slug"], p["title"], p["date"], p["category_cn"],
         p["reading_min"], p["summary"], tags)


def render_page(title, desc, content, prefix="", extra_head=""):
    return (BASE
            .replace("{TITLE}", title)
            .replace("{DESC}", desc)
            .replace("{PREFIX}", prefix)
            .replace("{EXTRA_HEAD}", extra_head)
            .replace("{CONTENT}", content))


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    shutil.rmtree(OUT_DIR, ignore_errors=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    posts = load_posts()

    # ---- 首页 ----
    posts_json = json.dumps([
        {
            "title": p["title"], "date": p["date"], "category": p["category"],
            "category_cn": p["category_cn"], "tags": p["tags"],
            "summary": p["summary"], "reading_min": p["reading_min"],
            "url": "posts/%s.html" % p["slug"],
        }
        for p in posts
    ], ensure_ascii=False)
    index_content = (load_template("index.html").replace("{POSTS_JSON}", posts_json))
    write(os.path.join(OUT_DIR, "index.html"),
          render_page("技术笔记", "记录算法、深度学习、编程与学习的个人博客", index_content))

    # ---- 文章页 ----
    post_tpl = load_template("post.html")
    posts_out = os.path.join(OUT_DIR, "posts")
    os.makedirs(posts_out, exist_ok=True)
    for p in posts:
        tags = "".join('<span class="tag">%s</span>' % t for t in p["tags"])
        content = (post_tpl
                   .replace("{TITLE}", p["title"])
                   .replace("{DATE}", p["date"])
                   .replace("{CATEGORY_CN}", p["category_cn"])
                   .replace("{READING}", str(p["reading_min"]))
                   .replace("{BODY}", p["html"])
                   .replace("{TAGS}", tags))
        write(os.path.join(posts_out, p["slug"] + ".html"),
              render_page(p["title"], p["summary"], content, prefix="../"))

    # ---- 分类页 ----
    cat_tpl = load_template("category.html")
    cat_out = os.path.join(OUT_DIR, "category")
    os.makedirs(cat_out, exist_ok=True)
    for cat, cn in CATEGORIES.items():
        items = [p for p in posts if p["category"] == cat]
        cards = "".join(card_html(p, "../") for p in items) or '<p class="empty">暂无文章。</p>'
        content = (cat_tpl
                   .replace("{CATEGORY_CN}", cn)
                   .replace("{COUNT}", str(len(items)))
                   .replace("{CARDS}", cards))
        write(os.path.join(cat_out, cat + ".html"),
              render_page(cn, cn + " 分类下的文章", content, prefix="../"))

    # ---- 关于页 ----
    if os.path.isfile(ABOUT_SRC):
        text = open(ABOUT_SRC, encoding="utf-8").read()
        fm, body = parse_frontmatter(text)
        content = (load_template("about.html")
                   .replace("{TITLE}", fm.get("title", "关于"))
                   .replace("{BODY}", render_markdown(body)))
        write(os.path.join(OUT_DIR, "about.html"),
              render_page(fm.get("title", "关于"), "关于本站", content))

    # ---- 静态资源 ----
    if os.path.isdir(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, os.path.join(OUT_DIR, "assets"))

    print("生成完成：%d 篇文章 -> %s" % (len(posts), OUT_DIR))


if __name__ == "__main__":
    main()
