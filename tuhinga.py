#!/usr/bin/env python3

SETTING_INPUT_INDENT = 2
SETTING_OUTPUT_INDENT = 2


class Parser:
    def __init__(self):
        '''Handle args and initialize instance variables'''
        self.latest_indentlvl = 0
        self.lineno = 0
        self.current_indentlvl = 0
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
                        / SETTING_INPUT_INDENT)
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
                _id = identifier[identifier.find('#') + 1:identifier.find('.')]
            else:
                _id = identifier[identifier.find('#') + 1:]
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
                args.append(i[1:])
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
        if indentlvl < self.current_indentlvl:
            self._closeNodes(indentlvl)

        self.parsed[indentlvl] = data
        self.latest_indentlvl = indentlvl
        self.nodes.append((1, data))
        self.current_indentlvl = indentlvl

    def _closeNodes(self, indentlvl):
        self.parsed[self.latest_indentlvl] = None
        for i in range(99, indentlvl - 1, -1):
            if self.parsed[i]:
                self.nodes.append((0, self.parsed[i]))
                self.parsed[i] = None


class Lexer:
    output = ''

    def __init__(self, parser):
        n = 0
        for node in parser.nodes:
            if node[0] == 1:
                next_lvl = parser.nodes[n + 1][1]['indentlvl']
                self.handleStartTag(data=node[1], next_lvl=next_lvl)
            elif node[0] == 0:
                self.handleEndTag(data=node[1])
            n += 1

    def handleStartTag(self, data, next_lvl):
        if data['element'] == 'html5':
            self.add(data['indentlvl'], '<!doctype html>\n<html>')
            return self

        t = '<' + data['element']
        t += ' id="{}"'.format(data['id']) if data['id'] else ''

        if data['class']:
            t += ' class="{}'.format(' '.join(data['class']))

        for a in data['arguments']:
            arg = a.split('=')
            t += ' {}="{}"'.format(arg[0], arg[1])

        t += '>'

        if data['content']:
            # properly align content depending on children nodes
            if data['indentlvl'] >= next_lvl:
                t += data['content']
            else:
                t += '\n{}{}'.format(
                    ((' ' * SETTING_OUTPUT_INDENT) * next_lvl), data['content']
                )

        # close tag if node has no children nodes
        if data['indentlvl'] >= next_lvl:
            t += '</{}>'.format(data['element'])

        self.add(data['indentlvl'], t)

    def handleEndTag(self, data):
        if data['element'] == 'html5':
            self.add(data['indentlvl'], '</html>')
            return self

        self.add(data['indentlvl'], '</{}>'.format(data['element']))

    def add(self, indentlvl, contents):
        self.output += ((' ' * SETTING_OUTPUT_INDENT)
                        * indentlvl) + contents + '\n'


if __name__ == '__main__':
    p = Parser()
    p.file('testdocument.tuhinga')

    # for i in p.nodes:
    #     print(i)

    lexer = Lexer(p)
    print(lexer.output)
