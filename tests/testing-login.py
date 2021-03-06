from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.core import management
from django.test.utils import override_settings
import time
from headLine.models import *

class TestingLogin(StaticLiveServerTestCase):
    #Set up testing
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chrome = webdriver.Chrome(ChromeDriverManager().install())
        cls.chrome.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.chrome.quit()
        super().tearDownClass()

    def setUp(self):
        management.call_command('flush', verbosity=0, interactive=False)
        self._database_data()

    #Test Login
    @override_settings(DEBUG=True)
    def testing_Login(self):
        self.chrome.get(self.live_server_url+"/login/")
        time.sleep(2)
        self.chrome.find_element_by_name("username").send_keys("testusername")
        self.chrome.find_element_by_name("password").send_keys("testpassword")
        login_button = self.chrome.find_element_by_id("login-button")
        time.sleep(2)
        login_button.click()
        time.sleep(4)
        
    

    #Load test data into test database
    def _database_data(self):
        user = User.objects.create(
            id=1, 
            username='testusername', 
            password=make_password("testpassword")
        )

        category = Category.objects.create(
            id=1, 
            category_name="Category Temp", 
            category_description="Testing Category"
        )
        category.selected_by.add(1)

        article = Article.objects.create(
            id=1, 
            article_title="Article Temp", 
            article_body="Once upon a time there was a Covid Aladeen.", 
            article_summary="COVID FLASHNEWS", 
            category=category
        )
