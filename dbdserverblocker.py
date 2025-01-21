import subprocess
import socket

# Define the servers with their region names and corresponding hostnames
SERVERS = {
    "US West (Oregon)": "gamelift.us-west-2.amazonaws.com",
    "US East (North Virginia)": "gamelift.us-east-1.amazonaws.com",
    "South America (São Paulo)": "gamelift.sa-east-1.amazonaws.com",
    "Europe (Frankfurt)": "gamelift.eu-central-1.amazonaws.com",
    "Europe (Ireland)": "gamelift.eu-west-1.amazonaws.com",
    "Asia Pacific (Mumbai)": "gamelift.ap-south-1.amazonaws.com",
    "Asia Pacific (Singapore)": "gamelift.ap-southeast-1.amazonaws.com",
    "Asia Pacific (Sydney)": "gamelift.ap-southeast-2.amazonaws.com",
    "Asia Pacific (Tokyo)": "gamelift.ap-northeast-1.amazonaws.com",
    "Asia Pacific (Seoul)": "gamelift.ap-northeast-2.amazonaws.com"
}

# A dictionary to track blocked servers
blocked_servers = {}

def resolve_hostname_to_ip(hostname):
    """Resolve a hostname to its IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        print(f"[ERROR] Could not resolve hostname: {hostname}")
        return None

def is_server_blocked(region_name):
    """Check if the server is blocked."""
    return blocked_servers.get(region_name, False)

def block_server(region_name):
    """Block a server by region name."""
    rule_name = f"Block-{region_name.replace(' ', '-').replace('(', '').replace(')', '')}"
    hostname = SERVERS[region_name]
    ip_address = resolve_hostname_to_ip(hostname)

    if not ip_address:
        print(f"[ERROR] Unable to block {region_name} as the hostname could not be resolved.")
        return

    if is_server_blocked(region_name):
        print(f"[INFO] Server {region_name} is already blocked.")
        return

    try:
        print(f"[INFO] Blocking server: {region_name}")
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name={rule_name}", "dir=out", "action=block",
             f"remoteip={ip_address}"], check=True
        )
        blocked_servers[region_name] = True
        print(f"[SUCCESS] Server {region_name} blocked.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not block {region_name}. {e}")

def unblock_server(region_name):
    """Unblock a server by region name."""
    if not is_server_blocked(region_name):
        print(f"[INFO] Server {region_name} is not blocked.")
        return

    rule_name = f"Block-{region_name.replace(' ', '-').replace('(', '').replace(')', '')}"

    try:
        print(f"[INFO] Unblocking server: {region_name}")
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"], check=True
        )
        blocked_servers[region_name] = False
        print(f"[SUCCESS] Server {region_name} unblocked.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not unblock {region_name}. {e}")

def block_all_servers():
    """Block all servers."""
    for region_name in SERVERS.keys():
        block_server(region_name)

def unblock_all_servers():
    """Unblock all servers."""
    for region_name in SERVERS.keys():
        unblock_server(region_name)

def list_servers():
    """List available servers and their block status."""
    print("[INFO] Available Servers:")
    for index, (region_name, hostname) in enumerate(SERVERS.items(), 1):
        status = "Blocked" if is_server_blocked(region_name) else "Unblocked"
        print(f"{index}. {region_name}: {hostname} [{status}]")

def main():
    """Main function to manage blocking and unblocking servers."""
    while True:
        print("\nOptions:")
        print("1. List Servers")
        print("2. Block a Server")
        print("3. Unblock a Server")
        print("4. Block All Servers")
        print("5. Unblock All Servers")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            list_servers()
        elif choice == '2':
            list_servers()
            server_choice = input("Enter the number of the server to block: ")
            try:
                server_index = int(server_choice) - 1
                region_name = list(SERVERS.keys())[server_index]
                block_server(region_name)
            except (ValueError, IndexError):
                print("[ERROR] Invalid choice. Please select a valid server number.")
        elif choice == '3':
            list_servers()
            server_choice = input("Enter the number of the server to unblock: ")
            try:
                server_index = int(server_choice) - 1
                region_name = list(SERVERS.keys())[server_index]
                unblock_server(region_name)
            except (ValueError, IndexError):
                print("[ERROR] Invalid choice. Please select a valid server number.")
        elif choice == '4':
            block_all_servers()
        elif choice == '5':
            unblock_all_servers()
        elif choice == '6':
            print("[INFO] Exiting.")
            break
        else:
            print("[ERROR] Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()
