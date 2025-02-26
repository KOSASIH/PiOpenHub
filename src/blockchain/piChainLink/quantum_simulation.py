from qiskit import QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector

class QuantumSimulation:
    def __init__(self):
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self):
        """Create a simple quantum circuit."""
        qc = QuantumCircuit(1)  # Single qubit
        qc.h(0)  # Apply Hadamard gate
        qc.t(0)  # Apply T gate
        return qc

    def run(self):
        """Run the quantum simulation."""
        qc = self.create_circuit()
        job = execute(qc, self.backend)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

    def visualize(self, statevector):
        """Visualize the state on the Bloch sphere."""
        plot_bloch_multivector(statevector)
        plt.show()

# Example usage
if __name__ == "__main__":
    simulation = QuantumSimulation()
    statevector = simulation.run()
    print(f"Statevector: {statevector}")
    simulation.visualize(statevector)
