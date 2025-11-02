# VitePress 博客启动器

## 项目概述

这是一个基于 VitePress 构建的博客启动器项目，集成了 UnoCSS、Vue 3 等现代前端技术，提供了完整的博客功能示例，包括文章发布、作者信息、分类标签等。

## 技术栈

- **VitePress 1.6.3**：基于 Vue 3 的静态站点生成器，专为文档网站设计
- **Vue 3.5.13**：渐进式 JavaScript 框架
- **UnoCSS 65.4.3**：即时原子化 CSS 引擎，提供高效的样式解决方案
- **Anu Vue 0.15.2**：Vue 3 UI 库
- **TypeScript**：类型安全的 JavaScript 超集
- **pnpm**：高性能的包管理器
- **GitHub Actions**：自动化部署工作流
- **Netlify**：可选的部署平台（配置文件已包含）

## 核心功能

- **博客系统**：完整的博客功能，支持文章列表、详情页、分类和标签
- **作者信息**：支持多作者配置和展示
- **搜索功能**：内置本地搜索
- **代码高亮**：Markdown 代码块语法高亮
- **响应式设计**：适配各种屏幕尺寸
- **原子化 CSS**：使用 UnoCSS 进行高效样式管理
- **图标系统**：集成多种图标集（Heroicons、Boxicons、Fluent Emoji 等）

## 项目结构

```
ai-blog/
├── .github/                  # GitHub 配置目录
│   └── workflows/            # GitHub Actions 工作流
│       └── deploy.yml        # 部署配置
├── docs/                     # 文档内容目录
│   ├── .vitepress/           # VitePress 配置目录
│   │   ├── config.mts        # VitePress 主配置文件
│   │   └── theme/            # 自定义主题目录
│   ├── blog/                 # 博客相关内容
│   │   ├── authors/          # 作者信息
│   │   ├── posts/            # 博客文章
│   │   └── index.md          # 博客首页
│   ├── guide/                # 指南文档
│   │   └── features/         # 功能说明
│   ├── config/               # 配置说明
│   ├── public/               # 静态资源
│   │   └── images/           # 图片资源
│   ├── index.md              # 网站首页
│   └── uno.config.ts         # UnoCSS 配置
├── eslint.config.js          # ESLint 配置
├── netlify.toml              # Netlify 配置
├── package.json              # 项目依赖配置
└── pnpm-lock.yaml            # pnpm 依赖锁文件
```

## 操作命令

### 安装依赖

```bash
pnpm install
```

### 开发服务器

启动本地开发服务器，实时预览网站效果：

```bash
pnpm dev
```

开发服务器默认运行在 `http://localhost:5173/ai-blog/`

### 构建网站

构建生产版本的静态网站：

```bash
pnpm build
```

构建产物将生成在 `docs/.vitepress/dist/` 目录

### 预览构建结果

本地预览构建后的网站：

```bash
pnpm serve
```

### 代码检查

运行 ESLint 检查代码质量：

```bash
pnpm lint
```

自动修复 ESLint 错误：

```bash
pnpm lint:fix
```

### 发布新版本

执行发布流程（包括 lint、build、生成 changelog、推送标签）：

```bash
pnpm release
```

## 部署流程

### GitHub Pages 部署

项目已配置 GitHub Actions 自动部署工作流，部署流程如下：

1. 当代码推送到主分支时，GitHub Actions 自动触发部署
2. 工作流执行以下步骤：
   - 检出代码仓库
   - 设置 Node.js 环境
   - 安装依赖
   - 构建网站
   - 部署到 GitHub Pages

### Netlify 部署

项目已包含 `netlify.toml` 配置文件，可直接在 Netlify 平台部署：

1. 在 Netlify 上创建新项目
2. 连接到 GitHub 仓库
3. Netlify 会自动检测配置并部署

## 如何添加新博客文章

1. 在 `docs/blog/posts/` 目录下创建新的 Markdown 文件（例如：`my-new-post.md`）
2. 在文件头部添加前置元数据（frontmatter）：

```markdown
---
date: 2024-01-01
title: 我的新博客文章
category: 教程
tags: [vue, vite]
---
```

3. 使用 Markdown 格式编写博客内容
4. 可选：使用 `<PostDetail>` 组件包装内容以获得更好的展示效果
5. 推送到仓库，触发自动部署

## 如何添加新作者

1. 在 `docs/blog/authors/` 目录下创建作者的 Markdown 文件
2. 设置作者信息的前置元数据
3. 在博客文章中引用对应的作者

## 配置说明

### VitePress 配置

主要配置位于 `docs/.vitepress/config.mts` 文件中：

- `base`：网站基础路径
- `title`：网站标题
- `description`：网站描述
- `themeConfig`：主题配置（导航、侧边栏、搜索等）
- `vite.plugins`：Vite 插件配置（如 UnoCSS）

### UnoCSS 配置

UnoCSS 配置位于 `docs/uno.config.ts` 文件中：

- `presets`：使用的预设（presetUno、presetIcons）
- `transformers`：使用的转换器
- `content`：内容处理配置

## 主题组件

项目自定义了多个博客相关组件，位于 `docs/.vitepress/theme/components/blog/` 目录：

- `Posts.vue`：博客文章列表组件
- `Post.vue`：单篇博客文章组件
- `PostDetail.vue`：博客文章详情包装组件
- `PostAuthor.vue`：作者信息组件
- `AuthorDetail.vue`：作者详情组件
- `PostIcon.vue`：文章图标组件

## 注意事项

- 确保 Node.js 版本与项目兼容（推荐使用 pnpm 和较新版本的 Node.js）
- 修改 `base` 配置时，请与实际部署路径保持一致
- 博客文章使用 Markdown 格式编写
- 代码推送到主分支后，部署通常需要几分钟完成

## 故障排除

- **依赖安装失败**：检查 Node.js 版本，尝试清除缓存后重新安装
- **构建失败**：检查 TypeScript 类型错误或其他编译错误
- **部署失败**：检查 GitHub Actions 日志以获取详细错误信息
- **本地开发问题**：确保 `pnpm dev` 命令执行成功，检查浏览器控制台错误信息
- **样式问题**：确认 UnoCSS 配置正确，检查类名拼写

## 许可证

本项目采用 MIT 许可证。详情请参阅 `LICENSE.md` 文件。
