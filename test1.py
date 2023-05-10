# 必要なライブラリをインポート
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram

# XORゲート
def xor_gate(qc, a, b, output):
    qc.cx(a, output)
    qc.cx(b, output)

# ANDゲート
def and_gate(qc, a, b, output):
    qc.ccx(a, b, output)

# NANDゲート
def nand_gate(qc, a, b, output):
    qc.ccx(a, b, output)
    qc.x(output)

# ORゲート
def or_gate(qc, a, b, output):
    qc.cx(a, output)
    qc.cx(b, output)
    qc.ccx(a, b, output)

# サンプル回路
def sample_circuit(gate_function):
    qc = QuantumCircuit(3)
    qc.x(0) # 入力ビットを設定
    qc.x(1) # 入力ビットを設定
    gate_function(qc, 0, 1, 2) # 選択したゲートを実行
    return qc

# サンプル回路を表示
gate_functions = [xor_gate, and_gate, nand_gate, or_gate]
gate_names = ['XOR', 'AND', 'NAND', 'OR']

for gate_function, gate_name in zip(gate_functions, gate_names):
    qc = sample_circuit(gate_function)
    print(f"{gate_name}ゲート")
    print(qc)
