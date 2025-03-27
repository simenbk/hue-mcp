from phue import Bridge
from config import HUE_IP, HUE_USERNAME

def main():
    print("Hello from hue-mcp!")

    b = Bridge(ip=HUE_IP, username=HUE_USERNAME)
    b.connect()
    # print(b.get_api())p
    b.set_light(1, 'bri', 100)


if __name__ == "__main__":
    main()
