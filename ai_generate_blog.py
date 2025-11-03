import os
import random
import re
import base64
from datetime import datetime
from zhipuai import ZhipuAI

# === 1. 初始化 ===
api_key = os.getenv("ZHIPUAI_API_KEY")
if not api_key:
    raise ValueError("❌ 请先配置环境变量 ZHIPUAI_API_KEY")

client = ZhipuAI(api_key=api_key)

# === 2. 选题 ===
topics = [
    "AI如何帮助程序员自动生成日报",
    "用AI生成并部署个人网站",
    "AI自动生成SQL报表并可视化",
    "AI如何帮你写README文档",
    "用AI自动生成代码注释",
    "AI生成自动化测试用例",
    "AI自动总结会议纪要",
    "AI监控网站运行状态",
    "AI生成项目周报",
    "AI生成知识笔记并发布博客"
]

topic = random.choice(topics)
today = datetime.now().strftime("%Y-%m-%d")
slug = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]+', '-', topic)

# === 3. 路径设置 ===
output_blog_dir = "docs/blog/posts"
output_xhs_dir = "docs/xhs"
image_dir = f"{output_blog_dir}/images"
os.makedirs(output_blog_dir, exist_ok=True)
os.makedirs(output_xhs_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

blog_filename = f"{output_blog_dir}/{today}-{slug}.md"
xhs_filename = f"{output_xhs_dir}/{today}-{slug}-xhs.md"
image_filename = f"{image_dir}/{today}-{slug}.png"

print(f"🧠 正在生成主题《{topic}》的博客...")

# === 4. 博客正文 ===
blog_prompt = f"""
你是一位拥有9年经验的全栈开发者，请写一篇主题为《{topic}》的原创技术博客。

要求：
- Markdown 格式
- 包含：问题场景、AI解决思路、实现步骤（带代码示例）、效果展示、总结
- 语气自然、有实操经验
- 输出时带 YAML 头部(title/date/tags/summary/author)，严格按照以下格式，只需要一个---开始和一个---结束，不要在YAML中使用额外的代码块或嵌套格式：
---
title: [文章标题]
date: [发布日期]
tags: [标签列表]
summary: [文章摘要]
author: AI助手
---
"""

resp = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": blog_prompt}],
)
content = resp.choices[0].message.content.strip()

# === 5. 生成封面图 ===
print("🎨 正在生成封面图...")

try:
    image_prompt = f"一张横版16:9的封面图，主题是“{topic}”，风格未来感、极简科技感、亮色调"

    img_resp = client.images.generations(
        model="cogview-3",
        prompt=image_prompt,
        size="1024x576"
    )

    # 判断返回是否正常
    if img_resp and hasattr(img_resp, "data") and len(img_resp.data) > 0:
        image_base64 = getattr(img_resp.data[0], "b64_json", None)
        if image_base64:
            with open(image_filename, "wb") as f:
                f.write(base64.b64decode(image_base64))
            print(f"🖼️ 封面已保存：{image_filename}")
        else:
            print("⚠️ 未返回有效图像数据，跳过封面保存。")
    else:
        print("⚠️ AI 未生成图像（data 为空），跳过封面生成。")

except Exception as e:
    print(f"⚠️ 生成封面失败：{e}")

# === 6. 插入封面路径和确保正确的YAML格式 ===
# 修复可能的嵌套YAML代码块问题
content = re.sub(r'```yaml[\s\S]*?```', '', content)

# 确保YAML中包含author字段
if "author:" not in content[:500]:
    # 查找第二个---并在其前面插入author字段
    parts = content.split("---")
    if len(parts) >= 3:
        yaml_part = parts[1]
        if not yaml_part.strip().endswith("author:"):
            parts[1] = yaml_part + "\nauthor: AI助手\n"
        content = "---".join(parts)

# 插入封面路径
if content.startswith("---"):
    # 检查是否已有cover字段，如果没有则添加
    if "cover:" not in content[:500]:
        content = content.replace("---", f"---\ncover: ./images/{today}-{slug}.png", 1)
else:
    content = f"---\ncover: ./images/{today}-{slug}.png\nauthor: AI助手\n---\n{content}"


with open(blog_filename, "w", encoding="utf-8") as f:
    f.write(content)
print(f"✅ 博客已生成：{blog_filename}")

# === 7. 小红书版本 ===
print("📱 正在生成小红书笔记版本...")
xhs_prompt = f"""
请将以下博客内容改写成一篇适合小红书发布的笔记风格文章。

要求：
- 语气轻松、有吸引力、有实用感
- 用 emoji 表情适当点缀1
- 开头要吸引人
- 添加3~5个小红书标签（如 #AI工具推荐 #效率神器 #编程日常）
- 内容长度控制在600字以内
- 最后附上一句总结性金句或call to action
博客内容如下：
{content}
"""

xhs_resp = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": xhs_prompt}],
)
xhs_text = xhs_resp.choices[0].message.content.strip()

xhs_header = f"""---
title: {topic}
date: {today}
cover: ../blog/posts/images/{today}-{slug}.png
platform: xiaohongshu
---

"""
with open(xhs_filename, "w", encoding="utf-8") as f:
    f.write(xhs_header + xhs_text)
print(f"✅ 小红书笔记已生成：{xhs_filename}")
