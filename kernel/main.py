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
    
    # TODO check WTF is this
    #get_cpulocal_var(proc_ptr) = get_cpulocal_var_ptr(idle_proc)
    #get_cpulocal_var(bill_ptr) = get_cpulocal_var_ptr(idle_proc)
    announce()
    
    for i in range(NR_BOOT_PROCS - NR_TASKS):
        RTS_UNSET(proc_addr(i), RTS_PROC_STOP)
    
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
    
    
#if __name__ == '__main__':