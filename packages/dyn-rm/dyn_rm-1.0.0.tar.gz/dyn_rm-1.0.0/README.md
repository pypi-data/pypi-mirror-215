# Time-X EuroHPC project: Dynamic Resource Manager

This repo contains Python scripts for a dynamic resource manager to be used with the [Time-X dynamic MPI Extensions](https://gitlab.inria.fr/dynres/dyn-procs/ompi).

The resource manager connects as PMIx Tool to the PMIx server of PRRTE and can then control PSet operations and spawn new jobs. 

At the moment it only supports very basic management, but it can be extended with more sophisticated scheduling policies (see corresponding class in my_system.py)

## Running the resource manager

The command to run jobs with the dynamic resource manager is:

```
python3 dynamic_resource_manager.py --jobs=[path_to_job_mix_file] --host=[host_names:slots] (optional: --verbosity=[1,4] (default: 1)) (optional: --sched_interval=[float] (default: 1))`
```

There are example job mix files provided in the examples subdirectory.
The command to run the resource manager on a system with 4 nodes á 8 slots and the job mix file "job_mix_alternate.txt" looks as like this:

```
python3 dynamic_resource_manager.py --jobs=examples/job_mix_alternate.txt --host=n01:8,n02:8,n03:8,n04:8
```

