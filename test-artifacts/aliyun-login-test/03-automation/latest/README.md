# 阿里云登录功能自动化测试

## 项目概述

本项目使用 **Playwright + pytest** 框架对阿里云登录功能进行自动化测试。

- **测试对象**: https://account.aliyun.com/login/login.htm
- **测试框架**: Playwright + pytest
- **编程语言**: Python 3.9+

## 测试用例覆盖

### P0 优先级测试用例（约 28 个）

| 模块 | 用例编号 | 用例数量 | 状态 |
|------|----------|----------|------|
| 账号密码登录 | TC-LOGIN-001 ~ TC-LOGIN-011 | 11 | ✅ 已实现 |
| 安全测试-SQL注入 | TC-SECURITY-001 ~ TC-SECURITY-005 | 5 | ✅ 已实现 |
| 安全测试-XSS注入 | TC-SECURITY-006 ~ TC-SECURITY-010 | 5 | ✅ 已实现 |
| 安全测试-CSRF | TC-SECURITY-011 | 1 | ✅ 已实现 |
| 安全测试-暴力破解 | TC-SECURITY-012 | 1 | ⚠️ 跳过（需Mock） |
| 安全测试-HTTPS | TC-SECURITY-013 | 1 | ✅ 已实现 |
| 安全测试-密码加密 | TC-SECURITY-014 | 1 | ✅ 已实现 |
| 安全测试-安全头 | TC-SECURITY-015 | 1 | ✅ 已实现 |
| 登录跳转 | TC-REDIRECT-001 ~ TC-REDIRECT-005 | 5 | ✅ 已实现 |
| 账号锁定 | TC-LOCK-001 ~ TC-LOCK-002 | 2 | ⚠️ 跳过（需Mock） |

## 目录结构

```
03-automation/v1/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures 和配置
│   ├── test_login.py            # 登录功能测试 (11 个用例)
│   ├── test_security.py         # 安全测试 (15 个用例)
│   └── test_redirect.py         # 跳转测试 (5 个用例)
├── pages/
│   ├── __init__.py
│   └── login_page.py            # 登录页面对象 (Page Object)
├── fixtures/
│   └── test-data.json           # 测试数据
├── reports/                     # 测试报告（执行后生成）
├── screenshots/                 # 失败截图（执行后生成）
├── requirements.txt             # Python 依赖
├── pytest.ini                   # pytest 配置
├── run_tests.sh                 # 执行脚本
├── .env.example                 # 环境变量示例
└── README.md                    # 使用说明
```

## 环境要求

- **Python**: 3.9+
- **浏览器**: Chromium（自动安装）
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要访问 https://account.aliyun.com

## 快速开始

### 1. 安装依赖

```bash
cd test-artifacts/aliyun-login-test/03-automation/v1/
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
python -m playwright install chromium
```

### 3. 配置环境变量（可选）

```bash
cp .env.example .env
# 编辑 .env 文件，配置测试环境参数
```

### 4. 执行测试

#### 执行全部测试

```bash
chmod +x run_tests.sh
./run_tests.sh all
```

#### 执行特定模块测试

```bash
# 仅执行登录功能测试
./run_tests.sh login

# 仅执行安全测试
./run_tests.sh security

# 仅执行跳转测试
./run_tests.sh redirect

# 仅执行 P0 优先级测试
./run_tests.sh p0
```

#### 使用 pytest 直接执行

```bash
# 执行所有测试
pytest tests/ -v

# 执行登录测试
pytest tests/test_login.py -v

# 执行安全测试
pytest tests/test_security.py -v

# 执行标记为 p0 的测试
pytest tests/ -m p0 -v

# 执行标记为 security 的测试
pytest tests/ -m security -v

# 指定浏览器
pytest tests/ --browser=chromium -v
pytest tests/ --browser=firefox -v
```

### 5. 查看结果

测试执行完成后，结果文件位于 `reports/run-{timestamp}/` 目录：

| 文件 | 说明 |
|------|------|
| `test-report.html` | HTML 格式测试报告 |
| `test-results.json` | JSON 格式测试结果 |
| `execution.log` | 执行日志 |
| `screenshots/` | 失败用例截图 |

## 测试标记 (Markers)

| 标记 | 说明 |
|------|------|
| `p0` | P0 优先级（最高优先级） |
| `p1` | P1 优先级 |
| `p2` | P2 优先级 |
| `login` | 登录功能测试 |
| `security` | 安全测试 |
| `redirect` | 跳转测试 |
| `lockout` | 账号锁定测试 |

## 注意事项

### 1. 验证码处理

由于阿里云登录页面有验证码机制，部分需要实际登录的用例会：
- 自动检测验证码并标记为 `xfail`（预期失败）
- 在测试环境中可以关闭验证码或使用测试专用环境

### 2. 安全测试限制

- **暴力破解测试** (`TC-SECURITY-012`): 默认跳过，因为会触发安全限制
- **账号锁定测试** (`TC-LOCK-001`, `TC-LOCK-002`): 默认跳过，需要 Mock 环境

### 3. 测试数据

- 所有测试数据使用模拟数据，不使用真实账号密码
- 测试数据配置在 `fixtures/test-data.json` 中
- 如需使用真实测试环境，请修改测试数据文件

### 4. 反爬虫机制

- 脚本中已添加合理的等待时间
- 使用真实的 User-Agent
- 避免高频请求

## 故障排查

### 问题：浏览器无法启动

```bash
# 重新安装 Playwright 浏览器
python -m playwright install --force chromium
```

### 问题：页面加载超时

- 检查网络连接
- 增加超时时间：在 `conftest.py` 中修改 `page.set_default_timeout()`

### 问题：元素定位失败

- 阿里云页面可能更新，需要检查 `login_page.py` 中的定位器
- 使用 `page.screenshot()` 截图调试

## 扩展开发

### 添加新的测试用例

1. 在 `tests/` 目录下创建新的测试文件
2. 使用 `@pytest.mark.p0` 等标记优先级
3. 在测试函数注释中标明对应的 TC 编号

### 添加新的页面对象

1. 在 `pages/` 目录下创建新的页面对象文件
2. 使用 Page Object 模式封装页面操作
3. 在 `conftest.py` 中添加对应的 fixture

## 联系方式

如有问题，请联系测试团队。
