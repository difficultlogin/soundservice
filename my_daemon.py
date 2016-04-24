#!/usr/bin/env python

import sys, time, os
from daemon import Daemon
from pydub import AudioSegment

class MyDaemon(Daemon):
    def run(self):
        current_files = []
        while True:
            for file in os.listdir(self.scan_directory):
                if file.endswith('.wav') and file not in current_files:
                    AudioSegment.from_wav(self.scan_directory+file).export(self.mp3_directory + file[:-3] + 'mp3', format='mp3')
                    current_files.append(file)

if __name__ == "__main__":
    """
        bin/ folder - It contains executables and log files
    """
    work_path = '' # with mp3 files folder
    daemon = MyDaemon('/tmp/daemon-example.pid', stdin=work_path+'bin/log.txt', stdout=work_path+'bin/log.txt', stderr=work_path+'bin/log.txt',  scan_directory=work_path, mp3_directory=work_path+'mp3/')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
