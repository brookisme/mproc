import itertools
from multiprocessing import Process, cpu_count
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from datetime import datetime


#
# CONFIG
#
MAX_POOL_PROCESSES=cpu_count()-1
MAX_THREADPOOL_PROCESSES=16



#
# METHODS
#
""" MAP METHODS

  Args:
    * map_function <function>: 
      a function to map over args list. the function's initial argument must
      is taken from args_list, additional kwargs may be passed to each call
      if multiple arguments are needed accept them as a single list or tuple
    * args_list <list>: the list of arguments to map over
    * max_process <int>: number of processes
      - for max_with_pool defaults to the number of cpus minus 1
      - for max_with_threadpool defaults to 16
      - map_sequential ignores this argument as its doesn't actually do 
        any multiprocesssing 

  Return:
    List of return values from map_function

  Notes:
    map_sequential does NOT multiprocess.  it can be used as a sequential drop-in 
    replacement for map_with_pool/threadpool.  this is useful for:
      - development 
      - debugging
      - benchmarking 

"""
def map_with_pool(
    map_function,
    args_list,
    max_processes=MAX_POOL_PROCESSES,
    **kwargs):
  pool=Pool(processes=min(len(args_list),max_processes))
  return _run_pool(
    pool,
    lambda a: map_function(a, **kwargs),
    args_list)


def map_with_threadpool(
    map_function,
    args_list,
    max_processes=MAX_THREADPOOL_PROCESSES,
    **kwargs):
  pool=ThreadPool(processes=min(len(args_list),max_processes))
  return _run_pool(
    pool,
    lambda a: map_function(a, **kwargs),
    args_list)


def map_sequential(
    map_function,
    args_list,
    max_processes='__ignored',
    print_args=False,
    noisy=False,
    **kwargs):
  if noisy:
    print('multiprocessing(test):')
  out=[]
  def _func(arg):
    return map_function(arg, **kwargs)
  for i,arg in enumerate(args_list):
      if noisy: 
        print('\t{}...'.format(i))
      if print_args:
        print('\t{}'.format(arg))
        print('-', kwargs)
      out.append(map_function(arg, **kwargs))
  if noisy: 
    print('-'*25)
  return out



""" simple: vanilla multiprocessing
  Args:
    * function <function>: function. function can take multiple arguments 
    * args_list <list>: the list of argument lists
    * join <bool[True]>: join processes before return

  Return: 
    List of processes 
"""
def simple(function,args_list,join=True):
  procs=[]
  for args in args_list:
      proc=Process(
          target=function, 
          args=args)
      procs.append(proc)
      proc.start()
  if join:
    for proc in procs:
        proc.join()
  return procs






""" MPList
Run the above methods on map_function,args_list pairs where the map_function
changes for each new set of args in args_list

Args:
    pool_type<str>: 
        one of MPList.POOL|THREAD|SEQUENTIAL.  determines which map_function 
        and default max_processes to use. If not MPList.THREAD|SEQUENTIAL it 
        will default to MPList.POOL.
    max_processes<int>:
        if not passed will set default based on pool_type
    jobs<list>:
        list of (target,args,kwargs) tuples. Note: use the append method rather than
        creating (target,args,kwargs) tuples
        
"""
class MPList():
    #
    # POOL TYPES
    #
    POOL='pool'
    THREAD='threading'
    SEQUENTIAL='sequential'
    

    #
    # PUBLIC
    #
    def __init__(self,pool_type=None,max_processes=None,jobs=None):
        self.pool_type=pool_type or self.POOL
        self.max_processes=max_processes
        self.jobs=jobs or []

        
    def append(self,target,*args,**kwargs):
        self.jobs.append((target,)+(args,)+(kwargs,))
        
    
    def run(self):
        self.start_time=datetime.now()
        map_func,self.max_processes=self._map_func_max_processes()
        out=map_func(self._target,self.jobs,max_processes=self.max_processes)
        self.end_time=datetime.now()
        self.duration=str(self.end_time-self.start_time)
        return out
        

    def __len__(self):
        return len(self.jobs)
    
    
    #
    # INTERNAL
    #    
    def _map_func_max_processes(self):
        if self.pool_type==MPList.THREAD:
            map_func=map_with_threadpool
            max_processes=self.max_processes or MAX_THREADPOOL_PROCESSES
        elif self.pool_type==MPList.SEQUENTIAL:
            map_func=map_sequential
            max_processes=False
        else:
            map_func=map_with_pool
            max_processes=self.max_processes or MAX_POOL_PROCESSES
        return map_func, max_processes
        
        
    def _target(self,args):
        target,args,kwargs=args
        return target(*args,**kwargs)
        
    

#
# INTERNAL METHODS
#
def _stop_pool(pool,success=True):
  pool.close()
  pool.join()
  return success


def _map_async(pool,map_func,objects):
  try:
    return pool.map_async(map_func,objects)
  except KeyboardInterrupt:
    print("Caught KeyboardInterrupt, terminating workers")
    pool.terminate()
    return False
  else:
    print("Failure")
    return _stop_pool(pool,False)


def _run_pool(pool,map_function,args_list):
  out=_map_async(pool,map_function,args_list)
  _stop_pool(pool)
  return out.get()


