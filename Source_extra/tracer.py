import os, logging

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
        self.v = False                                                              # log debug
        self.hits_nr = 0
        self.instruciton_nr = 0
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
            self.log.debug('\n\n')
            self.log.debug("{}) {}".format(i,line.strip()))
            # -- feed current command
            self.feed_line(i, line)
            # -- next command
            self.tracker.new_cmd()
            

    def feed_line(self, i:int, line):
        """Deals with each line accordingly

        Args:
            i (int): current line number in trace file
            line (int): current instruction at line number
        """
        if (len(line)<=2 and len(line)>0):                                          # v, p or h
            parts = line.split()
            if parts[0] == "v":
                self.v = not self.v
                if (self.v==True):
                    self.log.setLevel(logging.DEBUG)
                else:
                    self.log.setLevel(logging.INFO)
                self.log.debug('cmd = {}'.format(parts[0]))
                return
            elif parts[0] == "p":
                self.log.debug('cmd = {}'.format(parts[0]))
                for cache in self.caches:
                    print(cache)
                return
            elif parts[0] == "h":
                self.log.debug('cmd = {}'.format(parts[0]))
                hit_rate = 0 if(self.instruciton_nr==0) else (self.hits_nr/self.instruciton_nr)
                self.log.info('\nINSTRUCTIONS: {}; HITS: {}; HIT RATE: {}'\
                            .format(self.instruciton_nr, self.hits_nr, hit_rate))
                return
            else:
                self.log.warning("UNKNOWN TRACE FILE INSTRUCTION OR FORMATING ERROR: {}\n\
                                                        SKIPPING Instruction".format(line))
                return
        elif (len(line)>2):                                                           # read and write 
            parts = line.split()
            # -- split commands args
            cache_id, operation, address = int(parts[0][1:]), parts[1], int(parts[2])
            # assign to correct cache
            if operation == "R":
                hit = self.caches[cache_id].read(address=address)
                self.instruciton_nr += 1
                self.hits_nr += 1 if (hit==True) else 0
                return
            elif operation == "W":
                hit = self.caches[cache_id].write(address=address)
                self.instruciton_nr += 1
                self.hits_nr += 1 if (hit==True) else 0
                return
            else:
                self.log.warning("ERROR: Unknown access type or formating: {}\n\
                                    MIGHT BE DUE TO WHITE SPACE" .format(operation))
                return
        elif (len(line)==0):
            log.warning("EMPTY LINE DETECTED: {}){}\nSKIPPING".format(i,line))
            return
        else:
            log.warning("UNREADABLE LINE: {}) {}\nSKIPPING".format(i,line))
            return
