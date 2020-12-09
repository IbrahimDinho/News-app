from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.urls import reverse
from django.core import management
from django.test.utils import override_settings
import time
from headLine.models import *

class TestingArticleComment(StaticLiveServerTestCase):
    #Set up Testing
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

    #Test by commenting then deleting that same comment.
    @override_settings(DEBUG=True)
    def testingArticleComment(self):
        #Login
        self.chrome.get(self.live_server_url+"/login/")
        self.chrome.find_element_by_name("username").send_keys("testusername")
        self.chrome.find_element_by_name("password").send_keys("testpassword")
        login_button = self.chrome.find_element_by_id("login-button")
        time.sleep(2)
        login_button.click()

        #Write and submit comment
        time.sleep(5)
        article_link = self.chrome.find_element_by_id('article_title')
        assert article_link is not None
        article_link.click()
        time.sleep(5)
        input = self.chrome.find_element_by_css_selector(".form-control")
        input.send_keys("High-five! Very nice!")

        time.sleep(1)
        submit = "#comments-container .send"
        submit = self.chrome.find_element_by_link_text('Submit!')
        submit.click()
        time.sleep(5)
        
        #Delete comment
        self.chrome.find_element_by_css_selector(".btn.btn-danger.comment-delete-btn.app-btn").click()
        time.sleep(5)
        assert True

    #Load data into Test database
    def _database_data(self):
        user = User.objects.create(
            id=1, 
            username='testusername', 
            password=make_password("testpassword"),
            first_name='Mia', 
            last_name='Khalifa'
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