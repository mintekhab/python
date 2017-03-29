#!/usr/bin/env python
import pyinotify
import socket
import re
import os


wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY


class EventHandler (pyinotify.ProcessEvent):

    def __init__(self, file_path, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self._last_position = 0
        self.statsd_host = 'statsd.us-west-2.prod-p.expedia.com'
        self.statsd_port = 8125
        self.prefix = 'mongodb.reviewsbrandsummary.ip-10-8-134-81'
        self.metrics = 'responsetime'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logpats = r'QUERY'
        self.p1 = re.compile(r'([0-9]+)ms',re.IGNORECASE)
        self._logpat = re.compile(logpats)

    def process_IN_MODIFY(self, event):
        print "File changed: ", event.pathname
        if self._last_position > os.path.getsize(self.file_path):
            self._last_position = 0
        with open(self.file_path) as f:
            f.seek(self._last_position)
            loglines = f.readlines()
            self._last_position = f.tell()
            groups = (self._logpat.search(line.strip()) for line in loglines)
            for g in groups:
                if g:
                    #print g.string
                    if self.p1.search(g.string):
                       data = "%s.%s:%s|g" % (self.prefix,self.metrics,str(self.p1.findall(g.string)[0]))
                       print data
handler = EventHandler('/var/log/mongodb/mongodb.log')
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch(handler.file_path, mask)
notifier.loop()
