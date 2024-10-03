import requests

def download_file(url, filename):
    """
    Download a file from the given URL and save it with the specified filename.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"File '{filename}' downloaded successfully.")
        else:
            print(f"Error downloading file: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

# Example usage
url = "https://archive.org/compress/tamildancesongs/formats=VBR%20MP3&file=/tamildancesongs.zip"
filename = "file.zip"
download_file(url, filename)
