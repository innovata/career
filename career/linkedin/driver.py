
from .jobs import JobsDriver
from .profile import ProfileDriver
import os
import time
import inspect


class LinkedInDriver:
    """
    ============================================================
    UserID와 패스워드는 사전에 OS 환경변수에 저장해라.
    ============================================================
    """
    def __init__(self, driver):
        self.driver = driver
        self._is_readyto_login()

    def _is_readyto_login(self):
        try:
            self.userid = os.environ['USERID']
            self.pw = os.environ['PW']
        except Exception as e:
            print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n__doc__ :{self.__doc__}")
            self.readyto_login = False
        else:
            self.readyto_login = True
        return self

    def login(self, site='loginpage'):
        if self.readyto_login:
            if hasattr(self,'logined'):
                print(f"{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]} : Already logined. Move to main-page.")
                self.driver.get('https://www.linkedin.com/')
            else:
                print(f"{'='*60}\n{self.__class__} | {inspect.stack()[0][3]}\n driver.current_url 로그인 전 : {self.driver.current_url}")
                if site == 'loginpage':
                    self._login_loginpage()
                else:
                    self._login_homepage()
                print(f" driver.current_url 로그인 후 : {self.driver.current_url}")
                self.logined = True
        return self

    def _login_loginpage(self, sleepsecs=1):
        self.driver.get('https://www.linkedin.com/login/')
        time.sleep(sleepsecs)
        self.driver.find_element_by_id('username').clear()
        self.driver.find_element_by_id('username').send_keys(self.userid)
        time.sleep(sleepsecs)
        self.driver.find_element_by_id('password').clear()
        self.driver.find_element_by_id('password').send_keys(self.pw)
        time.sleep(sleepsecs)
        self.driver.find_element_by_class_name("login__form_action_container").find_element_by_tag_name("button").click()

    def _login_homepage(self, sleepsecs=1):
        self.driver.get('https://www.linkedin.com/')
        time.sleep(sleepsecs)
        login = self.driver.find_element_by_tag_name('form')
        time.sleep(sleepsecs)
        login.find_element_by_id('login-email').send_keys(self.userid)
        time.sleep(sleepsecs)
        login.find_element_by_id('login-password').send_keys(self.pw)
        time.sleep(sleepsecs)
        login.find_element_by_id('login-submit').click()

    def setup_services(self):
        if self.logined:
            self.jobs = JobsDriver(self.driver)
            self.profile = ProfileDriver(self.driver)
