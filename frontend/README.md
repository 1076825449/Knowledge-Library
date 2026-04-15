# frontend/ 前端目录

## 技术栈建议

当前阶段建议使用轻量方案：

- **React** 或 **Vue**（任选）
- 或使用 **Next.js**（React 全栈框架）
- 样式：CSS Modules / Tailwind CSS

## 起步

```bash
cd frontend
npm install
npm run dev
```

## 目录结构

```
frontend/
├── README.md           # 本文件
├── public/             # 静态资源
├── src/
│   ├── pages/          # 页面
│   ├── components/     # 可复用组件
│   ├── layouts/        # 布局组件
│   ├── services/       # API 请求层
│   ├── hooks/          # 自定义 Hooks
│   ├── utils/          # 工具函数
│   ├── styles/         # 样式文件
│   ├── types/          # TypeScript 类型定义
│   ├── constants/      # 常量
│   └── assets/         # 前端静态资源
└── package.json
```

## 核心页面

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页 | `/` | 搜索、阶段入口、模块入口、高频问题 |
| 问题列表 | `/questions` | 筛选、分页 |
| 问题详情 | `/questions/:code` | 问题卡片完整展示 |
| 标签页 | `/tags/:code` | 某标签下所有问题 |
| 更新日志 | `/updates` | 最近更新 |

## 组件清单

| 组件 | 说明 |
|------|------|
| `SearchBar` | 搜索框 |
| `QuestionCard` | 问题卡片摘要 |
| `PolicyBasisBlock` | 政策依据展示块 |
| `TagChip` | 标签徽章 |
| `StageNav` | 生命周期阶段导航 |
| `ModuleNav` | 主题模块导航 |
| `UpdateList` | 更新记录列表 |
