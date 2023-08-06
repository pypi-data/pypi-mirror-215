import sys
import os

ap = os.path.abspath('./krutils')
print ('imported:' + ap)

sys.path.append(ap)

import logger
l = logger.getlogger(__file__, 'settings.json')
# print (l)
l.syslog('[%%]', 's')
l.dblog('[%%]', 'd')
l.debug('[%%]', 123)
l.info('[%%]', 'info')
l.error('[%%]', '123eeeeeeee')





