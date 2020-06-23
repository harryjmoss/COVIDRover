class BaseConfig(object):
  DEBUG = False  
class Development(BaseConfig):
  DEBUG = True
  TESTING = True
class Production(BaseConfig):
  pass
