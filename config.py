from logging import DEBUG
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """ 
Load configuration from environment. 

In PRODUCTION conda sets up the environment,
so look in ~/.conda/envs/covid/etc/conda/activate.d/env_vars.sh
to see how it is set up. 
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "12345678"
 
    PORTAL_URL      = os.environ.get('PORTAL_URL')
    PORTAL_USER     = os.environ.get('PORTAL_USER')
    PORTAL_PASSWORD = os.environ.get('PORTAL_PASSWORD')

# Where data live
    TABLE_URL = os.environ.get('TABLE_URL')

    CELERY_BROKER = os.environ.get('CELERY_BROKER')
    CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

    pass

    @staticmethod
    def init_app(app):
        pass


if __name__ == "__main__":

    assert Config.TESTING
    assert Config.DEBUG
    
    assert Config.SECRET_KEY

    # These have to be defined in your environment
    # for example in a .env file or launch.json
    # or conda environment.
    
    assert Config.PORTAL_URL
    assert Config.PORTAL_USER
    assert Config.PORTAL_PASSWORD
    #assert Config.TABLE_URL
    pass

    print("That's all!")
