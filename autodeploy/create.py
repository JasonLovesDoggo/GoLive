from containerizer.types import Options
import subprocess
import json

def create_gcp_vm(options: Options):
    # Project ID
    project_id = "YOUR_GCP_PROJECT_ID"

    # VM Configuration
    vm_name = "your-vm-name"
    zone = "us-central1-a"  # Example zone
    machine_type = "e2-micro"

    # Create VM with firewall rules
    create_command = [
        "gcloud", "compute", "instances", "create", vm_name,
        "--project", project_id,
        "--zone", zone,
        "--machine-type", machine_type,
        "--tags", "http-server", "https-server",
        "--boot-disk-size", "10GB",
        "--boot-disk-type", "pd-standard",
        "--image-family", "debian-11",
        "--image-project", "debian-cloud"
    ]
    subprocess.run(create_command, check=True)

    # Get and print SSH keys (JSON format)
    get_keys_command = [
        "gcloud", "compute", "instances", "describe", vm_name,
        "--project", project_id,
        "--zone", zone,
        "--format", "json"
    ]
    keys_output = subprocess.run(get_keys_command, capture_output=True, text=True, check=True)
    vm_info = json.loads(keys_output.stdout)
    ssh_keys = vm_info["metadata"]["items"][0]["value"]

    print(f"\nSSH Keys for '{vm_name}':\n{ssh_keys}")
