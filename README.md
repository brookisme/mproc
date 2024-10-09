### MPROC

_multiprocessing made easy_

---

#### INSTALL

```bash
git clone https://github.com/brookisme/mproc.git
cd mproc
pip install -e .
```

---

#### MAP METHODS

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

---

#### MPList

The above methods are great when you have a single method you are calling multiple times with different arguments.

If you want to launch a multiple processes/threads for distinct methods and arguments use `MPList`.

The main instance methods are `append(method,*args,**kwargs)` which adds processes and `run()`  which starts the jobs.  An example might look like:

```python
def prediction(im,model_key,window,pad):
  """ predict-stuff """
  pass

def cloud_score(im,window,pad):
  """ compute-stuff """
  pass

mp_list=MPList()
mp_list.append(
    prediction,
    im.astype(DTYPE),
    model_key=model_key,
    window=window,
    pad=pad )
mp_list.append(
    cloud_score,
    im,
    window=window,
    pad=pad )
preds,(cmask,cscores)=mp_list.run()
```

```python
""" MPList
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
```


---

#### PYPI

```bash
python setup.py sdist
twine upload dist/*
```