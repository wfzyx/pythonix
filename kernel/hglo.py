# MXCM #
'''	Global variables used in the kernel. This file contains the declarations;
 	storage space for the variables is allocated in table.c, because EXTERN is
 	defined as extern unless the _TABLE definition is seen. We rely on the 
 	compiler's default initialization (0) for several global variables. '''

# TODO check imports

# Kernel Information Structures
class Global():
	kinfo = {} # Kenel info for users
	machine = {} # machine info for users
	kmessages = {} # diagnostic msgs in kernel
	loadinfo = {} # status of load average
	minix_kerninfo = {}
	# TODO check extern =/= EXTERN
	krandom = {} # gather kernel random info WTF ?!
	# TODO check vir_bytes
	minix_kerninfo_user = {}

	# TODO check necessity for binding and remove later
	kmess = kmessages
	kloadinfo = loadinfo

	# Process scheduling information and kernel reentry count
	vmrequest = {} # first process on vmrequest queue
	lost_ticks = 0	 # clock ticks counted outside clock task
	ipc_call_names[IPCNO_HIGHTEST+1] = '' # human-read call names
	kbill_kcall = {} # process that made kernel call
	kbill_ipc = {} # process that invoked ipc

	# Interrupt related variables
	# TODO check irq_hook	
	irq_hook[NR_IRQ_HOOKS] = {} # hooks for general use
	irq_actids[NR_IRQ_VECTORS] = 0 # IRQ ID bits active
	irq_use = 0 # map of all in-use irq's
	system_hz = 0 # HZ value TODO check u22_t type

	# Misc
	boottime = time.ctime() # TODO check ctime implementation
	verboseboot = 0 # verbose boot, init'ed in cstart

	if DEBUG_TRACE:
		verboseflags = 0

	if USE_APIC:
		config_no_apic
		config_apic_timer_x

	# TODO check u64_t
	cpu_hz[CONFIG_MAX_CPUS]
	def cpu_set_freq(cpu, freq):
		cpu_hz[pcu] = freq

	def cpu_get_freq(cpu):
		return cpu_hz[cpu]

	# TODO implement SMP flag
	# config_no_smp = 1

	# VM
	vm_running = 0
	catch_pagefaults = 0
	kernel_may_alloc = 0

	# Variables thar are init'ed elsewhere are just extern here
	image[NR_BOOT_PROCS] = {} # system image process
	# TODO check how python implement volatile var
	serial_debug_active = 0
	cpu_info[CONFIG_MAX_CPUS] = {}

	# BKL stats
	# TODO u64_t again, next 2 lines
	kernel_ticks[CONFIG_MAX_CPUS] = 0
	bkl_ticks[CONFIG_MAX_CPUS] = 0
	# TODO check Unsigned, 2 lines
	bkl_tries[CONFIG_MAX_CPUS] = 0
	bkl_succ[CONFIG_MAX_CPUS] = 0