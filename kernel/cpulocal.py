class Cpulocal:
	# TODO Check SMP override
	def get_cpu_var(self,cpu=0,name):
		return CPULOCAL_STRUCT[cpu][name]

	def get_cpulocal_var(self,name):
		# TODO  check how cpuid is created
		return get_cpu_var(cpuid,name)

	# MXCM #
	# FIXME - padd the structure so that items in the array do not share
	# cacheline with other CPUS
	# TODO check the necessity of implementing local declarations