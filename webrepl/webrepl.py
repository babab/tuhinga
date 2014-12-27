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


from bottle import response, route, run, static_file, template

import tuhinga


TEMPLATE_DOC = '''html5
  head
    meta :charset=utf-8
    meta :name=viewport device-width, initial-scale=1.0
  body
    .container
      h1.page-header tuhinga webREPL
      small version 0.1.0
'''


@route('/')
def index():
    '''Frontend view: convert tuhinga to html and pass as bottle template'''
    tpl = tuhinga.file('webrepl.tpl.tuh')
    html = tuhinga.string(TEMPLATE_DOC)
    response.content_type = 'text/html; charset=utf-8'
    return template(tpl, initial_doc=TEMPLATE_DOC, initial_html=html)


@route('/api')
def api():
    '''Backend view: convert POST input to html'''
    response.content_type = 'text/html; charset=utf-8'
    return template(tuhinga.file('examples/webrepl.tpl.tuh'))


@route('/source')
def source():
    '''Frontend view: display tuhinga source code'''
    with open('webrepl.tpl.tuh') as f:
        code = f.read()

    response.content_type = 'text/plain; charset=utf-8'
    return code


@route('/webrepl.js')
def script():
    return static_file('webrepl.js', root='.')

run(host='localhost', port=8080)
