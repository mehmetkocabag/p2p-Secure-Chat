***Usage:***

pip install pycryptodome

1. Open p2pChatAppPy folder in a code editor and RUN "main.py" or run modules on their own.
(for debug as responder and initiator depends on other modules)

2. You will be asked to state you username and broadcast will start. (Along with discovery and responder)

3. You can then use users, chat or history.

4. If you intend to run it on a single device, send a message to your own username you will receive the message and you can 
also see both sent/received in history.

***Known Limitations:***

1. If you run the app on a single device it will not notify for "your own username" is online. Intentionally wanted to not get 
notified by own status. But you can see your name and state if you list users.

2. If you run the app on a single device it will take 8 seconds after you type your username to discover itself. 
This means if you immediately try to chat with yourself, app will print "user not found". 
Just use chat again or let the app run for 8 seconds after choosing name. 
You can see if it discovered itself in users list (away/online).

3. If you run the app on a single device after stating your username and if you immediately type users you will see the users 
from the latest instance the app was run. But after 8 seconds it will get updated. If there is another device 
running the app on the same network it will not take 8 seconds to discover that one.

4.Do not use space on your username.