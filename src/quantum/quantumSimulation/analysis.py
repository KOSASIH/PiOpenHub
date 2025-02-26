# quantumSimulation/analysis.py

import matplotlib.pyplot as plt

def analyze_results(counts):
    """Analyze the simulation results and calculate probabilities."""
    total_counts = sum(counts.values())
    probabilities = {key: value / total_counts for key, value in counts.items()}

    print("Analysis of Results:")
    for state, probability in probabilities.items():
        print(f"Probability of {state}: {probability:.2f}")

    return probabilities

def plot_results(probabilities):
    """Plot the probabilities of the measurement results."""
    states = list(probabilities.keys())
    values = list(probabilities.values())

    plt.bar(states, values, color='blue')
    plt.xlabel('States')
    plt.ylabel('Probability')
    plt.title('Measurement Probabilities')
    plt.ylim(0, 1)
    plt.xticks(states)
    plt.grid(axis='y')

    # Show the plot
    plt.show()

# Example usage
if __name__ == "__main__":
    from quantumSimulation.quantum_process import simulate_quantum_process

    # Simulate a quantum process and analyze the results
    counts = simulate_quantum_process()
    probabilities = analyze_results(counts)
    plot_results(probabilities)
