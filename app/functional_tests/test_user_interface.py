"""Functional tests wtith Selenium"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from off.models import Favorite
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestFunctionalBrowser(StaticLiveServerTestCase):
    """testing a user journey with Selenium"""
    
    fixtures = [
        'fixture_category',
        'fixture_product',
        'fixture_user'
    ]
    
    def setUp(self):
        self.browser = webdriver.Chrome('c:/drivers/chromedriver.exe')
        # self.browser.set_window_position(2000,0)
        self.browser.maximize_window()
    
    def tearDown(self):
        self.browser.close()
        
    def live(self, url, kwargs={}):
        return self.live_server_url + reverse(url, kwargs=kwargs)
        
    def test_user_journey(self):
        
        """ user journey for :
            # displaying home page
            # displaying signup page
            # creating user account
            # searching for "le moelleux"
            # clicking on "Remplacer"
            # clicking on "Enregistrer" on second occurence
            # disconnecting
        """
        
        # displaying home page
        self.browser.get(self.live_server_url)
        
        self.assertEqual(self.browser.current_url, self.live('index'))
            
        # displaying signup page
        signup = self.browser.find_element_by_class_name('signup')
        signup.click()
        self.assertEqual(self.browser.current_url, self.live('signup'))
        
        # # creating user account
        # self.browser.find_element_by_class_name('username').send_keys('Julien')
        # self.browser.find_element_by_class_name('email').send_keys('julien@gmail.com')
        # self.browser.find_element_by_class_name('psw1').send_keys('jemedemandesituvasbien')
        # self.browser.find_element_by_class_name('psw2').send_keys('jemedemandesituvasbien')
        # self.browser.find_element_by_id('form_submit').click()

        # searching for 'Le Moelleux'
        search_zone = self.browser.find_element_by_id('home_search')
        search_zone.send_keys('Le Moelleux')
        search_zone.send_keys(Keys.RETURN)
        
        # clicking on Remplacer
        self.browser.find_element_by_class_name('replacement_btn').click()
        # time.sleep(1)
        
        # # clicking on Enregistrer on second occurence
        # self.browser.find_elements_by_class_name('replacement_btn')[1].click()
        # self.assertEqual(Favorite.objects.count(), 1)


        # disconnecting
        # self.browser.find_element_by_class_name('logout').click()
        # self.assertEqual(self.browser.current_url, self.live('index'))
