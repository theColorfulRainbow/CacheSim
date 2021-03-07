import numpy as np
class Tracker:
    """Class ersponsible of tracking actions at each line of the trace file
    """

    def __init__(self, logger_):
        self.log = logger_
        self._initialize_varaibles()
    
    def _initialize_varaibles(self):
        """Initialzie varaibles used to track stats
        """
        # -- lists --> hold info over all trace file
        self._private_accesses         = []
        self._remote_accesses          = []
        self._off_chip_access          = []
        self._total_accesses           = []
        self._replacement_writebacks   = []
        self._coherence_writebacks     = []
        self._invalidations_sent       = []
        self._average_latency          = []
        self._priv_average_latency     = []
        self._rem_average_latency      = []
        self._off_chip_averave_latency = []
        self._total_latency            = []
        # -- ints --> holds ifo at current instruction only
        self.private_accesses_i         = 0
        self.remote_accesses_i          = 0
        self.off_chip_access_i          = 0
        self.total_accesses_i           = 0
        self.replacement_writebacks_i   = 0
        self.coherence_writebacks_i     = 0
        self.invalidations_sent_i       = 0
        self.average_latency_i          = 0
        self.priv_average_latency_i     = False
        self.rem_average_latency_i      = False
        self.off_chip_averave_latency_i = False
        self.total_latency_i            = 0
        # -- extra
        self.compulsory_miss            = 0
        self.conflict_miss              = 0 


    def add_total_latency(self, latency):
        """Increments latency by given amount

        Args:
            latency (int): incrementing amuont
        """
        self.total_latency_i += latency

    
    def new_cmd(self):
        """Moved onto new command
        Reseting varaibles
        """
        self._add_variables_to_history()
        self._reset_variables()
    

    def show_results(self):
        """Function called at the end to present results of the trace file
        """
        self._average_latency = 0 if (len(self._total_latency)==0) else sum(self._total_latency)/len(self._total_latency)

        priv_latency_idx = [i for i, x in enumerate(self._private_accesses) if x!=0]
        priv_latency_sum = sum([self._total_latency[i] for i in priv_latency_idx])
        priv_avg_latency = 0 if (len(priv_latency_idx)==0) else priv_latency_sum / len(priv_latency_idx)

        rem_latency_idx = [i for i, x in enumerate(self._remote_accesses) if x!=0]
        rem_latency_sum = sum([self._total_latency[i] for i in rem_latency_idx])
        rem_avg_latency = 0 if (len(rem_latency_idx)==0) else rem_latency_sum / len(rem_latency_idx)

        mem_latency_idx = [i for i, x in enumerate(self._off_chip_access) if x!=0]
        mem_latency_sum = sum([self._total_latency[i] for i in mem_latency_idx])
        mem_avg_latency = 0 if (len(mem_latency_idx)==0) else mem_latency_sum / len(mem_latency_idx)
        
        print("SHOWING OVERALL RESULTS      \n\
                Private-accesses:         {}\n\
                Remote-accesses:          {}\n\
                Off-chip-accesses:        {}\n\
                Total-accesses:           {}\n\
                Replacement-writebacks:   {}\n\
                Coherence-writebacks:     {}\n\
                Invalidations-sent:       {}\n\
                Average-latency:          {}\n\
                Priv-average-latency:     {}\n\
                Rem-average-latency:      {}\n\
                Off-chip-average-latency: {}\n\
                Total-latency:            {}\n\
                ".format(
                    sum(self._private_accesses),
                    sum(self._remote_accesses),
                    sum(self._off_chip_access),
                    sum(self._private_accesses) + sum(self._remote_accesses) + sum(self._off_chip_access),
                    sum(self._replacement_writebacks),
                    sum(self._coherence_writebacks),
                    sum(self._invalidations_sent),
                    self._average_latency,
                    priv_avg_latency,
                    rem_avg_latency,
                    mem_avg_latency,
                    sum(self._total_latency)))


    def _add_variables_to_history(self):
        """add variables to history
        """
        self._total_latency.append(self.total_latency_i)
        self._private_accesses.append(self.private_accesses_i)
        self._remote_accesses.append(self.remote_accesses_i)
        self._off_chip_access.append(self.off_chip_access_i)
        # <!>
        # self._total_accesses.append(sum(self._private_accesses) + sum(self._remote_accesses) + sum(self._off_chip_access),)
        #<!>
        self._total_accesses.append(self.total_accesses_i)
        self._replacement_writebacks.append(self.replacement_writebacks_i)
        self._coherence_writebacks.append(self.coherence_writebacks_i)
        self._invalidations_sent.append(self.invalidations_sent_i)
        # self._average_latency.append(self.average_latency_i)
        self._priv_average_latency.append(self.priv_average_latency_i)
        self._rem_average_latency.append(self.rem_average_latency_i)
        self._off_chip_averave_latency.append(self.off_chip_averave_latency_i)

    def _reset_variables(self):
        """Reset varaibles for next instruciton line
        """
        self.private_accesses_i         = 0
        self.remote_accesses_i          = 0
        self.off_chip_access_i          = 0
        self.total_accesses_i           = 0
        self.replacement_writebacks_i   = 0
        self.coherence_writebacks_i     = 0
        self.invalidations_sent_i       = 0
        self.average_latency_i          = 0
        self.priv_average_latency_i     = False
        self.rem_average_latency_i      = False
        self.off_chip_averave_latency_i = False
        self.total_latency_i            = 0


    def show_current_step(self):
        """Prints variablesa at current step only
        """
        print("BEFORE: Adding to history\n\
                self.total_latency_i           {}\n\
                self.private_accesses_i        {}\n\
                self.remote_accesses_i         {}\n\
                self.off_chip_access_i         {}\n\
                self.total_accesses_i          {}\n\
                self.replacement_writebacks_i  {}\n\
                self.coherence_writebacks_i    {}\n\
                self.invalidations_sent_i      {}\n\
                ".format(
                self.total_latency_i, self.private_accesses_i, self.remote_accesses_i, 
                self.off_chip_access_i, self.total_accesses_i, self.replacement_writebacks_i, 
                self.coherence_writebacks_i, self.invalidations_sent_i))