import os
# import logging as log

from Source_extra.utils import *
from Source_extra.cache import Cache
from Source_extra.memory_controller import MemoryController
from Source_extra.tracker import Tracker

'''
Parse through the tracer file and interpretr the commands
'''
NUMBER_OF_PROCESSORS = 4
CACHE_LINES          = 512
CACHE_LINE_SIZE      = 4

class Simulator():
    
    def __init__(self, logger_):
        self.log               = logger_
        self.tracker           = Tracker(logger_=self.log)
        self.caches            = []                                                 # list of cache objects
        self.memory_controller = MemoryController(tracker=self.tracker, logger_=self.log)                   
        self.cache_line_size   = get_bit_length(CACHE_LINE_SIZE)
        self.cache_lines       = get_bit_length(CACHE_LINES) 
        # initialise caches
        for i in range(NUMBER_OF_PROCESSORS):
            self.caches.append(Cache(tracker=self.tracker, memory_controller=self.memory_controller, 
                                     id=i, cache_lines=CACHE_LINES, cache_line_size=CACHE_LINE_SIZE, logger_=self.log))

    def run(self, traceFile_dir:str):
        """Runs the simulation

        Args:
            traceFile_dir (string): path to trace file
        """
        self.parse_traceFile(traceFile_dir=traceFile_dir)
        self.log.debug('Finished Parsing')
        self.feed_traceFile_lines()
        self.tracker.show_results()

    def parse_traceFile(self,traceFile_dir:str):
        """Function that simulates the cache given a trace file

        Args:
            traceFile_dir (string): path to trace file
        """
        # -- get file and lines
        self.traceFile_Lines = open(traceFile_dir, 'r').readlines()
        
    
    def feed_traceFile_lines(self):
        """Function feeds each trace file line to the appropriate cache
        """
        # -- Strips the newline character
        for i,line in enumerate(self.traceFile_Lines):
            self.log.debug("\n \n{}) {}".format(i,line.strip()))
            # -- feed current command
            self.feed_line(i, line)
            # -- next command
            self.tracker.new_cmd()
            # <!> DEBUG <!>
            # stop = False
            # if self.tracker._invalidations_sent[-1]!=0 or stop==True:
            #     self.log.info("\n \n{}) {}".format(i,line.strip()))
            #     stop = True
            #     self.tracker.show_results()
            #     input()

    def feed_line(self, i:int, line):
        """Deals with each line accordingly

        Args:
            i (int): current line number in trace file
            line (int): current instruction at line number
        """
        if (len(line)==1):                                                          # v, p or h
            pass
        if (len(line)>1):                                                           # read and write 
            parts = line.split()
            # -- split commands args
            cache_id, operation, address = int(parts[0][1:]), parts[1], int(parts[2])
            # assign to correct cache
            if operation == "R":
                self.caches[cache_id].read(address=address)
            elif operation == "W":
                self.caches[cache_id].write(address=address)
            else:
                self.log.warning("ERROR: Unknown access type: {}" .format(operation))
                return
