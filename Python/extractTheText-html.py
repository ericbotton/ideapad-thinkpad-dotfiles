

from tkinter import Tk, Label, Entry, Button
import requests
from bs4 import BeautifulSoup

def extract_plain_text():
    """_summary_"""
    web_address = web_address_entry.get()

    # Make a request to the web page
    response = requests.get(web_address, timeout=5)

    # Parse the HTML response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the plain text from the HTML
    plain_text = soup.get_text()

    # Return the plain text
    return plain_text

def put_plain_text_back_together_into_html_file(plain_text):
    """_summary_Args: plain_text (_type_): _description_"""
    # Create a new HTML file
    html_file = open("plain_text.html", "w", encoding="utf-8")

    # Write the plain text to the HTML file
    html_file.write(plain_text)

    # Close the HTML file
    html_file.close()

    
# def main():
#     """_start here_ build Tk window"""
#     print("Hello World!")

root = Tk()

web_address_label = Label(root, text="Web Address: ")

web_address_entry = Entry(root)

extract_button = Button(root, text="Extract", command=extract_plain_text)

put_plain_text_back_together_button = Button(root, text="Put plain text back together into HTML file", command=put_plain_text_back_together_into_html_file)

web_address_label.grid(row=0, column=0)
web_address_entry.grid(row=0, column=1)
extract_button.grid(row=1, column=0)
put_plain_text_back_together_button.grid(row=1, column=1)

root.mainloop()



# if __name__ == "__main__":
#     main()