import unittest, os
from Source_extra.tracer import Simulator as Simulator_extra
import logging 
log = logging.getLogger('root')
FORMAT = "\n" + "[%(funcName)15s():%(lineno)s]::%(message)s\n"
logging.basicConfig(format=FORMAT)
log.setLevel(logging.INFO)


class TraceTest(unittest.TestCase): 
    
    def initialise_simulation(self):
        """Creates the Simulator_extra objects for a test
        """
        my_Simulator_extra = Simulator_extra(logger_=log)
        trace_files_dir = os.path.join('Tests','TraceFiles')
        trace_file_path = os.path.join(trace_files_dir,'trace_extra.txt')
        my_Simulator_extra.parse_traceFile(trace_file_path)
        return my_Simulator_extra

    def test_initialization(self):         
        """Makes sure states of cache lines are set to INVALID when initialized
        """ 
        self.my_Simulator_extra = self.initialise_simulation()
        log.debug('nr caches = {}'.format(len(self.my_Simulator_extra.caches)))
        for cache in self.my_Simulator_extra.caches:
            self.assertTrue(len(cache.lines)==0)
    

    def test_traceFile_lines(self):
        """Tets that simulator_extra reads and stores instructions from trace file
        """
        self.my_Simulator_extra = self.initialise_simulation()
        self.assertEqual(18, len(self.my_Simulator_extra.traceFile_Lines))


    def test_trace_file(self):
        """Test up to line numebr from file
        """
        self.my_Simulator_extra = self.initialise_simulation()
        i_ = 17
        instructions = self.my_Simulator_extra.traceFile_Lines
        # -- feed line to simulation
        for i, instruction in enumerate(instructions[:i_+1]):
            self.my_Simulator_extra.feed_line(i=i,line=instruction)
            log.info('{}) {}'.format(i, instruction))
            self.my_Simulator_extra.tracker.show_current_step()
            self.current_step(i=i)
            if i != i_:
                self.my_Simulator_extra.tracker.new_cmd()
    
    def current_step(self,i:int):
        """Used to test results at each step of simulationS
        """
        results = [
                    [29, 0, 0, 1, 0, 0, 0],      # 0
                    [2,  1, 0, 0, 0, 0, 0],      # 1
                    [2,  1, 0, 0, 0, 0, 0],      # 2
                    [2,  1, 0, 0, 0, 0, 0],      # 3
                    [2,  1, 0, 0, 0, 0, 0],      # 4
                    [2,  1, 0, 0, 0, 0, 0],      # 5
                    [2,  1, 0, 0, 0, 0, 0],      # 6
                    [29, 0, 0, 1, 0, 0, 0],      # 7
                    [2,  1, 0, 0, 0, 0, 0],      # 8
                    [2,  1, 0, 0, 0, 0, 0],      # 9
                    [29, 0, 0, 1, 0, 0, 0],      # 10
                    [2,  1, 0, 0, 0, 0, 0],      # 11
                    [2,  1, 0, 0, 0, 0, 0],      # 12
                    [22, 0, 1, 0, 0, 0, 1],      # 13 C WB ?
                    [29, 0, 0, 1, 0, 0, 0],      # 14
                    [2,  1, 0, 0, 0, 0, 0],      # 15
                    [18, 0, 1, 0, 0, 1, 1],      # 16
                    [2,  1, 0, 0, 0, 0, 0],      # 17
                  ]
        # --  latency, Pr, Re, Off, R_RB, C_RB, Inv
        results_i = results[i]
        # -- check values
        self.assertEqual(self.my_Simulator_extra.tracker.total_latency_i, results_i[0])
        self.assertEqual(self.my_Simulator_extra.tracker.private_accesses_i, results_i[1])
        self.assertEqual(self.my_Simulator_extra.tracker.remote_accesses_i, results_i[2])
        self.assertEqual(self.my_Simulator_extra.tracker.off_chip_access_i, results_i[3])
        self.assertEqual(self.my_Simulator_extra.tracker.replacement_writebacks_i, results_i[4])
        self.assertEqual(self.my_Simulator_extra.tracker.coherence_writebacks_i, results_i[5])
        self.assertEqual(self.my_Simulator_extra.tracker.invalidations_sent_i, results_i[6])