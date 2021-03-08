import os, sys
# from Source.tracer import Simulator
from Source_extra.tracer import Simulator as Simulator_extra
from Source_extra.utils import MESI, FLOPS
import logging 
log = logging.getLogger('root')
FORMAT = "[%(funcName)15s():%(lineno)s]::%(message)s"
logging.basicConfig(format=FORMAT)
log.setLevel(logging.INFO)
log.debug('Finished importing')

# GLOBALS
trace_files_dir = 'TraceFiles'

def main_extra(mesi:str, flops:str, filename:str):
    
    global MESI, FLOPS
    
    trace_file_path = os.path.join(trace_files_dir, filename)
    
    MESI = True if (mesi=='True') else MESI
    FLOPS = True if (flops=='True') else FLOPS
    
    log.info('RUNNING EXTRA\nMESI: {}; FLOPS: {}; filename: {}'.format(MESI,FLOPS,filename))
    
    simulator = Simulator_extra(logger_=log)
    simulator.run(trace_file_path)


if __name__ == "__main__":
    mesi, flops, filename = sys.argv[1], sys.argv[2], sys.argv[3]
    main_extra(mesi=mesi, flops=flops, filename=filename)
