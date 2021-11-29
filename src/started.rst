Getting Started
===============

IgnisHPC is a modularized docker framework consisting of multiple source code repositories. The framework is 
OpenSource and all repositories can be found in GitHub: `IgnisHPC <https://github.com/ignishpc>`_.

The following is a summary of the minimum steps to run a minimum job in IgnisHPC.

------------
Requirements
------------

IgnisHPC is a dockerized framework, all system modules are executed inside docker containers. In addition, 
IgnisHPC external dependencies such as Schedulers or image storage can be installed independently, but IgnisHPC 
includes a dockerized version of them.

Therefore, the minimum requirements to run Ignis are:

  1. Docker: It must be installed and accessible. All modules will be launched as containers. It is recommended 
     to use the newest version available.
  2. Python3: Available by default in most linux distributions. It is used to run a deploy script and simplify 
     the execution of IgnisHPC and its dependencies.
  3. Pip: The IgnisHPC deploy script is available as a pip package, although it can be downloaded from source, 
     this is the quickest and easiest way.
  4. Git (optional): The git binary is required for building IgnisHPC images from repositories.
   
   
------------
Installation
------------

IgnisHPC can be installed just by running::

 $ pip install ignishpc

Once the command is executed, we can check that we have the ``ignis-deploy`` command available in the path.
This process must be carried out in all the nodes where IgnisHPC is going to be executed.


----------------------------
Creating IgnisHPC Containers
----------------------------

Images of IgnisHPC containers are not available for download, they must be built in your runtime environment. 
This allows the creation of custom development environments with full isolation from other framework installations 
even on the same machines.

In this example we will use a local docker repository and ignishpc as the base path for all images.
::

 $ ignis-deploy registry start --default

| This command will launch a docker repository that will be available on port 5000. 
| ``--default`` parameter indicates that other calls to ``ignis-deploy`` should use this repository as the default source. 


Once executed we will receive the following warning:

.. code-block:: text

    info: add '{insecure-registries" : [ "myhost:5000" ]}' to /etc/docker/daemon.json and restart 
           docker daemon service
          use myhost:5000 to refer the registry
          
The docker registry requires a certificate for validation, we can create one locally or add 
``{insecure-registries" : [ "myhost:5000" ]}`` to ``/etc/docker/daemon.json`` to force docker to use an insecure one. Do not forget 
to restart the docker daemon to reload the configuration.

Once the registration is available, we can proceed to the creation of IgnisHPC images::

 $ ignis-deploy images build --full --sources \
    https://github.com/ignishpc/dockerfiles.git \
    https://github.com/ignishpc/backend.git \
    https://github.com/ignishpc/core-cpp.git \
    https://github.com/ignishpc/core-python.git

The first two repositories are essential for the construction of the base images. The command can be executed in several phases, it is 
not necessary to specify all the repositories in the same execution. The only restriction is that if you use the ``--full`` parameter, which 
creates an extra image with all core repositories, you must have all cores you want to use together. This allows you to create an 
image that can run Python and C++ in the same container. 

-----------------------------
Deploying IgnisHPC Containers
-----------------------------

Once all images are created, it can be executed. IgnisHPC jobs are launched with the Submitter module, but we need a Scheduler, 
so we must first launch one. 

Docker (Only local)
^^^^^^^^^^^^^^^^^^^^
Submitter using a http endpoint::

 $ ignis-deploy submitter start --dfs <working-directory-path> --scheduler docker tcp://myhost:2375

Submitter using a Unix-socket::

 $ ignis-deploy submitter start --dfs <working-directory-path> --scheduler docker /var/run/docker.sock \
   --mount /var/run/docker.sock /var/run/docker.sock


Nomad
^^^^^

First node::

 $ ignis-deploy nomad start --password 1234
 
Remainder nodes::

 $ ignis-deploy nomad start --password 1234 --join myhost1 --default-registry myhost1:5000 
 
Submitter::

 $ ignis-deploy submitter start --dfs <working-directory-path\*> \ 
    --scheduler nomad http://myhostX:4646
 
 
\* The working directory must be available on all nodes via an NFS (Network File System) or a DFS (Distributed File 
System). (Only required for working with files)
 
Mesos
^^^^^

Zookeeper is requiered by mesos::

 $ ignis-deploy zookeeper start --password 1234
 
Master node::

 $ ignis-deploy mesos start -q 1 --name master -zk  zk://master:2281 \
    --service [marathon | singularity] --port-service 8888
 
Worker nodes::

 $ ignis-deploy mesos start --name nodoX -zk  zk://master:2281 \
    --port-service 8888 --default-registry master:5000
 
Submitter::

 $ ignis-deploy submitter start --dfs <working-directory-path*> \
    --scheduler [marathon | singularity] http://master:8888 


\* The working directory must be available on all nodes via an NFS (Network File System) or a DFS (Distributed File 
System). (Only required for working with files)


-----------------------
Launching the first Job
-----------------------

The first step to launch a job is to connect to the Submiter container, default password is ``ignis``, we can change 
it inside the container or choose one when we launch the submitter.::

 $  ssh root@myhost -p 2222 
 
The code we will use as an example is the classic Wordcount, which can be seen below.
 
.. code-block:: python

    #!/usr/bin/python
   
    import ignis

    # Initialization of the framework
    ignis.Ignis.start()
    # Resources/Configuration of the cluster
    prop = ignis.IProperties()
    prop["ignis.executor.image"] = "ignishpc/python"
    prop["ignis.executor.instances"] = "1"
    prop["ignis.executor.cores"] = "2"
    prop["ignis.executor.memory"] = "1GB"
    # Construction of the cluster
    cluster = ignis.ICluster(prop)

    # Initialization of a Python Worker in the cluster
    worker = ignis.IWorker(cluster, "python")
    # Task 1 - Tokenize text into pairs ('word', 1)
    text =  worker.textFile("text.txt")
    words = text.flatmap(lambda line: [(word, 1) for word in line.split()])
    # Task 2 - Reduce pairs with same word and obtain totals
    count = words.reduceBykey(lambda a, b: a + b)
    # Print results to file
    count.saveAsTextFile("wordcount.txt")

    # Stop the framework
    ignis.Ignis.stop()
    
    
In order to run it, we need to create a file containing a text sample (``text.txt``) and store it in the working 
directory. By default the submitter sets the working directory to ``/media/dfs``. All relative paths used in the 
source code are resolved using this working directory, so ``/media/dfs/text.txt`` is an alias of ``text.txt``.

Finally, we can execute our code using the submitter::

 $ ignis-submit ignishpc/python python3 driver.py

or::

  $ ignis-submit ignishpc/python ./driver.py 


When the execution has finished, we can see the result of the execution in ``wordcount.txt`` located in the working
directory. If we want to check the execution logs, we must navegate to the scheduler web or use ``docker log`` in case 
of using docker directly.

 

 

    

