"""
阿里云登录功能自动化测试 (Login Function Tests)

测试用例覆盖：
- TC-LOGIN-001 ~ TC-LOGIN-008: 账号密码登录测试
- TC-LOCK-001, TC-LOCK-002: 账号锁定机制测试

使用 pytest + Playwright 框架
"""

import pytest
import logging
import time
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


# ============================================================
# TC-LOGIN-001: 正常登录 - 手机号
# ============================================================

class TestLoginPhone:
    """手机号登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    @pytest.mark.parametrize("account_type", ["phone"])
    def test_login_001_valid_phone_login(self, login_page, test_data, account_type):
        """
        TC-LOGIN-001: 使用有效手机号正常登录

        前置条件：
        - 用户已注册阿里云账号
        - 账号状态正常

        测试步骤：
        1. 打开登录页面
        2. 输入有效手机号
        3. 输入正确密码
        4. 点击登录按钮

        预期结果：
        - 登录成功
        - 跳转到控制台首页
        """
        logger.info("=== TC-LOGIN-001: 有效手机号登录 ===")

        # 获取测试数据
        valid_account = next(
            (acc for acc in test_data["login"]["valid_accounts"] if acc["type"] == account_type),
            None
        )

        if valid_account is None:
            pytest.skip("No valid phone account available in test data")

        # 执行登录
        login_page.login(valid_account["account"], valid_account["password"])

        # 验证：登录成功应跳转到非登录页面
        # 注意：由于需要验证码，此用例标记为 xfail
        # 实际环境中需要处理验证码或使用测试环境
        is_on_login = login_page.is_on_login_page()

        # 如果仍在登录页面，检查是否有验证码提示
        if is_on_login:
            error_msg = login_page.get_error_message()
            if error_msg and ("验证码" in error_msg or "captcha" in error_msg.lower()):
                pytest.xfail("需要验证码验证，跳过此用例")

        # 验证登录成功
        assert not is_on_login, "登录成功后应该离开登录页面"
        logger.info("TC-LOGIN-001: 手机号登录测试通过")


# ============================================================
# TC-LOGIN-002: 正常登录 - 邮箱
# ============================================================

class TestLoginEmail:
    """邮箱登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    @pytest.mark.parametrize("account_type", ["email"])
    def test_login_002_valid_email_login(self, login_page, test_data, account_type):
        """
        TC-LOGIN-002: 使用有效邮箱正常登录

        前置条件：
        - 用户已使用邮箱注册阿里云账号
        - 账号状态正常

        测试步骤：
        1. 打开登录页面
        2. 输入有效邮箱地址
        3. 输入正确密码
        4. 点击登录按钮

        预期结果：
        - 登录成功
        - 跳转到控制台首页
        """
        logger.info("=== TC-LOGIN-002: 有效邮箱登录 ===")

        valid_account = next(
            (acc for acc in test_data["login"]["valid_accounts"] if acc["type"] == account_type),
            None
        )

        if valid_account is None:
            pytest.skip("No valid email account available in test data")

        login_page.login(valid_account["account"], valid_account["password"])

        is_on_login = login_page.is_on_login_page()

        if is_on_login:
            error_msg = login_page.get_error_message()
            if error_msg and ("验证码" in error_msg or "captcha" in error_msg.lower()):
                pytest.xfail("需要验证码验证，跳过此用例")

        assert not is_on_login, "登录成功后应该离开登录页面"
        logger.info("TC-LOGIN-002: 邮箱登录测试通过")


# ============================================================
# TC-LOGIN-003: 正常登录 - 会员名
# ============================================================

class TestLoginUsername:
    """会员名登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    @pytest.mark.parametrize("account_type", ["username"])
    def test_login_003_valid_username_login(self, login_page, test_data, account_type):
        """
        TC-LOGIN-003: 使用有效会员名正常登录

        前置条件：
        - 用户已设置会员名
        - 账号状态正常

        测试步骤：
        1. 打开登录页面
        2. 输入有效会员名
        3. 输入正确密码
        4. 点击登录按钮

        预期结果：
        - 登录成功
        - 跳转到控制台首页
        """
        logger.info("=== TC-LOGIN-003: 有效会员名登录 ===")

        valid_account = next(
            (acc for acc in test_data["login"]["valid_accounts"] if acc["type"] == account_type),
            None
        )

        if valid_account is None:
            pytest.skip("No valid username account available in test data")

        login_page.login(valid_account["account"], valid_account["password"])

        is_on_login = login_page.is_on_login_page()

        if is_on_login:
            error_msg = login_page.get_error_message()
            if error_msg and ("验证码" in error_msg or "captcha" in error_msg.lower()):
                pytest.xfail("需要验证码验证，跳过此用例")

        assert not is_on_login, "登录成功后应该离开登录页面"
        logger.info("TC-LOGIN-003: 会员名登录测试通过")


# ============================================================
# TC-LOGIN-004: 异常登录 - 账号为空
# ============================================================

class TestLoginEmptyAccount:
    """空账号登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    def test_login_004_empty_account(self, login_page, test_data):
        """
        TC-LOGIN-004: 账号为空时尝试登录

        前置条件：
        - 打开登录页面

        测试步骤：
        1. 不输入账号
        2. 输入密码
        3. 点击登录按钮

        预期结果：
        - 登录失败
        - 显示错误提示"请输入账号"
        - 停留在登录页面
        """
        logger.info("=== TC-LOGIN-004: 账号为空登录 ===")

        invalid_account = next(
            (acc for acc in test_data["login"]["invalid_accounts"] if acc["account"] == ""),
            None
        )

        # 执行登录（空账号）
        login_page.login("", invalid_account["password"])

        # 等待错误提示出现
        login_page.page.wait_for_timeout(1000)

        # 验证：仍在登录页面
        assert login_page.is_on_login_page(), "账号为空时应该停留在登录页面"

        # 验证：显示错误提示
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "应该显示错误提示信息"
        logger.info(f"Error message: {error_msg}")

        logger.info("TC-LOGIN-004: 空账号登录测试通过")


# ============================================================
# TC-LOGIN-005: 异常登录 - 密码为空
# ============================================================

class TestLoginEmptyPassword:
    """空密码登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    def test_login_005_empty_password(self, login_page, test_data):
        """
        TC-LOGIN-005: 密码为空时尝试登录

        前置条件：
        - 打开登录页面

        测试步骤：
        1. 输入账号
        2. 不输入密码
        3. 点击登录按钮

        预期结果：
        - 登录失败
        - 显示错误提示"请输入密码"
        - 停留在登录页面
        """
        logger.info("=== TC-LOGIN-005: 密码为空登录 ===")

        invalid_account = next(
            (acc for acc in test_data["login"]["invalid_accounts"] if acc["password"] == ""),
            None
        )

        # 执行登录（空密码）
        login_page.login(invalid_account["account"], "")

        # 等待错误提示出现
        login_page.page.wait_for_timeout(1000)

        # 验证：仍在登录页面
        assert login_page.is_on_login_page(), "密码为空时应该停留在登录页面"

        # 验证：显示错误提示
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "应该显示错误提示信息"
        logger.info(f"Error message: {error_msg}")

        logger.info("TC-LOGIN-005: 空密码登录测试通过")


# ============================================================
# TC-LOGIN-006: 异常登录 - 密码错误
# ============================================================

class TestLoginWrongPassword:
    """错误密码登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    def test_login_006_wrong_password(self, login_page, test_data):
        """
        TC-LOGIN-006: 使用错误密码尝试登录

        前置条件：
        - 账号存在且状态正常

        测试步骤：
        1. 输入有效账号
        2. 输入错误密码
        3. 点击登录按钮

        预期结果：
        - 登录失败
        - 显示错误提示"账号或密码错误"
        - 停留在登录页面
        """
        logger.info("=== TC-LOGIN-006: 错误密码登录 ===")

        invalid_account = next(
            (acc for acc in test_data["login"]["invalid_accounts"]
             if acc["description"] == "Wrong password"),
            None
        )

        # 执行登录（错误密码）
        login_page.login(invalid_account["account"], invalid_account["password"])

        # 等待登录响应
        login_page.page.wait_for_timeout(2000)

        # 验证：仍在登录页面
        assert login_page.is_on_login_page(), "密码错误时应该停留在登录页面"

        # 验证：显示错误提示
        error_msg = login_page.get_error_message()
        # 注意：实际错误提示可能因验证码而不同
        if error_msg and ("验证码" in error_msg or "captcha" in error_msg.lower()):
            pytest.xfail("需要验证码验证，跳过此用例")

        assert error_msg is not None, "密码错误时应该显示错误提示"
        logger.info(f"Error message: {error_msg}")

        logger.info("TC-LOGIN-006: 错误密码登录测试通过")


# ============================================================
# TC-LOGIN-007: 异常登录 - 账号不存在
# ============================================================

class TestLoginNonExistentAccount:
    """不存在账号登录测试"""

    @pytest.mark.p0
    @pytest.mark.login
    def test_login_007_nonexistent_account(self, login_page, test_data):
        """
        TC-LOGIN-007: 使用不存在的账号尝试登录

        前置条件：
        - 账号在系统中不存在

        测试步骤：
        1. 输入不存在的账号
        2. 输入任意密码
        3. 点击登录按钮

        预期结果：
        - 登录失败
        - 显示错误提示"账号不存在"或"账号或密码错误"
        - 停留在登录页面
        """
        logger.info("=== TC-LOGIN-007: 不存在账号登录 ===")

        invalid_account = next(
            (acc for acc in test_data["login"]["invalid_accounts"]
             if acc["description"] == "Non-existent account"),
            None
        )

        # 执行登录（不存在的账号）
        login_page.login(invalid_account["account"], invalid_account["password"])

        # 等待登录响应
        login_page.page.wait_for_timeout(2000)

        # 验证：仍在登录页面
        assert login_page.is_on_login_page(), "账号不存在时应该停留在登录页面"

        # 验证：显示错误提示
        error_msg = login_page.get_error_message()
        # 安全考虑：系统可能统一显示"账号或密码错误"
        assert error_msg is not None, "账号不存在时应该显示错误提示"
        logger.info(f"Error message: {error_msg}")

        logger.info("TC-LOGIN-007: 不存在账号登录测试通过")


# ============================================================
# TC-LOGIN-008: 登录页面元素验证
# ============================================================

class TestLoginPageElements:
    """登录页面元素验证测试"""

    @pytest.mark.p0
    @pytest.mark.login
    def test_login_008_page_elements(self, login_page):
        """
        TC-LOGIN-008: 验证登录页面基本元素

        前置条件：
        - 打开登录页面

        测试步骤：
        1. 检查页面标题
        2. 检查账号输入框
        3. 检查密码输入框
        4. 检查登录按钮
        5. 检查忘记密码链接
        6. 检查注册链接

        预期结果：
        - 所有元素都可见且可用
        """
        logger.info("=== TC-LOGIN-008: 登录页面元素验证 ===")

        page = login_page.page

        # 验证页面标题
        title = login_page.get_page_title()
        assert title is not None and len(title) > 0, "页面标题不应为空"
        logger.info(f"Page title: {title}")

        # 验证账号输入框
        account_input = page.locator("#fm-login-id")
        assert account_input.is_visible(), "账号输入框应该可见"
        assert account_input.is_enabled(), "账号输入框应该可用"

        # 验证密码输入框
        password_input = page.locator("#fm-login-password")
        assert password_input.is_visible(), "密码输入框应该可见"
        assert password_input.is_enabled(), "密码输入框应该可用"

        # 验证密码输入框类型为 password（遮蔽）
        input_type = password_input.get_attribute("type")
        assert input_type == "password", "密码输入框类型应该是 password"

        # 验证登录按钮
        login_button = page.locator("#fm-login-submit")
        assert login_button.is_visible(), "登录按钮应该可见"
        assert login_button.is_enabled(), "登录按钮应该可用"

        logger.info("TC-LOGIN-008: 登录页面元素验证通过")


# ============================================================
# TC-LOCK-001: 账号锁定 - 多次失败登录
# ============================================================

class TestAccountLockout:
    """账号锁定机制测试"""

    @pytest.mark.p0
    @pytest.mark.lockout
    @pytest.mark.skip(reason="需要真实账号且可能触发安全限制，使用 Mock 环境测试")
    def test_lock_001_account_lockout_after_max_attempts(self, login_page, test_data):
        """
        TC-LOCK-001: 连续多次登录失败后账号被锁定

        前置条件：
        - 账号存在且状态正常
        - 知道正确的密码

        测试步骤：
        1. 使用错误密码连续登录 max_attempts 次
        2. 第 max_attempts+1 次尝试登录

        预期结果：
        - 前 max_attempts 次显示密码错误
        - 第 max_attempts+1 次显示账号已锁定
        """
        logger.info("=== TC-LOCK-001: 账号锁定测试 ===")

        max_attempts = test_data["lockout"]["max_attempts"]
        valid_account = test_data["login"]["valid_accounts"][0]
        wrong_password = "WrongPassword123!"

        # 连续使用错误密码登录
        for attempt in range(max_attempts):
            logger.info(f"Failed login attempt {attempt + 1}/{max_attempts}")
            login_page.login(valid_account["account"], wrong_password)
            login_page.page.wait_for_timeout(1000)

            error_msg = login_page.get_error_message()
            if error_msg and ("锁定" in error_msg or "lock" in error_msg.lower()):
                logger.info(f"Account locked after {attempt + 1} attempts")
                break

            # 如果触发验证码，跳过
            if error_msg and ("验证码" in error_msg or "captcha" in error_msg.lower()):
                pytest.xfail("触发验证码，无法继续测试锁定机制")

        # 验证账号被锁定
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "应该显示错误提示"
        assert "锁定" in error_msg or "lock" in error_msg.lower(), "账号应该被锁定"

        logger.info("TC-LOCK-001: 账号锁定测试通过")

    @pytest.mark.p0
    @pytest.mark.lockout
    @pytest.mark.skip(reason="需要等待锁定时间，使用 Mock 环境测试")
    def test_lock_002_account_unlock_after_timeout(self, login_page, test_data):
        """
        TC-LOCK-002: 账号锁定一段时间后自动解锁

        前置条件：
        - 账号已被锁定

        测试步骤：
        1. 等待锁定时间过期
        2. 使用正确密码尝试登录

        预期结果：
        - 登录成功
        """
        logger.info("=== TC-LOCK-002: 账号解锁测试 ===")

        lockout_duration = test_data["lockout"]["lockout_duration_seconds"]
        valid_account = test_data["login"]["valid_accounts"][0]

        # 等待锁定时间
        logger.info(f"Waiting {lockout_duration} seconds for account unlock...")
        time.sleep(lockout_duration)

        # 使用正确密码登录
        login_page.login(valid_account["account"], valid_account["password"])

        # 验证登录成功
        assert not login_page.is_on_login_page(), "解锁后应该能成功登录"

        logger.info("TC-LOCK-002: 账号解锁测试通过")


# ============================================================
# 额外测试：登录方式切换
# ============================================================

class TestLoginModeSwitch:
    """登录方式切换测试"""

    @pytest.mark.p0
    @pytest.mark.login
    def test_switch_to_sms_login(self, login_page):
        """
        TC-LOGIN-009: 切换到短信登录模式

        测试步骤：
        1. 打开登录页面
        2. 点击"短信登录"标签

        预期结果：
        - 切换到短信登录界面
        - 显示手机号输入框
        - 显示验证码输入框
        """
        logger.info("=== TC-LOGIN-009: 切换到短信登录 ===")

        # 切换到短信登录
        login_page.switch_to_sms_login()

        # 验证短信登录元素
        page = login_page.page
        phone_input = page.locator("#mobile")
        assert phone_input.is_visible(), "手机号输入框应该可见"

        sms_code_input = page.locator("#mobilecode")
        assert sms_code_input.is_visible(), "验证码输入框应该可见"

        logger.info("TC-LOGIN-009: 切换到短信登录测试通过")

    @pytest.mark.p0
    @pytest.mark.login
    def test_switch_to_qr_login(self, login_page):
        """
        TC-LOGIN-010: 切换到扫码登录模式

        测试步骤：
        1. 打开登录页面
        2. 点击"扫码登录"标签

        预期结果：
        - 切换到扫码登录界面
        - 显示二维码
        """
        logger.info("=== TC-LOGIN-010: 切换到扫码登录 ===")

        # 切换到扫码登录
        login_page.switch_to_qr_login()

        # 验证二维码显示
        assert login_page.is_qr_code_displayed(), "二维码应该显示"

        logger.info("TC-LOGIN-010: 切换到扫码登录测试通过")

    @pytest.mark.p0
    @pytest.mark.login
    def test_switch_back_to_password_login(self, login_page):
        """
        TC-LOGIN-011: 从其他登录方式切换回密码登录

        测试步骤：
        1. 打开登录页面
        2. 切换到短信登录
        3. 切换回密码登录

        预期结果：
        - 显示账号密码输入框
        """
        logger.info("=== TC-LOGIN-011: 切换回密码登录 ===")

        # 先切换到短信登录
        login_page.switch_to_sms_login()

        # 切换回密码登录
        login_page.switch_to_password_login()

        # 验证密码登录元素
        page = login_page.page
        account_input = page.locator("#fm-login-id")
        assert account_input.is_visible(), "账号输入框应该可见"

        password_input = page.locator("#fm-login-password")
        assert password_input.is_visible(), "密码输入框应该可见"

        logger.info("TC-LOGIN-011: 切换回密码登录测试通过")
