import unittest, os
from Source.tracer import Simulator
from Source.cache import LineState
import logging 
log = logging.getLogger('root')
FORMAT = "\n" + "[%(funcName)15s():%(lineno)s]::%(message)s\n"
logging.basicConfig(format=FORMAT)
log.setLevel(logging.INFO)


class Address1Test(unittest.TestCase): 
    
    def initialise_simulation(self):
        """Creates the Simulator objects for a test
        """
        my_Simulator = Simulator(logger_=log)
        trace_files_dir = os.path.join('Tests','TraceFiles')
        trace_file_path = os.path.join(trace_files_dir,'trace_addr_1.txt')
        my_Simulator.parse_traceFile(trace_file_path)
        return my_Simulator

    def test_initialization(self):         
        """Makes sure states of cache lines are set to INVALID when initialized
        """ 
        self.my_Simulator = self.initialise_simulation()
        log.debug('nr caches = {}'.format(len(self.my_Simulator.caches)))
        for cache in self.my_Simulator.caches:
            self.assertTrue(len(cache.lines)==0)
    

    def test_traceFile_lines(self):
        """Tets that simulator reads and stores instructions from trace file
        """
        self.my_Simulator = self.initialise_simulation()
        self.assertEqual(9, len(self.my_Simulator.traceFile_Lines))


    def test_0(self):
        """Test nr 0: P0 R 1
        """
        self.my_Simulator = self.initialise_simulation()
        i = 0
        instruction = self.my_Simulator.traceFile_Lines[i]
        # self.my_Simulator.tracker.show_results()
        # -- feed line to simulation
        self.my_Simulator.feed_line(i=i, line=instruction)
        # -- check values
        self.assertEqual(self.my_Simulator.tracker.total_latency_i, 29)
        self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 1)
        self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)


    def test_1(self):
        """Test nr 1: P0 R 1
        """
        self.my_Simulator = self.initialise_simulation()
        i_ = 1
        instructions = self.my_Simulator.traceFile_Lines
        self.my_Simulator.tracker.show_results()
        # -- feed line to simulation
        for i, instruction in enumerate(instructions[:i_+1]):
            self.my_Simulator.feed_line(i=i,line=instruction)
            log.info('{}) {}'.format(i, instruction))
            self.my_Simulator.tracker.show_current_step()
            if i != i_:
                self.my_Simulator.tracker.new_cmd()
        # -- check values
        self.assertEqual(self.my_Simulator.tracker.total_latency_i, 2)
        self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 1)
        self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
        self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)


    def test_2(self):
        """Test nr 2: P1 R 1
        """
        self.my_Simulator = self.initialise_simulation()
        i_ = 2
        instructions = self.my_Simulator.traceFile_Lines
        self.my_Simulator.tracker.show_results()
        # -- feed line to simulation
        for i, instruction in enumerate(instructions[:i_+1]):
            self.my_Simulator.feed_line(i=i,line=instruction)
            log.info('{}) {}'.format(i, instruction))
            self.my_Simulator.tracker.show_current_step()
            if i != i_:
                self.my_Simulator.tracker.new_cmd()
        # -- check values
        self.assertEqual(self.my_Simulator.tracker.total_latency_i, 19)
        self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 1)
        self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
        self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)
    

    def test_3(self):
        """Test nr 3: P1 R 1
        """
        self.my_Simulator = self.initialise_simulation()
        i_ = 3
        instructions = self.my_Simulator.traceFile_Lines
        self.my_Simulator.tracker.show_results()
        # -- feed line to simulation
        for i, instruction in enumerate(instructions[:i_+1]):
            self.my_Simulator.feed_line(i=i,line=instruction)
            log.info('{}) {}'.format(i, instruction))
            self.my_Simulator.tracker.show_current_step()
            if i != i_:
                self.my_Simulator.tracker.new_cmd()
        # -- check values
        self.assertEqual(self.my_Simulator.tracker.total_latency_i, 2)
        self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 1)
        self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
        self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)

    
    def test_4(self):
        """Test nr 4: P1 W 1
        """
        self.my_Simulator = self.initialise_simulation()
        i_ = 4
        instructions = self.my_Simulator.traceFile_Lines
        self.my_Simulator.tracker.show_results()
        # -- feed line to simulation
        for i, instruction in enumerate(instructions[:i_+1]):
            self.my_Simulator.feed_line(i=i,line=instruction)
            log.info('{}) {}'.format(i, instruction))
            self.my_Simulator.tracker.show_current_step()
            if i != i_:
                self.my_Simulator.tracker.new_cmd()
        # -- check values
        self.assertEqual(self.my_Simulator.tracker.total_latency_i, 18)
        self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 1)
        self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
        self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 1)


    def test_5(self):
        """Test nr 5: P1 W 1
        """
        self.my_Simulator = self.initialise_simulation()
        i_ = 5
        instructions = self.my_Simulator.traceFile_Lines
        self.my_Simulator.tracker.show_results()
        # -- feed line to simulation
        for i, instruction in enumerate(instructions[:i_+1]):
            self.my_Simulator.feed_line(i=i,line=instruction)
            log.info('{}) {}'.format(i, instruction))
            self.my_Simulator.tracker.show_current_step()
            if i != i_:
                self.my_Simulator.tracker.new_cmd()
        # -- check values
        self.assertEqual(self.my_Simulator.tracker.total_latency_i, 2)
        self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 1)
        self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
        self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
        self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
        self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)

    
        def test_6(self):
            """Test nr 6: P1 R 1
            """
            self.my_Simulator = self.initialise_simulation()
            i_ = 6
            instructions = self.my_Simulator.traceFile_Lines
            self.my_Simulator.tracker.show_results()
            # -- feed line to simulation
            for i, instruction in enumerate(instructions[:i_+1]):
                self.my_Simulator.feed_line(i=i,line=instruction)
                log.info('{}) {}'.format(i, instruction))
                self.my_Simulator.tracker.show_current_step()
                if i != i_:
                    self.my_Simulator.tracker.new_cmd()
            # -- check values
            self.assertEqual(self.my_Simulator.tracker.total_latency_i, 2)
            self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 1)
            self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 0)
            self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
            self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
            self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
            self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 0)
            self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)


        def test_7(self):
            """Test nr 7: P0 W 1
            """
            self.my_Simulator = self.initialise_simulation()
            i_ = 7
            instructions = self.my_Simulator.traceFile_Lines
            self.my_Simulator.tracker.show_results()
            # -- feed line to simulation
            for i, instruction in enumerate(instructions[:i_+1]):
                self.my_Simulator.feed_line(i=i,line=instruction)
                log.info('{}) {}'.format(i, instruction))
                self.my_Simulator.tracker.show_current_step()
                if i != i_:
                    self.my_Simulator.tracker.new_cmd()
            # -- check values
            self.assertEqual(self.my_Simulator.tracker.total_latency_i, 25)
            self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 0)
            self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 1)
            self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
            self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
            self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
            self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 1)
            self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 1)


        def test_8(self):
            """Test nr 8: P3 R 1
            """
            self.my_Simulator = self.initialise_simulation()
            i_ = 8
            instructions = self.my_Simulator.traceFile_Lines
            self.my_Simulator.tracker.show_results()
            # -- feed line to simulation
            for i, instruction in enumerate(instructions[:i_+1]):
                self.my_Simulator.feed_line(i=i,line=instruction)
                log.info('{}) {}'.format(i, instruction))
                self.my_Simulator.tracker.show_current_step()
                if i != i_:
                    self.my_Simulator.tracker.new_cmd()
            # -- check values
            self.assertEqual(self.my_Simulator.tracker.total_latency_i, 25)
            self.assertEqual(self.my_Simulator.tracker.private_accesses_i, 0)
            self.assertEqual(self.my_Simulator.tracker.remote_accesses_i, 1)
            self.assertEqual(self.my_Simulator.tracker.off_chip_access_i, 0)
            self.assertEqual(self.my_Simulator.tracker.total_accesses_i, 0)
            self.assertEqual(self.my_Simulator.tracker.replacement_writebacks_i, 0)
            self.assertEqual(self.my_Simulator.tracker.coherence_writebacks_i, 1)
            self.assertEqual(self.my_Simulator.tracker.invalidations_sent_i, 0)




if __name__ == '__main__': 
    unittest.main() 