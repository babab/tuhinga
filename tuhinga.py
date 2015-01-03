#!/usr/bin/env python

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

DEFAULT_INPUT_INDENT = 2
'''The standard value of tuhinga's indentation is 2 spaces'''

DEFAULT_OUTPUT_INDENT = 2
'''The output can be set as a negative value to create condensed one liners'''

## Default mapper for LexerXML ###############################################

mapper = {
    'html5': {
        'area': {'v': True},
        'base': {'v': True},
        'br': {'v': True},
        'col': {'v': True},
        'embed': {'v': True},
        'hr': {'v': True},
        'img': {'v': True},
        'keygen': {'v': True},
        'param': {'v': True},
        'source': {'v': True},
        'track': {'v': True},
        'wbr': {'v': True},
        'css': {'v': True, 'e': 'link', 'c': 'href', 'h': 'rel="stylesheet"'},
        'input': {'v': True, 'c': 'value'},
        'input-button': {'v': True, 'e': 'input', 'c': 'value',
                         'h': 'type="button"'},
        'input-checkbox': {'v': True, 'e': 'input', 'c': 'value',
                           'h': 'type="checkbox"'},
        'input-color': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="color"'},
        'input-date': {'v': True, 'e': 'input', 'c': 'value',
                       'h': 'type="date"'},
        'input-datetime': {'v': True, 'e': 'input', 'c': 'value',
                           'h': 'type="datetime"'},
        'input-datetime-local': {'v': True, 'e': 'input', 'c': 'value',
                                 'h': 'type="datetime-local"'},
        'input-email': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="email"'},
        'input-file': {'v': True, 'e': 'input', 'c': 'value',
                       'h': 'type="file"'},
        'input-hidden': {'v': True, 'e': 'input', 'c': 'value',
                         'h': 'type="hidden"'},
        'input-image': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="image"'},
        'input-month': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="month"'},
        'input-number': {'v': True, 'e': 'input', 'c': 'value',
                         'h': 'type="number"'},
        'input-password': {'v': True, 'e': 'input', 'c': 'value',
                           'h': 'type="password"'},
        'input-radio': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="radio"'},
        'input-range': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="range"'},
        'input-reset': {'v': True, 'e': 'input', 'c': 'value',
                        'h': 'type="reset"'},
        'input-search': {'v': True, 'e': 'input', 'c': 'value',
                         'h': 'type="search"'},
        'input-submit': {'v': True, 'e': 'input', 'c': 'value',
                         'h': 'type="submit"'},
        'input-tel': {'v': True, 'e': 'input', 'c': 'value',
                      'h': 'type="tel"'},
        'input-text': {'v': True, 'e': 'input', 'c': 'value',
                       'h': 'type="text"'},
        'input-time': {'v': True, 'e': 'input', 'c': 'value',
                       'h': 'type="time"'},
        'input-url': {'v': True, 'e': 'input', 'c': 'value',
                      'h': 'type="url"'},
        'input-week': {'v': True, 'e': 'input', 'c': 'value',
                       'h': 'type="week"'},
        'js': {'e': 'script', 'c': 'src', 'h': 'type="text/javascript"'},
        'link': {'v': True, 'c': 'href'},
        'meta': {'v': True, 'c': 'content'},
        'meta-charset': {'v': True, 'e': 'meta', 'c': 'charset'},
        'script-src': {'e': 'script', 'c': 'src'},
    },
}
'''Mapping of contents to arguments / list of void elements

Possible keys:
    - 'v': True if void element like <meta>. Default = false
    - 'e': HTML element. Default = <name_of_dict_key>
    - 'c': Content mapping, see below. Default = '>'
    - 'h': Extra html arguments. Default = false

Possible value of content:
    - '>': print contents after start tag (default)
    - '-': strip any contents
    - 'some-string': map any contents to an html argument
'''


## Parser and Lexer objects ##################################################

class LexerError(Exception):
    pass


class Parser:
    '''Parse a tuhinga doc and create nodes to be processed with a lexer'''

    def __init__(self, input_indent=DEFAULT_INPUT_INDENT):
        '''Handle args and initialize instance variables'''
        self.input_indent = input_indent

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
        indentlvl = int((len(line) - len(line.lstrip())) / self.input_indent)
        splitted = line.lstrip().split()

        # Skip empty lines and comment lines
        if not splitted or splitted[0].startswith(';'):
            return self

        # parse element, id and classes
        identifier = splitted[0]
        _id = None
        _class = []

        if '#' in identifier:
            element = identifier[:identifier.find('#')]
            if '.' in identifier:
                _id = identifier[identifier.find('#') + 1:identifier.find('.')]
                _class = identifier.split('.')[1:]
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

        # If a word starts with ':' and is not an argument,
        # it should be escaped '\:'
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

    def __init__(self, parser, output_indent=DEFAULT_OUTPUT_INDENT):
        '''Object init is the only public method'''
        self.output = ''
        self.doctype = 'html5'
        self.output_indent = output_indent

        n = 0
        for node in parser.nodes:
            if node[0] == 1:
                try:
                    next_lvl = parser.nodes[n + 1][1]['indentlvl']
                except IndexError:
                    raise LexerError('Markup Tree Error: parser did not '
                                     'properly close all nodes')
                self._startNode(data=node[1], next_lvl=next_lvl)
            elif node[0] == 0:
                self._endNode(data=node[1])
            n += 1

    def _startNode(self, data, next_lvl):
        out = ''
        is_element = True

        # defaults, possibly overridden by mapping
        element = data['element']
        content_dest = '>'
        extra_args = ''
        void_elem = False

        if data['element'] in mapper[self.doctype].keys():
            # apply mapping
            if 'e' in mapper[self.doctype][data['element']]:
                element = mapper[self.doctype][data['element']]['e']
            if 'v' in mapper[self.doctype][data['element']]:
                void_elem = mapper[self.doctype][data['element']]['v']
            if 'c' in mapper[self.doctype][data['element']]:
                content_dest = mapper[self.doctype][data['element']]['c']
            if 'h' in mapper[self.doctype][data['element']]:
                extra_args = mapper[self.doctype][data['element']]['h']

        # hardcoded special elements
        if element == 'html5':
            # Do not print a newline if output_indent setting <= -1
            newl = '\n' if self.output_indent > -1 else ''
            self._addOutput(
                data['indentlvl'],
                '<!doctype html>{newl}{indent}<html>'.format(
                    newl=newl,
                    indent=((' ' * self.output_indent) * data['indentlvl'])
                )
            )
            return self
        elif element == '::':
            is_element = False

        if is_element:
            out += '<' + element  # Begin start tag
            out += ' id="{}"'.format(data['id']) if data['id'] else ''

            if data['class']:
                out += ' class="{}"'.format(' '.join(data['class']))

            out += ' {}'.format(extra_args) if extra_args else ''
            for a in data['arguments']:
                arg = a.split('=')
                out += ' {}="{}"'.format(arg[0], arg[1])

            # Use content as argument according to mapping
            if data['content'] and content_dest != '>' and content_dest != '-':
                out += ' {}="{}"'.format(content_dest, data['content'])
            out += '>'  # Close start tag

        # Add content, if any.
        # Properly align content depending on children nodes
        if data['content'] and content_dest == '>':
            if data['indentlvl'] >= next_lvl:
                out += data['content']
            else:
                out += '\n{}{}'.format(self._indent(next_lvl), data['content'])

        # close tag if node has no children nodes
        if is_element and not void_elem:
            if data['indentlvl'] >= next_lvl:
                out += '</{}>'.format(element)

        self._addOutput(data['indentlvl'], out)

    def _endNode(self, data):
        if data['element'] == 'html5':
            self._addOutput(data['indentlvl'], '</html>')
            return self

        self._addOutput(data['indentlvl'], '</{}>'.format(data['element']))

    def _indent(self, indentlvl):
        return (' ' * self.output_indent) * indentlvl

    def _addOutput(self, indentlvl, contents):
        # Do not print a newline if output_indent setting <= -1 and
        # unescape any special tokens
        newl = '\n' if self.output_indent > -1 else ''
        contents = contents.replace('\\:', ':')
        self.output += self._indent(indentlvl) + contents + newl


## Shortcut functions ########################################################

def string(string, input_indent=DEFAULT_INPUT_INDENT,
           output_indent=DEFAULT_OUTPUT_INDENT):
    '''Shortcut for parsing, lexing and mapping a document from a string'''
    parser = Parser(input_indent=input_indent).string(string)
    return LexerXML(parser, output_indent=output_indent).output


def file(filelocation, input_indent=DEFAULT_INPUT_INDENT,
         output_indent=DEFAULT_OUTPUT_INDENT):
    '''Shortcut for parsing, lexing and mapping a document from file'''
    parser = Parser(input_indent=input_indent).file(filelocation)
    return LexerXML(parser, output_indent=output_indent).output


def stdin(input_indent=DEFAULT_INPUT_INDENT,
          output_indent=DEFAULT_OUTPUT_INDENT):
    '''Shortcut for parsing, lexing and mapping from stdin/fileinput'''
    parser = Parser(input_indent=input_indent).fileinput()
    return LexerXML(parser, output_indent=output_indent).output

## When invoked as script, read files or stdin ###############################

if __name__ == '__main__':
    # print(file('examples/dev-test.tuh'))
    try:
        print(stdin())
    except KeyboardInterrupt:
        print('Bye')
