import logging
import masterView
import ctypes
import sys


logging.basicConfig(format='%(levelname)s:  %(asctime)s: %(threadName)s > %(message)s', filename='Scrumbles.log',level=logging.DEBUG)
logging.info('Application starting')


try:
        if 'win' in sys.platform:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
        logging.warning('SetProcessDpiAwareness.dll not found')
app = masterView.masterView()

app.mainloop()

