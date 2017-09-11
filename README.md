[![Licence](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hakancelik96/Luo/blob/master/LICENSE.txt)

before
---
[install requirements.txt](https://github.com/TheLuoProject/Luo/blob/master/requirements.txt)


# you can check or run by talking

 commands that can be executed by the program
 ---------

  use as follows
  -----

  ```python
  from assis import Luo
  Luo(Luo().listen())
  ```
 - and you can speak

  example speak ;
  ------
  + help
    - help
    - help me

  + you can learn the time
    - what time is it
    - what time
    - time

  + you can search
    - search drivers #to find the all drivers from pc
    - search folder name new file
    - search all folder # to find the all folder from pc
    - search file name readme
    - search on web python

  + Luo can read the text on the screen
    - read this
    - read
    - yes read
    - yes read this
    - yeah read

if os.name == "nt": # you can run this commands

  + you can open drivers of your computer
    - open d driver

  + you can run defined applications on your desktop
    - open google chrome application
    - open media player application

  + Luo can open or run on the screen
    - open 3
    - open 5


# you can check with commands instead of talking

example ;
 ------
```python

from assis import Luo,Search
import os
while True:
    Luo(Luo().listen())
# or

Luo("open d drivers")
Luo("search folder name python")
Luo("search drivers")
Luo("search file name django")
Luo("search on web face")
Luo("search on web python programming")
Search("search driver")
Search("search all folder")
Luo().talk("hello everyone")
data = Luo().listen("can i help yoo ?")
data = Luo().listen()
if os.name == "nt":
  Luo("open chrome applications")
# to read text on the screen
read = Luo().read("read this messages .")
# before print(read this messages)
# and
# if it says yes read this
# after
# Luo talk = read this messages and return this data
# does not say yes read this and return this data


 ```
