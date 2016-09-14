import logging
import sys

from sqlalchemy import or_

import ckan.plugins as p

REQUESTS_HEADER = {'content-type': 'application/json',
                   'User-Agent': 'ckanext-ksext commands'}


class CkanApiError(Exception):
    pass


class KsextCommand(p.toolkit.CkanCommand):

    summary = __doc__.split('\n')[0]
    usage = __doc__
    min_args = 0

    def __init__(self, name):
        super(KsextCommand, self).__init__(name)
        #self.parser.add_option('-q', '--queue',
        #                       action='store',
        #                       dest='queue',
        #                       help='Send to a particular queue')

    def command(self):
        """
        Parse command line arguments and call appropriate method.
        """
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print KsextCommand.__doc__
            return

        cmd = self.args[0]
        self._load_config()

        # Now we can import ckan and create logger, knowing that loggers
        # won't get disabled
        self.log = logging.getLogger('ckanext.ksext')

        if cmd == 'test':
            self.test()
        else:
            self.log.error('Command "%s" not recognized' % (cmd,))

    def test(self):
        print 'Before test:'
        print 'After test:'
