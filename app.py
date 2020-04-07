from gevent import monkey
monkey.patch_all(subprocess=False, thread=False, socket=False)
from gevent.pywsgi import WSGIServer
from service import app

# Internal packages:
from logger_init import get_logger

if __name__ == '__main__':
    logger = get_logger()
    server = WSGIServer(('0.0.0.0', 8080), application=app)
    logger.info("Starting server...")
    server.serve_forever()
