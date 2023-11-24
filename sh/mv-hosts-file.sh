#!/bin/bash

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
hosts_list=${HOME}/Shared/ad-hosts.txt
wget http://sbc.io/hosts/alternates/fakenews/hosts -O $hosts_list

# Replace the hosts file
mv $hosts_list /etc/hosts

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
EOF
