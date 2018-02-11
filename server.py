import socker
import sockerserver
import logging
from termcolor import colored
from openmath import openmath as om, convert as conv

from scscp.client import TimeoutError, CONNECTED
from scscp.server import SCSCPServer
from scscp import scscp

class SCSCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.server.log.info("New connection from %s:%d" % self.client_address)
        self.log = self.server.log.getChild(self.client_address[0])
        self.scscp = SCSCPServer(self.request, self.server.name,
                                     self.server.version, logger=self.log)
        
    def handle(self):
        self.scscp.accept()
        while True:
            try:
                call = self.scscp.wait()
            except TimeoutError:
                continue
            except SCSCPQuit as e:
                self.log.info(e)
                break
            except ConnectionResetError:
                self.log.info('Client closed unexpectedly.')
                break
            except SCSCPProtocolError as e:
                self.log.info('SCSCP protocol error: %s.' % str(e))
                self.log.info('Closing connection.')
                self.scscp.quit()
                break
            self.handle_call(call)

    def handle_call(self, call):
        if (call.type != 'procedure_call'):
            raise SCSCPProtocolError('Bad message from client: %s.' % call.type, om=call.om())
        try:
            head = call.data.elem.name
            self.log.debug('Requested head: %s...' % head)
            
            if call.data.elem.cd == 'scscp2' and head in CD_SCSCP2:
                res = getattr(self, head)(call.data)
            elif call.data.elem.cd == 'singular' and head in CD_SINGULAR:
                #args = [conv.to_python(a) for a in call.data.arguments]
                args = call.data.arguments
                handler = get_handler(head)
                name = makename()
                handler(name, args)
                res = retrieve(name)
            else:
                self.log.debug('...head unknown.')
                return self.scscp.terminated(call.id, om.OMError(
                    om.OMSymbol('unhandled_symbol', cd='error'), [call.data.elem]))

            strlog = str(res)
            print(colored(strlog, "green"))
            self.log.debug('...sending result: %s' % (strlog[:20] + (len(strlog) > 20 and '...')))
            return self.scscp.completed(call.id, res)
        except (AttributeError, IndexError, TypeError) as e:
            traceback.print_exc()
            self.log.debug('...client protocol error.')
            return self.scscp.terminated(call.id, om.OMError(
                om.OMSymbol('unexpected_symbol', cd='error'), [call.data]))
        except Exception as e:
            self.log.exception('Unhandled exception:')
            return self.scscp.terminated(call.id, 'system_specific',
                                             'Unhandled exception %s.' % str(e))

    def get_allowed_heads(self, data):
        return scscp.symbol_set([om.OMSymbol(head, cd='scscp2') for head in CD_SCSCP2]
                                    + [om.OMSymbol(head, cd='singular') for head in CD_SINGULAR],
                                    cdnames=['scscp1'])
    
    def is_allowed_head(self, data):
        head = data.arguments[0]
        return conv.to_openmath((head.cd == 'scscp_trans_1' and head.name in CD_SCSCP_TRANS)
                                    or (head.cd == 'scscp2' and head.name in CD_SCSCP2)
                                    or (head.cd == 'singular'and head.name in CD_SINGULAR)
                                    or head.cd == 'scscp1')

    def get_service_description(self, data):
        return scscp.service_description(self.server.name.decode(),
                                             self.server.version.decode(),
                                             self.server.description)

    def get_signature(self, data):
        print(colored(str(data), "blue"))
        if data.arguments[0].name == "groebner":
            sig_sym = om.OMSymbol("signature", "scscp2")
            func_sym = om.OMSymbol("groebner", "singular")
            zero_sym = om.OMInteger(0)
            infinity_sym = om.OMSymbol("infinity", "nums1")
            all_set_sym = om.OMSymbol("symbol_set_all", "scscp2")
            return om.OMApplication(sig_sym, [func_sym, zero_sym, infinity_sym, all_set_sym])
        return om.OMApplication(om.OMSymbol("symbol_set", "scscp2"), [])

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer, object):
    allow_reuse_address = True
    
    def __init__(self, host='localhost', port=26135,
                     logger=None, name=b'SingularServer', version=b'1.0.1',
                     description='Singular SCSCP Server'):
        super(Server, self).__init__((host, port), SCSCPRequestHandler)
        self.log = logger or logging.getLogger(__name__)
        self.name = name
        self.version = version
        self.description = description
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('singular_server')
    srv = Server(logger=logger)

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
        srv.server_close()
