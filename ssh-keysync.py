# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ssh-keysync.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: severin <severin@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 18:48:43 by severin           #+#    #+#              #
#    Updated: 2021/02/02 02:13:19 by severin          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from selenium.webdriver.common.keys import Keys
import stdiomask, time, argparse
from get_driver import download_driver, get_chrome_driver
from ssh_key import get_ssh_key
from animation import animate_progress, TermEscapeColors

ESC = TermEscapeColors()
GIT_LINK = "https://github.com/severinferard/42-ssh-keysync"

def parse_flags():
	parser = argparse.ArgumentParser(description='Update your public ssh key on the Intra')
	parser.add_argument('--new', '-n', default=False, action='store_true', help="Create a new ssh key pair, overwriting the previous one")
	parser.add_argument('--debug', '-d', default=False, action='store_true', help="Run without headless mode, opening a chrome window")
	args = parser.parse_args()
	return args

def get_credentials():
	login = input("Login: ")
	password = stdiomask.getpass("Password: ")
	return login, password

@animate_progress(f"{ESC.BOLD}Connecting to the {ESC.PURPLE}\U00002728Intra\U00002728{ESC.NORMAL}")
def connect_to_intra(driver, login, password):
	try:
		driver.get('https://signin.intra.42.fr/users/sign_in')
		login_field = driver.find_element_by_id('user_login')
		password_field = driver.find_element_by_id('user_password')
		login_field.send_keys(login)
		password_field.send_keys(password)
		time.sleep(0.1)
		password_field.send_keys(Keys.RETURN)
		return 1
	except:
		return 0

@animate_progress(f"{ESC.BOLD}Entering the new \U0001F510 ssh key {ESC.NORMAL}\U0001F510")
def enter_key(driver, key):
	try:
		driver.get("https://profile.intra.42.fr/gitlab_users/new")
		new_btn = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div/a[1]')
		new_btn.click()
		time.sleep(0.1)
		ssh_key_field = driver.find_element_by_id('gitlab_user_public_key')
		ssh_key_field.send_keys(key)
		time.sleep(0.1)
		submit_btn = driver.find_element_by_xpath('//*[@id="new_gitlab_user"]/button')
		submit_btn.click()
		return 1
	except:
		return 0

def main():
	args = parse_flags()
	print("""
	 _           _                                   
 ___ ___| |__       | | _____ _   _ ___ _   _ _ __   ___ 
/ __/ __| '_ \ _____| |/ / _ \ | | / __| | | | '_ \ / __|
\__ \__ \ | | |_____|   <  __/ |_| \__ \ |_| | | | | (__ 
|___/___/_| |_|     |_|\_\___|\__, |___/\__, |_| |_|\___|
                              |___/     |___/     sferard
	""")
	print(f"{ESC.DIM}NOTE: Your credentials are needed to connect to the Intra. They are not and won't be stored, logged, sent, or \
used for any other purposes than logging you in. Your credentials will be destroyed as the program exits and you will need to enter \
them every time you use this program. You can take a look at the code here {GIT_LINK} if you have trust issues (which you always should \
when entering private informations on an unoffical medium).\n{ESC.NORMAL}")
	print(f"{ESC.DIM}NOTE: This program is distributed under MIT Licence which basically means \"Do whatever you want with it but don't \
get me responsible for the sh*t you can get in while using it\". Please be responsible and don't flood the Intra servers using it. \
Remember, you're logging in with {ESC.BOLD}YOUR{ESC.NORMAL}{ESC.DIM} login. If it doesn't work don't spam it but try changing your ssh key manually and report issues on the GitHub page if you'd like.\n{ESC.NORMAL}")

	login, password = get_credentials()
	ssh_key = get_ssh_key(new=args.new)
	print(ssh_key)
	if args.debug:
		print(f" \U0001F4A1    {ESC.BOLD}Running in debug mode{ESC.NORMAL}")
	driver, ret = get_chrome_driver(not args.debug)
	if ret < 0:
		if (ret == -1):
			print(f" ⚠️    {ESC.BOLD}Couldn't find chrome drivers {ESC.LBLUE}{ESC.NORMAL}")
		if (ret == -2):
			print(f" ⚠️    {ESC.BOLD}The chrome drivers found does not match your actual version of chrome {ESC.LBLUE}{ESC.NORMAL}")
		download_driver()
		driver = get_chrome_driver(not args.debug)

	connect_to_intra(driver, login, password)
	enter_key(driver, ssh_key)

	print(f"{ESC.BOLD}{ESC.LGREEN}Your {ESC.NORMAL}{ESC.BOLD}\U0001F510 ssh key \U0001F510 {ESC.BOLD}{ESC.LGREEN}have been changed successfully on the {ESC.PURPLE}\U00002728Intra\U00002728{ESC.NORMAL}{ESC.BOLD}{ESC.LGREEN}!{ESC.NORMAL}")

if __name__ == "__main__":
	main()
	

