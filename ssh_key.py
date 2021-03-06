# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ssh_key.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: severin <severin@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/01/31 20:45:42 by severin           #+#    #+#              #
#    Updated: 2021/02/02 18:44:26 by severin          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from os.path import expanduser
from os import system
from animation import animate_progress, TermEscapeColors

ESC = TermEscapeColors()

@animate_progress(f"{ESC.BOLD}Fetching ssh key{ESC.NORMAL}")
def get_key(path):
	try:
		f = open(path, 'r')
		f.close
		with open(path, 'r') as f:
			return 1, f.read()
	except:
		return 0, None

@animate_progress(f"{ESC.BOLD}Creating a new ssh key pair...{ESC.NORMAL}")
def create_ssh_key(path='~/.ssh/id_rsa'):
	system(f'sh genkey.sh {path}')
	return 1, None

def get_ssh_key(new=False, path=None):
	if path is None:
		path = f'{expanduser("~")}/.ssh/id_rsa.pub'
	if new:
		create_ssh_key()
	_, key = get_key(path)
	if not key:
		print(f"      ⚠️   {ESC.BOLD}Couldn't find an ssh key in {ESC.LBLUE}{path}{ESC.NORMAL}")
		create_ssh_key()
		print(f"      {ESC.BOLD}A new \U0001F9FC fresh \U0001F9FC ssh key has been created in {ESC.LBLUE}{path}{ESC.NORMAL}")
		_, key = get_key(path)
	return (key)
