import keyring
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Config
from supported_settings import valid_room_settings


def calc_date(days):
    """return: date in 'days' number of days """
    today = datetime.today()
    two_weeks = today + timedelta(days=days)
    book_date = two_weeks.strftime("%d.%m.%Y")

    return book_date


class NTNU:

    def __init__(self):
        self.driver = None
        self.__username = Config.username
        self.__password = keyring.get_password('ntnu', self.__username)
        self.chromedriver_path = Config.chromedriver

    def change_login_info(self, username, passwd):
        self.__username = username
        self.__password = passwd

    def start_session(self, headless=True):
        """this function starts selenium, you can toggle gui with headless"""


        if headless:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--log-level=off')
            self.driver = webdriver.Chrome(self.chromedriver_path, options=options)
            return

        self.driver = webdriver.Chrome(self.chromedriver_path)

    def login(self, headless=True):
        """this loges in to ntnu"""
        self.start_session(headless)

        # self.driver.minimize_window()

        self.driver.get("https://innsida.ntnu.no/c/portal/login")

        # username
        self.driver.find_element_by_id('username').send_keys(self.__username)

        # password
        self.driver.find_element_by_id('password').send_keys(self.__password)

        # click login button
        # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.xPATH, "/html/body/div/article/section[2]/div[1]/form[1]/button"))).click()
        self.driver.find_element_by_xpath('/html/body/div/article/section[2]/div[1]/form[1]/button').click()

        # self.driver.find_element_by_id('students-menu-button').click()

    def book_room(self, **kwargs):
        """has to continue after login"""
        # pass in kwargs corresponding to parameters to change it
        parameters = {
            'start_time': '08:00',
            'duration': '04:00',  # this is duration from booking in hours
            'days': 14,
            'area': 'Gl??shaugen',
            'building': "Elektro E/F",
            'min_people': None,
            'room_id': 'E204',
            'description_text': "Studering"
      }

        for key, value in kwargs.items():
            parameters[key] = value


        self.driver.get("http://www.ntnu.no/romres")

        # tries to press yes, comtinue button, if element not found we skip this part as we dont need it
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "Yes"))).click()
        except Exception:
            pass

        # start time
        start_time = parameters['start_time']
        select_start = Select(self.driver.find_element_by_id("start"))
        select_start.select_by_value(start_time)

        # end time
        duration = parameters['duration']
        select_end = Select(self.driver.find_element_by_id('duration'))
        select_end.select_by_value(duration)

        # date
        days = parameters['days']
        date = calc_date(days)  # max
        select_date = self.driver.find_element_by_id('preset_date')
        select_date.clear()
        select_date.send_keys(date)
        select_date.send_keys(Keys.ENTER)

        # area
        area = parameters['area']
        select_area = Select(self.driver.find_element_by_id('area'))
        select_area.select_by_visible_text(area)

        # building
        building = parameters['building']
        select_building = Select(self.driver.find_element_by_id('building'))
        select_building.select_by_visible_text(building)

        # min people
        min_people = parameters['min_people']
        if min_people:
            people_input_box = self.driver.find_element_by_id('size')
            people_input_box.send_keys(min_people)
            people_input_box.send_keys(Keys.ENTER)

        # press "vis ledige rom" button
        self.driver.find_element_by_id('preformsubmit').click()

        # UNCOMMENT LINE UNDER TO GET TEXT ELEMENT OF ALL ROOMS THAT OCCURS
        # available_rooms_text = self.driver.find_element_by_id('room_table').text

        # this fetches the right input str for the chosen room (see supported_settings.py)
        room_id = valid_room_settings[0][parameters['area']][parameters['building']][parameters['room_id']]

        # choose the room

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, room_id))).click()
            # self.driver.find_element_by_id(room_id).click()
            fail = False
        except:
            print(f"room: {room_id} not found. \n trying to book a random room")
            fail = True

        # booking your desired room failed, will continue to try booking first element
        if fail:
            try:
                self.driver.find_elements_by_xpath(
                    '/html/body/div[4]/div[2]/div[2]/section/form/div/section[1]/fieldset/ul/li[1]/div[1]/input').click()
            except:
                print("first try failed")
                try:
                    self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div[2]/section/form/div/section[1]/fieldset/ul/li/div[1]/input').click()
                except:
                    print('failed on second try. \nCanceling')
                    self.driver.close()
                    return

        # order button
        self.driver.find_element_by_id('rb-bestill').click()

        # description
        description_text = parameters['description_text']
        # description_box = self.driver.find_element_by_id('name')
        description_box = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'name')))
        description_box.send_keys(description_text)

        # confirm buttton
        self.driver.find_element_by_name('confirm').click()

        # send comfirmation email
        self.driver.find_element_by_name('sendmail').click()

        print("\nBooking complete! \n-----------------------------------------------")

        self.driver.quit()

    def tab(self, **action):
        """currently supported kwargs: newtab, switch"""
        options = {
            'newtab': False,
            'switch': None
        }
        for key, value in options.items():
            if key in action.keys():
                options[key] = action[key]
                print(options)

        # open new tab and switch to it
        if options['newtab'] and options['switch'] is True:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # if url is spesified go to that url
            if str(options['newtab'])[:3] == 'http':
                self.driver.get(options['new_tab'])

        if type(options['switch']) is int:
            tab = options['switch']
            self.driver.switch_to.window(self.driver.window_handles[tab])


if __name__ == '__main__':
    book = NTNU()
    book.login(False)
    book.book_room()
