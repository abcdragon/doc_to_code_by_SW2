class DataModel:
    def __init__(self):
        self.header = {
            'class': ['name', 'parent'],
            'method': ['name', 'parameter', 'return'],
            'variable': ['name', 'type', 'initial value']
        }

        self.data = {'class': [['', '']], 'method': [], 'variable': []}

    def add(self, ele):
        new_datum = [''] * len(self.header[ele])
        if ele == 'variable':
            new_datum[1] = 'str'

        self.data[ele].append(new_datum)

    def remove(self, element, row):
        del self.data[element][row]
