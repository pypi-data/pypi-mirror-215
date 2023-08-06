from patchelfy import Patchelf

p = Patchelf("./nopeeking")
p.log(0x1651, "mmap returned 0x%lx\\n", ["rax"])
p.log(0x1651, "I'm at address: 0x%lx\\n", [0x1651])
p.log(0x1651, "This is a log\\n", [])
p.log(0x1662, "rcx: %ld\\n", ["rcx"])
p.save("./nopeeking_test")
from pwn import *
#p = process("./nopeeking_test", aslr=False)
#p.recvline().strip() == b"mmap returned 0x155555511000"
#p.recvline().strip() == b"rcx: 33"

from gdb_plus import *
dbg = Debugger("./nopeeking_test").set_split_on_fork(interrupt=True)
dbg.c()
pid = dbg.wait_split()
child = dbg.children[pid]
# just want to test if it is faster
dbg = dbg.split_child(n=1)
dbg.emulate_ptrace(manual=False)
child.emulate_ptrace(manual=False)
dbg.b(0x154c)
child.b(0x154c)
child.c(wait=False)
dbg.c(wait=False)