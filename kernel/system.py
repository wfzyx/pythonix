'''This task handles the interface between the kernel and user-level servers.
System services can be accessed by doing a system call. System calls are 
transformed into request messages, which are handled by this task. By 
convention, a sys_call() is transformed in a SYS_CALL request message that
is handled in a function named do_call(). 

A private call vector is used to map all system calls to the functions that
handle them. The actual handler functions are contained in separate files
to keep this file clean. The call vector is used in the system task's main
loop to handle all incoming requests.  

In addition to the main sys_task() entry point, which starts the main loop,
there are several other minor entry points:
get_priv:		assign privilege structure to user or system process
set_sendto_bit:	allow a process to send messages to a new target
unset_sendto_bit:	disallow a process from sending messages to a target
fill_sendto_mask:	fill the target mask of a given process
send_sig:		send a signal directly to a system process
cause_sig:		take action to cause a signal to occur via a signal mgr
sig_delay_done:	tell PM that a process is not sending
get_randomness:	accumulate randomness in a buffer
clear_endpoint:	remove a process' ability to send and receive messages
sched_proc:	schedule a process

Changes:
Nov 22, 2009   get_priv supports static priv ids (Cristiano Giuffrida)
Aug 04, 2005   check if system call is allowed  (Jorrit N. Herder)
Jul 20, 2005   send signal to services with message  (Jorrit N. Herder) 
Jan 15, 2005   new, generalized virtual copy function  (Jorrit N. Herder)
Oct 10, 2004   dispatch system calls from call vector  (Jorrit N. Herder)
Sep 30, 2004   source code documentation updated  (Jorrit N. Herder)'''

# TODO check imports

'''Declaration of the call vector that defines the mapping of system calls 
to handler functions. The vector is initialized in sys_init() with map(), 
which makes sure the system call numbers are ok. No space is allocated, 
because the dummy is declared extern. If an illegal call is given, the 
array size will be negative and this won't compile.'''

# TODO check WTF is call_vec

def map(call_nr,handler):
	call_index = call_nr-KERNEL_CALL
	assert(call_index >= 0 and call_index < NR_SYS_CALLS)
	call_vec[call_index] = handler

def kernel_call_finish(caller,msg,result):
	if result == VMSUSPEND:
		'''Special case: message has to be saved for handling
		until VM tells us it's allowed. VM has been notified
		and we must wait for its reply to restart the call.'''
		assert(RTS_ISSET(caller,RTS_VMREQUEST))
		# TODO check caller struct
		assert(caller['p_vmrequest']['type'] == VMSTYPE_KERNELCALL)
		caller['p_vmrequest']['saved']['reqmsg'] = msg
		caller['p_misc_flags'] |= MF_KCALL_RESUME
	else:
		''' call is finished, we could have been suspended because
		of VM, remove the request message'''
		caller['p_vmrequest']['saved']['reqmsg']['m_source'] = None
		if result != EDONTREPLY:
			# Copy the result as a message to the original user buffer
			msg['m_source'] = SYSTEM
			msg['m_type'] = result
			if DEBUG_IPC_HOOK: hook_ipc_msgkresult(msg,caller)
			if copy_msg_to_user(msg,caller['p_delivermsg_vir']):
				print('WARNING wrong user pointer {} from process {} /\
					{}'.format(caller['p_delivermsg_vir'],caller['p_name'],
						caller['p_endpoint']
						)
					)
				cause_sig(proc_nr(caller),SIGSEGV)

def kernel_call_dispatch(caller,msg):
	result = OK
	if DEBUG_IPC_HOOK: hook_ipc_msgkresult(msg,caller)
	call_nr = msg['m_type'] - KERNEL_CALL

	# See if the caller made a valid request and try to handle it
	if call_nr < 0 or call_nr >= NR_SYS_CALLS: result = EBADREQUEST
	elif not GET_BIT(priv(caller)['s_k_call_mask'],call_nr): result = ECALLDENIED	
	else: # handle the system call
		if call_vec[call_nr]:
			result = call_vec[call_nr](caller,msg) # TODO check WTF
		else:
			print("Unused kernel call {} from {}".format(
				call_nr,caller['p_endpoint'])
			)

	if result in [EBADREQUEST,ECALLDENIED]:
		print('SYSTEM: illegal request {} from {}'.format(
		call_nr,msg['m_source'])
	)

	return result

def kernel_call(m_user,caller):
	''' Check the basic syscall parameters and if accepted
	dispatches its handling to the right handler'''
	result = OK
	msg = {}

	# TODO check vir_bytes casting
	caller['p_delivermsg_vir'] = m_user

	''' the ldt and cr3 of the caller process is loaded because	it just've
	trapped into the kernel or was already set in switch_to_user() before we
	resume execution of an interrupted kernel call'''
	if !copy_msg_from_user(m_user,msg):
		msg['m_source'] = caller['p_endpoint']
		result = kernel_call_dispatch(caller,msg)
	else:
		print('WARNING wrong user pointer {} from process {} / {}'.format(
			m_user,caller['p_name'],caller['p_endpoint'])
		)

	kbill_kcall = caller
	kernel_call_finish(caller,msg,result)

# TODO implement
def initialize():
	pass

def get_priv(rc,priv_id):
	''' Allocate a new privilege structure for a system process.
	Privilege ids can be assigned either statically or dynamically.'''
	# TODO check sp loop
	if priv_id == NULL_PRIV_ID: # allocate slot dynamically
		for sp in range(BEG_DYN_PRIV_ADDR+1,END_DYN_PRIV_ADDR):
			if sp['s_proc_nr'] == None: break
		if sp >= END_DYN_PRIV_ADDR return ENOSPC
	else: # allocate slot from id
		if not is_static_priv_id(priv_id): return EINVAL # invalid id
		if priv[priv_id].s_proc_nr != None: return EBUSY # slot in use
		sp = priv['priv_id']

	rc['p_priv'] = sp # assign new slow
	rc['p_priv']['s_proc_nr'] = proc_nr(rc) # set association

	return OK

def set_sendto_bit(rp,_id):
	''' Allow a process to send messages to the process(es) associated
	with the system privilege structure with the given id.'''

	''' Disallow the process from sending to a process privilege structure
	with no associated process, and disallow the process from sending to
	itself.'''
	if id_to_nr(_id) == None or priv_id(rp) == _id:
		unset_sys_bit(priv(rp)['s_ipc_to'], _id)
		return

	set_sys_bit(priv(rp)['s_ipc_to'],_id)

	''' The process that this process can now send to, must be able to reply
	(or	vice versa). Therefore, its send mask should be updated as well.
	Ignore receivers that don't support traps other than RECEIVE, they can't
	reply or send messages anyway.'''

	if priv_addr(_id)['s_trap_mask'] & ~(1 <<  RECEIVE):
		set_sys_bit(priv_addr(_id)['s_ipc_to'], priv_id(rp))

def unset_sendto_bit(rp,_id):
	''' Prevent a process from sending to another process. Retain the send
	mask symmetry by also unsetting the bit for the other direction.'''
	unset_sys_bit(priv(rp)['s_ipc_to'],_id)
	unset_sys_bit(priv_addr(_id)['s_ipc_to'],priv_id(rp))

def fill_sendto_mask(rp, _map):
	for i in range(len(NR_SYS_PROCS)):
		if get_sys_bit(_map, i):
			set_sendto_bit(rp, i)
		else:
			unset_sendto_bit(rp, i)

def send_sig(ep, sig_nr):
	''' Notify a system process about a signal. This is straightforward. Simply
	set the signal that is to be delivered in the pending signals map and 
	send a notification with source SYSTEM. '''
	if not isokendpt(ep,proc_nr) or isemptyn(proc_nr):
		return EINVAL

	rp = proc_addr(proc_nr)
	priv = priv(rp)
	if not priv: return ENOENT
	sigaddset(priv['s_sig_pending'], sig_nr)
	increase_proc_signals(rp)
	mini_notify(proc_addr(SYSTEM), rp['p_endpoint'])

	return OK
