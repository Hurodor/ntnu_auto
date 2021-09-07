from ntnu import NTNU
import config

booking_settings = config.get_settings()['room_settings']

book = NTNU()
book.login()
book.book_room(**booking_settings)

