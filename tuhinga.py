#!/usr/bin/env python3

# Copyright (c) 2014 Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import fileinput

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2014  Benjamin Althues"
__version_info__ = (0, 1, 0, 'alpha', 0)
__version__ = '0.1.0'

## Setting defaults ##########################################################

SETTING_INPUT_INDENT = 2
SETTING_OUTPUT_INDENT = 2

## Default mapper for lexerXML ###############################################

mapper = {
    'html5': {

        'br': {'single': True, 'element': 'br', 'content': '-'},
        'input': {'single': True, 'element': 'input', 'content': 'value'},
        # js: alternative for script-src
        'js': {'single': False, 'element': 'script', 'content': 'src'},
        'meta': {'single': True, 'element': 'meta', 'content': 'content'},
        'link': {'single': True, 'element': 'link', 'content': 'href'},
        'script-src': {'single': False, 'element': 'script', 'content': 'src'},

    },
}
'''List of single tags and mapping of contents to arguments

Possible value of content:
    - '>': print contents after start tag (default)
    - '-': strip contents if any
    - 'some-string': map any contents to an html argument
'''


## Parser and Lexer objects ##################################################

class Parser:
    '''Parse a tuhinga doc and create nodes to be processed with a lexer'''

    def __init__(self):
        '''Handle args and initialize instance variables'''
        self.latest_indentlvl = 0
        self.lineno = 0
        self.current_indentlvl = 0
        self.nodes = []
        self.parsed = []

        for i in range(0, 100):
            self.parsed.append(None)

    def string(self, string):
        '''Parse a complete tuhinga document as string'''
        for line in string.split('\n'):
            self.parseLine(line)
        return self.close()

    def file(self, filename):
        '''Parse a complete tuhinga document by filename'''
        with open(filename) as f:
            for line in f:
                self.parseLine(line)
        return self.close()

    def fileinput(self):
        '''Parse stdin or files with the fileinput module'''
        for line in fileinput.input():
            self.parseLine(line)
        return self.close()

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
        if not splitted or (indentlvl == 0 and splitted[0].startswith(';')):
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
        self.nodes.append((1, data))
        self.latest_indentlvl = indentlvl
        self.current_indentlvl = indentlvl

    def _closeNodes(self, indentlvl):
        self.parsed[self.latest_indentlvl] = None
        for i in range(99, indentlvl - 1, -1):
            if self.parsed[i]:
                self.nodes.append((0, self.parsed[i]))
                self.parsed[i] = None


class LexerXML:
    '''Lexical compilation of parsed nodes to XML markup'''

    def __init__(self, parser):
        '''Object init is the only public method'''
        self.output = ''
        self.doctype = 'html5'

        n = 0
        for node in parser.nodes:
            if node[0] == 1:
                try:
                    next_lvl = parser.nodes[n + 1][1]['indentlvl']
                except IndexError:
                    raise Exception('Markup Tree Error: parser did not '
                                    'properly close all nodes')
                self._startNode(data=node[1], next_lvl=next_lvl)
            elif node[0] == 0:
                self._endNode(data=node[1])
            n += 1

    def _startNode(self, data, next_lvl):
        if data['element'] in mapper[self.doctype].keys():
            element = mapper[self.doctype][data['element']]['element']
            single = mapper[self.doctype][data['element']]['single']
            content_dest = mapper[self.doctype][data['element']]['content']
        else:
            element = data['element']
            single = False
            content_dest = '>'

        if element == 'html5':
            self._addOutput(
                data['indentlvl'],
                '<!doctype html>\n{}<html>'.format(
                    ((' ' * SETTING_OUTPUT_INDENT) * data['indentlvl'])
                )
            )
            return self

        t = '<' + element
        t += ' id="{}"'.format(data['id']) if data['id'] else ''

        if data['class']:
            t += ' class="{}"'.format(' '.join(data['class']))

        for a in data['arguments']:
            arg = a.split('=')
            t += ' {}="{}"'.format(arg[0], arg[1])

        # Use content as argument according to mapping
        if data['content'] and content_dest != '>' and content_dest != '-':
            t += ' {}="{}"'.format(content_dest, data['content'])

        t += ' />' if single else '>'

        if data['content'] and content_dest == '>':
            # properly align content depending on children nodes
            if data['indentlvl'] >= next_lvl:
                t += data['content']
            else:
                t += '\n{}{}'.format(
                    ((' ' * SETTING_OUTPUT_INDENT) * next_lvl), data['content']
                )

        # close tag if node has no children nodes
        if not single:
            if data['indentlvl'] >= next_lvl:
                t += '</{}>'.format(element)

        self._addOutput(data['indentlvl'], t)

    def _endNode(self, data):
        if data['element'] == 'html5':
            self._addOutput(data['indentlvl'], '</html>')
            return self

        self._addOutput(data['indentlvl'], '</{}>'.format(data['element']))

    def _addOutput(self, indentlvl, contents):
        self.output += ((' ' * SETTING_OUTPUT_INDENT)
                        * indentlvl) + contents + '\n'


## Shortcut functions ########################################################

def string(string):
    '''Shortcut for parsing, lexing and mapping a document from a string'''
    return LexerXML(Parser().string(string)).output


def file(filelocation):
    '''Shortcut for parsing, lexing and mapping a document from file'''
    return LexerXML(Parser().file(filelocation)).output


def stdin():
    '''Shortcut for parsing, lexing and mapping from stdin/fileinput'''
    return LexerXML(Parser().fileinput()).output

## When invoked as script, read files or stdin ###############################

if __name__ == '__main__':
    # print(file('examples/dev-test.tuh'))
    try:
        print(stdin())
    except KeyboardInterrupt:
        print('Bye')
