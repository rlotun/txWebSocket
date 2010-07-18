Twisted WebSocket Server
========================

To run:

    $ sudo python simple_server.py

In your browser go to http://localhost:8080.

N.B.: Why sudo? It's because the simple server hosts a flash socket policy file on port
843. This is optional, of course.

Notes
=====

This code is based off the associated branch for
http://twistedmatrix.com/trac/ticket/4173, and includes support for the new
`"hixie-76"` handshake (http://www.whatwg.org/specs/web-socket-protocol/) which
is the latest draft as of June 17, 2010.

The difference between this and what may actually be included in Twisted is
that this version contains definite backwards-support for `hixie-75`, and will
track the latest standard as fast as I can implement it. That means that this
server should work with Chrome 5, Safari 5 and the latest development version
of Chrome 6.

If using browsers that do *not* support WebSockets, consider using a fallabck
implementation to Flash, as seen in http://github.com/gimite/web-socket-js. The
bundled `test_server.py` will also start a simple Flash Socket Policy server
(see http://www.adobe.com/devnet/flashplayer/articles/socket_policy_files.html)
and should be immediately usable with `web-socket-js`.

