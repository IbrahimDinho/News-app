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
import os

class TestingArticleLike(StaticLiveServerTestCase):
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

    
    @override_settings(DEBUG=True)
    def testing_Login(self):
        self.chrome.get(self.live_server_url+"/headline/register/")
        time.sleep(2)
        
        user_field = self.chrome.find_element_by_name("username")
        user_password = self.chrome.find_element_by_name("password")
        user_email = self.chrome.find_element_by_name("email")
        user_fname = self.chrome.find_element_by_name("first_name")
        user_lname = self.chrome.find_element_by_name("last_name")
        dob_field = self.chrome.find_element_by_name("date_of_birth")
        image_field = self.chrome.find_element_by_name("profile_photo")

    

        user_field.send_keys("test_new_username")
        user_password.send_keys("testpassword")
        user_email.send_keys("ibby@yahoo.com")
        user_fname.send_keys("Bob")
        user_lname.send_keys("Smith")
        dob_field.clear()
        dob_field.send_keys("01012020")
        image_field.send_keys(os.path.abspath("media/uploads/cattest2.jpg"))
        time.sleep(2)
        login_button = self.chrome.find_element_by_id("login-button")
        login_button.click()
        time.sleep(4)

        
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

