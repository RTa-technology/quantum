from qiskit import *
from qiskit.circuit.library.standard_gates import C3XGate, C4XGate, MCXGate
from qiskit.tools.visualization import *
from qiskit import execute, Aer
from math import gcd
from fractions import Fraction
import math
import matplotlib.pyplot as plt
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq.managed import IBMQJobManager

from qiskit import execute, Aer
from qiskit.qasm import pi
from qiskit.tools.visualization import plot_histogram
from qiskit_ibm_provider import IBMProvider
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import RYGate
from qiskit.circuit.add_control import add_control
from qiskit_ibm_provider import least_busy
from qiskit_ibm_runtime import QiskitRuntimeService

import numpy as np

def Swap(qci, s1, s2):
    qci.cx(s1, s2)
    qci.cx(s2, s1)
    qci.cx(s1, s2)

def iqft(qci, q, n):
    for i in range(n):
        for j in range(i):
            qci.cp(-math.pi/float(2**(i-j)), q[i], q[j])
        qci.h(q[i])

while 1:
    N = int(input('Enter an integer N: '))
    print('You entered:', N)
    m = int(input('Enter an integer m: '))
    print('You entered:', m)
    if gcd(N, m) == 1:
        break

bx = 9
print("bx =", bx)
by = 16
print("by =", by)
cn = by
qx = QuantumRegister(bx)
qy = QuantumRegister(by)
c = ClassicalRegister(cn)
qc = QuantumCircuit(qx, qy, c)

for i in range(bx):
    qc.h(qx[i])

for i in range(2**bx):
    X = i
    for j in range(bx):
        if (X & 2**(bx-1)) == 0:
            qc.x(qx[j])
        X = X << 1

    Y = (m**i) % N

    for j in range(by):
        if (Y & 2**bx) != 0:
            if bx == 3:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qy[j]])
            elif bx == 4:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qy[j]])
            elif bx == 5:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qy[j]])
            elif bx == 6:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qx[5], qy[j]])
            elif bx == 7:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qx[5], qx[6], qy[j]])
            elif bx == 8:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qx[5], qx[6], qx[7], qy[j]])
            elif bx == 9:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qx[5], qx[6], qx[7], qx[8], qy[j]])
            elif bx == 10:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qx[5], qx[6], qx[7], qx[8], qx[9], qy[j]])
            elif bx == 11:
                qc.append(MCXGate(bx), [qx[0], qx[1], qx[2], qx[3], qx[4], qx[5], qx[6], qx[7], qx[8], qx[9], qx[10], qy[j]])
            else:
                print("bx is too large")
        Y = Y << 1

    X = i
    for j in range(bx):
        if (X & 2**(bx-1)) == 0:
            qc.x(qx[j])
        X = X << 1

iqft(qc, qx, bx)
if bx == 3:
    Swap(qc, qx[0], qx[2])
elif bx == 4:
    Swap(qc, qx[0], qx[3])
    Swap(qc, qx[1], qx[2])
elif bx == 5:
    Swap(qc, qx[0], qx[4])
    Swap(qc, qx[1], qx[3])
elif bx == 6:
    Swap(qc, qx[0], qx[5])
    Swap(qc, qx[1], qx[4])
    Swap(qc, qx[2], qx[3])
elif bx == 7:
    Swap(qc, qx[0], qx[6])
    Swap(qc, qx[1], qx[5])
    Swap(qc, qx[2], qx[3])
elif bx == 8:
    Swap(qc, qx[0], qx[7])
    Swap(qc, qx[1], qx[6])
    Swap(qc, qx[2], qx[5])
    Swap(qc, qx[3], qx[4])
elif bx == 9:
    Swap(qc, qx[0], qx[8])
    Swap(qc, qx[1], qx[7])
    Swap(qc, qx[2], qx[6])
    Swap(qc, qx[3], qx[5])
elif bx == 10:
    Swap(qc, qx[0], qx[9])
    Swap(qc, qx[1], qx[8])
    Swap(qc, qx[2], qx[7])
    Swap(qc, qx[3], qx[6])
    Swap(qc, qx[4], qx[5])
elif bx == 11:
    Swap(qc, qx[0], qx[10])
    Swap(qc, qx[1], qx[9])
    Swap(qc, qx[2], qx[8])
    Swap(qc, qx[3], qx[7])
    Swap(qc, qx[4], qx[6])
else:
    print("bx is too large")
    exit()

fig = qc.draw(fold=-1)
#print(fig)

for i in range(bx):
    qc.measure(qx[bx-1-i], c[i])
backend_sim = Aer.get_backend('aer_simulator')
r = execute(qc,backend_sim, shots=4096*4).result()
rc = r.get_counts()

print(rc)

x = []
y = []
j=0
for i in r.get_counts():
  c=rc.get(i)
  if c > 600:
    x.append(j)
    y.append(int(i,2))
    j=j+1
y.sort()  
print(x)
print(y)

xx = np.array(x)
yy = np.array(y)

def reg1dim(x, y):
    a = np.dot(x, y)/ (x**2).sum()
    return a

a = reg1dim(xx, yy)
r=round((2**bx)/a)
print("r=",r)

p=m**(r//2)-1
q=m**(r//2)+1
pp=gcd(p,N)
qq=gcd(q,N)
print("N=",N," m=",m," r=",r)
print("p=",int(pp))
print("q=",int(qq))

plt.scatter(xx, yy, color="k")
plt.plot([0,xx.max()], [0, a * xx.max()]) 
# plt.show()

plt=plot_histogram (rc, figsize = (12,7))
# plt.show()