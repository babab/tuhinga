#!/usr/bin/env python3

SETTING_INDENT_SPACES = 2


class Parser:
    def __init__(self, debug=False):
        '''Handle args and initialize instance variables'''
        self.debug = debug

        self.latest_node = 0
        self.lineno = 0
        self.nodelvl = 0
        self.nodes = []
        self.parsed = []

        for i in range(0, 100):
            self.parsed.append(None)

    def file(self, filename):
        '''Parse a file, this will simply call parseLine() for each line'''
        with open(filename) as f:
            for line in f:
                self.parseLine(line)
        return self

    def parseLine(self, line):
        '''Parse a single line'''
        self.lineno += 1
        indentlvl = int((len(line) - len(line.lstrip()))
                        / SETTING_INDENT_SPACES)
        splitted = line.lstrip().split()

        # Skip empty lines and comment lines
        if not splitted or (indentlvl == 0 and splitted[0].startswith('#')):
            return self

        # parse element, id and classes
        identifier = splitted[0]
        _id = None
        _class = []

        if '#' in identifier:
            element = identifier[:identifier.find('#')]
            if '.' in identifier:
                _id = identifier[identifier.find('#'):identifier.find('.')]
            else:
                _id = identifier[identifier.find('#'):]
        elif '.' in identifier:
            element = identifier[:identifier.find('.')]
            _class = identifier.split('.')[1:]
        else:
            element = identifier

        if identifier.startswith('#') or identifier.startswith('.'):
            element = 'div'

        # parse content and arguments
        remainder = splitted[1:]
        content = []
        args = []

        for i in remainder:
            if i.startswith(':'):
                args.append(i)
            else:
                content.append(i)

        data = {
            # 'line': self.lineno,
            # 'indentlvl': indentlvl,
            # 'splitted': splitted,

            'type': 'open',
            'element': element,
            'id': _id,
            'class': _class,
            'arguments': args,
            'content': ' '.join(content),
        }

        # register node to handle the tree structure
        self._registerNode(indentlvl, data)
        return self

    def close(self):
        '''Close all open nodes'''
        self._closeNodes(0)
        return self

    def _registerNode(self, indentlvl, data):
        if indentlvl < self.nodelvl:
            self._closeNodes(indentlvl)

        self.parsed[indentlvl] = data
        self.latest_node = indentlvl

        if self.debug:
            print('{}<{}>'.format(
                ((' ' * SETTING_INDENT_SPACES) * indentlvl), data['element']
            ))
        self.nodelvl = indentlvl

    def _closeNodes(self, indentlvl):
        self.parsed[self.latest_node] = None
        for i in range(99, indentlvl - 1, -1):
            if self.parsed[i]:
                if self.debug:
                    print('{}</{}>'.format(
                        ((' ' * SETTING_INDENT_SPACES) * i),
                        self.parsed[i]['element']
                    ))
                self.parsed[i] = None

if __name__ == '__main__':
    p = Parser(debug=True)
    p.file('testdocument.tuhinga').close()
