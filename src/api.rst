API
===


-------------------
BasicType Reference
-------------------

.. class:: Boolean

    References True of False value condition.

.. class:: Integer

    References a non-decimal number.

.. class:: Float

    References a decimal number.

.. class:: String

    References a text type.
    
.. class:: Json

    References a json type, each language implements it in a different way.

.. class:: List(T)

    References a ordered collection.
    
    :param T: Element type.

.. class:: Map(K, V)

    References a mapping between a key and a value.
    
    :param K: Key type.
    :param V: Value type.

------
Driver
------

Ignis
^^^^^

The class :class:`Ignis` manages the driver environment. Any driver function called before :meth:`Ignis.start` and 
after :meth:`Ignis.stop` will fail.

.. class:: Ignis()

    .. method::  start()
        :staticmethod:
    
        Starts the driver environment. The backend module is launched as a sub-process and the other driver functions 
        can now be called. The function will not return until the entire backend configuration process has been completed.
        
    .. method:: stop()
        :staticmethod:
        
        Stops the driver environment. The Backend releases all resources and finishes its execution.  The function will
        not return until backend has finished.


IProperties
^^^^^^^^^^^

The class :class:`IProperties` represents a persistent set of properties. Properties can be read, modified or deleted, 
initially instances do not contain any properties. If a property that is not stored is read, its default value will be 
returned if it exists.

.. class:: IProperties()

    .. method:: set(key, value)
    
        Sets a new property with the specified key.
    
        :param String key: Property key.
        :param String value: Property value.
        :return: previous value for ``key`` or an empty string.
        :rtype: String
        
    .. method:: get(key)
    
        Searches for the property with the specified key. If the key is not found, default value is returned. 
    
        :param String key: Property key.
        :return: value for ``key`` or an empty string if it has no default value..
        :rtype: String
        
    .. method:: rm(key)
    
        Removes a property with the specified key and returns its current value. 
        
        :param String key: Property key.
        :return: value for ``key`` or an empty string.
        :rtype: String
        
    .. method:: contains(key)
    
        Returns True if property with the specified key has a value or a default value.
        
        :param String key: Property key.
        :return: property with ``key`` is defined.
        :rtype: Boolean
        
        
    .. method:: toMap(defaults)
    
        Gets all properties and their values.
        
        :param Boolean defaults: if true, unstored properties with default values are also returned.
        :return: all properties and their values.
        :rtype: Map(String, String)
        
    .. method:: fromMap(map)
    
        Sets all properties defined in the argument.
        
        :param Map(String, String) map: A set of properties with their values.
       
        
    .. method:: load(path)
    
        Sets all properties defined in the file references by the path. The file must be formatted as 
        `.properties format <https://en.wikipedia.org/wiki/.properties>`_ where each line stores a 
        property as ``key=value`` or ``key:value`` format.
        
        :param String path: File path.
        :exception IDriverException: An error is generated if the file does not exist, cannot be read or has an 
         incorrect format.
        
    .. method:: store(path)
    
        Stores all properties defined in the file references by the path. 
    
        :param String path: File path.
        :exception IDriverException: An error is generated if the file cannot be created.
        
    .. method:: clear()
    
        Removes all properties. 


ICluster
^^^^^^^^

The class :class:`ICluster` represents a group of executors containers. Containers are identical 
instances with the same assigned resources, which are obtained from the properties defined in :class:`IProperties`.

.. class:: ICluster(properties, name)

    :param IProperties properties: Set of properties that will be used to configure the execution environment. Future
     modifications to the properties will have no effect.
    :param String name: (Optional) Gives a name to the :class:`ICluster`, it will be used to identify the 
     :class:`ICluster` in the job logs and also in the Scheduler, if it supports it.


    .. method:: start()
    
        By default, the cluster will only be started when the first computation is to be performed.  This function allows 
        you to force their creation and eliminate the time associated with requesting and granting resources. It must be 
        used to perform performance measurements on the platform.
    

    .. method:: destroy()

        Destroys the current running environment and frees all resources associated with it. Future executions will have 
        to recreate the environment from scratch.

    .. method:: setName(name)

        Sets or changes the name associated with the :class:`ICluster`. The new name will only affect the :class:`ICluster` 
        log itself and future tasks created. The Scheduler and the existing tasks will keep the name used during their 
        creation.
        
        :param String name: New name.

    .. method:: execute(args)
    
        Runs a command on all containers associated with the :class:`ICluster`. This function does not trigger the creation 
        of the :class:`ICluster`, it will only be executed if the environment has already been created previously, otherwise 
        the function will be registered to be invoked immediately after its creation.
    
        :param List(String) args: Command and its arguments.


    .. method:: executeScript(script)
    
        Like :meth:`ICluster.execute` but argument is a shell script instead of single command.
    
        :param String script: Linux Shell script.


    .. method:: sendFile(source, target)
    
        Sends a file to all containers associated with the :class:`ICluster`. This function does not trigger the creation 
        of the :class:`ICluster`, the file only be sent if  the environment has already been created previously, otherwise 
        the function will be registered to be invoked immediately after its creation.
    
        :param String source: Source path in driver container.
        :param String target: Target path in each executor container.


    .. method:: sendCompressedFile(source, target)
    
        Like :meth:`ICluster.sendFile` but file is extracted once it has been sent. Supported formats are: ``.tar``, 
        ``.tar.bz2``, ``.tar.bz``, ``.tar.xz``, ``.tbz2``, ``.tgz``, ``.gz``, ``.bz2``,  ``.xz``, ``.zip``, ``.Z``.
        Note that ``.rar`` is also supported, but its license requires it to be installed by the user.

ISource
^^^^^^^

The class :class:`ISource` is an auxiliary class used by meta-functions in the driver. A meta-function is a function that
defines part of its implementation using another function that is passed as a parameter. The way in which the function is 
defined depends on each implementation. 

Typically the following format should be available:

1. *Ignis path*: String representation consisting of a file path and a class. The file indicates where the code is stored 
   and the class defines the function to be executed. Format is as follows: ``path:class``

2. *Name*: Defines only the name of the function, it is also defined as a string and differs from the previous case 
   because it does not contain ``:`` separator.

3. *Source Code*: Function is defined using the syntax of the executor's source code. Executor will recognize it as 
   source code and compile it if necessary.

4. *Lambda*: The function is defined in the driver code and then sent as bytes to the executor. In this case driver 
   and executor must be programmed in the same programming language and it must support serialization of executable code.


.. class:: ISource(function, native)

    :param function: Overloaded argument to accept all possible function definitions supported in each implementation.
    :param Boolean native: (Optional) Type of serialization used to send parameters. If true, the driver language's own 
     serialization will be used, if and only if the executor also has the same language. Otherwise the multi-language 
     serialization will always be used.
    

    .. method:: addParam(name, value)

        Defines a parameter associated with the function. The value of the parameter can be obtained by the get function
        during its execution.
        
        :param String name: Parameter name.
        :param value: Value to be stored in the parameter, can have any type.

IWorker
^^^^^^^

The class :class:`IWorker` represents a group of processes of the same programming language. There is at least one 
process in each of the :class:`ICluster` containers where the worker is created, and all containers have the same number
of executor processes. 

.. class:: IWorker(cluster, type, name, cores, instances)

    :param ICluster cluster: :class:`ICluster` where the executors will be created. 
    :param String type: Name of the worker to be used, the names of the workers are associated to the programming language
     they execute. The available workers are associated with the image used to create the class :class:`ICluster`.
    :param String name: (Optional) Like :class:`ICluster` a worker can have a name that identifies it in the job log.
    :param Integer cores: (Optional) Number of cores associated to each executor, by default each executor uses all
     available cores inside the container.
    :param Integer instances: (Optional) Number of executors to be launched in each container, by default 
     only one is launched.


    .. method:: start()
    
        By default, the worker will only be started when the first computation is to be performed.  This function allows 
        you to force their creation.
    

    .. method:: destroy()

        Destroys all processes associated with the worker. Future executions will have to start the processes again. 
        Destroying the executors means deleting cached data in memory, only disk cache will be kept.


    .. method:: getCluster()
    
        gets :class:`ICluster` where worker is created.


    .. method:: setName(name)

        Sets or changes the name associated with the :class:`IWorker`. The new name will only affect the worker
        log itself and future tasks created. Existing tasks will keep the name used during their creation.
        
        :param String name: New name.

    .. method:: parallelize(data, partitions, src, native)
    
       Creates a :class:`IDataFrame` from an existing collection present in the driver. The elements present in the collection 
       are distributed to the executors for a parallel processing.
       
       :param List(T) data: A collection object present in the driver.
       :param Integer partitions: How many partitions the collection elements will be divided. For optimal processing, there 
         should be at least one partition for all cores on each of the executors.
       :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
        Must implement at least :class:`IBeforeFunction` interface.
       :param Boolean native: (Optional) Type of serialization used to send data. If true, the driver language's own 
        serialization will be used, if and only if the executor also has the same language. Otherwise the multi-language 
        serialization will always be used.
       :return: A parallel collection with the same type of ``data`` elements.
       :rtype: IDataFrame(T)

    .. method:: importDataFrame(data, src)

        Imports a parallel collection from another worker. The number of partitions will be the same as in the original
        worker. 
        
        :param IDataFrame(T) data: Parallel collection of source data.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at least :class:`IBeforeFunction` interface.      
        :return: A parallel collection with ``data`` elements.
        :rtype: IDataFrame(T)


    .. method:: textFile(path, minPartitions)

        Creates a parallel collection by splitting a text file to create at least ``minPartitions`` partitions.
        
        :param String path: File path.
        :param Integer minPartitions: Minimal number of partitions.
        :return: A parallel collection of strings.
        :rtype: IDataFrame(String)
        :exception IDriverException: An error is generated if the file does not exist or cannot be read.

    .. method:: partitionObjectFile(path, src)
    
        Creates a parallel collection from binary partition files. 
        See :meth:`IDataFrame.saveAsObjectFile`
        
        :param String path: File path without the ``.part*`` extension.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at east :class:`IBeforeFunction` interface.  
        :return: A parallel collection with type stored in the binary file.
        :rtype: IDataFrame(T)
        :exception IDriverException: An error is generated if any file do not exist or cannot be read.


    .. method:: partitionTextFile(path)
    
        Creates a parallel collection from text partition files. 
        See :meth:`IDataFrame.saveAsTextFile`
        
        :param String path: File path without the ``.part*`` extension.
        :return: A parallel collection of strings.
        :rtype: IDataFrame(String)
        :exception IDriverException: An error is generated if any file do not exist or cannot be read.


    .. method:: partitionJsonFile(path, src, objectMapping)
    
        Creates a parallel collection from json partition files. 
        See :meth:`IDataFrame.saveAsJsontFile`
        
        :param String path: File path without the ``.part*`` extension.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at least :class:`IBeforeFunction` interface.  
        :param Boolean objectMapping: (Optional) If true, json objects are transformed to objects. 
        :return: A parallel collection of mapped object, if ``objectMapping`` is true or otherwise a generic json type is used.
        :rtype: IDataFrame(Json) or IDataFrame(T).
        :exception IDriverException: An error is generated if any file do not exist or cannot be read.


    .. method:: loadLibrary(path)
    
        Loads a library of functions in the executor processes. Functions may be invoked using only their name in any 
        :class:`ISource`. Library type depends on the programming language of executor.
        
        The library can be defined in two ways:
        
        1. Path to a library file. Library must be compiled if the language requires it.     
        2. Source code in plain text, executor will take care of compiling if necessary. This allows you to create 
           functions dynamically from the driver. 
        
        :param String path: Library path or Source code.
        :exception IDriverException: An error is generated if libreary does not exist or cannot be read.


    .. method:: execute(src)
    
        Runs a `IVoidFunction0` in the executors. 
        
        :param ISource src: Function to be executed, it must implement `IVoidFunction0` interface.


    .. method:: executeTo(src)

        Runs a `IFunction0` in the executors. 
        
        :param ISource src: Function to be executed, it must implement `IFunction0` interface.
        :return: A parallel collection created with the elements returned by ``src`` function.
        :rtype: IDataFrame(T).

    .. method:: call(src, data)
    
        Runs a function that has been previously loaded by :meth:`IWorker.loadLibrary`. Values returned by the function
        will generate a parallel collection. Note, this function is designed to execute functions in format *name*, it 
        does not allow to use the other formats.
        
        :param ISource src: Function name and its arguments. It must implement `IFunction` interface if ``data`` is supplied
         or `IFunction0` otherwise. 
        :param IDataFrame(T) data: (Optional) A parallel collection of data to be processed by the ``src`` function.
        :return: A parallel collection created with the elements returned by ``src`` function.
        :rtype: IDataFrame(T).

    .. method:: voidCall(src, data)
    
        Runs a function that has been previously loaded by :meth:`IWorker.loadLibrary`. Like :meth:`IWorker.call` but
        with no return.
        
        :param ISource src: Function name and its arguments. It must implement `IVoidFunction` interface if ``data`` is supplied or
         `IVoidFunction0` otherwise. Note, this function is designed to execute functions in format *name*, it does not allow to use 
         the other formats.
        :param IDataFrame(T) data: (Optional) A parallel collection of data to be processed by the ``src`` function.


IDataFrame
^^^^^^^^^^

The class :class:`IDataFrame` represents a parallel collection of elements distributed among the worker executors. All 
functions defined within this class process the elements in a parallel and distributed way.


.. class:: IDataFrame

    .. class:: T
        
        Represents the type associated with the parallel collection. Dynamic languages do not have to make it visible 
        to the user, it is the input value type for most of the functions defined in :class:`IDataFrame`
    

    .. method:: setName(name)

        Sets or changes the name associated with the :class:`IDataFrame`. The new name will affect only 
        this :class:`IDataFrame` and future tasks created.
        
        :param String name: New name.    


IDriverException
^^^^^^^^^^^^^^^^

The class :class:`IDriverException` represents an execution error. Exceptions are defined together with the function that
generates them, but they are actually thrown by the function that causes the execution. 

.. class:: IDriverException()


--------
Executor
--------

.. class:: IContext()


.. class:: IBeforeFunction()


.. class:: IVoidFunction0()


.. class:: IVoidFunction()


.. class:: IVoidFunction2()


.. class:: IFunction0()


.. class:: IFunction()


.. class:: IFunction2()