class DocToCode:
    def __init__(self, file_path, root):
        tab = lambda w: ' ' * 4 * w

        with open(file_path + '.py', 'w') as file:
            for obj in root:
                _class = obj.data['class'][0]
                _class_declare = 'class ' + _class[0]

                if _class[1]:
                    _class_declare += '(%s)' % _class[1]

                _class_declare += ':\n'
                file.write(_class_declare)

                _variable = obj.data['variable']
                _variable_declare = tab(1) + 'def __init__(self):\n'

                for var_info in _variable:
                    if var_info[0]:
                        _variable_declare += tab(2) + 'self.%s = ' % var_info[0]
                        _variable_declare += ("'%s'\n" if var_info[1] == 'str' else '%s') % var_info[2]

                if '=' not in _variable_declare:
                    _variable_declare += tab(2) + 'pass\n\n'

                file.write(_variable_declare)

                _method = obj.data['method']
                _method_declare = ''
                for method_info in _method:
                    if method_info[0]:
                        _method_declare += tab(1) + 'def %s(self' % method_info[0]
                        if method_info[1]:
                            _method_declare += ', %s' % method_info[1]

                        _method_declare += '):\n%spass\n\n' % tab(2)

                file.write(_method_declare + '\n')
