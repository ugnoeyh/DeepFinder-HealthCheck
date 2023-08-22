MUTE_FILE = "mute.txt"

def mute_ip(ip_address):
    with open("mute.txt", "a") as file:
        file.write(ip_address + "\n")

def get_muted_ips():
    with open("mute.txt", "r") as file:
        return [ip.strip() for ip in file.readlines()]

def unmute_ip(ip_address):
    muted_ips = get_muted_ips()
    if ip_address in muted_ips:
        muted_ips.remove(ip_address)
        with open("mute.txt", "w") as file:
            for ip in muted_ips:
                file.write(ip + "\n")
        return True
    return False
