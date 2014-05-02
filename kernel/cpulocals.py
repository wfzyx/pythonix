class Cpulocals:
    # TODO Check SMP override
    def get_cpu_var(self, name, cpu=0):
        return CPULOCAL_STRUCT[cpu][name]

    def get_cpulocal_var(self, name):
        # TODO  check how cpuid is created
        return get_cpu_var(name, cpuid)

    # MXCM #
    # FIXME - padd the structure so that items in the array do not share
    # cacheline with other CPUS