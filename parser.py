from html.parser import HTMLParser
import json
import os
import datetime
import time
import string

class BaseMessageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.state = -1
        '''
        States:
         0: Thread name
         1: New thread name list
         2: Name of sender
         3: Time sent
         4: Message
        '''
        self.active = False
        self.thread_name = ""

    def handle_starttag(self, tag, attrs):
        attrs = {x[0]: x[1] for x in attrs}
        if not 'class' in attrs and not tag in ['h3', 'p', 'div']:
            return
        if tag == 'h3':
            self.state = 0
        elif tag == 'p':
            self.state = 4
        elif attrs['class'] == 'thread':
            self.active = True
            self.state = 1
        elif attrs['class'] == 'user':
            self.state = 2
        elif attrs['class'] == 'meta':
            self.state = 3
        else:
            self.state = -1

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.state = 1

    def handle_data(self, data):
        if not self.active:
            return
        data = data.strip()
        if self.state == 0:
            # Thread name
            thread_name = data[len("Conversation with "):]
            #  print(data)
            self.handle_thread_name(thread_name)
        elif self.state == 1:
            # Thread
            users = data[len("Participants: "):].split(', ')
            users = ['Unknown' if x == '' else x for x in users]
            self.handle_users(users)
        elif self.state == 2:
            # Sender
            if data == '': data = 'Unknown'
            self.handle_sender(data)
        elif self.state == 3:
            # Timestamp
            if data[0] not in string.ascii_uppercase:
                return
            self.handle_timestamp(data)
        else:
            # Message
            self.handle_message(data)
    # You should only need to implement these four (and possibly __init__)
    
    def handle_thread_name(self, timestamp):
        pass

    def handle_timestamp(self, timestamp):
        pass

    def handle_message(self, message):
        pass

    def handle_sender(self, sender):
        pass

    def handle_users(self, users):
        self.users = users

class JSONSaver(BaseMessageParser):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.threads = []
        self.filename = 'json/'

    def handle_thread_name(self, name):
        #  print('thread')
        self.threads.append({
                'users': [],
                'messages': [{}]
            }
        )
        self.threads[-1]['name'] = name
        self.filename += name.replace(' ', '_').lower().replace('/', '_') + '.json'

    def handle_timestamp(self, timestamp):
        #  print('time')
        timestamp = datetime.datetime.strptime(timestamp + "00", "%A, %B %d, %Y at %H:%M%p UTC%z") 
        self.threads[-1]['messages'][-1]['timestamp'] = time.mktime(timestamp.timetuple())

    def handle_message(self, message):
        #  print('message')
        self.threads[-1]['messages'][-1]['message'] = message

    def handle_sender(self, sender):
        #  print('sender')
        if not self.threads[-1]['messages'][0] == {}:
            self.threads[-1]['messages'].append({})
        self.threads[-1]['messages'][-1]['user'] = sender

    def handle_users(self, users):
        #  print('users')
        users.append(self.user)
        self.threads[-1]['users'] = users
    
    def close(self):
        super().close()
        if not os.path.exists(self.filename):
            open(self.filename, 'x').close()
        with open(self.filename, 'w') as f:
            json.dump(self.threads, f)
