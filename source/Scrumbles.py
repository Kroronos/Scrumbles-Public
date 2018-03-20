import masterView
import subprocess
import sys
import tkinter

# The following can be removed
# pyver = sys.version_info
# assert pyver[0] == 3, 'Python version must be 3.6.4'
# assert pyver[1] == 6, 'Python version must be 3.6.4'
# assert pyver[2] == 4, 'Python version must be 3.6.4'
# versions = subprocess.run(['pip','freeze'], stdout=subprocess.PIPE)
# versions = versions.stdout.decode('ascii')
# versions = versions.split('\r\n')
# assert 'matplotlib==2.1.2' in versions, 'Version requirement matplotlib==2.1.2'
# assert 'mysqlclient==1.3.12' in versions, 'Version requirement mysqlclient==1.3.12'
# assert  'tkcalendar==1.1.4' in versions, 'Version requirement tkcalendar==1.1.4'
# assert tkinter.TkVersion == 8.6, 'Version requirement tkinter version 8.6'
# import ctypes
# import sys
#
# if 'win' in sys.platform:
#         ctypes.windll.shcore.SetProcessDpiAwareness(1)

app = masterView.masterView()

app.mainloop()
