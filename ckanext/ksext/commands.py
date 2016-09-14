import logging
import sys

from sqlalchemy import or_

import ckan.plugins as p

REQUESTS_HEADER = {'content-type': 'application/json',
                   'User-Agent': 'ckanext-ksext commands'}


class CkanApiError(Exception):
    pass


class KsextCommand(p.toolkit.CkanCommand):
    '''
    ksext doc content.
    '''

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

        if cmd == 'ckidle':
            self.ckidle()
        else:
            self.log.error('Command "%s" not recognized' % (cmd,))

    def ckidle(self):
        from ckan import model
        #print 'Before test:'
        sql = '''
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname in ('ckan_default','datastore_default')
    AND pid <> pg_backend_pid()
    AND state in ('idle', 'idle in transaction', 'idle in transaction (aborted)', 'disabled')
    AND current_timestamp - state_change > interval '5 minutes';
        '''
        model.meta.engine.execute(sql)
        model.Session.commit()

        print 'Remove PostgreSQL idels.'



