# hue_connection.py
from phue import Bridge

def setup_bridge(bridge_ip=None, bridge_username=None):
    """Setup and return a Bridge connection"""
    bridge = Bridge(bridge_ip, bridge_username)
    bridge.connect()
    return bridge

# Test connection
if __name__ == "__main__":
    bridge = setup_bridge()
    print("Connected to bridge successfully")
    print("Available lights:", bridge.get_light_objects('name').keys())
