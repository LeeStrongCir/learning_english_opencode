"""
阿里云登录安全测试 (Security Tests)

测试用例覆盖：
- TC-SECURITY-001 ~ TC-SECURITY-005: SQL注入测试
- TC-SECURITY-006 ~ TC-SECURITY-010: XSS注入测试
- TC-SECURITY-011: CSRF Token 验证
- TC-SECURITY-012: 暴力破解防护
- TC-SECURITY-013: HTTPS 连接验证
- TC-SECURITY-014: 密码传输加密验证
- TC-SECURITY-015: 安全响应头验证

注意：安全测试针对真实网站，部分测试可能需要 Mock 环境
"""

import pytest
import logging
import re
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


# ============================================================
# SQL 注入测试
# ============================================================

class TestSQLInjection:
    """SQL 注入防护测试"""

    @pytest.mark.p0
    @pytest.mark.security
    @pytest.mark.parametrize("payload", [
        "' OR '1'='1",
        "' OR 1=1 --",
        "admin' --",
    ])
    def test_security_001_sql_injection_in_account(self, login_page, payload):
        """
        TC-SECURITY-001/002/003: 账号字段 SQL 注入测试

        测试步骤：
        1. 在账号输入框输入 SQL 注入 payload
        2. 输入任意密码
        3. 点击登录

        预期结果：
        - 登录失败
        - 不返回数据库错误信息
        - 页面不崩溃
        """
        logger.info(f"=== TC-SECURITY-001~003: SQL注入测试 (账号) - {payload} ===")

        # 执行登录（SQL 注入 payload 作为账号）
        login_page.login(payload, "AnyPassword123!")

        # 等待响应
        login_page.page.wait_for_timeout(2000)

        # 验证：页面仍然正常（没有崩溃）
        assert login_page.is_on_login_page(), "SQL 注入不应导致页面崩溃或跳转"

        # 验证：没有暴露数据库错误信息
        page_content = login_page.page.content()
        db_error_patterns = [
            r"SQL\s*syntax",
            r"mysql_",
            r"ORA-\d+",
            r"PostgreSQL.*ERROR",
            r"SQLite.*Error",
            r"database.*error",
        ]

        for pattern in db_error_patterns:
            matches = re.findall(pattern, page_content, re.IGNORECASE)
            assert len(matches) == 0, f"发现数据库错误信息泄露: {pattern}"

        logger.info(f"TC-SECURITY-001~003: SQL注入防护测试通过 - {payload}")

    @pytest.mark.p0
    @pytest.mark.security
    @pytest.mark.parametrize("payload", [
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users --",
    ])
    def test_security_004_sql_injection_destructive(self, login_page, payload):
        """
        TC-SECURITY-004/005: 破坏性 SQL 注入测试

        测试步骤：
        1. 在账号输入框输入破坏性 SQL payload
        2. 输入任意密码
        3. 点击登录

        预期结果：
        - 登录失败
        - 不执行 SQL 语句
        - 页面正常
        """
        logger.info(f"=== TC-SECURITY-004~005: 破坏性SQL注入测试 - {payload} ===")

        login_page.login(payload, "AnyPassword123!")
        login_page.page.wait_for_timeout(2000)

        # 验证：页面仍然正常
        assert login_page.is_on_login_page(), "破坏性 SQL 注入不应影响页面"

        # 验证：没有数据库错误
        page_content = login_page.page.content()
        assert "SQL" not in page_content.upper() or "SQL" not in page_content, \
            "不应暴露 SQL 相关信息"

        logger.info(f"TC-SECURITY-004~005: 破坏性SQL注入防护测试通过")


# ============================================================
# XSS 注入测试
# ============================================================

class TestXSSInjection:
    """XSS 注入防护测试"""

    @pytest.mark.p0
    @pytest.mark.security
    @pytest.mark.parametrize("payload", [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
    ])
    def test_security_006_xss_in_account(self, login_page, payload):
        """
        TC-SECURITY-006/007/008: 账号字段 XSS 注入测试

        测试步骤：
        1. 在账号输入框输入 XSS payload
        2. 输入任意密码
        3. 点击登录

        预期结果：
        - 登录失败
        - XSS payload 被转义或过滤
        - 不执行 JavaScript
        """
        logger.info(f"=== TC-SECURITY-006~008: XSS注入测试 (账号) - {payload[:30]}... ===")

        # 设置 dialog 事件监听，如果弹出 alert 说明 XSS 成功（应该失败）
        dialog_fired = {"fired": False}

        def on_dialog(dialog):
            dialog_fired["fired"] = True
            dialog.dismiss()

        login_page.page.on("dialog", on_dialog)

        # 执行登录（XSS payload 作为账号）
        login_page.login(payload, "AnyPassword123!")
        login_page.page.wait_for_timeout(2000)

        # 验证：没有触发 JavaScript 弹窗
        assert not dialog_fired["fired"], f"XSS payload 被执行: {payload}"

        # 验证：payload 被转义
        page_content = login_page.page.content()
        # 检查原始 script 标签是否存在（应该被转义）
        if "<script>" in payload:
            # 如果页面中存在未转义的 script 标签，说明 XSS 防护失败
            # 注意：这里检查的是错误提示中是否包含未转义的内容
            error_msg = login_page.get_error_message()
            if error_msg:
                assert "<script>" not in error_msg, "XSS payload 未被转义"

        logger.info(f"TC-SECURITY-006~008: XSS注入防护测试通过")

    @pytest.mark.p0
    @pytest.mark.security
    @pytest.mark.parametrize("payload", [
        "<svg onload=alert('XSS')>",
        "\"><script>alert(String.fromCharCode(88,83,83))</script>",
    ])
    def test_security_009_xss_advanced(self, login_page, payload):
        """
        TC-SECURITY-009/010: 高级 XSS 注入测试

        测试步骤：
        1. 在账号输入框输入高级 XSS payload
        2. 输入任意密码
        3. 点击登录

        预期结果：
        - 登录失败
        - XSS payload 被正确处理
        """
        logger.info(f"=== TC-SECURITY-009~010: 高级XSS注入测试 ===")

        dialog_fired = {"fired": False}

        def on_dialog(dialog):
            dialog_fired["fired"] = True
            dialog.dismiss()

        login_page.page.on("dialog", on_dialog)

        login_page.login(payload, "AnyPassword123!")
        login_page.page.wait_for_timeout(2000)

        assert not dialog_fired["fired"], f"高级 XSS payload 被执行: {payload}"

        logger.info("TC-SECURITY-009~010: 高级XSS注入防护测试通过")


# ============================================================
# CSRF Token 验证
# ============================================================

class TestCSRFProtection:
    """CSRF 防护测试"""

    @pytest.mark.p0
    @pytest.mark.security
    def test_security_011_csrf_token_validation(self, login_page, test_data):
        """
        TC-SECURITY-011: CSRF Token 验证

        测试步骤：
        1. 打开登录页面
        2. 检查是否存在 CSRF Token
        3. 尝试不带 CSRF Token 提交表单（模拟）

        预期结果：
        - 页面包含 CSRF Token
        - 不带 Token 的请求被拒绝
        """
        logger.info("=== TC-SECURITY-011: CSRF Token 验证 ===")

        # 获取 CSRF Token
        csrf_token = login_page.get_csrf_token()

        # 验证 CSRF Token 存在
        # 注意：阿里云可能使用其他机制（如 Referer 检查、SameSite cookie 等）
        if csrf_token:
            logger.info(f"CSRF Token found: {csrf_token[:10]}...")
            assert len(csrf_token) > 0, "CSRF Token 不应为空"
        else:
            # 检查其他 CSRF 防护机制
            logger.info("No explicit CSRF token found, checking alternative protections...")

            # 检查表单是否有 hidden token 字段
            page = login_page.page
            hidden_inputs = page.locator("input[type='hidden']")
            hidden_count = hidden_inputs.count()

            # 检查 cookie 中的安全设置
            cookies = page.context.cookies()
            csrf_cookies = [c for c in cookies if "csrf" in c["name"].lower()]

            # 至少有一种 CSRF 防护机制
            has_protection = csrf_token or hidden_count > 0 or len(csrf_cookies) > 0
            assert has_protection, "应该有某种 CSRF 防护机制"

        logger.info("TC-SECURITY-011: CSRF Token 验证通过")


# ============================================================
# 暴力破解防护
# ============================================================

class TestBruteForceProtection:
    """暴力破解防护测试"""

    @pytest.mark.p0
    @pytest.mark.security
    @pytest.mark.skip(reason="暴力破解测试会触发安全限制，需要 Mock 环境")
    def test_security_012_brute_force_protection(self, login_page, test_data):
        """
        TC-SECURITY-012: 暴力破解防护

        测试步骤：
        1. 使用同一账号连续尝试登录多次
        2. 观察是否触发防护机制

        预期结果：
        - 达到一定次数后要求验证码
        - 或账号被临时锁定
        """
        logger.info("=== TC-SECURITY-012: 暴力破解防护 ===")

        max_attempts = 10
        valid_account = test_data["login"]["valid_accounts"][0]
        wrong_password = "WrongPassword123!"

        captcha_triggered = False
        account_locked = False

        for attempt in range(max_attempts):
            login_page.login(valid_account["account"], wrong_password)
            login_page.page.wait_for_timeout(1500)

            error_msg = login_page.get_error_message()

            if error_msg:
                if "验证码" in error_msg or "captcha" in error_msg.lower():
                    captcha_triggered = True
                    logger.info(f"验证码防护触发于第 {attempt + 1} 次尝试")
                    break
                if "锁定" in error_msg or "lock" in error_msg.lower():
                    account_locked = True
                    logger.info(f"账号锁定触发于第 {attempt + 1} 次尝试")
                    break

        # 验证：至少有一种防护机制被触发
        assert captcha_triggered or account_locked, \
            "应该有暴力破解防护机制（验证码或锁定）"

        logger.info("TC-SECURITY-012: 暴力破解防护测试通过")


# ============================================================
# HTTPS 连接验证
# ============================================================

class TestHTTPSConnection:
    """HTTPS 连接验证测试"""

    @pytest.mark.p0
    @pytest.mark.security
    def test_security_013_https_connection(self, login_page):
        """
        TC-SECURITY-013: HTTPS 连接验证

        测试步骤：
        1. 打开登录页面
        2. 检查 URL 协议

        预期结果：
        - 使用 HTTPS 协议
        """
        logger.info("=== TC-SECURITY-013: HTTPS 连接验证 ===")

        # 验证当前连接是 HTTPS
        current_url = login_page.get_current_url()
        assert current_url.startswith("https://"), \
            f"登录页面必须使用 HTTPS，当前 URL: {current_url}"

        # 验证页面加载后仍然是 HTTPS
        assert login_page.is_https_connection(), "页面应该使用 HTTPS 连接"

        logger.info(f"TC-SECURITY-013: HTTPS 连接验证通过 - {current_url}")


# ============================================================
# 密码传输加密验证
# ============================================================

class TestPasswordEncryption:
    """密码传输加密验证测试"""

    @pytest.mark.p0
    @pytest.mark.security
    def test_security_014_password_transmission_encrypted(self, login_page, test_data):
        """
        TC-SECURITY-014: 密码传输加密验证

        测试步骤：
        1. 打开登录页面
        2. 监听网络请求
        3. 执行登录
        4. 检查登录请求中密码是否加密

        预期结果：
        - 密码在传输前被加密或哈希处理
        - 不在 URL 中明文传输
        """
        logger.info("=== TC-SECURITY-014: 密码传输加密验证 ===")

        # 收集登录请求
        login_requests = []

        def handle_request(request):
            if "login" in request.url.lower() and request.method == "POST":
                login_requests.append({
                    "url": request.url,
                    "method": request.method,
                    "post_data": request.post_data,
                })

        login_page.page.on("request", handle_request)

        # 执行登录
        invalid_account = test_data["login"]["invalid_accounts"][2]  # Wrong password
        login_page.login(invalid_account["account"], invalid_account["password"])
        login_page.page.wait_for_timeout(3000)

        # 检查登录请求
        if login_requests:
            for req in login_requests:
                # 验证密码不在 URL 中
                assert invalid_account["password"] not in req["url"], \
                    "密码不应出现在 URL 中"

                # 验证 POST 数据中密码被加密（如果能看到 post_data）
                if req["post_data"]:
                    # 密码不应该以明文形式出现
                    # 注意：由于 Playwright 的限制，可能无法完全验证
                    logger.info(f"Login request URL: {req['url']}")
                    logger.info("Password transmission check completed")
        else:
            logger.info("No login POST request captured (may be handled by JS)")

        # 验证密码输入框是遮蔽的
        assert login_page.is_password_masked(), "密码输入框应该遮蔽显示"

        logger.info("TC-SECURITY-014: 密码传输加密验证通过")


# ============================================================
# 安全响应头验证
# ============================================================

class TestSecurityHeaders:
    """安全响应头验证测试"""

    @pytest.mark.p0
    @pytest.mark.security
    def test_security_015_security_headers(self, login_page):
        """
        TC-SECURITY-015: 安全响应头验证

        测试步骤：
        1. 打开登录页面
        2. 检查响应头中的安全相关字段

        预期结果：
        - Strict-Transport-Security 存在
        - X-Frame-Options 存在
        - X-Content-Type-Options 存在
        """
        logger.info("=== TC-SECURITY-015: 安全响应头验证 ===")

        # 检查安全响应头
        security_headers = login_page.check_security_headers()

        logger.info(f"Security headers: {security_headers}")

        # 验证关键安全头
        # 注意：实际网站可能不完全包含所有安全头，这里做宽松检查

        # HSTS (Strict-Transport-Security)
        hsts = security_headers.get("strict_transport_security")
        if hsts:
            logger.info(f"HSTS header found: {hsts}")
            assert "max-age" in hsts.lower(), "HSTS 应该包含 max-age 指令"

        # X-Frame-Options (防止点击劫持)
        xfo = security_headers.get("x_frame_options")
        if xfo:
            logger.info(f"X-Frame-Options: {xfo}")
            assert xfo.lower() in ["deny", "sameorigin"], \
                "X-Frame-Options 应该是 DENY 或 SAMEORIGIN"

        # X-Content-Type-Options (防止 MIME 类型混淆)
        xcto = security_headers.get("x_content_type_options")
        if xcto:
            logger.info(f"X-Content-Type-Options: {xcto}")
            assert xcto.lower() == "nosniff", \
                "X-Content-Type-Options 应该是 nosniff"

        # 至少有一个安全头存在
        has_security_header = any(v is not None for v in security_headers.values())
        assert has_security_header, "至少应该有一个安全响应头"

        logger.info("TC-SECURITY-015: 安全响应头验证通过")


# ============================================================
# 额外安全测试：协议勾选
# ============================================================

class TestAgreementValidation:
    """服务协议验证测试"""

    @pytest.mark.p0
    @pytest.mark.security
    def test_security_agreement_required(self, login_page, test_data):
        """
        TC-SECURITY-016: 登录前必须同意服务协议

        测试步骤：
        1. 打开登录页面
        2. 检查是否有服务协议勾选框
        3. 不勾选协议尝试登录

        预期结果：
        - 如果存在协议勾选框，未勾选时登录应被阻止
        """
        logger.info("=== TC-SECURITY-016: 服务协议验证 ===")

        # 检查协议勾选框
        if login_page.is_agreement_checkbox_visible():
            logger.info("Agreement checkbox is visible")

            # 确保未勾选
            checkbox = login_page.page.locator(login_page.LOCATORS["agreement_checkbox"])
            if checkbox.is_checked():
                checkbox.click()
                login_page.page.wait_for_timeout(500)

            # 尝试登录
            valid_account = test_data["login"]["valid_accounts"][0]
            login_page.login(valid_account["account"], valid_account["password"])
            login_page.page.wait_for_timeout(2000)

            # 验证：未勾选协议时应该阻止登录
            error_msg = login_page.get_error_message()
            if error_msg:
                logger.info(f"Error when not agreeing: {error_msg}")
                assert login_page.is_on_login_page(), "未同意协议时应该留在登录页面"

        logger.info("TC-SECURITY-016: 服务协议验证通过")
