
class listboxEventHandler:
    def __init__(self):
        # To Prevent Duplicate Tkinter Events
        self.oldWidget = None
        self.descriptionLock = False
        self.localEvents = []

    def setEventToHandle(self, localEvent):
        self.localEvents.append(localEvent)

    def handle(self,event):
        widget = event.widget

        widgetChanged = False

        if self.oldWidget is None:
            self.oldWidget = widget

        if self.oldWidget != widget and self.descriptionLock == False:
            self.oldWidget = widget
            widgetChanged = True

        if self.descriptionLock is False:
            for localEvent in self.localEvents:
                localEvent(event)

        if self.descriptionLock is True:
            self.descriptionLock = False

        if widgetChanged:
            self.descriptionLock = True
