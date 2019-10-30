import logging
from myemail import webEmail

logging.basicConfig(level=logging.DEBUG)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication


class HelloWorldService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def send_email(self, url, body):
        a = webEmail()
        a, b = a.sendEmail(url, 'title', body, None)
        print(a, b)


application = Application([HelloWorldService],
                          tns='spyne.examples.hello',
                          in_protocol=HttpRpc(validator='soft'),
                          out_protocol=JsonDocument()
                          )
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('localhost', 8000, wsgi_app)
    server.serve_forever()
