import os, time, random, spintax, requests, config, videos
import datetime
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# login bot===================================================================================================
def youtube_login(email, password):
    op = webdriver.ChromeOptions()
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--disable-gpu')
    op.add_argument("--window-size=1920,1080")
    op.add_argument("disable-infobars")
    op.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=op, executable_path='chromedriver.exe')
    driver.execute_script("document.body.style.zoom='80%'")
    driver.get('https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620')

    print("=============================================================================================================")
    print("Google Login")

    # finding email field and putting our email on it
    email_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
    email_field.send_keys(email)
    driver.find_element_by_id("identifierNext").click()
    print("email - done")
    time.sleep(5)

    # finding pass field and putting our pass on it
    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5)
    print("password - done")
    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    print("Successfully login")
    print("============================================================================================================")

    return driver

# ==============================================================================================================
def seconds_to_hours(sec):
    h = ((sec // 3600)) % 24
    m = (sec // 60) % 60
    s = sec % 60
    return str(h) + ':' + str(m) + ':' + str(s)
# comment bot===================================================================================================
def comment_page(driver, urls, times, comment):
    if len(urls) == 0:
        print("Done!")
        return False

    url = urls.pop()
    time_ = times.pop()

    driver.get(url)
    print(url)
    driver.implicitly_wait(1)
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, 600);")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")))
    driver.find_element_by_css_selector("ytd-comments ytd-comment-simplebox-renderer div#placeholder-area").click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(comment+f'\nНачало просмотра: {time.strftime("%H:%M", time.localtime())}')
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(Keys.CONTROL, Keys.ENTER)

    post = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-comments ytd-comment-simplebox-renderer'))
    )
    post.click()

    # finding comment box and submiting our comment on it
    # comment_box = EC.presence_of_element_located((By.CSS_SELECTOR, '#placeholder-area'))
    # WebDriverWait(driver, 4).until(comment_box)
    # comment_box1 = driver.find_element_by_css_selector('#placeholder-area')
    # ActionChains(driver).move_to_element(comment_box1).click(comment_box1).perform()
    # add_comment_onit = driver.find_element_by_css_selector('#contenteditable-root')
    # add_comment_onit.send_keys(comment)
    # driver.find_element_by_css_selector('#submit-button').click()
    # print("done")

    time.sleep(np.random.randint(2, 5))
    print(f'Waiting time: {seconds_to_hours(time_)}')
    time.sleep(time_)

    driver.get(url)
    print("Video url:" + url)
    driver.implicitly_wait(1)

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    update_comment(driver)
    time.sleep(3)
    return comment_page(driver, urls, times, random_comment())

# ==============================================================================================================
def update_comment(driver):
    driver.implicitly_wait(1)
    editMenu = driver.find_element_by_xpath("//ytd-comment-thread-renderer[@class='style-scope ytd-item-section-renderer'][1]//div[@id='action-menu']//button[@id='button']")
    editMenu.click()
    driver.implicitly_wait(1)
    editButton = driver.find_element_by_css_selector("[role='menuitem'] a")
    editButton.click()
    driver.implicitly_wait(1)
    commentField = driver.find_element_by_css_selector("[id='contenteditable-root']")
    commentField.send_keys(f'\nКонец просмотра: {time.strftime("%H:%M", time.localtime())}')
    driver.implicitly_wait(1)
    submitButton = driver.find_element_by_css_selector("#submit-button a")
    submitButton.click()

# comment section
def random_comment():
    return videos.comments[np.random.randint(0, len(videos.comments))]

# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':
    driver = youtube_login(config.email, config.password)
    # urls = [
    #     'https://www.youtube.com/watch?v=P-SVpUvFN8g',
    #     'https://www.youtube.com/watch?v=P-SVpUvFN8g',
    # ]
    # times = [
    #     30,
    #     30,
    # ]
    # times = times[::-1]

    # comment_page(driver, urls, times, random_comment())
    comment_page(driver, videos.urls[::-1], videos.times[::-1], random_comment())
