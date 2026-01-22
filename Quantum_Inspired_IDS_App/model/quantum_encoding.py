import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def angle_encoding(features):
    """
    Quantum-inspired angle encoding using Qiskit simulator
    """

    num_features = len(features)
    qc = QuantumCircuit(num_features)

    # Apply angle encoding using Ry rotation
    for i, value in enumerate(features):
        qc.ry(value, i)

    # Simulate quantum state
    state = Statevector.from_instruction(qc)

    # Return real part of statevector as features
    quantum_features = np.real(state.data)

    return quantum_features
