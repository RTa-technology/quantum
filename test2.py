from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram
from tabulate import tabulate
import matplotlib.pyplot as plt


def xor_gate(qc, a, b, output):
    qc.cx(a, output)
    qc.cx(b, output)

def and_gate(qc, a, b, output):
    qc.ccx(a, b, output)

def nand_gate(qc, a, b, output):
    qc.ccx(a, b, output)
    qc.x(output)

def or_gate(qc, a, b, output):
    qc.cx(a, output)
    qc.cx(b, output)
    qc.ccx(a, b, output)

def execute_circuit(qc):
    qc.measure_all()
    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    result = backend.run(transpiled_circuit).result()
    return result.get_counts()



input_combinations = [(0, 0), (0, 1), (1, 0), (1, 1)]

gate_functions = [xor_gate, and_gate, nand_gate, or_gate]
gate_names = ['XOR', 'AND', 'NAND', 'OR']



def print_result(input_bits, result):
    output_bit = list(result.keys())[0][-1]
    return [input_bits[0], input_bits[1], output_bit]

def print_circuit_and_results(qc, result):
    circuit_text = qc.draw('text', fold=60)
    print(circuit_text)
    print(tabulate([result], headers=["q_0", "q_1", "q_2"]))





headers = ["q_0", "q_1", "c_0"]
for gate_function, gate_name in zip(gate_functions, gate_names):
    print(f"{gate_name}ゲートの結果:")
    for inputs in input_combinations:
        qc = QuantumCircuit(3)
        if inputs[0]:
            qc.x(0)
        if inputs[1]:
            qc.x(1)
        gate_function(qc, 0, 1, 2)
        result = execute_circuit(qc)
        result_table = print_result(inputs, result)
        print_circuit_and_results(qc, result_table)
    print()