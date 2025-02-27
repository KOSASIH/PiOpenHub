# src/main/services/monitoring_system.py

import time
import subprocess
import logging
import smtplib
from email.mime.text import MIMEText
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from qiskit import Aer
from qiskit.circuit.library import QuantumFeatureMap
from qiskit_machine_learning.algorithms import QSVC
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(filename='service_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ServiceMonitor:
    def __init__(self, services, check_interval=10):
        self.services = services  # List of services to monitor
        self.check_interval = check_interval  # Time interval between checks
        self.performance_data = []  # Store performance metrics for anomaly detection
        self.quantum_backend = Aer.get_backend('aer_simulator')
        self.isolation_forest = IsolationForest(contamination=0.1)  # Classical anomaly detection model

    def check_service(self, service):
        """Check if a service is running."""
        try:
            result = subprocess.run(['pgrep', '-f', service], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0  # Return True if the service is running
        except Exception as e:
            logging.error(f"Error checking service {service}: {e}")
            return False

    def restart_service(self, service):
        """Restart a service."""
        try:
            subprocess.run(['systemctl', 'restart', service], check=True)
            logging.info(f"Service {service} restarted successfully.")
            self.send_notification(service, "Service Restarted", f"The service {service} has been restarted.")
        except Exception as e:
            logging.error(f"Failed to restart service {service}: {e}")

    def send_notification(self, service, subject, message):
        """Send a notification email."""
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = 'monitor@example.com'
            msg['To'] = 'admin@example.com'

            with smtplib.SMTP('localhost') as server:
                server.send_message(msg)
            logging.info(f"Notification sent for service {service}.")
        except Exception as e:
            logging.error(f"Failed to send notification for service {service}: {e}")

    def monitor_services(self):
        """Monitor the services continuously."""
        while True:
            for service in self.services:
                if not self.check_service(service):
                    logging.warning(f"Service {service} is down. Attempting to restart...")
                    self.restart_service(service)
                else:
                    # Simulate performance metrics for anomaly detection
                    self.record_performance_metrics(service)

            # Check for anomalies
            self.detect_anomalies()
            time.sleep(self.check_interval)

    def record_performance_metrics(self, service):
        """Record performance metrics for the service."""
        # Simulate performance data (e.g., CPU usage, response time)
        cpu_usage = np.random.rand()  # Simulated CPU usage
        response_time = np.random.rand()  # Simulated response time
        self.performance_data.append([service, cpu_usage, response_time])

    def detect_anomalies(self):
        """Detect anomalies in service performance using classical and quantum methods."""
        if len(self.performance_data) < 10:  # Ensure we have enough data
            return

        # Convert performance data to DataFrame
        df = pd.DataFrame(self.performance_data, columns=['Service', 'CPU Usage', 'Response Time'])
        X = df[['CPU Usage', 'Response Time']].values

        # Fit Isolation Forest for classical anomaly detection
        self.isolation_forest.fit(X)
        anomalies = self.isolation_forest.predict(X)

        # Log anomalies
        for i, anomaly in enumerate(anomalies):
            if anomaly == -1:  # Anomaly detected
                                  logging.warning(f"Anomaly detected in service {df.iloc[i]['Service']} with metrics: {df.iloc[i][1:].values}")

        # Quantum anomaly detection (using QSVC)
        self.quantum_anomaly_detection(X)

    def quantum_anomaly_detection(self, X):
        """Detect anomalies using a quantum support vector classifier."""
        feature_map = QuantumFeatureMap(feature_dimension=X.shape[1], reps=2)
        qsvc = QSVC(quantum_instance=self.quantum_backend, feature_map=feature_map)

        # Fit the quantum model
        qsvc.fit(X, np.ones(X.shape[0]))  # Dummy labels for fitting

        # Predict anomalies
        predictions = qsvc.predict(X)
        for i, prediction in enumerate(predictions):
            if prediction == -1:  # Anomaly detected
                logging.warning(f"Quantum anomaly detected in service with metrics: {X[i]}")

    def visualize_performance(self):
        """Visualize the performance metrics of the services."""
        if not self.performance_data:
            logging.warning("No performance data to visualize.")
            return

        df = pd.DataFrame(self.performance_data, columns=['Service', 'CPU Usage', 'Response Time'])
        plt.figure(figsize=(12, 6))
        for service in df['Service'].unique():
            service_data = df[df['Service'] == service]
            plt.plot(service_data['CPU Usage'], label=f'{service} CPU Usage')
            plt.plot(service_data['Response Time'], label=f'{service} Response Time')

        plt.title('Service Performance Metrics')
        plt.xlabel('Time')
        plt.ylabel('Metrics')
        plt.legend()
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    services_to_monitor = [
        'quantum_data_analysis.py',
        'quantum_cryptography.py',
        'market_prediction.py',
        'quantum_portfolio_optimization.py',
        'quantum_anomaly_detection.py',
        'quantum_recommendation_system.py'
    ]

    monitor = ServiceMonitor(services=services_to_monitor, check_interval=10)
    try:
        monitor.monitor_services()
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
        monitor.visualize_performance()
