import os
import sys

cwd = os.getcwd()
sys.path.append('/var/www/stng')

from stng import app as application