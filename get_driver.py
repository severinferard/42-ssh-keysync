# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    get_driver.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: severin <severin@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 19:06:28 by severin           #+#    #+#              #
#    Updated: 2021/02/02 01:50:22 by severin          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from os import popen, system
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from animation import animate_progress, TermEscapeColors
import sys

ESC = TermEscapeColors()

@animate_progress(f"{ESC.BOLD}Getting chrome version{ESC.NORMAL}")
def get_chrome_version():
	stream = popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version')
	return (stream.read().split()[-1])

@animate_progress(f"{ESC.BOLD}Downloading chrome drivers for version{ESC.NORMAL}")
def download(version):
	sys.stdout.write(f'\r                                             {ESC.LBLUE}{version}{ESC.NORMAL}')
	system(f'curl --silent https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64.zip --output chromedriver.zip > /dev/null')
	return (1)

@animate_progress(f"{ESC.BOLD}unzipping file{ESC.NORMAL}")
def unzip():
	system('unzip ./chromedriver.zip > /dev/null')
	system('rm -f chromedriver.zip')
	return (1)

def download_driver():
	global version
	version = get_chrome_version()
	system('rm -f chromedriver')
	download(version)
	unzip()
	print(f' \U0001F4BE   {ESC.BOLD}Chrome WebDriver installed succesfully{ESC.NORMAL}')


@animate_progress(f"{ESC.BOLD}Retrieving chrome drivers{ESC.NORMAL}")
def get_chrome_driver(headless=True):
	try:
		chrome_options = Options()
		if headless:
			chrome_options.add_argument("--headless") 
		driver = webdriver.Chrome('./chromedriver', options=chrome_options)
		return (driver , 1)
	except Exception as e:
		if "executable needs to be in PATH" in e.args[0]:
			return (None, -1)
		elif "This version of ChromeDriver only supports Chrome version" in e.args[0]:
			return (None, -2)

	