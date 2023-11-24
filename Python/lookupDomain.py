import socket
import pyperclip

domain = input("Enter a domain name: ")
ip_address = socket.gethostbyname(domain)
print("The IP address of", domain, "is", ip_address)
pyperclip.copy(ip_address)


