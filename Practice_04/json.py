import json

# Load simplified JSON file
with open("sample-data-simple.json") as f:
    data = json.load(f)

print("Interface Status")
print("="*79)
print(f"{'DN':50} {'Speed':6} {'MTU':6}")
print("-"*50, "-"*6, "-"*6)

# Iterate through each interface directly
for item in data:
    dn = item.get("DN", "")
    speed = item.get("SPEED", "")
    mtu = item.get("MTU", "")
    
    print(f"{dn:50} {speed:6} {mtu:6}")

# Example Output:
# Interface Status
# ===============================================================================
# DN                                                 Speed  MTU  
# -------------------------------------------------- ------ ------
# topology/pod-1/node-201/sys/phys-[eth1/33]       inherit 9150 
# topology/pod-1/node-201/sys/phys-[eth1/34]       inherit 9150 
# topology/pod-1/node-201/sys/phys-[eth1/35]       inherit 9150