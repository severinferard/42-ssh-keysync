# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    animation.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: severin <severin@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/02 00:44:47 by severin           #+#    #+#              #
#    Updated: 2021/02/02 18:46:02 by severin          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
import sys
import itertools
import threading
from queue import Queue

SUCCESS = 1
UNKNOWN = 2
FAILED = 3

class TermEscapeColors():
	def __init__(self):
		self.BOLD = '\033[1m'
		self.NORMAL = '\033[0m'
		self.LBLUE = '\033[94m'
		self.DIM = '\033[2m'
		self.PURPLE = '\033[35m'
		self.LGREEN = '\033[92m'
		self.RED = '\033[31m'


def animate_progress(message, indentation=0):
	def _animate_progress(func):
		def wrapper(*args,  **kwargs):
			q = Queue()
			t = threading.Thread(target=animate, args=(message, q, indentation))
			t.start()
			ret = func(*args,  **kwargs)
			q.put(ret[0])
			t.join()
			return ret
		return wrapper
	return _animate_progress

def animate(message, q, indentation):
	i = 0
	frames =  ([f"{' '* 4 * indentation}{' ' * i}\U0001F7E1{' ' * (4 - i)}" for i in range(4)]
		+ [f"{' ' * 4 * indentation}{' ' * (4 - i)}\U0001F7E1{' ' * i}" for i in range(4)])
	while q.empty():
		c = frames[i]
		sys.stdout.write('\r' + c + message)
		sys.stdout.flush()
		time.sleep(0.1)
		i += 1
		if i == len(frames):
			i = 0
	ret = q.get()
	if (ret > 0):
		sys.stdout.write(f'\r{" "* 4 * indentation} \U00002705  \n')
	else:
		sys.stdout.write(f'\r{" "* 4 * indentation} \U0000274C  \n')
