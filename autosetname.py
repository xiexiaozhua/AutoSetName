import os
import json
import random
import string
import threading
import time

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException


def find_edge_executable():
    edge_paths = [
        os.path.join(os.getenv('LOCALAPPDATA'), r'Microsoft\Edge\Application\msedge.exe'),
        os.path.join(os.getenv('PROGRAMFILES(X86)'), r'Microsoft\Edge\Application\msedge.exe'),
        os.path.join(os.getenv('PROGRAMFILES'), r'Microsoft\Edge\Application\msedge.exe')
    ]

    for path in edge_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("Microsoft Edge not found at default locations.")


def load_settings():
    settings_file = 'Settings.json'
    settings = {}

    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        print(f"Settings file {settings_file} not found.")

    return settings


def get_edge_executable_path(settings):
    edge_executable_path = settings.get('edge_executable_path')

    if not edge_executable_path or not os.path.exists(edge_executable_path):
        print("Edge executable path not set correctly or does not exist. Searching default locations...")
        edge_executable_path = find_edge_executable()

    return edge_executable_path


def click_close_button_if_exists(driver, max_attempts=20, wait_time=30):
    attempts = 0
    while attempts < max_attempts:
        try:
            # 等待元素变得可点击
            close_button = WebDriverWait(driver, wait_time).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.MC_modal_close'))
            )
            close_button.click()
            print("Close button clicked.")
            break  # 成功点击后退出循环
        except (TimeoutException, NoSuchElementException):
            print("Close button not found or not clickable. Attempting again...")
            attempts += 1
            if attempts >= max_attempts:
                print("Max attempts reached. Could not click the close button.")
                break
def click_login_button_if_exists(driver, wait_time=10):
    try:
        # 等待元素变得可点击，这里使用 data-testid 属性来定位元素
        login_button = WebDriverWait(driver, wait_time).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="MSALoginButtonLink"]'))
        )
        login_button.click()
        print("Login button clicked.")


    except (TimeoutException, NoSuchElementException) as e:
        print("Login button not found or not clickable within the given time:", str(e))


def handle_another_account_prompt(driver, wait_time=10):
    try:
        # 等待元素变得可点击，这里使用 data-testid 属性来定位元素
        another_account_element = WebDriverWait(driver, wait_time).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="mainText"]:contains("使用另一个帐户")'))
        )
        another_account_element.click()
        print("Clicked '使用另一个帐户'.")
    except (TimeoutException, NoSuchElementException):
        print("'使用另一个帐户' element not found or not clickable. Skipping...")


def input_email_and_click_next(driver, email):
    try:
        # 等待元素变得可交互
        email_input = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[name="loginfmt"]'))
        )
        email_input.clear()  # 清空输入框以防有预填充的文本
        email_input.send_keys(email)  # 输入电子邮件地址
        print("Email entered.")

        # 点击“下一个”按钮
        next_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'idSIButton9'))
        )
        next_button.click()
        print("Clicked 'Next' button.")

    except (TimeoutException, NoSuchElementException) as e:
        print("Failed to enter email or click the next button:", str(e))


def input_password_and_click_login(driver, password):
    try:
        # 等待密码输入框变得可交互
        password_input = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[name="passwd"]'))
        )
        password_input.clear()  # 清空输入框以防有预填充的文本
        password_input.send_keys(password)  # 输入密码
        print("Password entered.")

        # 点击“登录”按钮
        login_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'idSIButton9'))
        )
        login_button.click()
        print("Clicked 'Login' button.")

    except (TimeoutException, NoSuchElementException) as e:
        print("Failed to enter password or click the login button:", str(e))


def set_profile_name(driver, wait_time=5,prefix=None):
    random_name = generate_random_string(12, prefix)
    try:
        # 生成随机名称
        print(f"Generated random name: {random_name}")

        # 定位并填写 <input> 元素
        input_element = WebDriverWait(driver, wait_time).until(
            ec.presence_of_element_located((By.ID, 'change-java-profile-name'))
        )
        input_element.clear()  # 清空输入框
        input_element.send_keys(random_name)

        # 使用更具体的 CSS 选择器来定位 <button> 元素
        button_css_selector = 'button.MC_Button.MC_Button_Hero.MC_Style_Green_5.redeem__text-transform[aria-label="设置您的档案名称"]'

        # 确保按钮是可点击的并点击它
        button_element = WebDriverWait(driver, wait_time).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector))
        )
        button_element.click()

        print(f"Successed to set username: {random_name}")

        # 等待3秒
        time.sleep(0.5)

    except (TimeoutException, NoSuchElementException):
        print("Failed to locate or interact with the specified elements.")
    except InvalidSessionIdException:
        print("WebDriver session is invalid during the operation.")
def monitor_close_button(driver, wait_time=5, timeout=5, click_count=3):
    def check_and_click_close_button():
        start_time = time.time()
        clicked = 0  # 记录点击次数

        while clicked < click_count and time.time() - start_time < timeout:
            try:
                # 检查 WebDriver 会话是否仍然有效
                if driver is None or not hasattr(driver, 'session_id'):
                    print("WebDriver session is invalid.")
                    break

                # 尝试定位并点击关闭按钮
                close_button = WebDriverWait(driver, 2).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.MC_modal_close[aria-label="关闭 Aria"]'))
                )
                close_button.click()
                print(f"Close button clicked. Attempt {clicked + 1}")
                clicked += 1  # 成功点击后增加计数

                if clicked < click_count:
                    print(f"Waiting for the close button to appear again. Attempt {clicked + 1}...")
                    time.sleep(0.1)  # 等待一段时间让页面响应点击事件

            except (TimeoutException, NoSuchElementException):
                # 如果找不到关闭按钮，则等待一段时间再重试
                time.sleep(0.1)
            except InvalidSessionIdException:
                print("WebDriver session is invalid during the operation.")
                break

        if clicked == 0:
            print("Close button not detected within the given timeout.")
        else:
            print(f"Completed {clicked} attempts of clicking the close button.")

    # 创建并启动子线程
    thread = threading.Thread(target=check_and_click_close_button)
    thread.start()
    return thread


def generate_random_string(length=12, prefix=None):
    """Generate a random string of fixed length with an optional prefix."""
    letters_and_digits = string.ascii_letters + string.digits

    # If a prefix is provided, include it in the final string.
    if prefix:
        prefix_length = len(prefix)
        # Ensure that the final string will have the desired length.
        if prefix_length > length:
            raise ValueError("Prefix length cannot be longer than the total length of the string.")
        random_part_length = length - prefix_length
        return prefix + ''.join(random.choice(letters_and_digits) for i in range(random_part_length))
    else:
        # If no prefix is provided, generate a string of the full requested length.
        return ''.join(random.choice(letters_and_digits) for i in range(length))
def skip_security_check_if_needed(driver: object, wait_time: object = 5) -> object:
    while True:
        try:
            # 尝试定位并点击“暂时跳过”链接
            skip_link = WebDriverWait(driver, wait_time).until(
                ec.element_to_be_clickable((By.ID, 'iShowSkip'))
            )
            skip_link.click()
            print("Clicked '暂时跳过' link.")

            # 给页面一点时间响应点击事件
            time.sleep(0.5)  # 可根据实际情况调整等待时间

        except (TimeoutException, NoSuchElementException):
            print("'暂时跳过' link not found or not clickable. Skipping security check completed.")
            break  # 如果找不到元素或超时，退出循环

    try:
        # 等待页面加载完成，并检查是否有“保持登录状态?”提示
        keep_me_signed_in_title = WebDriverWait(driver, wait_time).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="heading"][aria-level="1"][id="kmsiTitle"]'))
        )

        if keep_me_signed_in_title.text == "保持登录状态?":
            print("Detected '保持登录状态?' prompt.")

            # 定位并点击“否”按钮
            decline_button = WebDriverWait(driver, wait_time).until(
                ec.element_to_be_clickable((By.ID, 'declineButton'))
            )
            decline_button.click()
            print("Clicked '否' button.")

            # 给页面一点时间响应点击事件
            time.sleep(0.5)  # 可根据实际情况调整等待时间

            # 启动子线程监控关闭按钮，设置点击次数为3次
            close_button_thread = monitor_close_button(driver, timeout=30, click_count=3)

            # 检查线程是否成功启动后再等待其结束
            if close_button_thread is not None:
                close_button_thread.join()

    except (TimeoutException, NoSuchElementException):
        print("'保持登录状态?' prompt not detected or timed out waiting for it.")

def open_edge_with_selenium_inprivate(user_email, user_password,prefix):
    driver = None  # 初始化为空，确保可以在finally块中检查
    try:
        settings = load_settings()
        edge_executable_path = get_edge_executable_path(settings)

        edge_options = Options()
        edge_options.binary_location = edge_executable_path
        edge_options.add_argument('inprivate')

        service = Service()  # 如果msedgedriver不在系统PATH中，请指定其完整路径

        driver = webdriver.Edge(service=service, options=edge_options)

        try:
            driver.get('https://www.minecraft.net/zh-hans/msaprofile/mygames/editprofile')

            # 尝试点击关闭按钮（假设之前已经定义了该函数）
            click_close_button_if_exists(driver)

            # 尝试点击登录按钮
            click_login_button_if_exists(driver)

            # 输入电子邮件并点击“下一个”
            input_email_and_click_next(driver, user_email)

            # 等待页面加载并处理密码输入和点击登录
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'input[name="passwd"]'))
            )
            input_password_and_click_login(driver, user_password)

            # 检查是否需要跳过安全检查，并不断尝试直到成功
            skip_security_check_if_needed(driver)

            # 这里可以添加更多交互逻辑，比如继续登录过程等
            set_profile_name(driver,5,prefix)

            # 等待一段时间以便观察结果（可选）
            time.sleep(5)  # 例如等待30秒

        finally:
            if driver is not None:
                driver.quit()

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

























#儿子，妈妈什么都不要求，你别整天抱着你那手机拍你那脚了，也别闻莫名其妙的药水了，你看你肛门都大到要做手术了，都能塞苹果了，还有啊，别在网络上惹别人了，妈妈上抖音都看到咱们全家大头照满天飞了，你这是又惹谁了，你的锁妈妈帮你洗了洗，放在你床上了，以后飞机杯别乱丢了，也别花钱找人穿白袜，篮球鞋踩你了，有啥事跟妈说，明天要下暴雨就别全国飞到别人床上和别人乱搞了，在家里呆着哦，面条下好了，你看你瘦的脖子都被你金主用项圈勒出印子了，每天在家性瘾发作，你弟弟都要被你搞出精神衰弱了，你小时候很乖的，会帮妈妈洗衣做饭，现在这样子了呢，为什么会变成同性恋？宝贝告诉妈妈，是不是因为在手机上看到不好的东西了？是不是因为手机？是不是？为什么不回答我？你怎么会变成同性恋？妈妈辛辛苦苦把你养的这么大，你为什么要当同性恋？