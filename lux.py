"""
lux.py is the main module to run client side
"""
import argparse
import sys
from socket import error as SocketError
from PySide6.QtWidgets import QApplication, QMessageBox
from luxwindow import LuxWindow

def main():
    """
    Main function that runs the application
    """
    # parse command line args
    parser = argparse.ArgumentParser(description='Client for the YUAG application')
    parser.add_argument("host", help="the host on which the server is running")
    parser.add_argument("port", help="the port at which the server is listening")
    args = parser.parse_args()

    host = args.host
    port = int(args.port)

    # create the Gui app
    app = QApplication(sys.argv)
    window = LuxWindow(host, port)
    window.show()

    try:
        # run app
        exit_code = app.exec()
        sys.exit(exit_code)
    except SocketError as e_error:
        # display error message to the user
        error_message = f"Unable to connect to server: {e_error}"
        QMessageBox.critical(window, "Error", error_message)

# Main function that executes our application
if __name__ == '__main__':
    main()
