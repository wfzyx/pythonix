# TODO: Check dependencies #

def __set_idle_name(name, n):

    p_z = False

    if n > 999:
        n = 999

    name = 'idle'

    i = 4
    c = 100
    digit = 100
    while c > 0:

        digit = n//c
        n -= digit*c

        if p_z or digit != 0 or c == 1:
            p_z = True
            name = ''.join([name, str(i)])
            i += 1

        c = c//10
    name = ''.join([name, '\0'])


# TODO: Check depenencies #
def proc_init():
    rp = {}
    sp = {}

    rp = BEG_PROC_ADDR
    i = NR_TASKS * -1

    while rp < END_PROC_ADDR:
        rp += 1
        i += 1

        rp['p_rts_flags'] = RTS_SLOT_FREE
        rp['p_magic'] = PMAGIC
        rp['p_nr'] = i
        rp['p_endpoint'] = _ENDPOINT(0,rp['p_nr'])
        rp['p_scheduler'] = None
        rp['p_priority'] = 0
        rp['p_quantum_size_ms'] = 0

        arch_proc_reset(rp)

    sp = BEG_PRIV_ADDR
    i = 0

    while sp < END_PRIV_ADDR:
        sp += 1
        i += 1

        sp['s_proc_nr'] = NONE
        # TODO: Check how to do this casting operation #
        sp['s_id'] = (sys_id_t) i
        ppriv_addr[i] = sp
        sp['s_sig_mrg'] = NONE
        sp['s_bak_sig_mgr'] = NONE

    idle_priv.s_flags = IDL_F

    # Initialize IDLE structs (here implemented as dicts) for every CPU #
    i = 0
    while i < CONFI_MA_CPUS:
        ip = get_cpu_var_ptr(i,idle_proc)
        ip['p_endpoint'] = IDLE
        ip['p_priv'] = idle_priv
        # Iddle must never be scheduled #
        ip['p_rts_flags'] = ip['p_rts_flags'] & RTS_PROC_STOP
        __set_idle_name(ip['p_name'], i)
        i += 1


def __switch_address_space_idle():
    if CONFIG_SMP:
        switch_address_space(proc_addr(VM_PROC_NR))


def __idle():
    p = {}

    # Comentary from minix source code #
    ''' This function is called whenever there is no work to do.
	Halt the CPU, and measure how many timestamp counter ticks are
	spent not doing anything. This allows test setups to measure
	the CPU utilization of certain workloads with high precision.'''

    p = get_cpulocal_var(proc_ptr) = get_cpulocal_var_ptr(idle_proc)

    if priv(p)['s_flags'] & BILLABLE:
        get_cpulocal_var(bill_ptr) = p

    __switch_address_space_idle()

    if CONFIG_SMP:
        get_cpulocal_var(cpu_is_idle) = 1
        if cpuid != bsp_cpu_id:
            stop_local_timer()
        else:
            restart_local_timer()

    contex_stop(proc_addr(KERNEL))

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
