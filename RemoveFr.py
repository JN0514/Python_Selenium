
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import webdriver

import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException

from selenium.webdriver.support.wait import WebDriverWait
import logging
logging.basicConfig(filename="remove_frnd_log.txt", format="%(asctime)s %(message)s", level=logging.DEBUG)


option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

profile_xpath = "/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div[1]/ul/li/div/a/div[1]/div[2]/div/div/div/div/span/span"
friends_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[3]/div"
menu_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div[1]/div[3]/div/div/div"
popUp_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div"


driver = webdriver.WebDriver(options=option)
driver.maximize_window()
driver.get("https://www.facebook.com/")
logging.debug("Facebook page is loaded")
actions = ActionChains(driver)
#Login To The Account
def login(id,password):
  emailID = driver.find_element(By.ID, "email")
  emailID.send_keys(id)

  passcode = driver.find_element(By.ID, "pass")
  passcode.send_keys(password)


  loginBtn = driver.find_element(By.NAME, "login")
  loginBtn.click()
  logging.debug("Logged in to account")
  pass

def finding_total_friends():
  total_friends = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH,
                                                                           "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a"))
  total_friends_text = total_friends.text
  nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
  total = 0
  for i in range(0, len(total_friends_text)):
    if total_friends_text[i] in nums:
      total = total * 10 + int(total_friends_text[i])
    else: break
  return total

def going_to_All_freinds_page():
  try:

    logging.debug("Searching for profile")

    profile = WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH, profile_xpath))
    logging.debug("Founded profile")
    logging.debug("Clicking profile...")
    while not is_element_present(By.XPATH, friends_xpath):
      try:
        profile.click()
      except Exception:
        break


    logging.debug("Searching Friends")
    friendsPage = WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH, friends_xpath))
    logging.debug("Founded friends")
    logging.debug("Clicking Friends...")
    while not is_element_present(By.XPATH, menu_xpath):
      try:
        friendsPage.click()
      except ElementNotInteractableException:
        break
    time.sleep(10)
  except Exception as e:
    logging.debug(e.__class__, "has occured")
    pass
  pass



def is_element_present(type, xpath):
  try:
    return _element_if_visible(driver.find_element(type,xpath))
  except (StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException):
    return False

def _element_if_visible(element, visibility=True):
  return element if element.is_displayed() == visibility else False

def scroll_and_remove():
  total = finding_total_friends() + 1
  alert_xpath = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div"
  for i in range(1,total):
    m_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div[" + str(i) + "]/div[3]/div/div/div"

    logging.debug("Searching menu")
    menu = WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH, m_xpath))
    logging.debug("Founded menu")
    logging.debug("Clicking Menu...")
    while not is_element_present(By.XPATH, popUp_xpath):
        try:
          menu.click()
          print("poped")
        except (StaleElementReferenceException, ElementNotInteractableException):
          break
    unfriend_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[4]"

    if(is_element_present(By.XPATH, unfriend_xpath)):
      unfriend = driver.find_element(By.XPATH, unfriend_xpath)
    elif(is_element_present(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[3]")):
      unfriend = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[3]")
    elif(is_element_present(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]")):
      unfriend = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]")
    else:
      unfriend = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div")
    while not is_element_present(By.XPATH, alert_xpath):
      try:
        unfriend.click()
      except (ElementNotInteractableException, StaleElementReferenceException):
        break
    alert = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, alert_xpath))
    print("Unfriending...")
    actions.move_to_element(alert)
    actions.send_keys(Keys.TAB * 2)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print("done")
    time.sleep(5)



fbEmailID = "your ID"
passcode = "your Passcode"

login(fbEmailID,passcode)
going_to_All_freinds_page()
scroll_and_remove()
