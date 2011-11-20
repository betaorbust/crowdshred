"""
fab deployment script
====================================

"""
import os

from fabric.api import *
from fabric.contrib.project import *

from fab_deploy import *

def my_site():
    """ Default Configuration """
    env.conf = dict(
        PROVIDER = '',

		CONF_FILE = os.path.join(os.getcwd(),'fabric.conf'),
        INSTANCE_NAME = 'project_name',
        REPO = 'http://some.repo.com/project_name/',
    )

my_site()

