from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import datetime
import time
import os

def make_reservation(event=None, context=None):
    # This script will reserve 7 days from today's date
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Set your username, password & target reservation day (of the current month) before running script
    username = "greesy@gmail.com"  # email address
    password = "R!d3-0r-d!3"
    today = datetime.datetime.now().strftime("%d")
    reservation_day = str(int(today) + 7)
    #driver = webdriver.Chrome("/Users/garrettrees/chromedriver")
    current_month = datetime.datetime.now().strftime("%m")

    # Set implicit wait for the life of the webdriver object
    driver.implicitly_wait(30)
    # Maximize browser (so all elements are visible)
    driver.maximize_window()
    # Go to Reservations page
    driver.get("https://www.epicpass.com/info/reservation-details.aspx")
    # Close cookies banner at bottom of page
    close_banner = driver.find_element_by_id("onetrust-accept-btn-handler")
    close_banner.click()
    # Click Reserve button
    reserve_button = driver.find_element_by_link_text("RESERVE YOUR DAYS")
    reserve_button.send_keys(Keys.RETURN)

    # Login
    username_field = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div[2]/div/div/div[1]/form/div/div/div[3]/input")
    username_field.send_keys(username)
    password_field = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div[2]/div/div/div[1]/form/div/div/div[4]/input")
    password_field.send_keys(password)
    sign_in_button = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div[2]/div/div/div[1]/form/div/div/div[5]/button")
    sign_in_button.send_keys(Keys.RETURN)

    # Select Resort
    park_city = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div/div/div[2]/div/select/option[24]")
    park_city.click()
    check_availability = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div/div/div[3]/button")
    check_availability.click()

    #### Logic to handle reservations made less than 7 days from the end of the current month ####
    go_to_next_month = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button[2]")
    if (current_month == "1" or "3" or "5" or "7" or "8" or "10" or "12") and today >= "25":
        reservation_day = str(7 - (31 - (int(today))))
        go_to_next_month.click()
    elif current_month == "2" and today >= "22":
        reservation_day = str(7 - (28 - (int(today))))
        go_to_next_month.click()
    elif (current_month == "4" or "6" or "9" or "11") and today >= "24":
        reservation_day = str(7 - (30 - (int(today))))
        go_to_next_month.click()
    else:
        reservation_day = str(int(today) + 7)
    # Select Date
    desired_date = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[4]/button[" + reservation_day + "]")
    desired_date.click()

    # Assign Pass Holders
    pass_holder = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li/span/label/span")
    pass_holder.click()
    assign_button = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[3]/button[2]")
    assign_button.click()

    # Accept Terms & Conditions
    terms_conditions = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[6]/div[2]/div[2]/div[2]/label/input")
    driver.execute_script("arguments[0].click();", terms_conditions)

    # Complete Reservation
    complete_reservation = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[6]/div[3]/button")
    driver.execute_script("arguments[0].click();", complete_reservation)

    # Close browser & quit
    driver.close()
    driver.quit()