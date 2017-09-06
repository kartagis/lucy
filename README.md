[![Licence](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hakancelik96/lucy/blob/master/LICENSE.txt)

before
---
- pip install mutagen
- pip install gTTS
- pip install SpeechRecognition
- pip install requests
- pip install socket
- pip install bs4


# you can check or run with talking

 commands that can be executed by the program
 ---------

  use as follow
  -----

  ```python
  from assis import Lucy
  Lucy(Lucy().listen())
  ```
 - and you can speak

  example speak ;
  ------
  + help
    - help me
    - lucy help
    - lucy help me
    - hey lucy help me
    - hey lucy
    - hey lucy help

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

  + you can open drivers of your computer
    - open d driver

  + you can run defined applications on your desktop
    - open google chrome application
    - open media player application

  + lucy can read the text on the screen
    - read this
    - read
    - yes read
    - yes read this
    - yeah read

  + lucy can open or run on the screen
    - open 3
    - open 5


# you can check with commands instead of talking

example ;
 ------
```python

from assis import Lucy,Search

while True:
    Lucy(Lucy().listen())

# or

Lucy("open d drivers")
Lucy("search folder name python")
Lucy("search drivers")
Lucy("search file name django")
Lucy("open chrome applications")
Lucy("search on web face")
Lucy("search on web python programming")

Search("search driver")
Search("search folder name python")
Search("search file name python")
Search("search all folder")

Lucy().talk("hello everyone")

Lucy().talk("hello everyone",sleep = False)

data = Lucy().listen("can i help yoo ?")

data = Lucy().listen()

# to read text on the screen

read = Lucy().read("read this messages .")
# before print(read this messages)
# and
# if it says yes read this
# after
# lucy talk = read this messages and return this data
# does not say yes read this and return this data


 ```
