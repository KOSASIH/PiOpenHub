class DeviceRegistry:
    def __init__(self):
        self.devices = {}

    def register_device(self, device_id: str, device_info: dict) -> None:
        """Register a new device."""
        if device_id in self.devices:
            raise ValueError(f"Device '{device_id}' is already registered.")
        self.devices[device_id] = device_info
        print(f"Device '{device_id}' registered successfully.")

    def get_device_info(self, device_id: str) -> dict:
        """Retrieve information about a registered device."""
        if device_id not in self.devices:
            raise ValueError(f"Device '{device_id}' is not registered.")
        return self.devices[device_id]

# Example usage
if __name__ == "__main__":
    registry = DeviceRegistry()
    registry.register_device('device_1', {'location': 'Room 101', 'status': 'active'})
    print("Device Info:", registry.get_device_info('device_1'))
