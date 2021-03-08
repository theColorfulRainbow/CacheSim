'''
 Redered to as memory controller that allows communication between caches
'''
# import logging as log
from Source_extra.cache import Cache, LineState, CacheLine
from Source_extra.tracker import Tracker
from Source_extra.utils import *

class MemoryController():

    def __init__(self, tracker:Tracker, logger_):
        self.caches = []
        self.tracker = tracker
        self.log=logger_

    def add_cache(self, new_cache):
        self.caches.append(new_cache)

 
    def read_miss(self, cache_id:int, address:int, cache_line:CacheLine):
        """Notidy all caches of a read miss.

        Args:
            cache_id (int): id of the cache that missed
            address (int): adress that the cache has missed
            cache_line (CacheLine): cache line with read miss
        """
        # -- directory access
        self._dir_access()
        # -- find all and furthest sharer
        sharer_ids, sharer_id_furthest, hops = self._find_sharers(cache_id=cache_id, address=address, instruction='R')
        # -- no sharers == 0
        if len(sharer_ids)==0:
            # <!> set set cache line state
            cache_line.currentState = LineState.EXCLUSIVE
            # -- get data from memory
            self._fetch_from_mem()
            # -- send data to current cache
            self._send_data_to_cache()
            # > off-chip-access
            self.tracker.off_chip_access_i = 1
            # -- propagate read miss
            self._propragate_read_miss(cache_id=cache_id, address=address)
            return
        # -- no sharers > 0
        elif len(sharer_ids)>0:
            # <!> set set cache line state
            cache_line.currentState = LineState.SHARED
            # -- send message to furthest sharer to forward line
            self._message_furthest_to_forward_read(sharer_id_furthest=sharer_id_furthest, address=address, hops=hops)
            # > remote access
            self.tracker.remote_accesses_i = 1
            # -- propagate read miss
            self._propragate_read_miss(cache_id=cache_id, address=address)
            return
        # <!> something went wrong
        else:
            raise ValueError('INVALID READ MISS IN MEMORY CONTROLLER')

    def write_miss(self, cache_id:int, address:int, state:LineState):
        """Notify all caches of a write miss.

        Args:
            cache_id (int): id of the cache that missed
            address (int): adress that the cache has missed
            state (LineState): current state  of the cache line
        """
        # -- directory access
        self._dir_access()
        # -- find all and furthest sharers
        sharer_ids, sharer_id_furthest, hops = self._find_sharers(cache_id=cache_id, address=address, instruction='R')
        # -- no sharers == 0
        if len(sharer_ids)==0:
            # -- SHARED ?
            if state==LineState.SHARED:
                # -- respond there are no sharers: 5 cycles
                self._respond_no_sharers()
                # > private access
                self.tracker.remote_accesses_i = 1                                     # <!> DEBUG <!> according to flow chart
                # -- send invalidations
                self._propragate_write_miss(sharer_ids=sharer_ids, cache_id=cache_id, address=address)    
                return
            # -- INVALID ?
            elif state!=LineState.SHARED:
                # -- directory receives data from mem: 15 cycles 
                self._fetch_from_mem()
                # -- send data to current cache: 5 cycles
                self._send_data_to_cache()
                # > off chip access
                self.tracker.off_chip_access_i = 1
                # -- send invalidations
                self._propragate_write_miss(sharer_ids=sharer_ids, cache_id=cache_id, address=address) 
                return
            # <!> invalid state 
            else:
                raise ValueError('MEMORY CONTROLLER WRITE MISS\nNO SHARERS\nNOT ACCOUNTED FOR STATE: {}'.format(state))
        # -- nr sharers == 1
        elif (len(sharer_ids)==1) and (state!=LineState.SHARED):
            # -- send message to invalidate and forward when one sharer only
            self._message_furthest_to_forward_write_single(sharer_id_furthest=sharer_id_furthest, address=address, hops=hops)
            # > remote access
            self.tracker.remote_accesses_i = 1
            # -- send invalidations
            self._propragate_write_miss(sharer_ids=sharer_ids, cache_id=cache_id, address=address)
            return
        # -- nr sharers > 1 
        elif (len(sharer_ids)>1) or (state==LineState.SHARED):
            # -- send message to invalidate and forward when one sharer only
            self._message_furthest_to_forward_write_multi(sharer_id_furthest=sharer_id_furthest, address=address, hops=hops)
            # > remote access
            self.tracker.remote_accesses_i = 1
            # -- send invalidations
            self._propragate_write_miss(sharer_ids=sharer_ids, cache_id=cache_id, address=address)
            return
        # <!> invalid result
        else:
            raise ValueError('MEMORY WRITE MISS ERROR')


    def _propragate_write_miss(self,sharer_ids:int, cache_id:int, address:int):
        """Sends invalidations when a write miss occurs
        """
        # > invalidations sent
        self.tracker.invalidations_sent_i = len(sharer_ids)
        # -- invalidate copies
        for cache in self.caches:
            if cache.id != cache_id:                                                    # notidy only other caches
                cache.propagate_write_miss(address=address)


    def _propragate_read_miss(self, cache_id:int, address:int):
        """Informs other sharers of a read miss in local cache
        """
        for cache in self.caches:
            if cache.id != cache_id:                                                    # notidy only other caches
                cache.propagate_read_miss(address=address)


    def _dir_access(self):
        """Records the direcotry access
        1 cycle
        """
        self.tracker.add_total_latency(latency=1)


    def _find_sharers(self, cache_id:int, address:int,instruction:str):
        """Finds shareres ids and the furthest sharer

        Args:
            cache_id (int): current cache id (gets skipped)
            address (int): current address
            instruction (str): Read (R) or Write (W)

        Returns:
            list: lsit of sharer ids, futhest sharer id, no of hops
        """
        sharer_ids = []
        for cache in self.caches:
            if cache.id != cache_id:
                if cache.check_match(address=address):
                    sharer_ids.append(cache.id)
        sharer_id_furthest, hops = self._find_furthest_sharer(cache_id=cache_id, sharer_ids=sharer_ids)
        self._track_miss(instruction=instruction, nr_sharers=len(sharer_ids), hops=hops)
        hops = 1 if (hops==3 and FLOPS==True) else hops
        return sharer_ids, sharer_id_furthest, hops
      

    def _find_furthest_sharer(self, cache_id:int, sharer_ids:list):
        """Finds the furthes share given a lsit of shareres

        Args:
            cache_id (int): current cache id
            sharer_ids (list): lsit of sharers ids

        Returns:
            list: sharer_id_furthest, hops between processors
        """
        if len(sharer_ids) == 0:
            return None, None
        else: 
            hops_list = []
            for sharer_id in sharer_ids:
                hops_list.append( (cache_id - sharer_id) % len(self.caches) )
            hops = max(hops_list)
            sharer_id_furthest = sharer_ids[hops_list.index(hops)]
            return sharer_id_furthest, hops
    

    def _track_miss(self, instruction:str, nr_sharers:int, hops:int):
        """Tracks number of hops & nr sharers on an instruction miss  

        Args:
            instruciton (str): Read (R); Write (W)
            nr_sharers (int): number of shrers 
            hops (int): number of hops to perform
        """
        self._track_hops(hops=hops)
        if (nr_sharers==0):
            if (instruction=='R'):
                self.tracker.read_miss_no_sharers += 1
                return
            elif (instruction=='W'):
                self.tracker.write_miss_no_sharers += 1
                return
            else:
                return ValueError("INVALID INSTRUCTION TYPE")
        elif (nr_sharers<0):
            raise ValueError("CAN NOT HAVE NEGATIVE NR SHARERS: {}".format(nr_sharers))

    def _track_hops(self, hops:int):
        """tracks how many hops are performed

        Args:
            nr_hops (int): nr of hops to make 
        """
        if(hops==0 or hops==None):
            return
        elif(hops==1):
            self.tracker.hops_1 += 1
            return
        elif(hops==2):
            self.tracker.hops_2 += 1
            return
        elif(hops==3):
            self.tracker.hops_3 += 1
            return
        else:
            raise ValueError("INVALID NUMBER OF HOPS: {}".format(hops))


    def _fetch_from_mem(self):
        """Simulates taking data from mem
        15 cycles
        """
        self.tracker.add_total_latency(latency=15)


    def _send_data_to_cache(self):
        """Simulates esnding data to cache
        5 cycles
        """
        self.tracker.add_total_latency(latency=5)


    def _message_furthest_to_forward_read(self, sharer_id_furthest:int, address:int, hops:int):
        """Send message to furthest cache to forward
        5 cycles
        Args:
            sharer_id_furthest (int): id of furthests
        """
        self.tracker.add_total_latency(latency=5)                                                               # add latency
        for cache in self.caches:
            if cache.id == sharer_id_furthest:
                cache.read_forward_line(address=address, hops=hops)

    
    def _message_furthest_to_forward_write_single(self, sharer_id_furthest:int, address:int, hops:int):
        """Send message to furthest cache to forward
        5 cycles
        Args:
            sharer_id_furthest (int): id of furthests
            address (int): current address
            hops (int): how many processors to hop
        """
        self.tracker.add_total_latency(latency=5)                                                               # add latency
        for cache in self.caches:
            if cache.id == sharer_id_furthest:
                cache.write_forward_line_single(address=address, hops=hops)
    

    def _message_furthest_to_forward_write_multi(self, sharer_id_furthest:int, address:int, hops:int):
        """Send message to furthest cache to forward
        5 cycles
        Args:
            sharer_id_furthest (int): id of furthests
            address (int): current address
            hops (int): how many processors to hop
        """
        self.tracker.add_total_latency(latency=5)                                                               # add latency
        for cache in self.caches:
            if cache.id == sharer_id_furthest:
                cache.write_forward_line_multi(address=address, hops=hops)
    

    def _respond_no_sharers(self):
        """Simulates directory responding to cache that there are no sharers. On write miss
        5 cycles
        """
        self.tracker.add_total_latency(latency=5)
