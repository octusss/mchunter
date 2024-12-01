import sys
from mcstatus import JavaServer
from concurrent.futures import ThreadPoolExecutor
import re
import requests  # Import requests to make HTTP requests to the API

# Function to check a single server
def check_server(server_address):
    try:
        # Initialize the Minecraft server object (JavaServer is used for Minecraft servers in v5+)
        server = JavaServer.lookup(server_address)
        
        # Query server status as JSON response
        status = server.status()

        # Extract and clean up the description to remove any color codes
        description = status.description
        cleaned_description = re.sub(r"\u00a7[0-9A-FK-OR]", "", description)  # Remove Minecraft color codes
        
        # Check for "Forge", "white-listed", or whitelist attribute
        if ("Forge" in status.version.name or
            "white-listed" in str(status).lower() or
            "whitelisted" in str(status).lower() or
            "Forge" in str(status).lower() or
            "FML" in str(status).lower() or
            "FML" in status.version.name or
            getattr(status, "whitelist", False)):
            return  # Skip this server if any of these conditions are true
        
        # Check if the description contains the desired strings
        if any(keyword in cleaned_description.lower() for keyword in ["a minecraft server", "smp", "school", "college", "education", ".com", ".net", ".org", ".edu", "stinks", "private", "official"]):
            # Check if the server has more than 2 but less than 20 players online
            
            if 1 <= status.players.online <= 20:
                # Make the API request to check the "cracked" status
                try:
                    response = requests.get(f"https://mcapi.us/server/status?ip={server_address}")
                    response_data = response.json()
                    
                    # Check the online status and determine if the server is cracked
                    if response_data.get("online", False):
                        cracked_status = "no"
                    else:
                        cracked_status = "yes"
                    
                    # Now print the server information after determining the cracked status
                    print(f"Server: {server_address}")
                    print(f"Players online: {status.players.online}")
                    print(f"Version: {status.version.name}")
                    print(f"Description: {cleaned_description}")
                    print(f"Cracked: {cracked_status}")
                    print("-" * 50)
                    
                except requests.RequestException as e:
                    print(f"Error contacting API for {server_address}: {e}")
                    print("-" * 50)

    except Exception as e:
        pass

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 checker.py LIST.txt")
        sys.exit(1)
    
    # Open and read the list of servers from the provided text file
    list_file = sys.argv[1]
    try:
        with open(list_file, "r") as file:
            servers = file.readlines()
            servers = [server.strip() for server in servers]
    except FileNotFoundError:
        print(f"Error: The file {list_file} was not found.")
        sys.exit(1)
    
    # Limit the maximum number of threads to 1000
    max_threads = 10

    # Use ThreadPoolExecutor to limit the number of concurrent threads
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Check each server in the list using threading
        executor.map(check_server, servers)

if __name__ == "__main__":
    main()
