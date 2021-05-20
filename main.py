from selenium import webdriver
from time import sleep
from config import Config
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

from sendEmail import Gmail

browser = webdriver.Chrome()


def login_to_blackboard():
    go_to_login_path = "/html/body/div/div[1]/div/div[3]/div[2]/ul/li[1]/a"
    username_path = "/html/body/div/article/section[2]/div[1]/form[1]/div[1]/input"
    password_path = "/html/body/div/article/section[2]/div[1]/form[1]/div[2]/input"

    login_path = "/html/body/div/article/section[2]/div[1]/form[1]/button"

    browser.get("https://ntnu.blackboard.com/ultra/institution-page")

    browser.find_element_by_xpath(go_to_login_path).click()
    sleep(3)

    username_box = browser.find_element_by_xpath(username_path)
    password_box = browser.find_element_by_xpath(password_path)
    username_box.send_keys(Config.username)
    password_box.send_keys(Config.password)

    browser.find_element_by_xpath(login_path).click()


def check_room():
    timeplan_to_login = "/html/body/div[2]/section/div[1]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/p[2]/a"

    # area
    area_dropdown = "/html/body/div[4]/div[1]/form/section[1]/div[1]/section[1]/span/span[1]/span/span[2]/b"
    area_box_path = "/html/body/span/span/span[1]/input"

    # building
    building_dropdown = "/html/body/div[4]/div[1]/form/section[1]/div[1]/section[2]/span/span[1]/span/span[2]/b"
    building_path = "/html/body/span/span/span[1]/input"

    # room
    room_dropdown = "/html/body/div[4]/div[1]/form/section[1]/div[1]/section[3]/span/span[1]/span/span[2]/b"
    room_path = "/html/body/span/span/span[1]/input"

    
    browser.get('https://innsida.ntnu.no/romreservasjon')

    browser.find_element_by_xpath(timeplan_to_login).click()

    # Setting area to Gløs
    browser.find_element_by_xpath(area_dropdown).click()
    area_box = browser.find_element_by_xpath(area_box_path)
    area_box.send_keys("Gløshaugen")
    area_box.send_keys(Keys.ENTER)

    # setting building to elektro
    browser.find_element_by_xpath(building_dropdown).click()
    building_box = browser.find_element_by_xpath(building_path)
    building_box.send_keys("Elektro E/F")
    building_box.send_keys(Keys.ENTER)

    # setting room to E304
    browser.find_element_by_xpath(room_dropdown).click()
    room_box = browser.find_element_by_xpath(room_path)
    room_box.send_keys("E304")
    room_box.send_keys(Keys.ENTER)


    # area_box.send_keys(Keys.ENTER)
    #
    # browser.find_element_by_xpath(building).send_keys("Elektro E/F")
    #
    # browser.find_element_by_xpath(room).send_keys("E304")


def book_room():
    today = datetime.today()
    two_weeks = today + timedelta(days=14)
    book_date = two_weeks.strftime("%d.%m.%Y")
    print(book_date, "\n", type(book_date))

    go_to_booking_button = "/html/body/div[2]/section/div[1]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/p[1]/a"
    choose_institution = "/html/body/div/article/section[2]/div[1]/form/label/div/div[1]/input"

    username_path = "/html/body/div/article/section[2]/div[1]/form[1]/div[1]/input"
    password_path = "/html/body/div/article/section[2]/div[1]/form[1]/div[2]/input"
    login_button = "/html/body/div/article/section[2]/div[1]/form[1]/button"

    start_time_dropdown = "/html/body/div[4]/div[2]/form/div[1]/section[1]/span/span[1]/span/span[2]"
    start_time_path = "/html/body/span/span/span[1]/input"

    end_time_dropdown = "/html/body/div[4]/div[2]/form/div[1]/section[2]/span/span[1]/span/span[2]/b"
    end_time_path = "/html/body/span/span/span[1]/input"

    area_dropdown = "/html/body/div[4]/div[2]/form/div[2]/section[1]/span/span[1]/span/span[2]"
    area_path = "/html/body/span/span/span[1]/input"

    building_dropdown = "/html/body/div[4]/div[2]/form/div[2]/section[2]/span/span[1]/span/span[2]"
    building_path = "/html/body/span/span/span[1]/input"

    date_path = "/html/body/div[4]/div[2]/form/div[1]/section[3]/div[2]/div/input"

    show_rooms_button = "/html/body/div[4]/div[2]/form/div[4]/section[1]/button"

    choose_room_button = "/html/body/div[4]/div[2]/div[2]/section/form/div/section[1]/fieldset/ul/li[1]/div[1]/input"

    order_room_button = "/html/body/div[4]/div[2]/div[2]/section/form/div/section[2]/button"

    description_path = "/html/body/div[4]/form/div[3]/section/input"

    confirming_button = "/html/body/div[4]/form/div[6]/section[1]/button"

    browser.get('https://innsida.ntnu.no/romreservasjon')


    # login
    browser.find_element_by_xpath(go_to_booking_button).click()
    institutin_box = browser.find_element_by_xpath(choose_institution)
    institutin_box.send_keys("ntnu")
    institutin_box.send_keys(Keys.ENTER)

    browser.find_element_by_xpath(username_path).send_keys(Config.username)
    sleep(0.5)
    browser.find_element_by_xpath(password_path).send_keys(Config.password)
    sleep(0.5)
    browser.find_element_by_xpath(login_button).click()

    browser.find_element_by_xpath(start_time_dropdown).click()
    start_time_box = browser.find_element_by_xpath(start_time_path)
    start_time_box.send_keys("08:00")
    start_time_box.send_keys(Keys.ENTER)

    browser.find_element_by_xpath(end_time_dropdown).click()
    end_time_box = browser.find_element_by_xpath(end_time_path)
    end_time_box.send_keys("12:00")
    end_time_box.send_keys(Keys.ENTER)
    
    browser.find_element_by_xpath(area_dropdown).click()
    area_box = browser.find_element_by_xpath(area_path)
    area_box.send_keys("Gløshaugen")
    area_box.send_keys(Keys.ENTER)
    
    browser.find_element_by_xpath(building_dropdown).click()
    building_box = browser.find_element_by_xpath(building_path)
    building_box.send_keys("elektro E/F")
    building_box.send_keys(Keys.ENTER)

    date_box = browser.find_element_by_xpath(date_path)
    date_box.click()
    date_box.send_keys(Keys.CONTROL, "a")
    date_box.send_keys(Keys.BACKSPACE)
    date_box.send_keys(book_date)
    date_box.send_keys(Keys.ENTER)

    browser.find_element_by_xpath(show_rooms_button).click()
    sleep(1)
    browser.find_element_by_xpath(choose_room_button).click()
    sleep(1)
    browser.find_element_by_xpath(order_room_button).click()
    sleep(1)

    description_box = browser.find_element_by_xpath(description_path)
    description_box.send_keys("studering")
    sleep(1)

    command = input("are you sure? ")
    if command.lower() == "y" or command.lower() == "yes":
        browser.find_element_by_xpath(confirming_button).click()

        # send email on booking
        email = Gmail(Config.gmail, Config.gmail_password)
        message = f"You have booked a room \n see https://innsida.ntnu.no/romreservasjon for more information"
        email.send_email(message=message)
        sleep(2)

    else:
        print("you have canceld")

    browser.close()


book_room()



