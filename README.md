# Facebook Messages Parser
A module that parses and converts Facebook message data dumps

## Usage
The `messages` directory (containing the HTML files that Facebook gives you) needs to be in the same directory as `save.py`.

Change the `'YOUR NAME HERE'` in `save.py` to your name, and then:

```bash
$ python save.py
```

## Extending
The BaseMessageParser can be extended to convert/save messages in whatever format you like. The methods you would need to extend are as follows:

- `handle_thread_name(self, name)`
  - `name` is the name of the thread being parsed.
- `handle_timestamp(self, timestamp)`
  - `timestamp` is a datetime string representing when a message was sent.
  - The python `datetime.datetime.strptime()` format is something like `"%A, %B %d, %Y at %H:%M%p UTC%z"`.
- `handle_message(self, message)`
  - `message` is the contents of the message sent.
- `handle_sender(self, sender)`
  - `sender` is the full name of the sender of the message.
- `handle_users(self, users)`
  - `users` is a list of members currently in the thread.
  - Note that a thread's current user list does not include participants who have previously left.
