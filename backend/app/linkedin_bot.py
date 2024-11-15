from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class LinkedInBot:
    def __init__(self, cookie_file):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=self.options)
        self.cookie_file = cookie_file
        
    def load_cookies(self):
        with open(self.cookie_file, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
                
    def login(self):
        self.driver.get('https://www.linkedin.com')
        self.load_cookies()
        self.driver.refresh()
        
    def get_pending_connections(self):
        self.driver.get('https://www.linkedin.com/mynetwork/invitation-manager/')
        time.sleep(3)  # Wait for page load
        
        connections = []
        invitations = self.driver.find_elements(By.CLASS_NAME, 'invitation-card')
        
        for invitation in invitations:
            try:
                name = invitation.find_element(By.CLASS_NAME, 'invitation-card__name').text
                title = invitation.find_element(By.CLASS_NAME, 'invitation-card__occupation').text
                profile_url = invitation.find_element(By.CLASS_NAME, 'invitation-card__link').get_attribute('href')
                
                # Get invitation message if exists
                try:
                    message = invitation.find_element(By.CLASS_NAME, 'invitation-card__message').text
                except:
                    message = ""
                
                connections.append({
                    'name': name,
                    'title': title,
                    'profile_url': profile_url,
                    'message': message
                })
            except Exception as e:
                print(f"Error processing invitation: {e}")
                
        return connections
    
    def accept_connection(self, profile_url):
        self.driver.get(profile_url)
        accept_button = self.driver.find_element(By.CLASS_NAME, 'invitation-card__action-btn--accept')
        accept_button.click()
        
    def send_message(self, profile_url, message):
        self.driver.get(profile_url)
        message_button = self.driver.find_element(By.CLASS_NAME, 'message-anywhere-button')
        message_button.click()
        
        message_input = self.driver.find_element(By.CLASS_NAME, 'msg-form__contenteditable')
        message_input.send_keys(message)
        
        send_button = self.driver.find_element(By.CLASS_NAME, 'msg-form__send-button')
        send_button.click() 