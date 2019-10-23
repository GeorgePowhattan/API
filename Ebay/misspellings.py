class Misspellings:
    
    # string -> tsring, srting, stirng
    def rotation(self, item):
        variation = []
        for i in range(0, len(item)-1):
            variation.append(item[0:i] + item[i:i+2][::-1] + item[i+2:])
        return variation

    # sring, sting, strng 
    def missing(self, item):
        variation = []
        for i in range(0, len(item)-1):
            variation.append(item.replace(item[i],''))
        return variation

    # sttring, strring, striing
    def adding(self, item):
        variation = []
        for i in range(0, len(item)-1):
            variation.append(item.replace(item[i],item[i]*2))
        return variation

    # dtring, aring        
    def fat_fingers(self, item):
        pass     # neighbouring keys - to be implemented
             
    def misspelling(self, item):
        search_term = item
        search_term += ',' + ','.join(word for word in self.rotation(item))
        search_term += ',' + ','.join(word for word in self.missing(item))
        search_term += ',' + ','.join(word for word in self.adding(item))
        return search_term
