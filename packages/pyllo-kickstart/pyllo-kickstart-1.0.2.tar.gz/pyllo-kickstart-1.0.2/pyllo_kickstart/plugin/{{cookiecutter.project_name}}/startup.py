# -*- coding: utf-8 -*-
# Copyright © {{cookiecutter.company}}
# Author: {{cookiecutter.author}}


def install(package):
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", package])


if __name__ == "__main__":
    install(".")
    from pyllo.main import main
    main()
