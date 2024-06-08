import opentofu as tof  # Import OpenTOFU library

# Define VPS Configuration
config = {
    "provider": "your_provider",    # e.g., "digitalocean", "linode", etc.
    "region": "your_region",        # e.g., "nyc3", "lon1", etc.
    "size": "your_size",            # e.g., "s-1vcpu-1gb", "g-2vcpu-8gb", etc.
    "image": "your_image",          # e.g., "ubuntu-22-04-x64", "debian-11-x64"
    "ssh_keys": ["your_ssh_key"],   # Array of SSH key fingerprints
}

# Create VPS
server = tof.create_server(config)

# Check if server creation was successful
if server is not None:
    # Get SSH connection information
    ssh_user = server.get("ssh_user")
    ssh_host = server.get("ip_address")

    # Create SSH client (replace with your preferred SSH library)
    ssh = tof.create_ssh_client(ssh_user, ssh_host)

    if ssh.connect(): # Check if connected to VPS
        # Update package lists
        ssh.run("sudo apt update")

        # Upgrade packages
        ssh.run("sudo apt upgrade -y")

        # Install or update specific dependencies
        # ... (Example: Install Python)
        ssh.run("sudo apt install -y python3 python3-pip")

        # ... (Additional commands as needed)
        ssh.close()  # Close SSH connection

        # ... (Optional: Run your application's setup)
        # ... (Example: Install and configure Caddy)
        # ssh.run(...)

    else:
        print("Error connecting to VPS.")
else:
    print("Error creating VPS.")
