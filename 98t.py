from util import *  # 导入其他必要的模块

# 获取当前日期
today = datetime.now().strftime('%Y-%m-%d')

# 定义回帖记录文件路径
reply_record_file = '98t_record.txt'

# 判断是否已经回帖
def has_replied_today():
    if os.path.exists(reply_record_file):
        with open(reply_record_file, 'r') as file:
            last_reply_date = file.read().strip()
            return last_reply_date == today
    return False

# 记录回帖日期
def record_reply_date():
    with open(reply_record_file, 'w') as file:
        file.write(today)

username = os.getenv("sehua_username") # 登录账号
password = os.getenv("sehua_password") # 登录密码

@retry(stop_max_attempt_number=3)
def check_in_98t():
    try:
        driver = get_web_driver()
        wait = WebDriverWait(driver, 10)

        url = os.getenv("sehua_url")
        driver.get(f"https://{url}")
        time.sleep(5)
        load_cookies(driver, url, "98t_cookies.pkl")
        driver.get(f"https://{url}")
        time.sleep(5)

        # 检查是否第一次打开页面
        enter_button = driver.find_elements(By.CLASS_NAME, "enter-btn")
        if enter_button and enter_button[0].get_attribute("href"):
            #enter_button[0].click()
            actions = ActionChains(driver)
            actions.move_to_element(enter_button[0]).click().perform()
            print("已满18岁，进入主页")
        else:
            print("已进入主页")

        # 查找用户名和密码输入框
        username_input_elements = driver.find_elements(By.ID, "ls_username")
        password_input_elements = driver.find_elements(By.ID, "ls_password")
        if username_input_elements and password_input_elements:
            username_input = username_input_elements[0]
            password_input = password_input_elements[0]

            # 输入用户名和密码
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            # 勾选自动登录
            checkbox = wait.until(EC.element_to_be_clickable((By.ID, "ls_cookietime")))
            if not checkbox.is_selected():
                #checkbox.click()
                actions = ActionChains(driver)
                actions.move_to_element(checkbox).click().perform()

            # 查找并点击提交按钮
            submit_button = driver.find_element(By.XPATH, '//button[contains(., "登录") and @type="submit"]')
            #submit_button.click()
            actions = ActionChains(driver)
            actions.move_to_element(submit_button).click().perform()

            print("已提交登录信息")
        elif driver.find_elements(By.ID, "myitem"):
            print("当前已登录")
        else:
            print("登录失败，未知页面")

        wait.until(EC.visibility_of_element_located((By.ID, "myitem")))
        usertitle = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@title="访问我的空间"]')))
        print("当前登录用户名: "+usertitle.text)
        with open("98t_cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)
            print("保存cookie")

        # 判断今天是否已经回帖
        if not has_replied_today():
            # 随机选择一个热门回帖
            hot_elements = driver.find_elements(By.CSS_SELECTOR, "ul.slideshow li")
            random_hot = random.choice(hot_elements)
            random_hot_link_element = random_hot.find_element(By.TAG_NAME, "a")
            random_hot_link = random_hot_link_element.get_attribute("href")
            driver.get(random_hot_link)

            wait.until(EC.visibility_of_element_located((By.ID, "fastpostmessage")))
            wait.until(EC.visibility_of_element_located((By.ID, "fastpostsubmit")))
            print(f"随机贴子: {random_hot_link}")

            # 随机内容回复
            replay_input = driver.find_element(By.ID, "fastpostmessage")
            random_replay = random.choice(os.getenv("sehua_reply").split(","))
            replay_input.send_keys(random_replay)

            replay_button = driver.find_element(By.ID, "fastpostsubmit")
            #replay_button.click()
            actions = ActionChains(driver)
            actions.move_to_element(replay_button).click().perform()
            time.sleep(10)

            print(f"随机回复: {random_replay}")

            # 记录今天已回帖
            record_reply_date()
            print("回帖记录已更新")
        else:
            print("今天已经回过贴了，跳过回帖步骤")

        time.sleep(10)

        # 签到
        signin_a = driver.find_element(By.XPATH, '//a[contains(., "签到")]')
        #signin_a.click()
        actions = ActionChains(driver)
        actions.move_to_element(signin_a).click().perform()
        # 检查存在签到统计信息
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ddpc_sign_continuity")))
        print("进入签到页面")

        signin_button = driver.find_elements(By.CLASS_NAME, "ddpc_sign_btn_red")
        if signin_button:
            #print(signin_button.get_attribute('outerHTML'))
            #signin_button.click()
            actions = ActionChains(driver)
            actions.move_to_element(signin_button[0]).click().perform()
            
            wait.until(EC.visibility_of_element_located((By.NAME, "signsubmit")))
            question_td = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[input[@name='secanswer']]")))

            # 获取验证问答的文本，例如 '71 + 7 = ?'
            question_text = question_td.text
            match = re.search(r'(\d+\s*[+\-*/]\s*\d+)\s*=', question_text)
            if match:
                arithmetic_question = match.group(1)
                print(f"签到问题为: {arithmetic_question}")

                # 计算结果
                answer = eval(arithmetic_question)
                print(f"签到答案为: {answer}")

                # 输入答案
                answer_input = driver.find_element(By.NAME, "secanswer")
                answer_input.send_keys(str(answer))

                # 模拟按下 TAB 键，移动焦点到下一个元素
                answer_input.send_keys(Keys.TAB)

                wait.until(EC.visibility_of_element_located((By.XPATH, '//img[@src="static/image/common/check_right.gif"]')))
                print("答案校验成功")

                # 提交
                answer_button = driver.find_element(By.NAME, "signsubmit")
                #print(answer_button.get_attribute('outerHTML'))

                #answer_button.click()
                actions = ActionChains(driver)
                actions.move_to_element(answer_button).click().perform()
                time.sleep(10)
                
                driver.refresh()
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ddpc_sign_btn_grey')))
                print('98t签到成功')
                QLAPI.notify('定时签到-98t', '98t签到成功')
            else:
                print("未找到验证问答问题")
        else:
            print('当日已签到')
            QLAPI.notify('定时签到-98t', '98t当日已签到')

    except:
        QLAPI.notify('定时签到-98t', '98t签到失败')
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    check_in_98t()
