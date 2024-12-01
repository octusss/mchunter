import ipaddress

def convert_ips_to_cidr(input_file, output_file):
    # Read the IP addresses from the input file
    with open(input_file, 'r') as infile:
        ips = infile.readlines()

    # Remove any whitespace and duplicates
    ips = set(ip.strip() for ip in ips)

    # Open the output file to write the results
    with open(output_file, 'w') as outfile:
        for ip in ips:
            # Convert each IP to /24 CIDR notation
            try:
                # Create an IPv4 network object with /24 CIDR
                network = ipaddress.IPv4Network(f"{ip}/24", strict=False)
                # Write the network address with /24 CIDR
                outfile.write(str(network.network_address) + '/24' + '\n')
            except ValueError:
                print(f"Invalid IP address: {ip}")

# Input and output files
input_file = "RANDOMMM.txt"  # Input file containing the list of IP addresses
output_file = "output_cidrs.txt"  # Output file to save the CIDR notations

# Convert and write CIDR blocks to the output file
convert_ips_to_cidr(input_file, output_file)

print("CIDR conversion complete. Check the output file.")
