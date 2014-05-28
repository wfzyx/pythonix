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


def map_(call_nr, handler):
    call_index = call_nr - KERNEL_CALL
    assert(call_index >= 0 and call_index < NR_SYS_CALLS)
    # TODO check WTF is call_vec
    call_vec[call_index] = handler


def kernel_call_finish(caller, msg, result):
    if result == VMSUSPEND:
        '''Special case: message has to be saved for handling
        until VM tells us it's allowed. VM has been notified
        and we must wait for its reply to restart the call.'''
        assert(RTS_ISSET(caller, RTS_VMREQUEST))
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
            if DEBUG_IPC_HOOK:
                hook_ipc_msgkresult(msg, caller)
            if copy_msg_to_user(msg, caller['p_delivermsg_vir']):
                print('WARNING wrong user pointer {} from process {} /\
					{}'.format(caller['p_delivermsg_vir'], caller['p_name'],
                    caller['p_endpoint']
                )
                )
                cause_sig(proc_nr(caller), SIGSEGV)


def kernel_call_dispatch(caller, msg):
    result = OK
    if DEBUG_IPC_HOOK:
        hook_ipc_msgkresult(msg, caller)
    call_nr = msg['m_type'] - KERNEL_CALL

    # See if the caller made a valid request and try to handle it
    if call_nr < 0 or call_nr >= NR_SYS_CALLS:
        result = EBADREQUEST
    elif not GET_BIT(priv(caller)['s_k_call_mask'], call_nr):
        result = ECALLDENIED
    else:  # handle the system call
        if call_vec[call_nr]:
            result = call_vec[call_nr](caller, msg)  # TODO check WTF
        else:
            print("Unused kernel call {} from {}".format(
                call_nr, caller['p_endpoint'])
            )

    if result in [EBADREQUEST, ECALLDENIED]:
        print('SYSTEM: illegal request {} from {}'.format(
            call_nr, msg['m_source'])
        )

    return result


def kernel_call(m_user, caller):
    ''' Check the basic syscall parameters and if accepted
    dispatches its handling to the right handler'''
    result = OK
    msg = {}

    # TODO check vir_bytes casting
    caller['p_delivermsg_vir'] = m_user

    ''' the ldt and cr3 of the caller process is loaded because	it just've
	trapped into the kernel or was already set in switch_to_user() before we
	resume execution of an interrupted kernel call'''
    if not copy_msg_from_user(m_user, msg):
        msg['m_source'] = caller['p_endpoint']
        result = kernel_call_dispatch(caller, msg)
    else:
        print('WARNING wrong user pointer {} from process {} / {}'.format(
            m_user, caller['p_name'], caller['p_endpoint'])
        )

    kbill_kcall = caller
    kernel_call_finish(caller, msg, result)


def initialize():
        # TODO implement
    pass


def get_priv(rc, priv_id):
    ''' Allocate a new privilege structure for a system process.
    Privilege ids can be assigned either statically or dynamically.'''
    # TODO check sp loop
    if priv_id == NULL_PRIV_ID:  # allocate slot dynamically
        for sp in range(BEG_DYN_PRIV_ADDR + 1, END_DYN_PRIV_ADDR):
            if sp['s_proc_nr'] == None:
                break
        if sp >= END_DYN_PRIV_ADDR return ENOSPC
    else:  # allocate slot from id
        if not is_static_priv_id(priv_id):
            return EINVAL  # invalid id
        if priv[priv_id].s_proc_nr != None:
            return EBUSY  # slot in use
        sp = priv['priv_id']

    rc['p_priv'] = sp  # assign new slow
    rc['p_priv']['s_proc_nr'] = proc_nr(rc)  # set association

    return OK


def set_sendto_bit(rp, _id):
    ''' Allow a process to send messages to the process(es) associated
    with the system privilege structure with the given id.'''

    ''' Disallow the process from sending to a process privilege structure
	with no associated process, and disallow the process from sending to
	itself.'''
    if id_to_nr(_id) == None or priv_id(rp) == _id:
        unset_sys_bit(priv(rp)['s_ipc_to'], _id)
        return

    set_sys_bit(priv(rp)['s_ipc_to'], _id)

    ''' The process that this process can now send to, must be able to reply
	(or	vice versa). Therefore, its send mask should be updated as well.
	Ignore receivers that don't support traps other than RECEIVE, they can't
	reply or send messages anyway.'''

    if priv_addr(_id)['s_trap_mask'] & ~(1 << RECEIVE):
        set_sys_bit(priv_addr(_id)['s_ipc_to'], priv_id(rp))


def unset_sendto_bit(rp, _id):
    ''' Prevent a process from sending to another process. Retain the send
    mask symmetry by also unsetting the bit for the other direction.'''
    unset_sys_bit(priv(rp)['s_ipc_to'], _id)
    unset_sys_bit(priv_addr(_id)['s_ipc_to'], priv_id(rp))


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
    if not isokendpt(ep, proc_nr) or isemptyn(proc_nr):
        return EINVAL

    rp = proc_addr(proc_nr)
    priv = priv(rp)
    if not priv:
        return ENOENT
    sigaddset(priv['s_sig_pending'], sig_nr)
    increase_proc_signals(rp)
    mini_notify(proc_addr(SYSTEM), rp['p_endpoint'])

    return OK


def cause_sig(proc_nr, sig_nr):
    '''A system process wants to send a signal to a process.  Examples are:
    - HARDWARE wanting to cause a SIGSEGV after a CPU exception
    - TTY wanting to cause SIGINT upon getting a DEL
    - FS wanting to cause SIGPIPE for a broken pipe

    Signals are handled by sending a message to the signal manager assigned to
    the process. This function handles the signals and makes sure the signal
    manager gets them by sending a notification. The process being signaled
    is blocked while the signal manager has not finished all signals for it.
    Race conditions between calls to this function and the system calls that
    process pending kernel signals cannot exist. Signal related functions are
    only called when a user process causes a CPU exception and from the kernel
    process level, which runs to completion.'''

    # Lookup signal manager
    rp = proc_addr(proc_nr)
    sig_mgr = priv(rp)['s_sig_mgr']
    # TODO check self definition
    if sig_mgr == SELF:
        sig_mgr = rp['p_endpoint']

    # If the target is the signaol manager of itself
    # send the signal directly
    if rp['p_endpoint'] == sig_nr:
        if SIGS_IS_LETHAL(sig_nr):
            # If sig is lethal, see if a backup sig manager exists
            sig_mgr = priv(rp)['s_bak_sig_mgr']
            if sig_mgr != None and isokendpt(sig_mgr, sig_mgr_proc_nr):
                priv(rp)['s_sig_mgr'] = sig_mgr
                priv(rp)['s_bak_sig_mgr'] = None
                sig_mgr_rp = proc_addr(sig_mgr_proc_nr)
                RTS_UNSET(sig_mgr_rp, RTS_NO_PRIV)
                cause_sig(proc_nr, sig_nr)  # try again with new sig mgr
                return
            # no luck, time to panic
            proc_stacktrace(rp)
            panic("cause_sig: sig manager {} gets lethal signal {} for itself".format(
                rp['p_endpoint'], sig_nr))
        sigaddset(priv(rp)['s_sig_pending'], sig_nr)
        if send_sig(rp['p_endpoint'], SIGKSIGSM):
            panic('send_sig failed')
        return

    # Check if the signal is already pending. Process it otherwise
    if not sigismember(rp['p_pending'], sig_nr):
        sigaddset(rp['p_pending'], sig_nr)
        increase_proc_signals(rp)
        if not RTS_ISSET(rp, RTS_SIGNALED):
            RTS_SET(rp, RTS_SIGNALED | RTS_SIG_PENDING)
            if send_sig(sig_mgr, SIGKSIG) != OK:
                panic('send_sig failed')


def sig_delay_done(rp):
    '''A process is now known not to send any direct messages.
       Tell PM that the stop delay has ended, by sending a signal to the
       process. Used for actual signal delivery.'''
        rp['p_misc_flags'] &= ~MF_SIG_DELAY
        cause_sig(proc_nr(rp), SIGSNDELAY)


def _clear_ipc(rc):
        # TODO implement
    pass


def clear_endpoint(rc):
    if isemptyp(rc):
        panic('clear_proc: empty process {}'.format(rc['p_endpoint']))

    if DEBUG_IPC_HOOK:
        hook_ipc_clear(rc)

    # Make sure that the exiting proc is no longer scheduled
    RTS_SET(rc, RTS_NO_ENDPOINT)
    if priv(rc)['s_flags'] & SYS_PROC:
        priv(rc)['s_asynsize'] = 0

    # If the process happens to be queued trying to send a
    # message, then it must be removed from the message queues.

    _clear_ipc(rc)

    # Likewise, if another process was sending or receive a message to or from
    # the exiting process, it must be alerted that process no longer is alive.
    # Check all process

    clear_ipc_refs(rc, EDEADSRCDST)


def clear_ipc_refs(rc, caller_ret):
    # Clear IPC references for a given process slot

    # Tell processes that sent asynchronous messages to 'rc'
    # they are not going to be delivered
    src_id = has_pending_asend(rc, ANY)
    while src_id != NULL_PRIV_ID:
        cancel_async(proc_addr(id_to_nr), rc)
        src_id = has_pending_asend(rc, ANY)

    # TODO check this
    for rp in (BEG_PROC_ADDR, END_PROC_ADDR):
        if (isemptyp(rp)):
            continue
        # Unset pending notification bits
        unset_sys_bit(priv(rp)['s_notify_pending'], priv(rc)['s_id'])

        # Unset pending asynchronous messages
        unset_sys_bit(priv(rp)['s_asyn_pending'], priv(rc)['s_id'])

        # Check if process depends on given process.
        if P_BLOCKEDON(rp) == rc['p_endpoint']:
            rp['p_reg']['retreg'] = caller_ret

        clear_ipc(rp)


def kernel_call_resume(caller):
    assert(not RTS_ISSET(caller, RTS_SLOT_FREE))
    assert(not RTS_ISSET(caller, RTS_VMREQUEST))

    asset(caller['p_vmrequest']['saved']['reqmsg']
          ['m_source'] == caller['p_endpoint'])

	# re-execute the kernel call, with MF_KCALL_RESUME still set so
	# the call knows this is a retry.

	result = kernel_call_dispatch(caller, caller['p_vmrequest']['saved']['reqmsg'])

	# we are resuming the kernel call so we have to remove this flag so it
	# can be set again

	caller['p_misc_flags'] &= ~MF_KCALL_RESUME
	kernel_call_finish(caller, caller['p_vmrequest']['saved']['reqmsg'], result)

def sched(p, priority, quantum, cpu):
	# Make sure the values given are within the allowed range.*/
	if priority > NR_SCHED_QUEUES or (priority < TASK_Q and priority != -1):
		return EINVAL

	if quantum < 1 and quantum != -1:
		return EINVAL

    # TODO implement smp
	'''if CONFIG_SMP:
		if (cpu < 0 and cpu != -1) or (cpu > 0 and cpu >= ncpus)
			return EINVAL
		if cpu != -1 and not cpu_is_ready(cpu):
			return EBADCPU
    '''

	'''In some cases, we might be rescheduling a runnable process. In such
	a case (i.e. if we are updating the priority) we set the NO_QUANTUM
	flag before the generic unset to dequeue/enqueue the process'''

	# FIXME this preempts the process, do we really want to do that
	# FIXME this is a problem for SMP if the processes currently runs on a
	# different CPU

	if proc_is_runnable(p):
        pass
        # TODO implement SMP
		'''if CONFIG_SMP:
			if p->p_cpu != cpuid and cpu != -1 and cpu != p->p_cpu:
				smp_schedule_migrate_proc(p, cpu)'''
		RTS_SET(p, RTS_NO_QUANTUM)

	# TODO check, pro cis runnable again ?
	if proc_is_runnable(p):
		RTS_SET(p, RTS_NO_QUANTUM)

	if priority != -1:
		p['p_priority'] = priority
	if quantum != -1:
		p['p_quantum_size_ms'] = quantum
		p['p_cpu_time_left'] = ms_2_cpu_time(quantum)

    # TODO implement SMP
	'''if CONFIG_SMP:
		if cpu != -1:
			p['p_cpu'] = cpu
            '''

	# Clear the scheduling bit and enqueue the process
	RTS_UNSET(p, RTS_NO_QUANTUM)
	
	return OK
}