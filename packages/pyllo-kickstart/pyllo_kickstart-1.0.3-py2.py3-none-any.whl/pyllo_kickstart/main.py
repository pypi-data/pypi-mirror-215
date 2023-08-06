#!/usr/bin/env python
import os.path as osp
import sys
import subprocess
from rich import print
from cookiecutter.main import cookiecutter

logo = r"""
 ________  ___    ___ ___       ___       ________     
|\   __  \|\  \  /  /|\  \     |\  \     |\   __  \     
\ \  \|\  \ \  \/  / | \  \    \ \  \    \ \  \|\  \    
 \ \   ____\ \    / / \ \  \    \ \  \    \ \  \\\  \   
  \ \  \___|\/  /  /   \ \  \____\ \  \____\ \  \\\  \  
   \ \__\ __/  / /      \ \_______\ \_______\ \_______\
    \|__||\___/ /        \|_______|\|_______|\|_______|
         \|___|/     
        ╭──────────────────────────╮
        │   Welcome to the Pyllo   │
        │   Plugin Generator!      │
        ╰──────────────────────────╯
        
"""

HERE = osp.abspath(osp.dirname(__file__))

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        print(question + prompt)
        print("> ", end="")
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' "
                  "(or 'y' or 'n').\n")
            

def select_pick(title: str, options=[], default=None):
    while 1:
        print(f"{title} [1-{len(options)}]")
        for i, option in enumerate(options):
            print(f"{i+1}) {option}")
        
        print("> ", end="")
        choice = input().lower()
        if default is not None and choice == '':
            return default
        else:
            try:
                num = int(choice)
                if num < 1 or num > len(options):
                    raise IndexError
                return num - 1
            except Exception:
                print(f"Please respond with number in [1-{len(options)}].\n")



def main():
    # ----- start of main -----
    print(logo)
    title = '[bold]? What type of plugin do you want to create?[bold/]'
    options = ['New Container Plugin',
               'New Dockable Plugin',
               'New Language Support',
               'New Custom Editor',
               'New Code Editor Extension']
    index = select_pick(title, options, 1)
    if index == 0:
        result = cookiecutter(HERE, directory="plugin")
    elif index == 1:
        result = cookiecutter(HERE, directory="dockableplugin")

    if index in (0, 1):
        choice = query_yes_no("? Do you want to open project in Pyllo now? (Pyllo is needed)")
        if choice == "yes":
            subprocess.Popen(f"pyllo {result}",
                             shell=True,
                             start_new_session=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.STDOUT)



if __name__ == "__main__":
    main()
