class DataModel:
    def __init__(self):
        self.header = {
            'class': ['name', 'parent'],
            'method': ['name', 'parameter', 'return'],
            'variable': ['name', 'type', 'initial type']
        }

        self.data = {ele: [[''] * len(h)] for ele, h in self.header.items()}
        self.data['variable'][0][1] = 'str'

    def add(self, ele):
        new_datum = [''] * len(self.header[ele])
        if ele == 'variable':
            new_datum[1] = 'str'

        self.data[ele].append(new_datum)

    def remove(self, element, row):
        del self.data[element][row]
