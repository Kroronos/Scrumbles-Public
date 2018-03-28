import logging
import masterView
import ctypes
import sys


logging.basicConfig(format='%(levelname)s:  %(asctime)s:  %(message)s', filename='Scrumbles.log',level=logging.DEBUG)
logging.info('Application starting')



if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

app = masterView.masterView()

app.mainloop()

logging.info('Terminating Application')