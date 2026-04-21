# 人教版小学英语课本 - 自动化测试

## 测试范围

| 模块 | 文件 | 用例数 |
|------|------|--------|
| 导航功能 | test_navigation.py | 8 |
| 年级选择 | test_grade_selection.py | 12 |
| 册次选择 | test_volume_selection.py | 10 |
| 单元选择 | test_unit_selection.py | 9 |
| 内容展示 | test_content_display.py | 17 |
| 面包屑导航 | test_breadcrumb.py | 10 |
| **合计** | | **66** |

## 环境要求

- Python 3.9+
- Playwright 浏览器（Chromium）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 执行测试

```bash
# 运行全部测试
pytest tests/ -v

# 运行单个模块
pytest tests/test_navigation.py -v

# 运行带屏幕显示（非 headless）
pytest tests/ --headed -v

# 生成 HTML 报告
pytest tests/ --html=report.html --self-contained-html -v
```

### 3. 测试结构

```
tests/
├── conftest.py              # fixture：page_goto / page_with_grade / page_with_unit
├── test_navigation.py       # 首页/内容/关于视图切换
├── test_grade_selection.py  # 三至六年级卡片选择
├── test_volume_selection.py # 上册/下册按钮选择
├── test_unit_selection.py   # 单元按钮选择
├── test_content_display.py  # 词汇/句型/对话渲染
└── test_breadcrumb.py       # 面包屑路径与回退
```

### 4. Fixture 说明

| Fixture | 前置状态 |
|---------|----------|
| `page_goto` | 页面已加载，停留在首页 |
| `page_with_grade` | 已选择三年级，停留在内容视图（册次选择器可见） |
| `page_with_unit` | 完整链路：三年级 → 上册 → Unit 1（内容已展示） |
