class Misspellings:

    def __init__(self, item):
        
    # string -> tsring, srting, stirng
    def rotation(self, item):
        res = []
        for i in range(0, len(item)-1):
            res.append(item[0:i] + item[i:i+2][::-1] + item[i+2:])
        return res

    # sring, sting, strng 
    def missing(self, item):
        res = []
        for i in range(0, len(item)-1):
            res.append(item.replace(item[i],''))
        return res

    # sttring, strring, striing
    def adding(self, item):
        res = []
        for i in range(0, len(item)-1):
            res.append(item.replace(item[i],item[i]*2))
        return res

    # dtring, aring        
    def fat_fingers(self, item):
        res = []
        for i in range(0, len(item)-1):
            res.append()
        return res

    def misspelling(self, item):
        res = []
        self.rotation(item)
        self.missing(item)
        self.adding(item)
        #fat_fingers(item)
        return res

string = Misspellings()

print(string.misspellings('string'))