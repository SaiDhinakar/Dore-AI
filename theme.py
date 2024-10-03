import winreg

def change_theme(theme):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
        
        if theme.lower() == 'dark':
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
            print("Theme changed to Dark mode.")
        elif theme.lower() == 'light':
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
            print("Theme changed to Light mode.")
        else:
            print("Invalid theme. Please choose 'dark' or 'light'.")
        
        winreg.CloseKey(key)
    except Exception as e:
        print("An error occurred: ", str(e))

theme = input("Change theme to 'dark' or 'light': ")
change_theme(theme)
