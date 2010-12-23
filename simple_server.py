""" WebSocket test resource.

This code will run a websocket resource on 8080 and reachable at ws://localhost:8080/test.
For compatibility with web-socket-js (a fallback to Flash for browsers that do not yet support
WebSockets) a policy server will also start on port 843.
See: http://github.com/gimite/web-socket-js
"""

__author__ = 'Reza Lotun'


from datetime import datetime

from twisted.internet.protocol import Protocol, Factory
from twisted.web import resource
from twisted.web.static import File
from twisted.internet import task

from websocket import WebSocketHandler, WebSocketSite


class Testhandler(WebSocketHandler):
    def __init__(self, transport):
        WebSocketHandler.__init__(self, transport)
        self.periodic_call = task.LoopingCall(self.send_time)

    def __del__(self):
        print 'Deleting handler'

    def send_time(self):
        # send current time as an ISO8601 string
        data = datetime.utcnow().isoformat().encode('utf8')
        self.transport.write(data)

    def frameReceived(self, frame):
        print 'Peer: ', self.transport.getPeer()
        self.transport.write(frame)
        self.periodic_call.start(0.5)

    def connectionMade(self):
        print 'Connected to client.'
        # here would be a good place to register this specific handler
        # in a dictionary mapping some client identifier (like IPs) against
        # self (this handler object)

    def connectionLost(self, reason):
        print 'Lost connection.'
        self.periodic_call.stop()
        del self.periodic_call
        # here is a good place to deregister this handler object


class FlashSocketPolicy(Protocol):
    """ A simple Flash socket policy server.
    See: http://www.adobe.com/devnet/flashplayer/articles/socket_policy_files.html
    """
    def connectionMade(self):
        policy = '<?xml version="1.0"?><!DOCTYPE cross-domain-policy SYSTEM ' \
                 '"http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">' \
                 '<cross-domain-policy><allow-access-from domain="*" to-ports="*" /></cross-domain-policy>'
        self.transport.write(policy)
        self.transport.loseConnection()



if __name__ == "__main__":
    from twisted.internet import reactor

    # run our websocket server
    # serve index.html from the local directory
    root = File('.')
    site = WebSocketSite(root)
    site.addHandler('/test', Testhandler)
    reactor.listenTCP(8080, site)
    # run policy file server
    factory = Factory()
    factory.protocol = FlashSocketPolicy
    reactor.listenTCP(843, factory)
    reactor.run()

