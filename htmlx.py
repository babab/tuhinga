#!/usr/bin/env python3

SETTING_INDENT_SPACES = 2


class Parser:
    def __init__(self):
        self.data = []
        self.lineno = 0
        self.nodelvl = 0
        self.nodes = []
        self.latest_node = 0

        for i in range(0, 100):
            self.nodes.append(None)

    def file(self, filename):
        with open(filename) as f:
            for line in f:
                self.parseLine(line)

    def parseLine(self, line):
        self.lineno += 1
        indentlvl = int((len(line) - len(line.lstrip()))
                        / SETTING_INDENT_SPACES)
        stripped = line.lstrip().split()

        # Skip empty lines and comment lines
        if not stripped or (indentlvl == 0 and stripped[0].startswith('#')):
            return self

        self.registerNode(indentlvl, stripped[0])

        self.data.append({
            'line': self.lineno,
            'indentlvl': indentlvl,
            'stripped': stripped,
        })

    def registerNode(self, indentlvl, element):
        if indentlvl < self.nodelvl:
            self.nodes[self.latest_node] = None

            for i in range(99, indentlvl - 1, -1):
                if self.nodes[i]:
                    print('{}</{}>'.format(
                        ((' ' * SETTING_INDENT_SPACES) * i),
                        self.nodes[i]
                    ))
                    self.nodes[i] = None

        self.nodes[indentlvl] = element
        self.latest_node = indentlvl

        print('{}<{}>'.format(
            ((' ' * SETTING_INDENT_SPACES) * indentlvl), element
        ))
        self.nodelvl = indentlvl

if __name__ == '__main__':
    # import yaml

    p = Parser()
    p.file('test.htmlx')
    print(p.nodes)
    # print(yaml.dump(p.data))
