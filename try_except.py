import traceback
import logging

try:
	1/0
except Exception:
	traceback.print_exc()
	# print(e, file=sys.stderr)
	# logging.exception('an exception')

	exc_type, exc_value, exc_traceback = sys.exc_info()
	print(exc_value.filename, value.strerror)
	## file name
	# exc_traceback.tb_frame.f_locals.get('filename')

