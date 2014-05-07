#TODO implement all the library
def sys_getinfo(request, val_ptr,val_len,val_ptr2,val_len2):
	# TODO check syscall implementation
	pass

def sys_getkinfo(dst):
	sys_getinfo(GET_KINFO,dst,0,0,0)