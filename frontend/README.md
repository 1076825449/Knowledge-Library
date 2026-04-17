# frontend/ 前端目录

## 技术栈

- **Jinja2 模板** — 服务端渲染，由Flask后端直接render
- **原生HTML/CSS** — 无前端框架依赖
- **静态CSS** — `frontend/static/css/style.css`

当前为原型阶段，采用服务端渲染而非SPA架构。如需升级为React/Vue等框架，请参考 `docs/` 目录下的规划文档。

## 页面结构

```
frontend/
├── templates/           # Jinja2 HTML模板（由Flask render_template()调用）
│   ├── base.html        # 基础模板（导航栏、页脚）
│   ├── index.html       # 首页（高频问题、新手必看、最近更新）
│   ├── questions.html   # 问题列表页（支持多维过滤+搜索）
│   ├── detail.html       # 问题详情页（含政策依据、更新记录、关联问题）
│   ├── new_question.html # 新建问题表单（需admin认证）
│   ├── edit_question.html # 编辑问题表单（需admin认证）
│   └── admin_login.html  # 管理员登录页
├── static/
│   └── css/
│       └── style.css    # 全局样式
└── README.md
```

## URL路由对应

| 模板文件 | 对应URL | 说明 |
|----------|---------|------|
| index.html | `/` | |
| questions.html | `/questions` | |
| detail.html | `/question/<code>` | |
| new_question.html | `/question/new` | |
| edit_question.html | `/question/<code>/edit` | |
| admin_login.html | — | **不是独立路由**，由 `admin_required` 在访问 `/question/new` 或 `/question/<code>/edit` 检测到未认证时按需渲染的登录页模板 |

## 模板规范

- 所有模板继承 `base.html`
- 标签显示使用模板内嵌宏（`certainty_label()`、`policy_level_label()` 等），不接受 raw code 显示
- 政策依据按 `support_type` 分组显示
- 问答卡片使用结构化字段（`one_line_answer`、`detailed_answer`、`risk_warning` 等）

## 注意事项

- 前端无独立构建步骤，随Flask服务启动即可访问
- 静态文件通过 `/static/` 路径访问
- 当前无JavaScript交互逻辑（如需加，请扩展 `base.html` 的 `<script>` 块）
