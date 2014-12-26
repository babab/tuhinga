#!/usr/bin/env python3

SETTING_INDENT_SPACES = 2


class Parser:
    def __init__(self):
        '''Initialize some instance variables'''
        self.data = []
        self.latest_node = 0
        self.lineno = 0
        self.nodelvl = 0
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
        content = line.lstrip().split()

        # Skip empty lines and comment lines
        if not content or (indentlvl == 0 and content[0].startswith('#')):
            return self

        self._registerNode(indentlvl, content[0])

        self.data.append({
            'line': self.lineno,
            'indentlvl': indentlvl,
            'content': content,
        })
        return self

    def close(self):
        '''Close all open nodes'''
        self._closeNodes(0)
        return self

    def _registerNode(self, indentlvl, element):
        if indentlvl < self.nodelvl:
            self._closeNodes(indentlvl)

        self.parsed[indentlvl] = element
        self.latest_node = indentlvl

        print('{}<{}>'.format(
            ((' ' * SETTING_INDENT_SPACES) * indentlvl), element
        ))
        self.nodelvl = indentlvl

    def _closeNodes(self, indentlvl):
        self.parsed[self.latest_node] = None
        for i in range(99, indentlvl - 1, -1):
            if self.parsed[i]:
                print('{}</{}>'.format(
                    ((' ' * SETTING_INDENT_SPACES) * i),
                    self.parsed[i]
                ))
                self.parsed[i] = None

if __name__ == '__main__':
    p = Parser()
    p.file('test.htmlx').close()
