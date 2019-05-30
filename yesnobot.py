from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests

LOGIN = 'gloom_1992@mail.ru'
PASSWORD = 'Fynbctgnbr12121212'
YANDEX_KEY_TR = 'trnsl.1.1.20181111T103752Z.a6feae9da7119a9a.14a98a07d2043e6ab78c1863f0752ba0e4a581ee'
YANDEX_KEY_DICT = 'dict.1.1.20181111T121658Z.a1f93be012101a5d.f7ce9bf52f385071a6407c434e3b309c405baec5'

class Bot:
	def __init__(self):
		self.driver = webdriver.Firefox(executable_path=r'C:\Users\Sony\gecko\geckodriver.exe')

	def login(self):
		self.driver.get('https://puzzle-english.com/danetka')

		play_button = self.driver.find_element_by_xpath('//a[@class="j-play_sprint border-link border-link_style_white border-link_size_xl puzzle_va_middle puzzle_ta_center"]')
		play_button.click()

		email_button = self.driver.find_element_by_xpath('//span[@class="toggle-sign-in-form"]')
		email_button.click()

		email_input = self.driver.find_element_by_xpath('//input[@class="sign-in-form__input email-sign-in-form__input_focus email-sign-in-form__input_pr-65 ui-autocomplete-input"]')
		email_input.send_keys(LOGIN)
		email_input.send_keys(Keys.ENTER)

		password_input = self.driver.find_element_by_xpath('//input[@class="sign-in-form__input"]')
		sleep(1)
		password_input.send_keys(PASSWORD)
		password_input.send_keys(Keys.ENTER)

		sleep(6)

	def enter_the_game(self):
		play_button = self.driver.find_element_by_xpath('//a[@class="j-play_sprint border-link border-link_style_white border-link_size_xl puzzle_va_middle puzzle_ta_center"]')
		play_button.click()
		sleep(1)

	def play(self):
		eng_word = self.driver.find_element_by_xpath('//div[@class="b-field__words puzzle-sprint__word"]/span').text
		rus_word = self.driver.find_element_by_xpath('//div[@class="b-field__words b-field__words_translate puzzle-sprint__word_translation"]/span').text
		translated = self.translate_word(eng_word)
		translated_str = ', '.join(translated)
		if rus_word in translated:
			button_yes = self.driver.find_element_by_css_selector('button.b-button_right')
			print(translated_str + ' : ' + rus_word + ' - correct')
			#button_yes.click()
			button_yes.send_keys(Keys.ARROW_LEFT)
		else:
			button_no = self.driver.find_element_by_css_selector('button.b-button_wrong')
			print(translated_str + ' : ' + rus_word + ' - not correct')
			#button_no.click()
			button_no.send_keys(Keys.ARROW_RIGHT)
		return True

	def translate_word(self, word):
		url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang=en-ru&text={}'.format(YANDEX_KEY_DICT, word)
		r = requests.get(url)
		translations = []
		for t in r.json()['def']:
			for o in t['tr']:
				translations.append(o['text'])
				if 'syn' in o:
					for s in o['syn']:
						translations.append(s['text'])
		return translations

bot = Bot()
bot.login()
bot.enter_the_game()
while True:
	bot.play()
# <div class="b-field__words puzzle-sprint__word">
#                             <span>homework</span>
#                         </div>

# <div class="b-field__words b-field__words_translate puzzle-sprint__word_translation">
#                             <span>домашнее задание</span>
#                         </div>

# <button class="b-button b-button_green b-button_right j-puzzle_sprint_btn" data-correct="1">
#                             да
#                         </button>

# <button class="b-button b-button_red b-button_wrong j-puzzle_sprint_btn" data-correct="0">
#                             нет
#                         </button>


# words = ['привет']

# for word in words:
# 	url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang=ru-en&text={}'.format(YANDEX_KEY_DICT, word)
# 	r = requests.get(url)
# 	translations = []
# 	for t in r.json()['def']:
# 		for o in t['tr']:
# 			translations.append(o['text'])
# 			if 'syn' in o:
# 				for s in o['syn']:
# 					translations.append(s['text'])
# 	print( translations )

