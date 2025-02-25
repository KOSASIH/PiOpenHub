import time
import random ```python
class DeviceMonitor:
    def __init__(self, registry):
        self.registry = registry

    def monitor_device(self, device_id: str) -> None:
        """Monitor the status of a registered device."""
        if device_id not in self.registry.devices:
            raise ValueError(f"Device '{device_id}' is not registered.")
        
        # Simulate monitoring process
        while True:
            status = random.choice(['active', 'inactive', 'error'])
            print(f"Device '{device_id}' status: {status}")
            time.sleep(5)  # Monitor every 5 seconds

# Example usage
if __name__ == "__main__":
    registry = DeviceRegistry()
    registry.register_device('device_1', {'location': 'Room 101', 'status': 'active'})
    monitor = DeviceMonitor(registry)
    monitor.monitor_device('device_1')
