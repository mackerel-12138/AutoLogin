from util import *  # 导入其他必要的模块

username = os.getenv("fnclub_username") # 登录账号
password = os.getenv("fnclub_password") # 登录密码

@retry(stop_max_attempt_number=3)
def check_in_fnclub():
    try:
        driver = get_web_driver()
        wait = WebDriverWait(driver, 10)

        url = os.getenv("fnclub_url")
        driver.get(f"https://{url}")
        time.sleep(5)
        load_cookies(driver, url, "fnclub_cookies.pkl")
        driver.get(f"https://{url}")
        time.sleep(5)

        #print(driver.page_source)
        #wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "portal_block_summary")))
        signin_button = driver.find_elements(By.CSS_SELECTOR, ".btn.signin-btn")
        signin_a = signin_button[0].find_element(By.TAG_NAME, "a")
        if signin_a:
            print("去签到")
            signin_link = signin_a.get_attribute("href")
            driver.get(signin_link)
            
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bm_c")))
            checkin_button = driver.find_elements(By.CLASS_NAME, "btna")
            if "今日已打卡" in checkin_button[0].text:
                print('今日已签到')
                QLAPI.notify('定时签到-飞牛', '今日已签到')
            else:
                print("去打卡")
                actions = ActionChains(driver)
                actions.move_to_element(checkin_button[0]).click().perform()
                time.sleep(5)

                login_elements = driver.find_elements(By.NAME, "login")
                checkin_button = driver.find_elements(By.CLASS_NAME, "btna")
                if checkin_button and "今日已打卡" in checkin_button[0].text:
                    print('签到成功')
                    QLAPI.notify('定时签到-飞牛', '签到成功')
                elif login_elements:
                    # 查找用户名和密码输入框
                    wait.until(EC.visibility_of_element_located((By.NAME, "login")))
                    # login_elements = driver.find_elements(By.NAME, "login")

                    username_input_elements = login_elements[0].find_elements(By.NAME, "username")
                    password_input_elements = login_elements[0].find_elements(By.NAME, "password")
                    if username_input_elements and password_input_elements:
                        print("当前未登录")
                        username_input = username_input_elements[0]
                        password_input = password_input_elements[0]

                        # 输入用户名和密码
                        #username_input.clear()
                        username_input.send_keys(username)
                        #password_input.clear()
                        password_input.send_keys(password)
                        # 勾选自动登录
                        checkbox = wait.until(EC.element_to_be_clickable(login_elements[0].find_element(By.NAME, "cookietime")))
                        if not checkbox.is_selected():
                            #checkbox.click()
                            actions = ActionChains(driver)
                            actions.move_to_element(checkbox).click().perform()

                        # 查找并点击提交按钮
                        submit_button = driver.find_element(By.NAME, "loginsubmit")
                        #print(submit_button.get_attribute('outerHTML'))
                        actions = ActionChains(driver)
                        actions.move_to_element(submit_button).click().perform()
                        print("已提交登录信息")
                        time.sleep(5)

                        checkin_button = driver.find_elements(By.CLASS_NAME, "btna")
                        actions = ActionChains(driver)
                        actions.move_to_element(checkin_button[0]).click().perform()
                        time.sleep(5)
                        checkin_button = driver.find_elements(By.CLASS_NAME, "btna")
                        if checkin_button and "今日已打卡" in checkin_button[0].text:
                            print('签到成功')
                            QLAPI.notify('定时签到-飞牛', '签到成功')
                        elif "您今天已经打过卡了，请勿重复操作" in driver.page_source:
                            print('今日已签到')
                            QLAPI.notify('定时签到-飞牛', '今日已签到')
                else:
                    print("登录失败，未知页面")
                    QLAPI.notify('定时签到-飞牛', '签到失败')
                    sys.exit(0)
        else:
            QLAPI.notify('定时签到-飞牛', '未知页面')
            sys.exit(0)

        with open("fnclub_cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)
            print("保存cookie")
    except:
        QLAPI.notify('定时签到-飞牛', '签到失败')
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    check_in_fnclub()
