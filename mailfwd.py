from configparser import ConfigParser
import process

#Parse config
config = ConfigParser()
config.read('config.cfg')

mail = process.Mail('', config)
