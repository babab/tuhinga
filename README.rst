Tuhinga
==============================================================================

.. image:: https://travis-ci.org/babab/tuhinga.svg?branch=master
    :target: https://travis-ci.org/babab/tuhinga

Tuhinga is a minimalistic markup language that translates to XML/HTML.
It can help you reduce typing and quicken the editing process of HTML
pages. It may remind you a little of HAML since it shares a few common
concepts, but it has different goals. HAML is essentially a template
language, while tuhinga is a tiny markup language primarily aimed to be
just a precursor for XML/HTML documents.

The only true goal of Tuhinga is **conciseness**. And this is also
where it stands out against other solutions. It is the prettiest.
This means it may never support XML and HTML for the full 100%, since
that would cause the need for a much more expansive syntax. Use it if
you think HAML is a good idea, but not beatiful enough. Otherwise I'd
advise to just use HAML, since it is much more mature and has numerous
implementations.

The implementation of Tuhinga is written in Python. Supported Python
versions are 2.7 and 3.2 and later.

- Github: http://github.com/babab/tuhinga
- Bitbucket: http://bitbucket.org/babab/tuhinga


A tuhinga example document
------------------------------------------------------------------------------

An example of a HTML5 (\*.tuh) document::

   ; Comments start with ;

   html5
     head
       meta-charset utf-8
       meta :name=viewport device-width, initial-scale=1.0
       title Page title
     body
       #main.container
         h1.page-header Page title
         .row
           .col-lg-12
             p Paragraph line 1
               :: line 2
               :: line 3
               small line 4
             p
               :: line 1
               :: line 2
       #footer.container
         p.muted Copyright &amp; 2015 Me

After converting to HTML:

.. code-block:: html

   <!doctype html>
   <html>
     <head>
       <meta charset="utf-8">
       <meta name="viewport" content="device-width, initial-scale=1.0">
       <title>Page title</title>
     </head>
     <body>
       <div id="main" class="container">
         <h1 class="page-header">Page title</h1>
         <div class="row">
           <div class="col-lg-12">
             <p>
               Paragraph line 1
               line 2
               line 3
               <small>line 4</small>
             </p>
             <p>
               line 1
               line 2
             </p>
           </div>
         </div>
       </div>
       <div id="footer" class="container">
         <p class="muted">Copyright &amp; 2015 Me</p>
       </div>
     </body>
   </html>


The tuhinga equivalent of any HTML output uses roughly 33% less
characters, and not a single angle bracket.


Using Tuhinga to write XML / HTML5
------------------------------------------------------------------------------

The handling of certain symbols like `js`, `meta`, `input` and other
void elements and the *$content* that follows is done by applying a
set of rules, called a mapping. All other elements are treated with
the default handling of the Lexer (currently there is only a XML/HTML
Lexer).

What follows are the rules that are applied with the default mapping.
You can alter how these mappings work though. This means you can easily
add your own symbols.

Special symbols
###############

- **html5**: sets doctype; is expanded to <!doctype html><html> ... </html>
- **css**: expanded to <link rel="stylesheet" {href="*$content*"}>
- **input**: expanded to <input {value="*$content*"}>
- **input-***: expanded to <input type="*" {value="*$content*"}>
- **js**: an alternative for writing **script-src**
- **link**: expanded to <link {href="*$content*"}>
- **meta**: expanded to <meta {content="*$content*"}>
- **meta-charset**: expanded to <meta charset="*$content*">
- **script-src**: expanded to <script {src="*$content*"}></script>

Recognised as void elements (elements that do not close)
########################################################

area, base, br, col, embed, hr, img, keygen, param, source, track,
input (mapped content), link (mapped content), meta (mapped content),
wbr


Convert tuhinga templates with the python module
------------------------------------------------------------------------------

Tuhinga is distributed as a single module and can be downloaded and
used directly. If you install Tuhinga into your system or
virtualenv, you can use the more convenient **tuh** executable script.
If you use the module, simply replace **tuh** with **./tuhinga.py** in
the instructions below.

Converting a document is simple:

.. code-block:: console

   $ tuh somedocument.tuh > somedocument.html

You can also read from stdinput:

.. code-block:: console

   $ cat somedocument.tuh | tuh > somedocument.html  # passing a file
   $ tuh > somedocument.html # typing a doc directly in the terminal

The Tuhinga module itself has no external dependencies. The Tuhinga
webREPL is distributed independently and requires bottle.


Download and install
--------------------

Tuhinga itself has no external dependencies. If you have pip installed,
you can just:

.. code-block:: console

   # pip install tuhinga

To work with the current development version, do something like this:

.. code-block:: console

   $ git clone git://bitbucket.org/babab/tuhinga.git
   # cd tuhinga
   # python setup.py install


Convert tuhinga templates with the instant webREPL
------------------------------------------------------------------------------

Use the webREPL as an easy way to fiddle around with writing tuhinga
documents or use it as a serious tool to quickly write up your pages. It
will give instant feedback of the output after each keystroke.

The webREPL is written using the bottle Python micro-framework, which is
not a dependency of tuhinga itself. Therefore, you must be sure to have
bottle installed if you wish to use it.

Install bottle (in a virtualenv)
################################

.. code-block:: console

   $ pip install bottle

Run the webREPL
###############

.. code-block:: console

   $ ./tuhinga_webrepl.py

Now you can visit *http://localhost:8080/* and play around.


Syntax file for Vim
------------------------------------------------------------------------------

If you use Vim for your editing, you can install the syntax file to have
pretty syntax highlighting for Tuturu (\*.tuh) documents. It's my first
go at writing a syntax.vim file and it currently has some small bugs,
which should probably be resolved soon.

.. image:: http://i.imgur.com/uqpEpjN.png

Install the tuh.vim syntax file into your .vim folder:

.. code-block:: console

   $ mkdir -p ~/.vim/syntax
   $ cp tuh.vim ~/.vim/syntax

And use it in your Vim buffer with ``:set filetype=tuh``


License
-------

Copyright (c) 2014-2015 Benjamin Althues <benjamin@babab.nl>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
