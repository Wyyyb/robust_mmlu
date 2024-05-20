import json


with open("test_data.json", "r") as fi:
    text = fi.read()
    text = text.replace("\textdegree", "°")

with open("test_data_0520", "w") as fo:
    fo.write(json.dumps(text))



