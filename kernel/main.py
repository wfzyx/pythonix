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
    
    # MINIX is now ready. All boot image processes are on the ready queue.
    # Return to the assembly code to start running the current process.
    
    
    # TODO check WTF is this
    #get_cpulocal_var(proc_ptr) = get_cpulocal_var_ptr(idle_proc)
    #get_cpulocal_var(bill_ptr) = get_cpulocal_var_ptr(idle_proc)
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


    
def kmain(local_cbi={}):
    ip = {}
    rp = {}
    
    # TODO check if this is really necessary
    kinfo = local_cbi
    kmess = kinfo['kmess']
    
    machine['board_id'] = get_board_id_by_name(env_get(BOARDVARNAME))
    
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
    
    if(NR_BOOT_MODULES != kinfo['mbi']['mods_count'])
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
        
        
    
#if __name__ == '__main__':