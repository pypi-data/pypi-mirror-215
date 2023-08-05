__version__ = "5.0.0"

FRAPPE_VERSION = None

def set_frappe_version(bench_path='.'):
	global FRAPPE_VERSION
	if not FRAPPE_VERSION:
		FRAPPE_VERSION = "14.0"