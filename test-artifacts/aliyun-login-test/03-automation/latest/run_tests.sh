#!/bin/bash
# ============================================================
# 阿里云登录自动化测试执行脚本
# ============================================================

set -e

# 项目配置
PROJECT_NAME="aliyun-login-test"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# 结果目录
RESULT_DIR="$PROJECT_ROOT/reports/run-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================="
echo "  阿里云登录自动化测试"
echo "  项目: $PROJECT_NAME"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="
echo ""

# 检查 Python 环境
echo -e "${YELLOW}[1/5] 检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python3${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "Python 版本: $PYTHON_VERSION"

# 安装依赖
echo ""
echo -e "${YELLOW}[2/5] 安装依赖...${NC}"
pip install -r "$PROJECT_ROOT/requirements.txt" -q

# 安装 Playwright 浏览器
echo ""
echo -e "${YELLOW}[3/5] 安装 Playwright 浏览器...${NC}"
python3 -m playwright install chromium

# 创建报告目录
echo ""
echo -e "${YELLOW}[4/5] 创建报告目录...${NC}"
mkdir -p "$PROJECT_ROOT/reports"
mkdir -p "$PROJECT_ROOT/screenshots"
echo "报告目录: $RESULT_DIR"

# 执行测试
echo ""
echo -e "${YELLOW}[5/5] 开始执行测试...${NC}"
echo ""

cd "$PROJECT_ROOT"

# 根据参数选择测试类型
TEST_TYPE="${1:-all}"

case "$TEST_TYPE" in
    "login")
        echo "执行登录功能测试..."
        pytest tests/test_login.py \
            --html="$RESULT_DIR/test-report-login.html" \
            --self-contained-html \
            -v \
            2>&1 | tee "$RESULT_DIR/execution.log"
        ;;
    "security")
        echo "执行安全测试..."
        pytest tests/test_security.py \
            --html="$RESULT_DIR/test-report-security.html" \
            --self-contained-html \
            -v \
            2>&1 | tee "$RESULT_DIR/execution.log"
        ;;
    "redirect")
        echo "执行跳转测试..."
        pytest tests/test_redirect.py \
            --html="$RESULT_DIR/test-report-redirect.html" \
            --self-contained-html \
            -v \
            2>&1 | tee "$RESULT_DIR/execution.log"
        ;;
    "p0")
        echo "执行 P0 优先级测试..."
        pytest tests/ \
            -m p0 \
            --html="$RESULT_DIR/test-report-p0.html" \
            --self-contained-html \
            -v \
            2>&1 | tee "$RESULT_DIR/execution.log"
        ;;
    "all")
        echo "执行全部测试..."
        pytest tests/ \
            --html="$RESULT_DIR/test-report.html" \
            --self-contained-html \
            --json-report \
            --json-report-file="$RESULT_DIR/test-results.json" \
            -v \
            2>&1 | tee "$RESULT_DIR/execution.log"
        ;;
    *)
        echo "未知测试类型: $TEST_TYPE"
        echo "可用类型: all, login, security, redirect, p0"
        exit 1
        ;;
esac

# 输出结果
echo ""
echo "============================================="
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 测试执行完成${NC}"
else
    echo -e "${RED}❌ 测试执行失败${NC}"
fi
echo "============================================="
echo ""
echo "结果文件:"
echo "  - HTML 报告: $RESULT_DIR/test-report*.html"
echo "  - JSON 结果: $RESULT_DIR/test-results.json"
echo "  - 执行日志: $RESULT_DIR/execution.log"
echo "  - 截图目录: $PROJECT_ROOT/screenshots/"
echo ""
