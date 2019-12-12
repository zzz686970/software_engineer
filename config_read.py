from configparser import RawConfigParser, ConfigParser

config = RawConfigParser()
config.read('test.ini')

string_val = config.get('section_a', 'string_val')
config.set('section_a', 'string_val', 'world')

config.add_section('section_b')
config.set('section_b', 'string_val', 'world')

with open('test.ini', 'w') as config_file:
	config.write(config_file)

## allow dict for both keys and attribute access

class AttrDict(dict):
	def __init__(self, *args, **kwargs):
		super(AttrDict, self).__init__(*args, **kwargs)
		self.__dict__ = self
##
#[general]
#key = val

## how to use, read only access
# any access to config._sections['section']['key'] is private, returns the raw values
config = ConfigParser(dict_type = AttrDict)
config.read('test2.ini')
config._sections.general.key




