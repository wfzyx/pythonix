PYTHONIX
========

Python/Minix based operating system

The goal is to build an OS with the following characteristics :

* Availability and reliability
* Low resource consumption
* Portability and embedded computing
* Open-source ( MIT )
* Easy learning and maintenance

Documentation and Resources
---------------------------

* Operating Systems: Design And Implementation 3rd Edition by Andrew Tanenbaum
* git://git.minix3.org/minix # minix3 src, the basis for the development of Pythonix
* http://legacy.python.org/dev/peps/pep-0008/ # Style-Guide Python
* http://wiki.osdev.org/Main_Page # wiki for helping in OS development
* docs/TRANSLATION-GUIDE # Guide for C/Python translation
 
ROADMAP
-------

1. Translate /kernel to Python3 without SMP # Started<br/>
  1.2. Sys_calls, kernel dependencies<br/>
  1.1. Initially *.c files (clock, interrupt, ipc, vm, system, main, proc) # In Progress<br/>
  1.2. Search for dependencies and solve TODO to run *.py files # Waiting<br/>
  1.3. Make units test, and make kernel run without panic # Waiting<br/>
2. Translate /drivers to Python3
3. Translate /sys and start to make FS, and other basic stuff
4. Make applications, cat, echo , pwd, rm, ls, and others
5. Network and extra drivers
6. Package Manager
7. SMP suppport


FAQ
---

**Q**: How is possible to boot a Python O.S ? 

**A**: Actually, isn't possible. All the kernel, user-space, and applications
will be made in Python, but the bootloader and the lowest level will
run over another future project in Clang with a implementation of PyPy 
with a JIT compiler, which makes the system viable. See [Pythonix Overview](docs/images/overview.png) for details.

=====

**Q**: Why develop based on Minix and not on Linux or BSD for example?

**A**: Linux already has a highly developed kernel and code base very
large, and yet can not be a system with fully modular architecture
due to its monolithic nature, because Minix microkernel nature it's allows
ease functions to modularize the system , thereby improving the portability
and kernel security , besides being a project with reduced code base .

=====

**Q**: Why Python is a good choice to write an OS ?

**A**: Because it is a specification that is implemented in several languages, has
high portability (eg: IronPython , Jython ). In addition to being interpreted
this eliminates situations like the kernel compile, moreover, PyPy implementation
with JIT compilation proved be a reliable choice.

=====

**Q**: A kernel will be slow in a interpreted language ?

**A**: Not necessarily , it depends on the implementation and internal optimizations made
targeting performance , the Python implementation done in Python ( PyPy ) , proved
achieve a superior performance over the original implementation written in C,
and in some cases, even faster than C!
As seen in: [PyPy](http://speed.pypy.org/)
Or [PyPy > C](http://morepypy.blogspot.com.br/2011/02/pypy-faster-than-c-on-carefully-crafted.html)
Or [PyPy > C (yes,again)](http://morepypy.blogspot.com.br/2011/08/pypy-is-faster-than-c-again-string.html)

=====

**Q**: Why Python 3.x ?

**A**: Python 2.7 is only justifiable when a project has some lib legacy
or some resource that will be lost if the project is porteda to a more 
recent version. In the case of developing an operating system from scratch ,
literally speaking , it is good practice to always try to use the newest version
of Python, and where necessary implement own extensions

=====

**Q**: Why not use ctypes to write functions more accurately to original? 

**A**: The purpose of writing the OS in Python, and enables the ease of 
maintenance is to avoid as much use any kind of dependencies and libraries 
to non-essential to Python, allowing a clean and easy to understand code.

=====

**Q**: Why not just quit?

**A**: Because great guys already show some support, so the idea worth it
![](docs/images/guido.jpg)
![](docs/images/ast.jpg)
![](docs/images/arigo.jpg)
![](docs/images/ben.jpg)
