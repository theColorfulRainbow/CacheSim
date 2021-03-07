import os
from Source.tracer import Simulator
from Source_extra.tracer import Simulator as Simulator_extra
import logging 
log = logging.getLogger('root')
FORMAT = "[%(funcName)15s():%(lineno)s]::%(message)s"
logging.basicConfig(format=FORMAT)
log.setLevel(logging.INFO)
log.debug('Finished importing')

def main():
    log.info('RUNNING ORIGINAL')
    trace_files_dir = 'TraceFiles'
    trace_file_path = os.path.join(trace_files_dir,'file2.txt')
    simulator = Simulator(logger_=log)
    simulator.run(trace_file_path)

def main_extra():
    log.info('RUNNING EXTRA')
    trace_files_dir = 'TraceFiles'
    trace_file_path = os.path.join(trace_files_dir,'file2.txt')
    simulator = Simulator_extra(logger_=log)
    simulator.run(trace_file_path)

if __name__ == "__main__":
    main_extra()
