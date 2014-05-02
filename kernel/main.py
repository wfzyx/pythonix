''' This file contains the main program of PYTHONIX as well as its shutdown
    code. The routine main() initializes the system and starts the ball
    rolling by setting up the process table, interrupt vectors, and scheduling
    each task to run to initialize itself.
    The routine shutdown() does the opposite and brings down PYTHONIX.
    The entries into this file are:
    kmain: PYTHONIX main program
    prepare_shutdown:	prepare to take PYTHONIX down'''

# TODO check dependencies

def bsp_finish_booting():
    if SPOFILE:
        sprofiling = 0
    cprof_procs_no = 0

    cpu_identify()
    vm_running = 0
    # TODO check krandom struct

    krandom['random_sources'] = RANDOM_SOURCES
    krandom['random_elements'] = RANDOM_ELEMENTS

    # PYTHONIX is now ready. All boot image processes are on the ready queue.
    # Return to the assembly code to start running the current process.

    # TODO check WTF is this
    # get_cpulocal_var(proc_ptr) = get_cpulocal_var_ptr(idle_proc)
    # get_cpulocal_var(bill_ptr) = get_cpulocal_var_ptr(idle_proc)
    announce()

    # we have access to the cpu local run queue
    # only now schedule the processes.
    # We ignore the slots for the former kernel tasks
    for i in range(NR_BOOT_PROCS - NR_TASKS):
        RTS_UNSET(proc_addr(i), RTS_PROC_STOP)

    # enable timer interrupts and clock task on the boot CPU

    if(boot_cpu_init_timer(system_hz)):
        panic('''FATAL : failed to initialize timer interrupts,
                cannot continue without any clock source!''')

    fpu_init()

    # TODO check sanity checks
    '''
    if DEBUG_SCHED_CHECK:
        fixme("DEBUG_SCHED_CHECK enabled");

    if DEBUG_VMASSERT:
        fixme("DEBUG_VMASSERT enabled");

    if DEBUG_PROC_CHECK:
        fixme("PROC check enabled");
    '''

    debugextra('cycles_accounting_init()... ')
    cycles_accounting_init()
    debugextra('done')

    if CONFIG_SMP:
        cpu_set_flag(bsp_cpu_id, CPU_IS_READY)
        machine['processors_count'] = ncpus
        machine['bsp_id'] = bsp_cpu_id
    else:
        machine['processors_count'] = 1
        machine['bsp_id'] = 0

    kernel_may_alloc = 0

    switch_to_user()


def kmain(local_cbi={'kmess':None}):
    # TODO check if this is really necessary
    kinfo = local_cbi
    kmess = kinfo['kmess']

    machine['board_id'] =  get_board_id_by_name(env_get(BOARDVARNAME))

    if __arm__:
        arch_ser_init()

    # printing UP
    print('PYTHONIX booting')

    kernel_may_alloc = 1

    assert(len(kinfo['boot_procs'] == len(image)))
    kinfo['boot_procs'] = image

    cstart()
    BKL_LOCK()
    DEBUGEXTRA('main()')
    proc_init()

    if(NR_BOOT_MODULES != kinfo['mbi']['mods_count']):
        panic('expecting {} boot processes/modules, found {}'.format(
            NR_BOOT_MODULES, kinfo['mbi']['mods_count']))

    # Setting up proc table entries for proc in boot image
    for i in range(NR_BOOT_PROCS):
        ip = image[i]
        debugextra('initializing {}'.format(ip['proc_name']))
        rp = proc_addr(ip['proc_nr'])
        ip['endpoint'] = rp['p_endpoint']
        rp['p_cpu_time_left'] = 0
        if(i < NR_TASKS):
            rp['p_name'] = ip['proc_name']
        else:
            mb_mod = kinfo['module_list'][i - NR_TASKS]
            ip['start_addr'] = mb_mod['mod_start']
            # TODO check if this can be done with len()
            ip['len'] = mb_mod['mob_end'] - mb_mod['mb_start']

    reset_proc_accounting(rp)

    ''' See if this process is immediately schedulable.
    In that case, set its privileges now and allow it to run.
    Only kernel tasks and the root system process get to run immediately.
    All the other system processes are inhibited from running by the
    RTS_NO_PRIV flag. They can only be scheduled once the root system
    process has set their privileges.'''

    proc_nr = proc_nr(rp)
    
    schedulable_proc = iskernelln(proc_nr) or \
                        isrootsysn(proc_nr) or \
                        proc_nr == VM_PROC_NR

    if(schedulable_proc):
        get_priv(rp, static_priv_id(proc_nr))
        # Privileges for kernel tasks
        if(proc_nr == VM_PROC_NR):
            # TODO Check this priv(rp)
            # priv(rp)->s_flags = VM_F
            # priv(rp)->s_trap_mask = SRV_T
            # priv(rp)-> s_sig)mgr = SELF
            ipc_to_m = SRV_M
            kcall = SRV_KC
            rp['p_priority'] = SRV_Q
            rp['p_quantum_size_ms'] = SRV_QT
        elif(iskernelln(proc_nr)):
            # TODO Check this priv(rp)
            # priv(rp)->s_flags = (IDL_F if proc_nr == IDLE else TSK_F)
            # priv(rp)->s_trap_mask = CSK_T if proc_nr == CLOCK \
            #   proc_nr == SYSTEM else TSK_T
            ipc_to_m = TSK_M  # Allowed targets
            kcalls = TSK_KC  # Allowed kernel calls
        else:
            assert(isrootsysn(proc_nr))
            # TODO Check this priv(rp)
            # priv(rp)['sflags'] = RSYS_F       # priv flags
            # priv(rp)['s_trap_mask'] = SRV_T   # allowed traps
            ipc_to_m = SRV_M                    # allowed targets
            kcalls = SRV_KC                     # allowed kcalls
            # priv(rp)['s_sig_mgr'] = SRV_SM    # sign manager
            rp['p_priority'] = SRV_Q            # priority queue
            rp['p_quantum_size_ms'] = SRV_QT    # quantum size

        # TODO check the entire next block
        '''map = '0'*len(map)
        if(ipc_to_m == ALL_M):
            for j in range(NR_SYS_PROCS):
                set_sys_bit(map,j)

        fill_sendto_mask(rp,map)
        for j in range(SYS_CALL_MASK_SIZE):
            # WTF this line
            priv(rp)['s_k_call_mask']['j'] = 0 if kcall == NO_C else (~0)

        '''
    else:
        # Block process from running
        RTS_SET(rp, RTS_NO_PRIV | RTS_NO_QUANTUM)

    # Arch specific state initialization
    arch_boot_proc(ip, rp)

    # scheduing functions depend on proc_ptr pointing somewhere
    if not get_cpulocal_var(proc_ptr):
        # TODO Check SMP stuffs
        CPULOCAL_STRUCT[0][name] = rp

    # process isn't scheduled until VM has set up a pagetable for it
    if rp['p_nr'] != VM_PROC_NR and rp['p_nr'] >= 0:
        rp['p_rts_flags'] |= RTS_VMINHIBIT
        rp['p_rts_flags'] |= RTS_BOOTINHIBIT

    rp['p_rts_flags'] |= RTS_PROC_STOP
    rp['p_rts_flags'] &= ~RTS_SLOT_FREE
    DEBUGEXTRA('done')

    kinfo['boot_procs'] = image

    for n in [SEND, RECEIVE, SENDREC, NOTIFY, SENDNB, SENDA]:
        assert(n >= 0 and n <= IPCNO_HIGHEST)
        assert(not ipc_call_names[n])
        # TODO check # operator
        # ipc_call_names[n] = #n

    # System and processes initialization
    memory_init()
    DEBUGEXTRA('system_init()...')
    system_init()
    DEBUGEXTRA('done')

    # The bootstrap phase is over, so we can add the physical
    # memory used for ir to the free list
    # TODO Check this
    # kinfo = add_memmap()

    if CONFIG_SMP:
        if config_no_apic:
            BOOT_VERBOSE(
                print('APIC disabled, disables SMP, using legact PIC'))
            smp_single_cpu_fallback()
        elif config_no_smp:
            BOOT_VERBOSE(print('SMP disabled, using legacy'))
            smp_single_cpu_fallback
        else:
            smp_init()
            bsp_finish_booting()
    else:
        '''
        if configured for a single CPU, we are already
        on the kernel stack which we are going to use
        everytime we execute kernel code. We finish
        booting and we never return here'''
        bsp_finish_booting()

    return local_cbi


def __announce():
    print('''
    PYTHONIX
    Join us to make Pythonix better...
    https://github.com/vhpanisa/pythonix'''
          )


def prepare_shutdown(how):
    print('PYTHONIX will now shutdown...')
    # TODO Check tmr_arg functions
    # tmr_arg(&shutdown_timer)->ta_int = how;
    shutdown_timer = set_timer(shutdown_timer,
                               get_monotonic() + system_hz, pythonix_shutdown)


def pythonix_shutdown(tp):
    '''This function is called from prepare_shutdown or stop_sequence to bring
    down PYTHONIX. How to shutdown is in the argument: RBT_HALT (return to the
    monitor), RBT_RESET (hard reset).
    '''
    if CONFIG_SMP:
        # MXCM #
        '''FIXME:
        we will need to stop timers on all cpus if SMP is
        enabled and put them in such a state that we can
        perform the whole boot process once restarted from
        monitor again'''
        if ncpus > 1:
            smp_shutdown_aps()

    hw_intr_disable_all()
    stop_local_timer()
    # TODO check tmr_arg AGAIN
    how = tmr_arg(tp)['ta_int'] if tp else RBT_PANIC

    direct_cls()
    if how == RBT_HALT:
        direct_print('PYTHONIX has halted, you could turn off your computer')
    elif how == RBT_POWEROFF:
        direct_print('PYTHONIX has halted and will now power off.')
    else:
        direct_print('PYTHONIX will now reset.')

    arch_shutdown(how)

    return tp


def cstart():
    '''Perform system initializations prior to calling main().
    Most settings are determined with help of the environment
    strings passed by PYTHONIX loader.
    '''

    # low_level initialization
    prot_init()

    # determine verbosity
    if value == env_get(VERBOSEBOOTVARNAME):
        verboseboot = int(value)

    # Get clock tick frequency
    value = env_get('hz')
    if value:
        system_hz = str(value)
    if not value or system_hz < 2 or system_hz > 50000:  # sanity check
        system_hz = DEFAULT_HZ

    DEBUGEXTRA('cstart')

    # Record misc info for u-space server proc
    kinfo['nr_procs'] = NR_PROCS
    kinfo['nr_tasks'] = NR_TASKS
    kinfo['release'] = OS_RELEASE
    kinfo['version'] = OS_VERSION

    # Load average data initialization
    kloadinfo['proc_last_load'] = 0
    for h in range(_LOAD_HISTORY):
        kloadinfo['proc_load_history'][h] = 0

    if USE_APIC:
        value = env_get('no_apic')
        if(value):
            config_no_apic = int(value)
        else:
            config_no_apic = 1

        value = env_get('apic_timer_x')
        if(value):
            config_apic_timer_x = int(value)
        else:
            config_apic_timer_x = 1

    if USE_WATCHDOG:
        value = env_get(watchdog)
        if value:
            watchdog_enabled = int(value)

    if CONFIG_SMP:
        if(config_no_apic):
            config_no_smp = 1
        value = env_get('no_smp')
        if(value):
            config_no_smp = int(value)
        else:
            config_no_smp = 0

    intr_init(0)
    arch_init()


def get_value(params, name):
    # TODO write this function when boot monitor params are ready
    # Get environment value - kernel version of
    # getenv to avoid setting up the usual environment array.
    return None


def env_get(name):
    return get_value(kinfo['param_buf'], name)


def cpu_print_freq(cpu):
    freq = cpu_get_freq(cpu)
    # TODO check div64u
    print('CPU {} freq {} MHz'.format(cpu, freq))


def is_fpu():
    return get_cpulocal_var(fpu_presence)

if __name__ == '__main__':
    kmain()