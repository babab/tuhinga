#!/usr/bin/env python3

SETTING_INDENT_SPACES = 2


class Parser:
    def __init__(self, lexer):
        '''Handle args and initialize instance variables'''
        self.lexer = lexer

        self.latest_indentlvl = 0
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
        self.close()
        return self

    def close(self):
        '''Close all open nodes'''
        self._closeNodes(0)
        return self

    def parseLine(self, line):
        '''Parse a single line of tuhinga markup

        Make sure to run close() after the last call to parseLine.'''
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
            'indentlvl': indentlvl,
            'element': element,
            'id': _id,
            'class': _class,
            'arguments': args,
            'content': ' '.join(content),
            'line': self.lineno,
            'splitted': splitted,
        }

        # register node to handle the tree structure
        self._registerNode(indentlvl, data)
        return self

    def _registerNode(self, indentlvl, data):
        if indentlvl < self.nodelvl:
            self._closeNodes(indentlvl)

        self.parsed[indentlvl] = data
        self.latest_indentlvl = indentlvl

        if self.lexer:
            self.lexer.handleStartTag(data)
        self.nodelvl = indentlvl

    def _closeNodes(self, indentlvl):
        self.parsed[self.latest_indentlvl] = None
        for i in range(99, indentlvl - 1, -1):
            if self.parsed[i]:
                if self.lexer:
                    self.lexer.handleEndTag(self.parsed[i])
                self.parsed[i] = None


class Lexer:
    output = ''

    def handleStartTag(self, data):
        if data['element'] == 'html5':
            self.add(data['indentlvl'], '<!doctype html>\n<html>')
        else:
            self.add(data['indentlvl'], '<{}>'.format(data['element']))

    def handleEndTag(self, data):
        if data['element'] == 'html5':
            self.add(data['indentlvl'], '</html>')
        else:
            self.add(data['indentlvl'], '</{}>'.format(data['element']))

    def add(self, indentlvl, contents):
        self.output += ((' ' * SETTING_INDENT_SPACES)
                        * indentlvl) + contents + '\n'


if __name__ == '__main__':
    lexer = Lexer()
    p = Parser(lexer)
    p.file('testdocument.tuhinga')
    print(lexer.output)
