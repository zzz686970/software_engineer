"""metaclass in python

[description]
"""

class Base(object):
	def __init__(self, val):
		self.val = val

	@classmethod
	def make_obj(cls, val):
		return cls(val+1)

class Derived(Base):
	def __init__(self, val):
		super(Derived, self).__init__(val + 2)

	@classmethod
	def make_obj(cls, val):
		return super(Derived, cls).make_obj(val)

b1 = Base(0)
# b1.val == 0

b2 = Base.make_obj(0)
# b2.val == 1

d1 = Derived(0)
# d1.val == 1

d2 = Derived.make_obj(0)
# d2.val == 3