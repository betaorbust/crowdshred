import sys, os

#DEBUG = True
DEBUG = False

cwd = os.getcwd()
site_name = 'crowdshred'
site_home = os.path.join(cwd,site_name)
env_bin = os.path.join(cwd, site_name, 'env', 'bin')
print env_bin

cmd = 'source %s' % (os.path.join(env_bin,'activate'))
os.system(cmd)

# Invole the virtualenv
INTERP = '%s' % (os.path.join(env_bin,'python'))
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

# Set up the path
sys.stdout = sys.stderr
sys.path.append(site_home)
sys.path.append(os.path.join(site_home,'..'))
sys.path.append(os.path.join(site_home,'project'))
sys.path.append(os.path.join(env_bin,'/../lib/python2.7/site-packages'))
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

# Set up the django application
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
