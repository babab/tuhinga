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


from bottle import post, response, request, route, run, template

import tuhinga

frontend = '''; Tuhinga webREPL template for bottle
; Copyright (c) 2014 Benjamin Althues <benjamin@babab.nl>

html5
  head
    meta :charset=utf-8
    meta :name=viewport device-width, initial-scale=1.0
    title Tuhinga webREPL
    css //maxcdn.bootstrapcdn.com/bootswatch/3.3.1/darkly/bootstrap.min.css
    style textarea, pre {font-size: 12px;}
  body
    .container
      h1.page-header tuhinga webREPL
        small version 0.1.0
      ul.list-inline
        li
          p Display:
        li
          a#side-by-side :href=javascript:; side-by-side
        li
          a#full-width :href=javascript:; full-width
      .row
        .col-lg-6
          h2 input
            small tuhinga
          textarea#src.form-control :rows=20 {{ initial_doc }}
        .col-lg-6
          h2 output
            small html
          pre#dest {{ initial_html }}
    .container
      hr
      p.pull-right This page itself is written in tuhinga,
        a :href=/source view the source
      p Copyright &copy; 2014 Benjamin Althues
    js http://code.jquery.com/jquery-2.1.3.min.js
    js /webrepl.js

'''

js = '''
(function() {

    $('#full-width').click(function() {
        $('.col-lg-6').removeClass('col-lg-6').addClass('col-lg-12')
    });
    $('#side-by-side').click(function() {
        $('.col-lg-12').removeClass('col-lg-12').addClass('col-lg-6')
    });

    $('#src').keyup(function() {
        $.post('/api', {'src': $('#src').val()}, function(data) {
            $('#dest').html(data.html);
        });

    });

})();
'''

code = '''; A very minimal example of a document

html5
  head
    meta :charset=utf-8
    meta :name=viewport device-width, initial-scale=1.0
    title Page title
  body
    #main.container
      h1.page-header Page title
        small Page subtitle
    #footer.container
      p Copyright &amp; 2014 Me
'''


@route('/')
def index():
    '''Frontend view: convert tuhinga to html and pass as bottle template'''
    html = tuhinga.string(code)
    tpl = tuhinga.string(frontend)
    return template(tpl, initial_doc=code, initial_html=html)


@post('/api')
def api():
    '''Backend view: convert POST input to html'''
    string = request.forms.get('src')
    return {'html': template('{{ src }}', src=tuhinga.string(string))}


@route('/source')
def source():
    '''Frontend view: display tuhinga source code'''
    response.content_type = 'text/plain; charset=utf-8'
    return code


@route('/webrepl.js')
def script():
    return js

if __name__ == '__main__':
    run(host='localhost', port=8080)
