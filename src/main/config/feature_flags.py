import os
import json

class FeatureFlags:
    def __init__(self, flags_file='feature_flags.json'):
        self.flags_file = flags_file
        self.flags = self.load_flags()

    def load_flags(self):
        """Load feature flags from a JSON file."""
        if os.path.exists(self.flags_file):
            with open(self.flags_file, 'r') as f:
                return json.load(f)
        return {}

    def save_flags(self):
        """Save feature flags to a JSON file."""
        with open(self.flags_file, 'w') as f:
            json.dump(self.flags, f, indent=4)

    def is_feature_enabled(self, feature_name):
        """Check if a feature is enabled."""
        return self.flags.get(feature_name, False)

    def enable_feature(self, feature_name):
        """Enable a feature."""
        self.flags[feature_name] = True
        self.save_flags()

    def disable_feature(self, feature_name):
        """Disable a feature."""
        self.flags[feature_name] = False
        self.save_flags()

    def set_feature(self, feature_name, enabled):
        """Set the status of a feature."""
        self.flags[feature_name] = enabled
        self.save_flags()

    def list_features(self):
        """List all feature flags and their statuses."""
        return self.flags

# Example usage
if __name__ == "__main__":
    feature_flags = FeatureFlags()

    # Enable a feature
    feature_flags.enable_feature('self_healing')
    print("Enabled features:", feature_flags.list_features())

    # Check if a feature is enabled
    if feature_flags.is_feature_enabled('self_healing'):
        print("Self-healing feature is enabled.")

    # Disable a feature
    feature_flags.disable_feature('self_healing')
    print("Enabled features after disabling:", feature_flags.list_features())
