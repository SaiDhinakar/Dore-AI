import os
import win32api
import threading

def search_files(file_name, search_content=False, content_to_search=None):
    file_paths = []
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    threads = []

    for drive in drives:
        t = threading.Thread(target=search_drive, args=(drive, file_name, search_content, content_to_search, file_paths))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return file_paths

def search_drive(drive, file_name, search_content, content_to_search, file_paths):
    for root, dirs, files in os.walk(drive):
        for file in files:
            if file.lower() == file_name.lower():
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

                if search_content:
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                            if content_to_search.lower() in content.lower():
                                file_paths.append(file_path)
                    except:
                        pass

# Search for a file named "example.txt"
file_paths = search_files("Web capture_22-2-2022_21645_www.onlinegdb.com.jpeg")
print(file_paths)


# # Search for a file named "example.txt" and check if it contains the word "hello"
# file_paths = search_files("example.txt", search_content=True, content_to_search="hello")
# print(file_paths)
