### MPROC

_multiprocessing made easy_

---

###MAP METHODS

```
def map_with_pool(map_function,args_list,max_processes=MAX_POOL_PROCESSES)
```

```
def map_with_threadpool(map_function,args_list,max_processes=MAX_THREADPOOL_PROCESSES)
```

```
def map_sequential(map_function,args_list,print_args=False,noisy=False,**dummy_kwargs)
```

```
  Args:
    * map_function <function>: 
      a function to map over args list. the function should take a single argument.
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
```