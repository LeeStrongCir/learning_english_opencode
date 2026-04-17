"""
阿里云登录页面对象 (Alibaba Cloud Login Page Object)

封装登录页面的所有操作和元素定位器。
使用 Playwright 进行页面交互。
"""

import logging
import time
from typing import Optional
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class LoginPage:
    """阿里云登录页面对象"""

    # URL
    LOGIN_URL = "https://account.aliyun.com/login/login.htm"

    # 元素定位器 (基于实际页面结构更新)
    LOCATORS = {
        # 账号密码登录模式
        "account_input": "input[placeholder='请输入']",  # 账号名输入框
        "password_input": "input[type='password']",  # 密码输入框
        "login_button": "button:has-text('立即登录')",  # 登录按钮
        "remember_checkbox": "input[type='checkbox']",
        "forgot_password_link": "text=忘记登录名",

        # 错误提示
        "error_message": ".error-msg, .login-error, [class*='error'], .tips-error",
        "error_container": "#login-error, .error-container",

        # 登录方式切换 (基于实际页面标签)
        "password_login_tab": "text=账密登录",
        "sms_login_tab": "text=手机号登录",
        "passkey_login_tab": "text=通行密钥",
        "register_link_top": "text=前往注册",

        # 短信登录
        "phone_input_sms": "input[placeholder='请输入手机号']",
        "sms_code_input": "input[placeholder='请输入验证码']",
        "send_sms_button": "text=获取验证码",
        "sms_login_button": "button:has-text('登录')",

        # 扫码登录
        "qr_code_image": "img[src*='qr']",
        "qr_code_container": "#alibaba-login-box, .qr-code-container",

        # 注册链接
        "register_link": "a[href*='register']",

        # 第三方登录
        "alipay_login": "text=支付宝",
        "taobao_login": "text=淘宝",
        "dingtalk_login": "text=钉钉",
        "wechat_login": "text=微信",

        # 协议勾选
        "agreement_checkbox": "#login-agreement-checkbox, .agreement-checkbox, input[type='checkbox']",
        "service_agreement": "text=服务条款",
        "privacy_policy": "text=隐私政策",

        # 成功跳转后的元素
        "console_url": "https://home.console.aliyun.com",
        "user_menu": ".user-menu, .account-info, .nav-user",
    }

    def __init__(self, page: Page, base_url: str = None):
        """
        初始化登录页面对象

        Args:
            page: Playwright Page 实例
            base_url: 登录页面 URL，默认使用类常量
        """
        self.page = page
        self.base_url = base_url or self.LOGIN_URL
        logger.info(f"LoginPage initialized with URL: {self.base_url}")

    def navigate(self) -> None:
        """导航到登录页面"""
        logger.info(f"Navigating to login page: {self.base_url}")
        self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=30000)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        logger.info("Login page loaded successfully")

    def enter_account(self, account: str) -> None:
        """
        输入账号

        Args:
            account: 账号（手机号/邮箱/会员名）
        """
        logger.info(f"Entering account: {account[:3]}***")
        account_input = self.page.locator(self.LOCATORS["account_input"])
        account_input.wait_for(state="visible", timeout=10000)
        account_input.click()
        account_input.fill(account)
        logger.info("Account entered successfully")

    def enter_password(self, password: str) -> None:
        """
        输入密码

        Args:
            password: 密码
        """
        logger.info("Entering password")
        password_input = self.page.locator(self.LOCATORS["password_input"])
        password_input.wait_for(state="visible", timeout=10000)
        password_input.click()
        password_input.fill(password)
        logger.info("Password entered successfully")

    def click_login(self) -> None:
        """点击登录按钮"""
        logger.info("Clicking login button")
        login_button = self.page.locator(self.LOCATORS["login_button"])
        login_button.wait_for(state="visible", timeout=10000)
        login_button.click()
        # 等待登录请求完成
        self.page.wait_for_timeout(2000)
        logger.info("Login button clicked")

    def login(self, account: str, password: str) -> None:
        """
        执行完整登录流程

        Args:
            account: 账号
            password: 密码
        """
        self.enter_account(account)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> Optional[str]:
        """
        获取错误提示信息

        Returns:
            错误提示文本，如果没有错误则返回 None
        """
        try:
            error_element = self.page.locator(self.LOCATORS["error_message"])
            if error_element.is_visible(timeout=3000):
                error_text = error_element.text_content()
                logger.info(f"Error message found: {error_text}")
                return error_text.strip()
        except (PlaywrightTimeoutError, Exception) as e:
            logger.debug(f"No error message found: {e}")
        return None

    def is_login_successful(self) -> bool:
        """
        检查登录是否成功

        Returns:
            True 如果登录成功（页面跳转），否则 False
        """
        try:
            # 检查是否跳转到控制台或其他页面
            current_url = self.page.url
            logger.info(f"Current URL after login: {current_url}")

            # 如果 URL 不再是登录页面，说明登录成功
            if "login" not in current_url and "account.aliyun.com" not in current_url:
                return True

            # 检查是否有用户菜单元素
            user_menu = self.page.locator(self.LOCATORS["user_menu"])
            if user_menu.is_visible(timeout=3000):
                return True

            return False
        except Exception as e:
            logger.debug(f"Login success check failed: {e}")
            return False

    def is_on_login_page(self) -> bool:
        """
        检查是否仍在登录页面

        Returns:
            True 如果仍在登录页面，否则 False
        """
        try:
            current_url = self.page.url
            return "login" in current_url or "account.aliyun.com" in current_url
        except Exception:
            return False

    def switch_to_sms_login(self) -> None:
        """切换到短信登录模式"""
        logger.info("Switching to SMS login mode")
        sms_tab = self.page.locator(self.LOCATORS["sms_login_tab"])
        sms_tab.wait_for(state="visible", timeout=10000)
        sms_tab.click()
        self.page.wait_for_timeout(1500)
        logger.info("Switched to SMS login mode")

    def switch_to_qr_login(self) -> None:
        """切换到扫码登录模式（通过点击左侧二维码区域）"""
        logger.info("Switching to QR code login mode")
        # 扫码登录是默认显示的左侧二维码，点击"手机号登录"后再切回"账密登录"可看到二维码
        # 或者直接点击左侧二维码区域
        try:
            qr_tab = self.page.locator("text=扫码登录")
            if qr_tab.is_visible(timeout=3000):
                qr_tab.click()
            else:
                # 如果找不到扫码登录标签，尝试其他方式
                logger.info("QR login tab not found, trying alternative")
        except Exception as e:
            logger.warning(f"Failed to switch to QR login: {e}")
        self.page.wait_for_timeout(1500)
        logger.info("Switched to QR code login mode")

    def switch_to_password_login(self) -> None:
        """切换到密码登录模式"""
        logger.info("Switching to password login mode")
        password_tab = self.page.locator(self.LOCATORS["password_login_tab"])
        if password_tab.is_visible(timeout=5000):
            password_tab.click()
            self.page.wait_for_timeout(1500)
        logger.info("Switched to password login mode")

    def enter_phone_for_sms(self, phone: str) -> None:
        """
        输入短信登录的手机号

        Args:
            phone: 手机号
        """
        logger.info(f"Entering phone for SMS login: {phone[:3]}***")
        phone_input = self.page.locator(self.LOCATORS["phone_input_sms"])
        phone_input.wait_for(state="visible", timeout=10000)
        phone_input.fill(phone)

    def enter_sms_code(self, code: str) -> None:
        """
        输入短信验证码

        Args:
            code: 验证码
        """
        logger.info("Entering SMS code")
        code_input = self.page.locator(self.LOCATORS["sms_code_input"])
        code_input.wait_for(state="visible", timeout=10000)
        code_input.fill(code)

    def click_send_sms(self) -> None:
        """点击发送验证码按钮"""
        logger.info("Clicking send SMS code button")
        send_button = self.page.locator(self.LOCATORS["send_sms_button"])
        send_button.wait_for(state="visible", timeout=10000)
        send_button.click()

    def is_qr_code_displayed(self) -> bool:
        """
        检查二维码是否显示

        Returns:
            True 如果二维码显示，否则 False
        """
        try:
            qr_container = self.page.locator(self.LOCATORS["qr_code_container"])
            return qr_container.is_visible(timeout=5000)
        except Exception:
            return False

    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.page.title()

    def get_current_url(self) -> str:
        """获取当前 URL"""
        return self.page.url

    def is_agreement_checkbox_visible(self) -> bool:
        """检查协议勾选框是否可见"""
        try:
            checkbox = self.page.locator(self.LOCATORS["agreement_checkbox"])
            return checkbox.is_visible(timeout=3000)
        except Exception:
            return False

    def check_agreement(self) -> None:
        """勾选服务协议"""
        logger.info("Checking agreement checkbox")
        checkbox = self.page.locator(self.LOCATORS["agreement_checkbox"])
        if checkbox.is_visible(timeout=3000):
            if not checkbox.is_checked():
                checkbox.click()
                self.page.wait_for_timeout(500)
        logger.info("Agreement checkbox checked")

    def is_remember_checked(self) -> bool:
        """检查记住账号是否勾选"""
        try:
            checkbox = self.page.locator(self.LOCATORS["remember_checkbox"])
            return checkbox.is_checked()
        except Exception:
            return False

    def toggle_remember(self) -> None:
        """切换记住账号勾选状态"""
        checkbox = self.page.locator(self.LOCATORS["remember_checkbox"])
        checkbox.click()
        self.page.wait_for_timeout(500)

    def click_forgot_password(self) -> None:
        """点击忘记密码链接"""
        logger.info("Clicking forgot password link")
        link = self.page.locator(self.LOCATORS["forgot_password_link"])
        link.wait_for(state="visible", timeout=10000)
        link.click()

    def click_register(self) -> None:
        """点击注册链接"""
        logger.info("Clicking register link")
        link = self.page.locator(self.LOCATORS["register_link"])
        link.wait_for(state="visible", timeout=10000)
        link.click()

    def get_csrf_token(self) -> Optional[str]:
        """
        获取 CSRF Token（如果存在）

        Returns:
            CSRF Token 值，如果不存在则返回 None
        """
        try:
            # 尝试从 hidden input 获取
            csrf_input = self.page.locator("input[name*='csrf'], input[name*='_token']")
            if csrf_input.count() > 0:
                return csrf_input.first.get_attribute("value")

            # 尝试从 meta 标签获取
            csrf_meta = self.page.locator("meta[name*='csrf']")
            if csrf_meta.count() > 0:
                return csrf_meta.first.get_attribute("content")

            # 尝试从 cookie 获取
            cookies = self.page.context.cookies()
            for cookie in cookies:
                if "csrf" in cookie["name"].lower():
                    return cookie["value"]

            return None
        except Exception as e:
            logger.debug(f"Failed to get CSRF token: {e}")
            return None

    def is_password_masked(self) -> bool:
        """
        检查密码输入框是否被遮蔽

        Returns:
            True 如果密码被遮蔽，否则 False
        """
        try:
            password_input = self.page.locator(self.LOCATORS["password_input"])
            input_type = password_input.get_attribute("type")
            return input_type == "password"
        except Exception:
            return False

    def is_https_connection(self) -> bool:
        """
        检查当前连接是否为 HTTPS

        Returns:
            True 如果是 HTTPS 连接，否则 False
        """
        return self.page.url.startswith("https://")

    def get_response_headers(self) -> dict:
        """获取页面响应头"""
        response = self.page.wait_for_response(
            lambda response: response.url == self.base_url,
            timeout=10000
        )
        return response.headers

    def check_security_headers(self) -> dict:
        """
        检查安全响应头

        Returns:
            安全头信息字典
        """
        headers = self.get_response_headers()
        security_headers = {
            "strict_transport_security": headers.get("strict-transport-security", None),
            "x_frame_options": headers.get("x-frame-options", None),
            "x_content_type_options": headers.get("x-content-type-options", None),
            "content_security_policy": headers.get("content-security-policy", None),
        }
        return security_headers
