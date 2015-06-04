# Copyright (c) 2014-2015 Benjamin Althues <benjamin@babab.nl>
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

from nose.tools import eq_

import tuhinga


def test_shortcut_string():
    html = tuhinga.string('html5\n  head\n')
    eq_(html, '<!doctype html>\n<html>\n  <head></head>\n</html>\n')


def test_shortcut_string_args():
    html = tuhinga.string('html5\n   head\n', input_indent=3, output_indent=8)
    eq_(html, '<!doctype html>\n<html>\n        <head></head>\n</html>\n')


def test_mapping():
    html = tuhinga.string('html5\n  body\n    input-checkbox test\n')
    comp = ('<!doctype html>\n<html>\n  <body>\n'
            '    <input type="checkbox" value="test">\n'
            '  </body>\n</html>\n')
    eq_(html, comp)


def test_multiline_content():
    html = tuhinga.string('html5\n  body\n'
                          '    :: some test content\n'
                          '    :: some more test content')
    comp = ('<!doctype html>\n<html>\n  <body>\n'
            '    some test content\n'
            '    some more test content\n'
            '  </body>\n</html>\n')
    eq_(html, comp)
