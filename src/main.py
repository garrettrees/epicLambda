from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import datetime
import time
import os
import boto3

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

    today = datetime.datetime.now().strftime("%d")
    current_month = datetime.datetime.now().strftime("%m")

    driver = webdriver.Chrome(chrome_options=chrome_options)

    '''
    #Use AWS Parameter Store:
    def get_parameters(param_name):
        ssm = boto3.client('ssm', region_name='us-west-2')
        response = ssm.get_parameters(
            Names=[
                param_name,    def get_parameters(param_name):
        ssm = boto3.client('ssm', region_name='us-west-2')
        response = ssm.get_parameters(
            Names=[
                param_name,
            ],
            WithDecryption=True
        )
        credentials = response['Parameters'][0]['Value']
        return credentials
            ],
            WithDecryption=True
        )
        credentials = response['Parameters'][0]['Value']
        return credentials
    '''

    # Set your username, password & target reservation day (of the current month) before running script
<<<<<<< HEAD
    user = 'garrett'
    if user == 'byron':
        username = ""  # email address
        password = ""
        user_xpath = "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li[2]/span/label/span"
        #username = get_parameters('epic_username_byron')
        #password = get_parameters('epic_password_byron')
    else:
        username = ''
        password = ''
        user_xpath = "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li/span/label/span"
        #username = get_parameters('epic_username_garrett')
        #password = get_parameters('epic_password_garrett')
=======
    username = ""  # email address
    password = ""
    today = datetime.datetime.now().strftime("%d")
    reservation_day = str(int(today) + 7)
    #driver = webdriver.Chrome("/Users/garrettrees/chromedriver")
    current_month = datetime.datetime.now().strftime("%m")
>>>>>>> 33c7f7592f2a0d8f1df6c1e91f1e594354e04a7b

    # Set implicit wait for the life of the driver object
    # Set implicit wait for the life of the driver object
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
    if current_month == "01" or current_month == "03" or current_month == "05" or current_month == "07" or current_month == "08" or current_month == "10" or current_month == "12" and today >= "25":
        reservation_day = str(7 - (31 - (int(today))))
        go_to_next_month.click()
    elif current_month == "02" and today >= "22":
        reservation_day = str(7 - (28 - (int(today))))
        go_to_next_month.click()
    elif current_month == "04" or current_month == "06" or current_month == "09" or current_month == "11" and today >= "24":
        reservation_day = str(7 - (30 - (int(today))))
        go_to_next_month.click()
    else:
        reservation_day = str(int(today) + 7)
        go_to_next_month.click()

    # Select Date
    desired_date = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[4]/button[" + reservation_day + "]")
    desired_date.click()

    # Assign Pass Holders
    pass_holder = driver.find_element_by_xpath(user_xpath)
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
