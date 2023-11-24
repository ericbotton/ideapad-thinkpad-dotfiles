import sys
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QMessageBox

class DomainInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Domain Input")

        self.label = QLabel("Enter a domain name:")
        self.input_field = QInputDialog()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        self.setLayout(layout)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.accept)

        layout.addWidget(self.button)

    def get_domain_name(self):
        return self.input_field.text()

def get_domain_ip_address(domain_name):
    import socket
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = DomainInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        domain_name = dialog.get_domain_name()

        ip_address = get_domain_ip_address(domain_name)
        if ip_address is not None:
            QMessageBox.information(None, "IP Address", f"The IP address of {domain_name} is {ip_address}.")
        else:
            QMessageBox.critical(None, "Error", "Could not resolve the IP address of {domain_name}.")

    app.exec_()
