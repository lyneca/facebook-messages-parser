from parser import JSONSaver

print("Saving...")
parser = JSONSaver('travis.json', 'Luke Tuthill')
parser.feed(open("messages/591.html").read())
parser.close()
