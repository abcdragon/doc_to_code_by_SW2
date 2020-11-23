class DocToCode:
    def __init__(self, root):
        with open('new_file.py', 'w') as file:
            for obj in root:
                _class = obj['class']
                _class_declare = 'class ' + _class['name']

                if _class['parent']:
                    _class_declare += '(%s)' % _class['parent']

                _class_declare += ':\n'
                file.write(_class_declare)

                value = obj['variable']
                if value['name']:
                    file.write(' ' * 4 + 'def __init__(self):\n')
                    file.write(' ' * 8 + 'self.%s = %s\n' % (value['name'], value['inital value']))
                file.write('\n')

                method = obj['method']
                if not method['name']:
                    file.write('    pass\n\n')

                else:
                    file.write(' ' * 4 + 'def %s(%s):\n' % (method['name'], method['parameter']))
                    file.write(' ' * 8 + 'pass\n')
                file.write('\n\n')


