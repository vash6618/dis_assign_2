from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, String

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import random


class TransactionService(ServiceBase):
    @rpc(String, String, String, _returns=Iterable(String))
    def pay_using_card(ctx, card_name, card_number, expiry_date):
        """
        @param card_name the name on the card
        @param card_number the number on the card
        @param expiry_date expiry date on the card
        @return transaction status
        """
        res = random.randint(1, 100)
        if res <= 5:
            output = b"Failure"
        else:
            output = b"Success"
        yield output


application = Application([TransactionService], 'transactions.pay.via_card',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8002")
    logging.info("wsdl is at: http://localhost:8002/?wsdl")

    server = make_server('0.0.0.0', 8002, wsgi_application)
    server.serve_forever()