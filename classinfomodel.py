class DataModel:
    def __init__(self):
        self.header = {
            'class': ['name', 'parent'],
            'method': ['name', 'parameter', 'return'],
            'variable': ['name', 'type', 'initial type']
        }

        self.data = {ele: [[''] * len(h)] for ele, h in self.header.items()}
        print('DataModel', self.data)

    def add(self, ele):
        new_datum = [''] * len(self.header[ele])
        self.data[ele].append(new_datum)

    def remove(self, element, row):
        del self.data[element][row]
