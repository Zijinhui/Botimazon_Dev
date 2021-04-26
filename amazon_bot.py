import time
import sys
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException

def amazon_signin(account, password):
    driver.get("https://www.amazon.com/")
    driver.find_element_by_xpath("//*[@id='nav-link-accountList-nav-line-1']").click()
    # account = input("Enter account: ")
    # password = input("Enter password: ")
    driver.find_element_by_xpath("//input[@type='email']").send_keys(account)
    driver.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(3)

    # Detect verification
    if driver.find_elements_by_xpath("//div[@class='a-section a-spacing-large']") !=0:
        print("Please verify your amazon account")
        while True:
            if driver.find_elements_by_xpath("//div[1]/div/div/div/a[@class='nav-hidden-aria  ']"):
                print("Verification complete")
                break
            time.sleep(1)


def amazon_watch(link):
    driver.get(link)
    title = driver.find_element_by_xpath("//span[@id='productTitle']").text
    status = driver.find_element_by_xpath("//div[@id ='availability']").text.split(".")[0]
    return title, status

def amazon_buy(link):
    driver.get(link)
    driver.find_element_by_xpath("//input[@id='buy-now-button']").click()
    time.sleep(5)
    try:
        driver.switch_to.frame("turbo-checkout-iframe")
        driver.find_element_by_xpath("//input[@id='turbo-checkout-pyo-button']").click()
    except NoSuchFrameException:
        print("ERROR: No payment method available on your account")
        sys.exit()
    time.sleep(10)
    order_id = driver.current_url.split("&")[3].split("=")[1]
    # order_img = driver.find_element_by_xpath("//div[@class='a-section image-panel']/div/img").get_attribute('src')
    est_delivery = driver.find_element_by_xpath("//span[@class='a-color-success a-text-bold']").text
    return order_id, est_delivery

def ifttt_notify(order_id, title, est_delivery):
    data = {
        'value1': order_id,
        'value2': title,
        'value3': est_delivery
    }
    requests.post("https://maker.ifttt.com/trigger/amazon_order_status/with/key/b-oxyhDmYIHaQAMJB5i1wV", data=data)

def amazon_bot(link, account, password):
    global driver
    chromepath = "Others\\chromedriver.exe"
    driver = webdriver.Chrome(chromepath)
    while True:
        title, status = amazon_watch(link)
        #title =
        print(f'{title}: {status}')
        if status == "In Stock":
            amazon_signin(
                account=account,
                password=password
            )
            time.sleep(3)
            order_id, est_delivery = amazon_buy(link)
            break
    ifttt_notify(
        order_id = order_id,
        title = (title[:50] + '..') if len(title) > 75 else title,
        est_delivery = est_delivery
    )
