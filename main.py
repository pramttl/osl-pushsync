import os
import pyinotify

TRACKED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test/'))
print "Watching the follo. directory for events: " + TRACKED_DIR

wm = pyinotify.WatchManager()

# mask defines the events that are being watched
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        # Sync files on the slave servers
        # rsync -v -e ssh <source file/directory> user@hostname:<destionation_path>
        print "File Added: " + event.pathname

    def process_IN_DELETE(self, event):
        # Stuff to do when a file is deleted
        print "File Deleted: " + event.pathname

    def process_IN_MODIFY(self, event):
        print "File Modified: " + event.pathname


# exclude_list = ['^/']

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(TRACKED_DIR, mask, rec=True)

notifier.loop()
