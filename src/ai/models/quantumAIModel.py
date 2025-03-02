import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pennylane as qml

# Definisikan perangkat quantum
dev = qml.device("qiskit.aer", wires=2)

# Definisikan sirkuit quantum
@qml.qnode(dev)
def quantum_circuit(weights, x):
    # Memasukkan data ke dalam sirkuit
    for i in range(len(x)):
        qml.RX(x[i], wires=i)
    # Menambahkan gerbang parameterized
    qml.CNOT(wires=[0, 1])
    qml.RY(weights[0], wires=0)
    qml.RY(weights[1], wires=1)
    return qml.expval(qml.PauliZ(1))

class QuantumAIModel:
    def __init__(self, data):
        self.data = data
        self.model_weights = np.random.rand(2)  # Inisialisasi bobot model
        self.scaler = StandardScaler()

    def preprocess_data(self):
        # Menghapus nilai yang hilang
        self.data.dropna(inplace=True)
        # Memisahkan fitur dan target
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        # Normalisasi data
        X = self.scaler.fit_transform(X)
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self, epochs=100):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        for epoch in range(epochs):
            for x, y in zip(X_train, y_train):
                # Menghitung loss dan memperbarui bobot
                loss = self.loss_function(x, y)
                self.update_weights(x, y)
        # Evaluasi model
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f'Model accuracy: {accuracy:.2f}')

    def loss_function(self, x, y):
        # Hitung loss berdasarkan prediksi
        pred = quantum_circuit(self.model_weights, x)
        return (pred - y) ** 2

    def update_weights(self, x, y, learning_rate=0.1):
        # Pembaruan bobot menggunakan gradien
        for i in range(len(self.model_weights)):
            # Hitung gradien
            grad = (quantum_circuit(self.model_weights + np.array([0.01 if j == i else 0 for j in range(len(self.model_weights))]), x) - 
                     quantum_circuit(self.model_weights - np.array([0.01 if j == i else 0 for j in range(len(self.model_weights))]), x)) / 0.02
            self.model_weights[i] -= learning_rate * grad

    def predict(self, new_data):
        new_data = self.scaler.transform(new_data)
        predictions = [1 if quantum_circuit(self.model_weights, x) > 0 else 0 for x in new_data]
        return predictions

# Contoh penggunaan
if __name__ == "__main__":
    # Mengimpor data
    data = pd.read_csv('data.csv')  # Ganti dengan path ke dataset Anda
    quantum_ai_model = QuantumAIModel(data)
    quantum_ai_model.train_model(epochs=100)

    # Contoh prediksi dengan data baru
    new_data = np.array([[5.1, 3.5, 1.4, 0.2]])  # Ganti dengan fitur yang sesuai
    prediction = quantum_ai_model.predict(new_data)
    print(f'Prediksi untuk data baru: {prediction}')
