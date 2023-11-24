#!/bin/bash
# ad hosts 1: https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt
# ad hosts 2: http://sbc.io/hosts/hosts
# Check if the user is root
if [ "$(whoami)" != "root" ]; then
  echo "You must be root to run this script."
  exit 1
fi

# Get the current date and time
current_date_time=$(date +"%Y-%m-%d_%H:%M:%S")

# Create a backup of the hosts file
cp /etc/hosts /etc/hosts.bak.$current_date_time

# Download the new hosts file
# wget https://example.com/hosts
wget http://sbc.io/hosts/hosts -O ./hosts

# Replace the hosts file
mv hosts /etc/hosts

# Set the permission of the hosts file to 644
chmod 644 /etc/hosts

# Restart the networking service
service networking restart

# Check if the hosts file was replaced successfully
if [ -f /etc/hosts ]; then
  echo "The hosts file was replaced successfully."
else
  echo "Failed to replace the hosts file."
fi

