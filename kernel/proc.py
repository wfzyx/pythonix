# TODO: Check dependencies #


def _set_idle_name(name, n):

    p_z = False

    if n > 999:
        n = 999

    name = 'idle'

    i = 4
    c = 100
    while c > 0:
        digit = n // c
        n -= digit * c
        if p_z or digit != 0 or c == 1:
            p_z = True
            name = ''.join([name, chr(ord('0') + digit)])
            i += 1
        c = c // 10

    return name

PICK_ANY = 1
PICK_HIGHERONLY = 2


def BuildNotifyMessage(m_ptr, src, dst_ptr):
    m_ptr['m_type'] = NOTIFY_MESSAGE
    m_ptr['NOTIFY_TIMESTAMP'] = get_monotonic()
    # TODO: Check priv function
    if src == HARDWARE:
        m_ptr['NOTIFY_TAG'] = dst_ptr['s_int_pending']
        dst_ptr['s_int_pending'] = 0
    elif src == SYSTEM:
        m_ptr['NOTIFY_TAG'] = dst_ptr['s_sig_pending']
        dst_ptr['s_sig_pending'] = 0


def proc_init():

    rp = BEG_PROC_ADDR + 1
    i = -NR_TASKS + 1
    while rp < END_PROC_ADDR:
        rp['p_rts_flags'] = RTS_SLOT_FREE
        rp['p_magic'] = PMAGIC
        rp['p_nr'] = i
        rp['p_endpoint'] = _ENDPOINT(0, rp['p_nr'])
        rp['p_scheduler'] = None
        rp['p_priority'] = 0
        rp['p_quantum_size_ms'] = 0
        arch_proc_reset(rp)
        rp += 1
        i += 1

    sp = BEG_PRIV_ADDR + 1
    i = 1
    while sp < END_PRIV_ADDR:
        # TODO: Check Minix NONE value.
        sp['s_proc_nr'] = NONE
        # TODO: Check if this casting is needed #
        sp['s_id'] = sys_id_t(i)
        ppriv_addr[i] = sp
        sp['s_sig_mrg'] = NONE
        sp['s_bak_sig_mgr'] = NONE
        sp += 1
        i += 1

    idle_priv.s_flags = IDL_F

    # Initialize IDLE dicts for every CPU #
    for i in range(CONFIG_MAX_CPUS):
        ip = get_cpu_var_ptr(i, idle_proc)
        ip['p_endpoint'] = IDLE
        ip['p_priv'] = idle_priv
        # Idle must never be scheduled #
        ip['p_rts_flags'] |= RTS_PROC_STOP
        _set_idle_name(ip['p_name'], i)


def _switch_address_space_idle():
    # MXCM #
    ''' Currently we bet that VM is always alive and its pages available so
    when the CPU wakes up the kernel is mapped and no surprises happen.
    This is only a problem if more than 1 cpus are available.'''

    '''
    if CONFIG_SMP:
        switch_address_space(proc_addr(VM_PROC_NR))
    '''


def _idle():
    # MXCM #
    ''' This function is called whenever there is no work to do.
    Halt the CPU, and measure how many timestamp counter ticks are
    spent not doing anything. This allows test setups to measure
    the CPU utilization of certain workloads with high precision.'''

    # TODO: Check how to handle this in python
    # p = get_cpulocal_var(proc_ptr) = get_cpulocal_var_ptr(idle_proc)

    if priv(p)['s_flags'] & BILLABLE:
        # TODO check SMP stuff
        CPULOCAL_STRUCT[0][bill_ptr] = p

    _switch_address_space_idle()


    # TODO Check this if necessary
    restart_local_timer()
    '''if CONFIG_SMP:
        CPULOCAL_STRUCT[0][cpu_is_idle] = 1
        if (cpuid != bsp_cpu_id):
            stop_local_timer()
        else:
            restart_local_timer()
    '''

    # Start accounting for the idle time #
    context_stop(proc_addr(KERNEL))
    if not SPROFILE:
        halt_cpu()
    else:
        if not sprofiling:
            halt_cpu()
        else:
            v = get_cpulocal_var_ptr(idle_interrupted)
            interrupts_enable()
            while not v:
                arch_pause()
            interrupts_disable()
            v = 0
    ''' End of accounting for the idle task does not happen here, the kernel
    is handling stuff for quite a while before it gets back here!'''


# TODO: Translate switch_to_user() #
def switch_to_user():
    pass


# Handler for all synchronous IPC calls #
def _do_sync_ipc(caller_ptr, call_nr, src_dst_e, m_ptr):
    # MXCM #
    '''Check destination. RECEIVE is the only call that accepts ANY (in
    addition to a real endpoint). The other calls (SEND, SENDREC, and NOTIFY)
    require an endpoint to corresponds to a process. In addition, it is
    necessary to check whether a process is allowed to send to a given
    destination.'''

    if (
        call_nr < 0 or
        call_nr > IPCNO_HIGHEST or
        call_nr >= 32 or
        callname != ipc_call_names[call_nr]
    ):
        if DEBUG_ENABLE_IPC_WARNINGS:
            print('sys_call: trap {} not_allowed, caller {}, src_dst {}'
                  .format(call_nr, proc_nr(caller_ptr), src_dst_e))
        return ETRAPDENIED

    if src_dst_e == ANY:
        if call_nr != RECEIVE:
            return EINVAL
        src_dst_p = int(src_dst_e)
    else:
        if not isokendpt(src_dst_e, src_dst_p):
            return EDEADSRCDST

        # MXCM #
        ''' If the call is to send to a process, i.e., for SEND, SENDNB,
        SENDREC or NOTIFY, verify that the caller is allowed to send to
        the given destination.'''
        if call_nr != RECEIVE:
            if not may_send_to(caller_ptr, src_dst_p):
                if DEBUG_ENABLE_IPC_WARNINGS:
                    print('sys_call: ipc mask denied {} from {} to {}'
                          .format(callname, caller_ptr['p_endpoint'],
                                  src_dst_e))
                return ECALLDENIED

    # MXCM #
    ''' Check if the process has privileges for the requested call.
    Calls to the kernel may only be SENDREC, because tasks always
    reply and may not block if the caller doesn't do receive().'''

    if not priv(caller_ptr)['s_trap_mask'] & (1 << call_nr):
        if DEBUG_ENABLE_IPC_WARNINGS:
            print('sys_call: ipc mask denied {} from {} to {}'
                  .format(callname, caller_ptr['p_endpoint'], src_dst_e))
        return ETRAPDENIED

    if call_nr != SENDREC and call_nr != RECEIVE and iskerneln(src_dst_p):
        if DEBUG_ENABLE_IPC_WARNINGS:
            print('sys_call: ipc mask denied {} from {} to {}'
                  .format(callname, caller_ptr['p_endpoint'], src_dst_e))
        return ETRAPDENIED

    if call_nr == SENDREC:
        caller_ptr['p_misc_flags'] |= MF_REPLY_PEND
        # TODO tweak logic to swcase fall
    elif call_nr == SEND:
        result = mini_send(caller_ptr, src_dst_e, m_ptr, 0)
        if call_nr == SEND or result != OK:
            pass
        # TODO tweak logic to swcase break
        # TODO tweak logic to swcase fall
    elif call_nr == RECEIVE:
        # TODO tweak logic to swcase recheck
        caller_ptr['p_misc_flags'] &= ~MF_REPLY_PEND
        IPC_STATUS_CLEAR(caller_ptr)
        result = mini_receive(caller_ptr, src_dst_e, m_ptr, 0)
    elif call_nr == NOTIFY:
        result = mini_notify(caller_ptr, src_dst_e)
    elif call_nr == SENDNB:
        result = mini_send(caller_ptr, src_dst_e, m_ptr, NON_BLOCKING)
    else:
        result = EBADCALL

    # Return the result of system call to the caller #
    return result


def do_ipc(r1, r2, r3):
    # TODO: Check if this way of translating pointer is right
    caller_ptr = get_cpulocal_var(proc_ptr)
    call_nr = r1

    assert(not RTS_ISSET(caller_ptr, RTS_SLOT_FREE))

    # MXCM #
    # Bill kernel time to this process
    kbill_ipc = caller_ptr

    # MXCM #
    # If this process is subset to system call tracing,
    # handle that first

    if caller_ptr['p_misc_flags'] & (MF_SC_TRACE | MR_SC_DEFER):
        # MXCM #
        # Are we tracing this process, and is it the
        # first sys_call entry?

        if (
            (caller_ptr['p_misc_flags'] & (MF_SC_TRACE | MR_SC_DEFER)) ==
            MF_SC_TRACE
        ):
            # MXCM #
            '''We must notify the tracer before processing the actual
            system call. If we don't, the tracer could not obtain the
            input message. Postpone the entire system call.'''

            caller_ptr['p_misc_flags'] &= ~MF_SC_TRACE
            assert(not caller_ptr['p_misc_flags'] & MR_SC_DEFER)
            caller_ptr['p_misc_flags'] |= MF_SC_DEFER
            caller_ptr['p_defer']['r1'] = r1
            caller_ptr['p_defer']['r2'] = r2
            caller_ptr['p_defer']['r3'] = r3

            # Signal the "enter system call" event. Block the process.
            cause_sig(proc_nr(caller_ptr), SIGTRAP)

            # Preserve the return registrer's value.
            return caller_ptr['p_reg']['retreg']

        # If the MF_SC_DEFER flag is set, the syscall is now being resumed.
        caller_ptr['p_misc_flags'] &= ~MF_SC_DEFER
        assert(not caller_ptr['p_misc_flags'] & MF_SC_ACTIVE)

        # Set a flag to allow reliable tracing of leaving the system call.
        caller_ptr['p_misc_flags'] |= MF_SC_ACTIVE

    if caller['p_misc_flags'] & MF_DELIVERMSG:
        panic('sys_call: MF_DELIVERMSG on for {} / {}'
              .format(caller_ptr['p_name'], caller_ptr['p_endpoint']))

    # MXCM #
    '''Now check if the call is known and try to perform the request. The only
    system calls that exist in MINIX are sending and receiving messages.
    - SENDREC: combines SEND and RECEIVE in a single system call
    - SEND:    sender blocks until its message has been delivered
    - RECEIVE: receiver blocks until an acceptable message has arrived
    - NOTIFY:  asynchronous call; deliver notification or mark pending
    - SENDA:   list of asynchronous send requests'''

    if call_nr in [SENDREC, SEND, RECEIVE, NOTIFY, SENDNB]:
        # Process accounting for scheduling
        # TODO: Check castings here
        return _do_sync_ipc(caller_ptr, call_nr, r2, r3)

    elif call_nr == SENDA:
        # Get and check the size of the arguments in bytes
        # TODO: Check if len() get the needed size from r2
        msg_size = len(r2)

        # Process accounting for scheduling
        caller_ptr['p_accounting']['ipc_async'] += 1

        # Limit size to something reasonable. An arbitrary choice is 16
        # times the number of process table entries
        if msg_size > 16 * (NR_TASKS + NR_PROCS):
            return EDOM
        # TODO: Check castings here
        return mini_senda(caller_ptr, r3, msg_size)

    elif call_nr == PYTHONIX_KERNINFO:
        # It may not be initialized yet
        if not pythonix_kerninfo_user:
            return EBADCALL

        arch_set_secondary_ipc_return(caller_ptr, pythonix_kerninfo_user)
        return OK

    else:
        # Illegal system call
        return EBADCALL


# TODO: Check this function I was not sure how to translate it to python
def _deadlock(function, cp, src_dst_e):
    # MXCM #
    ''' Check for deadlock. This can happen if 'caller_ptr' and
    'src_dst' have a cyclic dependency of blocking send and
    receive calls. The only cyclic dependency that is not fatal
    is if the caller and target directly SEND(REC) and RECEIVE
    to each other. If a deadlock is found, the group size is
    returned. Otherwise zero is returned.'''
    pass


def _has_pending(_map, src_p, asynm):
    # MXCM #
    # Check to see if there is a pending message from
    # the desired source available.

    _id = NULL_PRIV_ID

    '''
    if CONFIG_SMP:
        p = {}
    '''

    # MXCM #
    '''Either check a specific bit in the mask map, or find the first
    bit set in it (if any), depending on whether the receive was
    called on a specific source endpoint.'''

    if src_p != ANY:
        src_id = nr_to_id(src_p)

        if get_sys_bit(_map, src_id):
            # This if does nothig while CONFIG_SMP is not implemented
            pass
            # TODO Implement SMP
            '''
            if CONFIG_SMP:
                p = proc_addr(id_to_nr(src_id))

                if asynm and RTS_ISSET(p, RTS_VMINHIBIT):
                    p['p_misc_flags'] |= MF_SENDA_VM_MISS
                else:
                    _id = src_id
            '''
    else:
        # Find a source with a pending message

        aux = True
        for src_id in range(0, NR_SYS_PROCS, BITCHUNCK_BITS):
            if get_sys_bits(_map, src_id) != 0:
                # TODO Implement SMP
                '''
                if CONFIG_SMP:
                    while src_id < NR_SYS_PROCS and aux:
                        while not get_sys_bit(_map, src_id) and aux:
                            if src_id == NR_SYS_PROCS:
                                aux = False
                                break
                            src_id += 1
                        if not aux:
                            break
                        p = proc_addr(id_to_nr(src_id))
                        # MXCM #
                        """ We must not let kernel fiddle with pages of a
                        process which are currently being changed by
                        VM.  It is dangerous! So do not report such a
                        process as having pending async messages.
                        Skip it."""
                        if asynm and RTS_ISSET(p, RTS_VMINHIBIT):
                            p['p_misc_flags'] |= MF_SENDA_VM_MISS
                            src_id += 1
                        else:
                            aux = False
                            break
                '''
                if aux:
                    # TODO: Change this if to elif when CONFIG_SMP is
                    # implemented
                    while not get_sys_bit(_map, src_id):
                        src_id += 1
                    aux = False
                    break

        if src_id < NR_SYS_PROCS:
            # Founf one
            _id = src_id
    return _id


def has_pending_notify(caller, src_p):
    _map = priv(caller)['s_notify_pending']
    return _has_pending(_map, src_p, 0)


def has_pending_asend(caller, src_p):
    _map = priv(caller)['s_asyn_pending']
    return _has_pending(_map, src_p, 1)


def unset_notify_pending(caller, src_p):
    _map = priv(caller)['s_notify_pending']
    unset_sys_bit(_map, src_p)


def mini_send(caller_ptr, dst_e, m_ptr, flags):
    dst_p = ENDPOINT(dst_e)
    dst_ptr = proc_addr(dst_p)

    if RTS_ISSET(dst_ptr, RTS_NO_ENDPOINT):
        return EDEADSRCDST

    # MXCM #
    '''Check if 'dst' is blocked waiting for this message. The
    destination's RTS_SENDING flag may be set when its SENDREC
    call blocked while sending'''

    if WILLRECEIVE(dst_ptr, caller_ptr['p_endpoint']):
        # Destination is indeed waiting for this message.
        assert(not (dst_ptr['p_misc_flags'] & MF_DELIVERMSG))

        if not (flags & FROM_KERNEL):
            if copy_msg_from_user(m_ptr, dst_ptr['p_delivermsg']):
                return EFAULT
        else:
            dst_ptr['p_delivermsg'] = m_ptr
            IPC_STATUS_ADD_FLAGS(dst_ptr, IPC_FLG_MSG_FROM_KERNEL)

        dst_ptr['p_delivermsg']['m_source'] = caller_ptr['p_endpoint']
        dst_ptr['p_misc_flags'] |= MF_DELIVERMSG

        if caller_ptr['p_misc_flags'] & MF_REPLY_PEND:
            call = SENDREC
        else:
            if flags & NON_BLOCKING:
                call = SENDNB
            else:
                call = SEND

        IPC_STATUS_ADD_CALL(dst_ptr, call)

        if dst_ptr['p_misc_flags'] & MF_REPLY_PEND:
            dst_ptr['p_misc_flags'] &= ~MF_REPLY_PEND

        RTS_UNSET(dst_ptr, RTS_RECEIVING)

        if DEBUG_IPC_HOOK:
            hook_ipc_msgsend(dst_ptr['p_delivermsg'], caller_ptr, dst_ptr)
            hook_ipc_msgrecv(dst_ptr['p_delivermsg'], caller_ptr, dst_ptr)

    else:
        if flags & NON_BLOCKING:
            return ENOTREADY

        # Check for a possible deadlock before actually blocking
        if deadlock(send, caler_ptr, dst_e):
            return ELOCKED

        # Destination is not waiting. Block and dequeue caller
        if not flags & FROM_KERNEL:
            if copy_msg_from_user(m_ptr, caller_ptr['p_sendmsg']):
                return EFAULT
        else:
            caller_ptr['p_sendmsg'] = m_ptr

            # MXCM #
            '''We need to remember that this message is from kernel
            so we can set the delivery status flags when the message
            is actually delivered'''

            caller_ptr['p_misc_flags'] |= MF_SENDING_FROM_KERNEL

        RTS_SET(caller_ptr, RTS_SENDING)
        caller_ptr['p_sendto_e'] = dst_e

        # Process is now blocked. Put in on destination's queue
        assert(caller_ptr['p_q_link'] == None)

        # TODO: Check how to do this
        '''
        while (*xpp) xpp = &(*xpp)->p_q_link;
	*xpp = caller_ptr;
        '''

        if DEBUG_IPC_HOOK:
            hook_ipc_msgsend(caller_ptr['p_sendmsg'], caller_ptr, dst_ptr)

    return OK


def _mini_receive():
    pass
