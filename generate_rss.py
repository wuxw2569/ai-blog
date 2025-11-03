import os
import datetime
import re
from glob import glob

BLOG_DIR = "docs/blog/posts"
RSS_FILE = f"docs/blog/feed.xml"
SITE_URL = "https://wuxw2569.github.io/ai-blog"  # 改成你博客实际地址

def extract_meta(md_path):
    """从 markdown 文件头部提取 title, date, summary"""
    title, date, summary = None, None, ""
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 提取 YAML 头部
    in_yaml = False
    for line in lines:
        if line.strip() == "---":
            in_yaml = not in_yaml
            continue
        if in_yaml:
            if line.startswith("title:"):
                title = line.replace("title:", "").strip()
            elif line.startswith("date:"):
                date = line.replace("date:", "").strip()
            elif line.startswith("summary:"):
                summary = line.replace("summary:", "").strip()
        elif title and date:
            break

    # 从文件内容生成简短描述
    if not summary:
        text = "".join(lines)
        summary = re.sub(r"[#>\-\*\n]", "", text)[:100]
    return title, date, summary

def build_rss():
    posts = sorted(glob(f"{BLOG_DIR}/*.md"), reverse=True)
    items = []
    for md in posts:
        title, date, summary = extract_meta(md)
        link = f"{SITE_URL}/{os.path.basename(md)}".replace(".md", ".html")
        item = f"""
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <description><![CDATA[{summary}]]></description>
            <pubDate>{date}</pubDate>
        </item>
        """
        items.append(item)

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>AI Blog 自动博客</title>
        <link>{SITE_URL}</link>
        <description>由 AI 自动生成的技术博客 + 小红书笔记</description>
        <language>zh-cn</language>
        <lastBuildDate>{datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')}</lastBuildDate>
        {''.join(items)}
    </channel>
    </rss>
    """
    os.makedirs(os.path.dirname(RSS_FILE), exist_ok=True)
    with open(RSS_FILE, "w", encoding="utf-8") as f:
        f.write(rss)
    print(f"✅ RSS feed generated: {RSS_FILE}")

if __name__ == "__main__":
    build_rss()
