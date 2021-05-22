import keyring
from time import sleep
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from config import Config


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

    def start_session(self):
        self.driver = webdriver.Chrome(self.chromedriver_path)


    def login(self):
        """this loges in to ntnu"""
        self.start_session()

        self.driver.minimize_window()

        self.driver.get("https://innsida.ntnu.no/c/portal/login")
        
        # username
        self.driver.find_element_by_id('username').send_keys(self.__username)

        # password
        self.driver.find_element_by_id('password').send_keys(self.__password)

        # click login button
        self.driver.find_element_by_xpath('/html/body/div/article/section[2]/div[1]/form[1]/button').click()


        # self.driver.find_element_by_id('students-menu-button').click()


    def book_room(self, **kwargs):
        """has to continue after login"""
        # go to room-booking
        parameters = {
            'start_time': '08:00',
            'duration': '04:00',
            'days': 12,   # this is duration from booking in hours7
            'area': 'Gløshaugen',
            'building': "Elektro E/F",
            'min_people': None,
            'room_id': 'E204',
            'description_text':  "Studering"
        }

        self.driver.get("http://www.ntnu.no/romres")


        # start time
        start_time = parameters['start_time']
        select_start = Select(self.driver.find_element_by_id("start"))
        select_start.select_by_value(start_time)

        # end time
        duration = parameters['duration']
        select_end = Select(self.driver.find_element_by_id('duration'))
        select_end.select_by_value(duration)

        # date
        date = calc_date(14)    # max
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
        min_people = None
        if min_people:
            people_input_box = self.driver.find_element_by_id('size')
            people_input_box.send_keys(min_people)
            people_input_box.send_keys(Keys.ENTER)

        sleep(1)
        # press submit button
        self.driver.find_element_by_id('preformsubmit').click()
        
        # UNCOMMENT LINE UNDER TO GET TEXT ELEMENT OF ALL ROOMS THAT OCCURS
        # available_rooms_text = self.driver.find_element_by_id('room_table').text
        # change this if you want another room

        room_ids = {'E204': 'input_341E204',
                     'F204': 'input_341F204',
                     'EL23': 'input_341EL23',
                     'F404': 'input_341F404',
                     'F304': 'input_341F304'}

        
        room_id = room_ids[parameters['room_id']]
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
            except:
                print("first try failed")
                try:
                    self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div[2]/section/form/div/section[1]/fieldset/ul/li/div[1]/input').click()
                except:
                    print('failed on second try. \n Canceling')
                    self.driver.close()
        
        # order button
        self.driver.find_element_by_id('rb-bestill').click()
        
        # description
        description_text = "Studering"
        description_box = self.driver.find_element_by_id('name')
        description_box.send_keys(description_text)
        
        # confirm

        # self.driver.find_element_by_name('confirm').click()

        # self.driver.find_element_by_name('sendmail').click()

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
    book.login()



