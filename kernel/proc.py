# TODO: Check dependencies #

def __set_idle_name(name, n):

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
            name = ''.join([name, chr(ord('0')+digit)])
            i += 1
        c = c // 10
    
PICK_ANY = 1
PICK_HIGHERONLY = 2
    
def BuildNotifyMessage(m_ptr,src,dst_ptr):
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
        rp['p_endpoint'] = _ENDPOINT(0,rp['p_nr'])
        rp['p_scheduler'] = None
        rp['p_priority'] = 0
        rp['p_quantum_size_ms'] = 0
        arch_proc_reset(rp)
        rp += 1
        i += 1

    sp = BEG_PRIV_ADDR+1
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
        ip = get_cpu_var_ptr(i,idle_proc)
        ip['p_endpoint'] = IDLE
        ip['p_priv'] = idle_priv
        # Idle must never be scheduled #
        ip['p_rts_flags'] |= RTS_PROC_STOP
        __set_idle_name(ip['p_name'], i)

def __switch_address_space_idle():
    # MXCM #
    ''' Currently we bet that VM is always alive and its pages available so
    when the CPU wakes up the kernel is mapped and no surprises happen.
    This is only a problem if more than 1 cpus are available.'''
    
    if CONFIG_SMP:
        switch_address_space(proc_addr(VM_PROC_NR))  

def __idle():
    # MXCM #
    ''' This function is called whenever there is no work to do.
	Halt the CPU, and measure how many timestamp counter ticks are
	spent not doing anything. This allows test setups to measure
	the CPU utilization of certain workloads with high precision.'''
    p = get_cpulocal_var(proc_ptr) = get_cpulocal_var_ptr(idle_proc)

    if priv(p)['s_flags'] & BILLABLE:
        get_cpulocal_var(bill_ptr) = p

    switch_address_space_idle()
    if not CONFIG_SMP:
        restart_local_timer();
    else:
        get_cpulocal_var(cpu_is_idle) = 1;
        if (cpuid != bsp_cpu_id):
            stop_local_timer();
        else:
            restart_local_timer()
        
    # start accounting for the idle time
    context_stop(proc_addr(KERNEL))
    if not SPROFILE:
        halt_cpu()
    else:
        if not sprofiling:
            halt_cpu()
        else:
            v = get_cpulocal_var_ptr(idle_interrupted)
            interrupts_enable();
            while not v:
                arch_pause();
            interrupts_disable();
            v = 0;
    ''' End of accounting for the idle task does not happen here, the kernel
    is handling stuff for quite a while before it gets back here!'''
