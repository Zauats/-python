import json, urllib

class contriesIteration():

    def __init__(self, write_file, json_file):
        self.index = -1
        self.write_file = open(write_file, "w", encoding="UTF-8")
        with open(json_file, "r", encoding="UTF-8") as f:
            self.file = json.loads(f.read())


    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        url = "https://ru.wikipedia.org/wiki/" + self.file[self.index]["name"]["official"].replace(" ", "_")
        print(url)
        self.write_file.write(url + " - " + self.file[self.index]["name"]["official"] + "\n")
        try:
            self.file[self.index + 1]
        except:
            self.write_file.close()
            raise StopIteration
        return url


my_class = contriesIteration()
j = 0
for i in my_class:
    j +=1
    print(j)