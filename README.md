# 42-ssh-keysync
A command tool to update your local ssh public key on the 42 Intranet

# Requirements
ssh-keysync uses Python3. You thus need to have python3 as well as pip3 installed and in your $PATH.

# Installation

```bash
git clone https://github.com/severinferard/42-ssh-keysync/ ~/.ssh-keysync
pip3 install -r ~/.ssh-keysync/requirements.txt
echo 'alias ssh-keysync="python3 ~/.ssh-keysync"' >> ~/.zshrc
```

# Usage
```bash
ssh-keysync ssh-keysync.py [-h] [--new] [--debug]
```
### Options
* `--new`: Generate a new ssh key pair before updating it on the Intra.
* `--debug`: Run without Selenium headleass mode, opening a chrome window.
* `--help`: Display a help message.
