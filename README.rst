Tuhinga
==============================================================================

Tuhinga is a minimalistic markup language that translates to XML/HTML.
It can help you reduce typing and quicken the editing process of HTML
pages.

A tuhinga example document
------------------------------------------------------------------------------

File: pretty-minimal.tuh::

   ; A pretty minimal example of a document with a form

   html5
     head
       meta :charset=utf-8
       meta :name=viewport device-width, initial-scale=1.0
       css http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css
       js http://code.jquery.com/jquery-2.1.3.min.js
       js /static/my_script.js
       title Please fill out you name
     body
       #main.container
         h1 Please fill out you name
         .row
           .col-lg-6
             form.form
               input.form-control :type=text :placeholder=Name John Doe
               hr
               input.form-control :type=submit Send name
           .col-lg-6
             p Please fill out the form
       #footer.container
         p Copyright &amp; 2014 Me

After converting to HTML::

   <!doctype html>
   <html>
     <head>
       <meta charset="utf-8" />
       <meta name="viewport" content="device-width, initial-scale=1.0" />
       <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" />
       <script src="http://code.jquery.com/jquery-2.1.3.min.js"></script>
       <script src="/static/my_script.js"></script>
       <title>Please fill out you name</title>
     </head>
     <body>
       <div id="main" class="container">
         <h1>Please fill out you name</h1>
         <div class="row">
           <div class="col-lg-6">
             <form class="form">
               <input class="form-control" type="text" placeholder="Name" value="John Doe" />
               <hr />
               <input class="form-control" type="submit" value="Send name" />
             </form>
           </div>
           <div class="col-lg-6">
             <p>Please fill out the form</p>
           </div>
         </div>
       </div>
       <div id="footer" class="container">
         <p>Copyright &amp; 2014 Me</p>
       </div>
     </body>
   </html>

The tuhinga equivalent of the HTML output uses 32% less characters, and
not a single angle bracket.


Using Tuhinga to write XML / HTML5
------------------------------------------------------------------------------

The handling of certain symbols like `js`, `meta`, `link` and 'other'
self-closing elements and the *$content* that follows is done by
applying a set of rules, called a mapping. All other elements are
treated with the default handling of the Lexer (currently there is only
a XML/HTML Lexer).

What follows are the rules that are applied with the default mapping.
You can alter how these mappings work though. This means you can easily
add your own symbols.

special symbols
###############

- **css**: expanded to <link rel="stylesheet" {href="*$content*"} />
- **html5**: expanded to <!doctype html><html> ... </html>
- **input**: expanded to <input {value="*$content*"} />
- **js**: an alternative for writing **script-src**
- **link**: expanded to <link {href="*$content*"} />
- **meta**: expanded to <meta {content="*$content*"} />
- **script-src**: expanded to <script {src="*$content*"}></script>

recognised as single tags
#########################

br, hr, input


license
-------

Copyright (c) 2014 Benjamin Althues <benjamin@babab.nl>

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
