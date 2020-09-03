import os, time, random, spintax, requests, config
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

def stop(n):
    time.sleep(randint(2, n))

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
    stop(5)
    print("email - done")

    # finding pass field and putting our pass on it
    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    stop(5)
    print("password - done")
    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    print("Successfully login")
    print("============================================================================================================")

    return driver

# ==============================================================================================================

# comment bot===================================================================================================
def comment_page(driver, urls, times, comment):
    # gettin a video link from the list
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
    driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(comment)
    driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(Keys.CONTROL, Keys.ENTER)

    post = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-comments ytd-comment-simplebox-renderer'))
    )
    post.click()

    r = np.random.randint(2, 5)
    time.sleep(r)
    print(f'Sleep {time_} secs')
    time.sleep(time_)

    driver.get(url)
    print("Video url:" + url)
    driver.implicitly_wait(1)

    # checking if video is unavailable
    if not check_exists_by_xpath(driver, '//*[@id="movie_player"]'):
        print("unavailbale")
        return comment_page(driver, urls, times, random_comment())

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(1)

    # finding comment box and submiting our comment on it
    # comment_box = EC.presence_of_element_located((By.CSS_SELECTOR, '#placeholder-area'))
    # WebDriverWait(driver, 4).until(comment_box)
    # comment_box1 = driver.find_element_by_css_selector('#placeholder-area')
    # ActionChains(driver).move_to_element(comment_box1).click(comment_box1).perform()
    # add_comment_onit = driver.find_element_by_css_selector('#contenteditable-root')
    # add_comment_onit.send_keys(comment)
    # driver.find_element_by_css_selector('#submit-button').click()
    # print("done")

    stop(5)

    update_comment(driver)
    stop(3)
    return comment_page(driver, urls, times, random_comment())

times = [876,832,474,323,548,399,616,437,513,337,470,449,448,159,535,766,660,602,598,901,784,422,850,772,901,517,765,892,562,901,225,335,518,707,861,834,711,712,472,237,563,675,863,865,897,167,222,890,1217,841,901,616,265,901,641,1390,794,791,901,895,901,834,901,901,679,901,804,901,901,891,901,901,901,170,1069,898,1058,1080,1723,1118,765,2141,2617,896,2654,1959]
# ==============================================================================================================
def update_comment(driver):
    editMenu = driver.find_element_by_xpath(
        "//ytd-comment-thread-renderer[@class='style-scope ytd-item-section-renderer'][1]//div[@id='action-menu']//button[@id='button']")
    editMenu.click()
    editButton = driver.find_element_by_css_selector("[role='menuitem'] a")
    editButton.click()
    commentField = driver.find_element_by_css_selector("[id='contenteditable-root']")
    commentField.send_keys('.')
    submitButton = driver.find_element_by_css_selector("#submit-button a")
    submitButton.click()


# comment section
def random_comment():
    # You can edit these lines if you want to add more comments===================================
    comments = [
        '3) Year - Год ( Happy New Year )',
        '4) Way - Дорога/Путь ( Can you show me the way ? )',
        '5) Day - День ( What day today? )',
        '6) Thing - Вещь ( What s that thing on your table ? )',
        '7) Man - Мужчина ( He is a man )',
        '8) World - Мир ( The World Is Mine )',
        '9) Life - Жизнь ( Wonderful life )',
        '10) Hand - Рука ( Give me your hand )',
        '11) Part - Часть ( America is the part of the world )',
        '12) Child - Ребёнок ( This child is only three years old )',
        '13) Eye - Глаз ( Close your eyes )',
        '14) Woman - Женщина ( Who s this woman ? )',
        '15) Place - Место ( Dubai is a wonderful place )',
        '16) Week - Неделя ( How many days are there in a week ? )',
        '17) Case - Дело ( He had to defend his case in court )',
        '18) Point - Смысл/Точка ( What the point in staying at home all day ? )',
        '19) Government - Правительство ( Government are people who run this country )',
        '20) Company - Компания ( I ran my own company )',
        '21) Number - Номер ( Can you give me a phone number ? )',
        '22) Group - Группа ( I m part of the singing group )',
        '23) Problem - Проблема ( What s yout problem ? )',
        '24) Fact - Факт (Baikal is the deepest lake on our planet. I am confident in this fact )',
        '25) Be - Есть не в прямом смысле ( I am student )',
        '26) Have - Иметь ( I have a dream )',
        '27) Do - Делать ( What are you doing tomorrow ? )',
        '28) Say - Сказать ( Can you say that onse again ? )',
        '29) Get - Получить ( Can i get that magazine please? )',
        '30) Make - Делать ( Let s make something amazing together )',
        '31) Go - Идти/Ехать/Лететь/Перемещение ( Let s go to Moscow )',
        '32) Know - Знать ( Do you know how many people live in China ? )',
        '33) Take - Взять ( Let me take that )',
        '34) See - Видеть ( I see you )',
        '35) Come - Приходить ( Come over tomorrow )',
        '36) Think - Думать ( What do you think about going to USA ? )',
        '37) Look - Смотреть ( look at you )',
        '38) Want - Хотеть ( I want this thing more anything in the world )',
        '39) Give - Давать ( I give you Pencil )',
        '40) Use - Использовать ( I use English dictionary )',
        '41) Find - Находить ( i ll find you )',
        '42) Tell - Рассказывать ( Let me tell something )',
        '43) Ask -Спрашивать ( Can ask you something ? )',
        '44) Work - Работать ( I work from home )',
        '45) Seem - Казаться ( My sorry seem to be the hardest word )',
        '46) Feel - Чувствовать ( I feel warm )',
        '47) Try - Пытаться ( Just keep trying )',
        '48) Leave - Оставлять ( I will just leve it here )',
        '49) Call - Звонить ( Can you call me tomorrow ? )',
        '50) Good - Хорошо ( Such a good day )',
        '51) New - Новый ( You bought a new phone ? )',
        '52) First - Первый ( What do you do when you Wake up ? )',
        '53) Last - Последний ( The last of us )',
        '54) Long - Длинный ( How long is this music ? )',
        '55) Great - Великолепно.',
        '56) Little - Маленький/Немного ( Little mouse )',
        '57) Own - своя ( This is my own car )',
        '58) Other - Другой ( It s the other way around )',
        '59) Old - Старый ( How old are you ? )',
        '60) Right,Left - Право,Лево.',
        '61) Big - Большой ( How bigis your home ? )',
        '62) High - Высоко ( How high this building ? )',
        '63) Different - Другой.',
        '64) Small - Маленький ( Small child )',
        '65) Large - Большой ( Large number )',
        '66) Next - Следующий ( What is the next month ? )',
        '67) Early - Рано ( How early do you wake up ? )',
        '68) Young - Молодой ( It is lovely young lady )',
        '69) Important - Важный ( Morning is a important part the day because you start you day )',
        '70) Few - Мало/ Несколько ( I have a few good friends )',
        '71) Public - Общественный/Публичный ( I like public speaking )',
        '72) Bad - Плохо ( Oh my god that s bad )',
        '73) Same - Одно и то же/Так же ( I m not the same person as i used to be a year ago )',
        '73) Able - Способный ( I able to do that )',
        '74) To - к, в ( I go to school )',
        '75) Of - часть чего-то ( Part of the world )',
        '76) In - в',
        '77) For - для',
        '78) On - на',
        '79) With - с',
        '80) At - в ( At 5 o clock )',
        '81) By - к,в/мимо ( I walked by the window )',
        '82) From - из ( From Russia with love )',
        '83) Up - Вверх ( Go up)',
        '84) About - о ( This is story about a superman )',
        '85) Into - в ( i m into you )',
        '86) Over - над ( This is over )',
    ]
    # =============================================================================================
    r = np.random.randint(0, len(comments))

    return comments[r]


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True


# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':
    email = 'i.plyton0@gmail.com'
    password = ''
    urls = [
        'https://www.youtube.com/watch?v=qX9nf86KJ8k',
        'https://www.youtube.com/watch?v=VfLpdsELJfU',
        'https://www.youtube.com/watch?v=0DHpbYBrKPs',
        'https://www.youtube.com/watch?v=K0PuS391dsI',
        'https://www.youtube.com/watch?v=_6qZlmLrMzM',
        'https://www.youtube.com/watch?v=UA3FteJn9oc',
        'https://www.youtube.com/watch?v=66YZEptO2Zo',
        'https://www.youtube.com/watch?v=iSYIjjW--pE',
        'https://www.youtube.com/watch?v=5ZFfT347-j0',
        'https://www.youtube.com/watch?v=vGOvU7de3DM',
        'https://www.youtube.com/watch?v=AFXGZBdzf-s',
        'https://www.youtube.com/watch?v=Fa9TCNpBPBg',
        'https://www.youtube.com/watch?v=F5t4jpezDPI',
        'https://www.youtube.com/watch?v=LmrzXWsV910',
        'https://www.youtube.com/watch?v=plesqDCozKg',
        'https://www.youtube.com/watch?v=BplCjZ0HZLg',
        'https://www.youtube.com/watch?v=YEneLXIAPAs',
        'https://www.youtube.com/watch?v=qLWeE5wiiwY',
        'https://www.youtube.com/watch?v=KD5wYlYHj_U',
        'https://www.youtube.com/watch?v=jCasz8Nitlw',
        'https://www.youtube.com/watch?v=_ke6TdV2Qj0',
        'https://www.youtube.com/watch?v=5sG5lfIjVoc',
        'https://www.youtube.com/watch?v=mleWEDCNh8s',
        'https://www.youtube.com/watch?v=AhipgYwSzcU',
        'https://www.youtube.com/watch?v=joChTd_bwKk',
        'https://www.youtube.com/watch?v=Uvx7NcZ-SWY',
        'https://www.youtube.com/watch?v=uH-SZgFtP3k',
        'https://www.youtube.com/watch?v=DI-GL2v0d1Y',
        'https://www.youtube.com/watch?v=QyeTkWTRrII',
        'https://www.youtube.com/watch?v=iBgdNphFYO8',
        'https://www.youtube.com/watch?v=2fcsPzC_ZuI',
        'https://www.youtube.com/watch?v=URDW6aaO3Ro',
        'https://www.youtube.com/watch?v=EnmwIi18p5Y',
        'https://www.youtube.com/watch?v=pAwVXWqiyA0',
        'https://www.youtube.com/watch?v=u2tEDpjOxdg',
        'https://www.youtube.com/watch?v=ioiS0I2WqRQ',
        'https://www.youtube.com/watch?v=hwlroASv9ws',
        'https://www.youtube.com/watch?v=ezXOQ2cNI74',
        'https://www.youtube.com/watch?v=QLnbJ9Wn68o',
        'https://www.youtube.com/watch?v=953YmmFivvc',
        'https://www.youtube.com/watch?v=auER8X-0OgU',
        'https://www.youtube.com/watch?v=NsmoKA4Fd8w',
        'https://www.youtube.com/watch?v=ieO_uImbSA4',
        'https://www.youtube.com/watch?v=nRIzyJWTv5U',
        'https://www.youtube.com/watch?v=T8IIqc4QG7g',
        'https://www.youtube.com/watch?v=rUz0iSKTLf4',
        'https://www.youtube.com/watch?v=pDp5EBpJrQY',
        'https://www.youtube.com/watch?v=xmDpgnBZJW4',
        'https://www.youtube.com/watch?v=Q1lILNGAKwU',
        'https://www.youtube.com/watch?v=qBjlp4RLeUA',
        'https://www.youtube.com/watch?v=-2XItBbxSto',
        'https://www.youtube.com/watch?v=g9as2CQPy7M',
        'https://www.youtube.com/watch?v=5h0zV_8nNko',
        'https://www.youtube.com/watch?v=zBMxVfcbli4',
        'https://www.youtube.com/watch?v=T9t51XoCR3g',
        'https://www.youtube.com/watch?v=HMJJ35BZK_g',
        'https://www.youtube.com/watch?v=O18mcC_wqwc',
        'https://www.youtube.com/watch?v=bNSqjHLb6MU',
        'https://www.youtube.com/watch?v=Rhvh13v1VzQ',
        'https://www.youtube.com/watch?v=LtUH-Oj2qUo',
        'https://www.youtube.com/watch?v=5ETHy1DkhBk',
        'https://www.youtube.com/watch?v=L0AGrHOtbj4',
        'https://www.youtube.com/watch?v=eL7gDSLDCgU',
        'https://www.youtube.com/watch?v=9mDh42chIhQ',
        'https://www.youtube.com/watch?v=n3r1MUd_D0M',
        'https://www.youtube.com/watch?v=_tUNvawSSRM',
        'https://www.youtube.com/watch?v=H3e4eXuC51s',
        'https://www.youtube.com/watch?v=SjJKGcsbESo',
        'https://www.youtube.com/watch?v=4dZ-GbdtS0U',
        'https://www.youtube.com/watch?v=y_vcOpBdc1c',
        'https://www.youtube.com/watch?v=fsXzduunBOs',
        'https://www.youtube.com/watch?v=y9yajPL82wQ',
        'https://www.youtube.com/watch?v=nz35ofz6Zxo',
        'https://www.youtube.com/watch?v=Jrrf-Uy2n4I',
        'https://www.youtube.com/watch?v=Rds8pdRCI-U',
        'https://www.youtube.com/watch?v=sEzVn2A1lOA',
        'https://www.youtube.com/watch?v=FRU_HZWSSlM',
        'https://www.youtube.com/watch?v=2FjixP1nMVg',
        'https://www.youtube.com/watch?v=bHGhoXzG4EU',
        'https://www.youtube.com/watch?v=dUzvNkQ9qsI',
        'https://www.youtube.com/watch?v=8XR5ZKAZzwE',
        'https://www.youtube.com/watch?v=P60KKsgyWwk',
        'https://www.youtube.com/watch?v=gHTBMTs2FZY',
        'https://www.youtube.com/watch?v=4gwAw3yHBZA',
        'https://www.youtube.com/watch?v=dFOCdTokhzw',
        'https://www.youtube.com/watch?v=oa25s_6Sfn0',

    ]
    times = [
        876,
        832,
        474,
        323,
        548,
        399,
        616,
        437,
        513,
        337,
        470,
        449,
        448,
        159,
        535,
        766,
        660,
        602,
        598,
        901,
        784,
        422,
        850,
        772,
        901,
        517,
        765,
        892,
        562,
        901,
        225,
        335,
        518,
        707,
        861,
        834,
        711,
        712,
        472,
        237,
        563,
        675,
        863,
        865,
        897,
        167,
        222,
        890,
        1217,
        841,
        901,
        616,
        265,
        901,
        641,
        1390,
        794,
        791,
        901,
        895,
        901,
        834,
        901,
        901,
        679,
        901,
        804,
        901,
        901,
        891,
        901,
        901,
        901,
        170,
        1069,
        898,
        1058,
        1080,
        1723,
        1118,
        765,
        2141,
        2617,
        896,
        2654,
        1959,

    ]
    urls = [
        'https://www.youtube.com/watch?v=P-SVpUvFN8g',
        'https://www.youtube.com/watch?v=P-SVpUvFN8g',
    ]
    times = times[::-1]
    times = [
        30,
        30,
    ]
    driver = youtube_login(email, password)

    comment_page(driver, urls, times, random_comment())
