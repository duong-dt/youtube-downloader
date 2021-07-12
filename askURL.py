from win32com.client import Dispatch

print('Enter Youtube URL (wrap in double quote): ', end='')
wsh=Dispatch('WScript.Shell')
wsh.sendKeys('""{LEFT}')