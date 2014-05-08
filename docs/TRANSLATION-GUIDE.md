Pythonix C/Python Translation-Guide

=====

Functions and variables of type "static" that are private to the module, state with 
the convention to prefix with two underscores 

static int try_async(); -> __try_async()
static void enqueue_head(); -> __enqueue_head()

---

All the functions treated as pointers, they should take the parameters by value and 
unpack the results in the proper parameters, except for dictionaries and lists 
which act as pointers naturally 

static void set_idle_name(char * name, int n) -> def set_idle_name(name,n): ... return name
set_idle_name(&name,n)  ->  name = set_idle_name(name,n)

---

All structs are simple dictionaries in Python, because structs can't take initial values
in C, a empty dict is enough to do the parity

struct proc * pick_proc -> pick_proc = {}

---

Simple for loops can be converted to for in range

for (i = 0; i < CONFIG_MAX_CPUS; i++) -> for i in range(CONFIG_MAX_CPUS)

Different for can be made with while and some tweaks


for (sp = BEG_PRIV_ADDR, i = 0; sp < END_PRIV_ADDR; ++sp, ++i){
...code...
}

This can be translated to

sp = BEG_PRIV_ADDR
i = 0
while sp < END_PRIV_ADDR:
    ...code...
    sp += 1
    i += 1
    
This tweaks are neeeded because the missing of classical for in Python

---

Headers (*.h) files are probably to become Python classes, with the parity file initiated with a 'h'.

see kernel/glo.c -> kernel/hglo.py for example
