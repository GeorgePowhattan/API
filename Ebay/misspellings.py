import misspellings

res = []

# string -> tsring, srting, stirng
def rotation(item):
    for i in range(0, len(item)-1):
        res.append(item[0:i] + item[i:i+2][::-1] + item[i+2:])
    return res

# sring, sting, strng 
def missing(item):
    for i in range(0, len(item)-1):
        res.append(item.replace(item[i],''))
    return res

# sttring, strring, striing
def adding(item):
    for i in range(0, len(item)-1):
        res.append(item.replace(item[i],item[i]*2))
    return res

# dtring, aring        
def fat_fingers(item):
    for i in range(0, len(item)-1):
        res.append()
    return res

def misspelling(item):
    rotation(item)
    missing(item)
    adding(item)
    #fat_fingers(item)
    return res

a = 'string'

print(misspelling(a))
