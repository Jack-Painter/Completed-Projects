import requests
import urllib3

# 1. Setup: Disable SSL warnings for lab/internal devices
urllib3.disable_warnings()

# 2. Variables: Set your login info and the list of switch IPs
username = "admin"
password = "yourpassword123"
device_list = ["172.16.0.35", "172.16.0.36", "172.16.0.37"]

# 3. Headers: Tell the router we are talking in 'JSON'
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

print("--- Starting Hostname Audit ---")

for ip in device_list:
    # Define our 'target' name - e.g., LON-SW-172.16.0.35
    target_name = f"LON-SW-{ip}"
    
    # The specific URL (YANG Model) for the hostname
    url = f"https={ip}/restconf/data/Cisco-IOS-XE-native:native/hostname"
    
    print(f"Checking {ip}...")

    # STEP A: Ask the router what its current name is (GET)
    response = requests.get(url, headers=headers, auth=(username, password), verify=False)

    if response.status_code == 200:
        current_name = response.json()["Cisco-IOS-XE-native:hostname"]
        
        if current_name == target_name:
            print(f"  [OK] {ip} is already named correctly.")
        else:
            print(f"  [MISMATCH] Found {current_name}. Updating to {target_name}...")
            
            # STEP B: Send the update (PUT)
            payload = {"Cisco-IOS-XE-native:hostname": target_name}
            update = requests.put(url, json=payload, headers=headers, auth=(username, password), verify=False)
            
            if update.status_code == 204:
                print(f"  [SUCCESS] {ip} updated.")
            else:
                print(f"  [FAILED] Could not update {ip}.")
    else:
        print(f"  [ERROR] Cannot connect to {ip}. Code: {response.status_code}")

print("--- Task Complete ---")
