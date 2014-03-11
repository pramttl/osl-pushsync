import os
import pyinotify
import subprocess

TRACKED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test/'))
TARGET_DIR = "/home/pranjal/projects/osl/test-ftphost"

# List of IP adress of ftp hosts at OSL
SLAVE_HOSTS = []

# Defines the user used to ssh into each ftp host during ssh based rsync
SLAVE_USERS = []

wm = pyinotify.WatchManager()

# Mask defines the events that are being watched
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY


def rsync_to_hosts():
    '''
    Function that runs rsync and copies files from TRACKED_DIR on master
    to TARGET_DIR on all the slaves.
    '''
    for i in range(len(SLAVE_HOSTS)):
        host = SLAVE_HOSTS[i]
        hostuser = SLAVE_USERS[i]

        args = ["rsync", "-avz", "--include='*/'", "-e", "ssh",
                TRACKED_DIR, hostuser + "@" + host + TARGET_DIR]

        print "Syncing to slaves " + ' '.join(args)
        subprocess.call(args)


class EventHandler(pyinotify.ProcessEvent):
    '''
    An event handler object will help us track changes to a directory and
    accordingly initiate rsync push calls.
    '''
    def process_IN_CREATE(self, event):
        print "File Added: " + event.pathname
        # Sync files on the slave servers
        rsync_to_hosts()

    def process_IN_DELETE(self, event):
        # Stuff to do when a file is deleted
        print "File Deleted: " + event.pathname
        # Sync files on the slave servers
        rsync_to_hosts()

    def process_IN_MODIFY(self, event):
        # Stuff to do when a file is modified.
        print "File Modified: " + event.pathname
        # Sync files on the slave servers
        rsync_to_hosts()


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(TRACKED_DIR, mask, rec=True)

print "Watching the follo. directory for events: " + TRACKED_DIR
notifier.loop()
