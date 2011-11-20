from settings import * 

# Include all the settings specific to 'production' machines
# such as DATABASES, TIME_ZONE
DEBUG = False
DATABASES = {
    'default': {
        'NAME': 'crowdshred_production',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'crowdshred_production_user',
        'PASSWORD': '[set password here]',
        'HOST': 'localhost'
    }
}
