import urllib.request
import time
import threading

class InternetConnectionMonitor:
    def __init__(self):
        self.is_online = False
        self.connection_monitor_thread = None

    def check_internet_connection(self):
        """
        Check if there is an active internet connection.
        Returns True if connected, False otherwise.
        """
        try:
            urllib.request.urlopen('https://www.google.com', timeout=5)
            return True
        except:
            return False

    def offline_code(self):
        """
        This function will be executed when the system is offline.
        Add your offline-specific code here.
        """
        print("Offline mode activated.")
        # Add your offline code here
        # For example:
        # - Perform local data processing
        # - Access local resources
        # - Queue up tasks for later synchronization

    def online_code(self):
        """
        This function will be executed when the system is online.
        Add your online-specific code here.
        """
        print("Online mode activated.")
        # Add your online code here
        # For example:
        # - Synchronize data with a remote server
        # - Upload queued tasks
        # - Access online resources

    def connection_monitor(self):
        """
        This function runs the internet connection check loop in a separate thread.
        """
        while True:
            if self.check_internet_connection():
                if not self.is_online:
                    self.is_online = True
                    self.online_code()
            else:
                if self.is_online:
                    self.is_online = False
                    self.offline_code()
            time.sleep(5)  # Check the connection every 5 seconds

    def start_monitoring(self):
        """
        Start the internet connection monitoring in a separate thread.
        """
        self.connection_monitor_thread = threading.Thread(target=self.connection_monitor)
        self.connection_monitor_thread.daemon = True  # Set the thread as a daemon to ensure it stops when the main program exits
        self.connection_monitor_thread.start()

# Usage example
if __name__ == "__main__":
    monitor = InternetConnectionMonitor()
    monitor.start_monitoring()

    # Your main program code goes here
    # testing 
    num = int(input('Enter  a number: '))
    print("Num = ",num)
