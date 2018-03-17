from parser import JSONSaver
import progressbar
import os

messages = os.listdir('messages')
bar = progressbar.ProgressBar(max_value=len(messages))
print("Saving...")
i = 0
for filename in messages:
    parser = JSONSaver('YOUR NAME HERE')
    parser.feed(open("messages/" + filename).read())
    parser.close()
    bar.update(i)
    i += 1
