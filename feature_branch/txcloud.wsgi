# activate_this = '/var/www/html/txcloud_env/bin/activate.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/html/txcloud_env/txcloud')

from analytics import app as application
