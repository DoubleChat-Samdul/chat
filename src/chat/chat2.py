# src/chat.py

from kafka import KafkaProducer, KafkaConsumer
from json import loads, dumps
import threading

import curses

# screens
stdscr = curses.initscr() 
stdscr.keypad(True)

# dimensions
height, width = stdscr.getmaxyx()
lowerwin_height = 3
lowerwin_y = height - lowerwin_height
lowerwin_x = 0

# windows
upperwin = stdscr.subwin(height - lowerwin_height, width, 0, 0)
lowerwin = stdscr.subwin(lowerwin_height, width, lowerwin_y, lowerwin_x)

# enable scrolling
upperwin.scrollok(True)
lowerwin.scrollok(True)

stdscr.clear()

lowerwin.addstr(0, 0, "Input chatroom name: ")
chatroom = lowerwin.getstr(0, 20, 70).decode('utf-8')
lowerwin.addstr(1, 0, "Input username: ")
username = lowerwin.getstr(1, 20, 70).decode('utf-8')

lowerwin.clear()
lowerwin.refresh()

upperwin.addstr(0, 0, f"[INFO] Initializing chatroom [{chatroom}] for user [{username}]...\n")
upperwin.addstr(1, 0, "[INFO] Initialize complete! Enjoy chatting :)\n\n")
upperwin.refresh()

def create_data(username, message, end):
    return {'sender': username, 'message': message, 'end': end}

# SENDER
def pchat(chatroom, username, lowerwin, upperwin):
    sender = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        # bootstrap_servers = ['ec2-43-203-182-252.ap-northeast-2.compute.amazonaws.com:9092'],
        value_serializer = lambda x: dumps(x).encode('utf-8'),
    )

    try:
        initial_msg = f"User [{username}] has entered the chat!"
        end = False

        data = create_data(username, initial_msg, end)
        sender.send(chatroom, data)
        sender.flush()        

        while True:
            lowerwin.clear()
            lowerwin.addstr(0, 0, f"{username}: ")
            lowerwin.refresh()

            message = lowerwin.getstr(0, len(f"{username}: "), 70).decode('utf-8')

            if message == 'exit':
                message = f"User [{username}] has exited the chatroom."
                end = True

            data = {'sender': username, 'message': message, 'end': end}       
            sender.send(chatroom, value=data)
            sender.flush()

            if end:
                upperwin.addstr(f"\nExiting chat...\n")
                return    

    except KeyboardInterrupt:
        upperwin.addstr("Encountered keyboard interrupt. Finishing chat...")
        upperwin.refresh()
        return

    
# RECEIVER
def cchat(chatroom, username, upperwin):
    receiver = KafkaConsumer(
        chatroom,
        bootstrap_servers = ['localhost:9092'],
        # bootstrap_servers = ['ec2-43-203-182-252.ap-northeast-2.compute.amazonaws.com:9092'],
        enable_auto_commit = True,
        value_deserializer = lambda x: loads(x.decode('utf-8'))
    )

    try:
        for message in receiver:
            data = message.value

            if data['end'] == True:
                # someone not me has exited
                if data['sender'] != username:
                    upperwin.addstr(f"User {data['sender']} has exited the chat.\n")
                    upperwin.addstr("Type in 'exit' to also finish the chat.\n")
                    upperwin.refresh()

                # I'm exiting!! finish thread
                else:
                    return

            else:
                upperwin.addstr(f"[{data['sender']}]: {data['message']}\n")
                upperwin.refresh()

            if upperwin.getyx()[0] >= upperwin.getmaxyx()[0] -1:
                upperwin.scroll(1)
                upperwin.refresh()

    except KeyboardInterrupt:
        upperwin.refresh()("Exiting chat...")
        return

# Threading

thread_1 = threading.Thread(target = pchat, args = (chatroom, username, lowerwin, upperwin))
thread_2 = threading.Thread(target = cchat, args = (chatroom, username, upperwin))

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()
