# hue_mcp_server.py
from mcp.server.fastmcp import FastMCP
from phue import Bridge
import json

# Import our bridge setup function
from hue_connection import setup_bridge

from config import HUE_IP, HUE_USERNAME

# Connect to the Hue Bridge
bridge = setup_bridge(HUE_IP, HUE_USERNAME)

# Create MCP server
mcp = FastMCP(name="Philips Hue Controller", 
                description="Control Philips Hue lights in your home")

# Tool to list all available lights
@mcp.tool()
async def list_lights(request):
    """List all available Philips Hue lights"""
    lights = bridge.get_light_objects('name')
    result = {name: {"on": light.on, "brightness": light.brightness} 
              for name, light in lights.items()}
    return {"lights": result}

# Tool to control specific lights
@mcp.tool()
async def control_light(request, light_name: str, on: bool = None, 
                        brightness: int = None, color: str = None):
    """
    Control a specific Philips Hue light
    
    Args:
        light_name: Name of the light to control
        on: Turn the light on (True) or off (False)
        brightness: Set brightness (0-254)
        color: Set color (as string name like "red", "blue", etc.)
    """
    lights = bridge.get_light_objects('name')
    
    if light_name not in lights:
        return {"error": f"Light '{light_name}' not found. Available lights: {', '.join(lights.keys())}"}
    
    light = lights[light_name]
    
    # Apply requested changes
    if on is not None:
        light.on = on
    
    if brightness is not None:
        if brightness < 0 or brightness > 254:
            return {"error": "Brightness must be between 0 and 254"}
        light.brightness = brightness
    
    if color is not None:
        # Simple color mapping - in a real implementation you would use proper XY or HSV values
        color_map = {
            "red": [0, 254],  # [hue, saturation]
            "green": [25500, 254],
            "blue": [46920, 254],
            "yellow": [12750, 254],
            "purple": [56100, 254],
            "white": [0, 0]
        }
        
        if color.lower() in color_map:
            hue, sat = color_map[color.lower()]
            light.hue = hue
            light.saturation = sat
        else:
            return {"error": f"Unknown color: {color}. Available colors: {', '.join(color_map.keys())}"}
    
    # Return current state
    return {
        "light": light_name,
        "state": {
            "on": light.on,
            "brightness": light.brightness
        }
    }

# Tool specifically for living room lights
@mcp.tool()
async def living_room_lights(request, action: str, brightness: int = None, color: str = None):
    """
    Control all lights in the living room
    
    Args:
        action: Either "on", "off", or "status"
        brightness: Set brightness level (0-254)
        color: Set color of all living room lights
    """
    # Assuming you have two lights in the living room
    lights = bridge.get_light_objects('name')
    
    # Find living room lights - adjust these names to match your actual light names
    living_room_lights = []
    for name, light in lights.items():
        if "living" in name.lower() or "room" in name.lower():
            living_room_lights.append((name, light))
    
    if not living_room_lights:
        return {"error": "No living room lights found. Please check your light names."}
    
    if action.lower() == "status":
        return {
            "living_room_lights": {
                name: {"on": light.on, "brightness": light.brightness}
                for name, light in living_room_lights
            }
        }
    
    # Apply the requested action to all living room lights
    for name, light in living_room_lights:
        if action.lower() == "on":
            light.on = True
        elif action.lower() == "off":
            light.on = False
            
        if brightness is not None:
            if brightness < 0 or brightness > 254:
                return {"error": "Brightness must be between 0 and 254"}
            light.brightness = brightness
            
        if color is not None:
            color_map = {
                "red": [0, 254],
                "green": [25500, 254],
                "blue": [46920, 254],
                "yellow": [12750, 254],
                "purple": [56100, 254],
                "white": [0, 0]
            }
            
            if color.lower() in color_map:
                hue, sat = color_map[color.lower()]
                light.hue = hue
                light.saturation = sat
    
    return {
        "success": True,
        "message": f"Living room lights turned {action.lower()}"
    }

if __name__ == "__main__":
    # Run the server on localhost
    mcp.run(transport="stdio")
