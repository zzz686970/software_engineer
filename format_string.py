"""KeyError for format

[description]
""" 
from collection import defaultdict 
from string import Template
from __future__ import print_function
import string  

# '{bond}, {james} {bond}'.format_map(defaultdict(str, bond='bond'))
## 'bond,  bond'

tpl = Template('$bond, $james $bond')
action = tpl.safe_substitute({'bond': 'bond'})

Template(msg).safe_substitute(**practise_dict)

class SafeDict(dict):
	def __missing__(self, key):
		return '{' + key + '}'


# '{bond}, {james} {bond}'.format_map(SafeDict(bond='bond'))
# 'bond, {james} bond'

class MyFormatter(string.Formatter):
	def __init__(self, default = '{{{0}}}'):
		self.default = default 

	def get_value(self, key, args, kwds):
		if isinstance(key, str):
			return kwds.get(key, self.default.format(key))
		else:
			return string.Formatter.get_value(key, args, kwds)

# fmt=MyFormatter()
# >>> fmt.format("{bond}, {james} {bond}", bond='bond', james='james')
# 'bond, james bond'
# >>> fmt.format("{bond}, {james} {bond}", bond='bond')
# 'bond, {james} bond'


class SafeFormatter(string.Formatter):
    def vformat(self, format_string, args, kwargs):
        args_len = len(args)  # for checking IndexError
        tokens = []
        for (lit, name, spec, conv) in self.parse(format_string):
            # re-escape braces that parse() unescaped
            lit = lit.replace('{', '{{').replace('}', '}}')
            # only lit is non-None at the end of the string
            if name is None:
                tokens.append(lit)
            else:
                # but conv and spec are None if unused
                conv = '!' + conv if conv else ''
                spec = ':' + spec if spec else ''
                # name includes indexing ([blah]) and attributes (.blah)
                # so get just the first part
                fp = name.split('[')[0].split('.')[0]
                # treat as normal if fp is empty (an implicit
                # positional arg), a digit (an explicit positional
                # arg) or if it is in kwargs
                if not fp or fp.isdigit() or fp in kwargs:
                    tokens.extend([lit, '{', name, conv, spec, '}'])
                # otherwise escape the braces
                else:
                    tokens.extend([lit, '{{', name, conv, spec, '}}'])
        format_string = ''.join(tokens)  # put the string back together
        # finally call the default formatter
        return string.Formatter.vformat(self, format_string, args, kwargs)

# >>> SafeFormatter().format('{one} {one:x} {one:10f} {two!r} {two[0]}', one=215, two=['James', 'Bond'])
# "215 d7 215.000000 ['James', 'Bond'] James"
# >>> SafeFormatter().format('{one} {one:x} {one:10f} {two!r} {two[0]}', one=215)
# '215 d7 215.000000 {two!r} {two[0]}'
# >>> SafeFormatter().format('{one} {one:x} {one:10f} {two!r} {two[0]}')
# '{one} {one:x} {one:10f} {two!r} {two[0]}'
# >>> SafeFormatter().format('{one} {one:x} {one:10f} {two!r} {two[0]}', two=['James', 'Bond'])
# "{one} {one:x} {one:10f} ['James', 'Bond'] James"  



>>> from collections import defaultdict
>>> kwargs = {"name": "mark"}
>>> template = "My name is {0[name]} and I'm really {0[adjective]}."
>>> template.format(defaultdict(str, kwargs))
"My name is mark and I'm really ."


from functools import partial

s = partial("{foo} {bar}".format, foo="FOO")
print s(bar="BAR")
# FOO BAR


import string

try:
    # Python 3
    from _string import formatter_field_name_split
except ImportError:
    formatter_field_name_split = str._formatter_field_name_split


class PartialFormatter(string.Formatter):
    def get_field(self, field_name, args, kwargs):
        try:
            val = super(PartialFormatter, self).get_field(field_name, args, kwargs)
        except (IndexError, KeyError, AttributeError):
            first, _ = formatter_field_name_split(field_name)
            val = '{' + field_name + '}', first
        return val


class FailsafeDict(dict):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            return "{" + str(item) + "}"
        # end try
    # end def
# end class




import string

class FormatDict(dict):
    def set_parent(self, parent):
        self.parent = parent

    def __init__(self, *args, **kwargs):
        self.parent = None
        self.last_get = ''
        for arg in (args or []):
            if isinstance(arg, dict):
                for k in arg:
                    self.__setitem__(k, arg[k])
        for k in (kwargs or {}):
            self.__setitem__(k, kwargs[k])

    def __getitem__(self, k):
        self.last_get = k
        try:
            val = dict.__getitem__(self, k)
            return val
        except:
            ancestry = [k]
            x = self.parent
            while x:
                ancestry.append(x.last_get)
                x = x.parent
            ancestry.reverse()
            return '{' + ancestry[0] + ''.join(['[' + x + ']' for x in ancestry[1:]]) + '}'

    def __setitem__(self, k, v):
        if isinstance(v, dict):
            v = FormatDict(v)
            v.set_parent(self)
        dict.__setitem__(self, k, v)

    def format(self, s):
        return string.Formatter().vformat(s, (), self)


import re

def my_format(template, *args, **kwargs):
  next_index = len(args)
  while True:
    try:
      return template.format(*args, **kwargs)
    except KeyError as e:
      key = e.args[0]
      finder = '\{' + key + '.*?\}'
      template = re.sub(finder, '{\g<0>}', template)
    except IndexError as e:
      args = args + ('{' + str(next_index) + '}',)
      next_index += 1


import string
class PartialFormatter(string.Formatter):
    def __init__(self, missing='~~', bad_fmt='!!'):
        self.missing, self.bad_fmt=missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # Handle a key not found
        try:
            val=super(PartialFormatter, self).get_field(field_name, args, kwargs)
            # Python 3, 'super().get_field(field_name, args, kwargs)' works
        except (KeyError, AttributeError):
            val=None,field_name 
        return val 

    def format_field(self, value, spec):
        # handle an invalid format
        if value==None: return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None: return self.bad_fmt   
            else: raise

fmt=PartialFormatter()
data = {'n': 3, 'k': 3.141594, 'p': {'a': '7', 'b': 8}}
print(fmt.format('{n}, {k:.2f}, {p[a]}, {p[b]}', **data))
# 3, 3.14, 7, 8
del data['k']
data['p']['b'] = None
print(fmt.format('{n}, {k:.2f}, {p[a]:.2f}, {p[b]}', **data))
# 3, ~~, !!, ~~              


