import logging


class Application(object):
    """The base class for the application"""
    def __init__(self, **kwargs):
        super(Application, self).__init__()
        self.name = kwargs.get('name')

    def startup(self):
        """
        Application bootstrap function.
        """
        logging.info('%s: starting up' % self)

    def run(self):
        logging.info('%s: is running' % self)

    def shutdown(self):
        """
        Application shutdown function.
        """
        logging.info('%s: shutting down' % self)

    def execute(self):
        try:
            self.startup()
            self.run()
        except KeyboardInterrupt:
            logging.info('Application %s interrupted by user - exiting...' % str(self))
        except Exception as e:
            logging.error(str(e))
            logging.warning('Application %s threw an exception - aborting...\n' % str(self))
            raise
        finally:
            self.shutdown()
