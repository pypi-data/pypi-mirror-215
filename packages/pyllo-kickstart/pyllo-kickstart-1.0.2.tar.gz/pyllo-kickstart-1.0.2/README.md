# pyllo-kickstart

## What is pyllo-kickstart?
pyllo-kickstart is a kick-start plugin template generator for Pyllo extension.

## What is Pyllo?
Pyllo is a plugin based meta-IDE platform create by Pyllo project team owned 
by SHCONNET INFO COMPANY.

## What is plugin?
A plugin is a software add-on that is installed on a program, enhancing its 
capabilities. Usually plugin is consisted of self-consistent functionalities, and provide API to other plugins.

## What kind of plugins Pyllo supports?
Pyllo supports two kinds of plugins. One is PylloPlugin which is plain and 
non-window plugin. PylloPlugin can has other plugins to give user buttons or 
actions to interact(such as add actions to MainMenu or add actions even 
widgets to Toolbar). Another one is PylloDockablePlugin which has one dockable 
window can be shown in MainWindow.

## How to create an PylloPlugin? 
```commandline
pip install pyllo-kickstart
```

Enter `pyllo-kickstart` in command line, select `New Container Plugin` at 
beginning and follow the instructions.

```commandline
% pyllo-kickstart

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
        

? What type of plugin do you want to create? [1-5]
1) New Container Plugin
2) New Dockable Plugin
3) New Language Support
4) New Custom Editor
5) New Code Editor Extension
> 1
project_name [helloworld]: 
plugin_class_name [HelloWorld]: 
plugin_description [Hello world plugin which doesn't contain dockable window.]: 
author [pyllo]: 
company [my awesome company]: 
? Do you want to open project in Pyllo now? (Pyllo is needed) [Y/n] 
> Y
%
```

Open the newly created project with your favorite code editor and navigate to the root directory.
```commandline
% cd helloworld
% tree .
.
├── __init__.py
├── helloworld
│   ├── __init__.py
│   ├── api.py
│   ├── confpage.py
│   ├── container.py
│   └── plugin.py
├── setup.py
└── startup.py
```
Notice: maybe you will see some __pycache__ files, it is ok to ignore them.
 
`startup.py` is a convenience script to instantly bring up Pyllo IDE with 
`helloworld` plugin loaded.

Now you can see the toolbar action `test` on the Pyllo main toolbar. Click it,
you will get a new message box shows that the `helloworld` plugin working like 
a charm!

![messagebox](data/1686626799664.jpg)

## How to create an PylloDockablePlugin?
```commandline
pip install pyllo-kickstart
```

Enter `pyllo-kickstart` in command line, select `New Dockable Plugin` at 
beginning and follow the instructions.

```commandline
% pyllo-kickstart

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
        

? What type of plugin do you want to create? [1-5]
1) New Container Plugin
2) New Dockable Plugin
3) New Language Support
4) New Custom Editor
5) New Code Editor Extension
> 2
project_name [hellodock]: 
plugin_class_name [HelloDock]: 
plugin_description [Hello world dockable plugin which contains dockable window.]: 
author [pyllo]: 
company [my awesome company]: 
? Do you want to open project in Pyllo now? (Pyllo is needed) [Y/n] 
> Y
%
```
Notice: maybe you will see some __pycache__ files, it is ok to ignore them.
 
`startup.py` is a convenience script to instantly bring up Pyllo IDE with 
`hellodock` plugin loaded.

Now you can see a new dock pane docked in main window. Click it out!

![messagebox](data/1686630107639.jpg)

## Check the plugins installed

Open the `Register plugins...` window in the `Help` menu and you will see all 
registered plugins. You can also disable these plugins and restart without
them.

![plugin tools](data/1686631106584.jpg)


