from selenium import webdriver
from time import sleep
from config import Config
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


from sendEmail import Gmail

def calc_date(days):
    """return: date in 'days' number of days """
    today = datetime.today()
    two_weeks = today + timedelta(days=14)
    book_date = two_weeks.strftime("%d.%m.%Y")

    return book_date



class NTNU:



    def __init__(self):
        self.driver = webdriver.Chrome()
        self.__username = Config.ntnu_username
        self.__password = Config.ntnu_password

    def change_login_info(self, username, passwd):
        self.__username = username
        self.__password = passwd

    def login(self):
        self.driver.get("https://innsida.ntnu.no/c/portal/login")
        
        # username
        self.driver.find_element_by_id('username').send_keys(Config.ntnu_username)

        # password
        self.driver.find_element_by_id('password').send_keys(Config.ntnu_password)

        # click login button
        self.driver.find_element_by_xpath('/html/body/div/article/section[2]/div[1]/form[1]/button').click()


        self.driver.find_element_by_id('students-menu-button').click()


    def book_room(self):
        """has to continue after login"""
        # go to room-booking
        self.driver.get("http://www.ntnu.no/romres")

        # start time
        start_time = '08:00'
        select_start = Select(self.driver.find_element_by_id("start"))
        select_start.select_by_value(start_time)

        # end time
        duration = '04:00'  # this is duration from booking in hours
        select_end = Select(self.driver.find_element_by_id('duration'))
        select_end.select_by_value('04:00')

        # date
        date = calc_date(12)
        select_date = self.driver.find_element_by_id('preset_date')
        select_date.clear()
        select_date.send_keys(date)
        select_date.send_keys(Keys.ENTER)

        # area
        area = 'Gløshaugen'
        select_area = Select(self.driver.find_element_by_id('area'))
        select_area.select_by_visible_text(area)
        
        # building
        building = "Elektro E/F"
        select_building = Select(self.driver.find_element_by_id('building'))
        select_building.select_by_visible_text(building)

        # min people
        min_people = None
        if min_people:
            people_input_box = self.driver.find_element_by_id('size')
            people_input_box.send_keys(min_people)
            people_input_box.send_keys(Keys.ENTER)

        sleep(1)
        # press submit button
        self.driver.find_element_by_id('preformsubmit').click()

        # choose from available
        room_ids = {'E204': 'input_341E204',
                    'F204': 'input_341F204',
                    'EL23': 'input_341EL23',
                    'F404': 'input_341F404',
                    'F304': 'input_341F304'}
        # UNCOMMENT LINE UNDER TO GET TEXT ELEMENT OF ALL ROOMS THAT OCCURS
        # available_rooms_text = self.driver.find_element_by_id('room_table').text
        # change this if you want another room
        room_id = room_ids['E204']

        # choose the room
        try:
            self.driver.find_element_by_id(room_id).click()
            fail = False
        except:
            print(f"room: {room_id} not found. \n trying to book a random room")
            fail = True

        # booking your desired room failed, will continue to try booking first element
        if fail:
            try:
                self.driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/section/form/div/section[1]/fieldset/ul/li[1]/div[1]/input').click()
                fail = False
            except:
                print("first try failed")
                fail = True

        if fail:
            try:
                self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/section/form/div/section[1]/fieldset/ul/li/div[1]/input').click()
                fail = False
            except:
                fail = True
                print('failed on second try. \n Canceling')
















        




    def __wait_and_get_by_id(self, element_id: str):

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        element.click()

        return element


test = NTNU()

test.login()
test.book_room()


input(" press any key to close --> ")
test.driver.close()
