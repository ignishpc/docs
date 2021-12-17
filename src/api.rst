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
    
    
.. class:: Pair(K, V)

    References a combination of key-value types stored together as a pair.
    
    :param K: Key type.
    :param V: Value type.


.. class:: List(T)

    References a ordered collection.
    
    :param T: Element type.

.. class:: Map(K, V)

    References a mapping between a key and a value.
    
    :param K: Key type.
    :param V: Value type.

.. class:: Iterable(T)

    References a collection capable of returning its members one at a time.
    
    :param T: Element type.

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
        :return: This ISource instance.
        :rtype: ISource

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
        Destroying the executors means deleting cached elements in memory, only disk cache will be kept.


    .. method:: getCluster()
    
        gets :class:`ICluster` where worker is created.


    .. method:: setName(name)

        Sets or changes the name associated with the :class:`IWorker`. The new name will only affect the worker
        log itself and future tasks created. Existing tasks will keep the name used during their creation.
        
        :param String name: New name.

    .. method:: parallelize(data, partitions, src, native)
    
       Creates a :class:`IDataFrame` from an existing collection present in the driver. The elements present in the collection 
       are distributed to the executors for a parallel processing.
       
       :param Iterable(T) data: A collection object present in the driver.
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
    
        Runs a function in the executors. 
        
        :param src: Function to be executed.
        :type src: IIVoidFunction0 or ISource


    .. method:: executeTo(src)

        Runs a function in the executors and generates a parallel collection. 
        
        :param ISource src: Function to be executed.
        :type src: IFunction0 or ISource
        :return: A parallel collection created with the elements returned by the function.
        :rtype: IDataFrame(T).

    .. method:: call(src, data)
    
        Runs a function that has been previously loaded by :meth:`IWorker.loadLibrary`. Values returned by the function
        will generate a parallel collection. Note, this function is designed to execute functions in format *name*, it 
        does not allow to use the other formats.
        
        :param src: Function name and its arguments. It must implement `IFunction` interface if ``data`` is supplied
         or `IFunction0` otherwise. 
        :type src: IFunction or IFunction0 or ISource
        :param IDataFrame(T) data: (Optional) A parallel collection of elements to be processed by the ``src`` function.
        :return: A parallel collection created with the elements returned by ``src`` function.
        :rtype: IDataFrame(T).

    .. method:: voidCall(src, data)
    
        Runs a function that has been previously loaded by :meth:`IWorker.loadLibrary`. Like :meth:`IWorker.call` but
        with no return.
        
        :param ISource src: Function name and its arguments. It must implement `IVoidFunction` interface if ``data`` is supplied or
         `IVoidFunction0` otherwise. Note, this function is designed to execute functions in format *name*, it does not allow to use 
         the other formats.
        :type src: IVoidFunction or IVoidFunction0 or ISource
        :param IDataFrame(T) data: (Optional) A parallel collection of elements to be processed by the ``src`` function.


IDataFrame
^^^^^^^^^^

The class :class:`IDataFrame` represents a parallel collection of elements distributed among the worker executors. All 
functions defined within this class process the elements in a parallel and distributed way.
    

.. class:: IDataFrame(T)

    .. class:: T
        
        Represents the type associated with the parallel collection. Dynamic languages do not have to make it visible 
        to the user, it is the input value type for most of the functions defined in :class:`IDataFrame`.
    

    .. method:: setName(name)

        Sets or changes the name associated with the :class:`IDataFrame`. The new name will affect only 
        this :class:`IDataFrame` and future tasks created from it.
        
        :param String name: New name.  

    .. method:: persist(cacheLevel)
    
        Sets a cache level for elements so that it only needs to be computed once.
        
        :param ICacheLevel cacheLevel: level of cache.
        
    .. method:: cache(cacheLevel)
    
        Sets a cache level :class:`ICacheLevel.PRESERVE` for elements so that it only needs to be computed once.

    .. method:: unpersist()
    
        Elements cache is disabled. Alias for :class:`IDataFrame.uncahe`.
        
    .. method:: uncahe()
    
        Elements cache is disabled. Alias for :class:`IDataFrame.unpersist`.
        
    .. method:: partitions()
        
        Gets the number of partitions. 
    
        :return: Number of partitions.
        :rtype: Integer.
        
    .. method:: saveAsObjectFile(path, compression)
    
        Saves elements as binary files.
    
        :param String path: path to store the data.
        :param Integer compression: compresion level (0-9).
        :exception IDriverException: An error is generated if files exists or cannot be write.
        
    .. method:: saveAsTextFile(path)
    
        Saves elements as text files.
    
        :param String path: path to store the data.
        :exception IDriverException: An error is generated if files exists or cannot be write.
        
    .. method:: saveAsJsonFile(path, pretty)
    
        Saves elements as json files.
    
        :param String path: path to store the data.
        :param Boolean pretty: uses an ident format instead of compact.
        :exception IDriverException: An error is generated if files exists or cannot be write.
        
    .. method:: repartition(numPartitions, preserveOrdering, global)
    
        Creates a new Dataframe with a fixes number of partitions. 

        :param Integer numPartitions: number of partitions.
        :param Boolean preserveOrdering: The order of the elements does not change.
        :param Boolean global: Elements are balanced between different executors. If false, Elements are only balanced 
         within each executor.
        :return: A Dataframe with ``numPartitions``.
        :rtype: IDataFrame(T).
        
    .. method:: partitionByRandom(numPartitions)
    
        Creates a new Dataframe with a fixes number of partitions. Elements are randomly distributed among the 
        executors.

        :param Integer numPartitions: number of partitions.
        :return: A Dataframe with ``numPartitions``.
        :rtype: IDataFrame(T).

    .. method:: partitionByHash(numPartitions)
    
        Creates a new Dataframe with a fixes number of partitions. Elements are distributed using a hash function 
        among the executors.

        :param Integer numPartitions: number of partitions.
        :return: A Dataframe with ``numPartitions``.
        :rtype: IDataFrame(T).

    .. method:: partitionBy(src, numPartitions)
    
        Creates a new Dataframe with a fixes number of partitions. Elements are distributed using a custom function 
        among the executors. The same function return assigns the same partition.

        :param src: Function argument.
        :type src: IFunction(T, Integer) or ISource.
        :param Integer numPartitions: number of partitions.
        :return: A Dataframe with ``numPartitions``.
        :rtype: IDataFrame(T).

    .. method:: map(src)
    
        Performs a map operation.

        :param src: Function argument.
        :type src: IFunction(T, R) or ISource.
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(R).

    .. method:: filter(src)
    
        Performs a filter operation. Only items that return True will be retained.

        :param src: Function argument.
        :type src: IFunction(T, Boolean) or ISource.
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(T).

    .. method:: flatmap(src)
    
        Performs a flatmap operation. Like :class:`IDataFrame.map` but each element
        can generate any number of results. 

        :param src: Function argument.
        :type src: IFunction(T, Iterable(R)) or ISource.
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(R).

    .. method:: keyBy(src)
    
        Assigns each element a key with the return of the function.

        :param src: Function argument.
        :type src: IFunction(T, R) or ISource.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(R, T).

    .. method:: mapPartitions(src, preservesPartitioning)
    
        Performs a specialized map that is called only once for each partition, elements can be accessed using an 
        iterator.
    
        :param src: Function argument.
        :type src: IFunction(IReadIterator(T), Iterable(R)) or ISource.
        :param Boolean preservesPartitioning: Preserves partitioning
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(R).

    .. method:: mapPartitionsWithIndex(src, preservesPartitioning)
    
        Performs a specialized map that is called only once for each partition, elements can be accessed using an 
        iterator. Like :class:`IDataFrame.mapPartitions` but the partition index is available as the first argument
        of the function.
    
        :param src: Function argument.
        :type src: IFunction2(Integer, IReadIterator(T), Iterable(R)) or ISource.
        :param Boolean preservesPartitioning: Preserves partitioning
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(R).

    .. method:: mapExecutor(src)
    
        Performs a specialized map that is called only once for each executor, elements can be accessed using a 
        list of lists where first list represents each partition. Function argument can be modified to add or 
        remove values, if you want to generate other value type use :class: `IDataFrame.mapExecutorTo`.
    
        :param src: Function argument.
        :type src: IVoidFunction(List(List(T))) or ISource.
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(R).

    .. method:: mapExecutorTo(src)
    
        Performs a specialized map that is called only once for each executor, elements can be accessed using a 
        list of lists where first list represents each partition. A new list of lists must be returned to 
        generate new partitions.
    
        :param src: Function argument.
        :type src: IFunction(List(List(T)), List(List(R))) or ISource.
        :return: A Dataframe with result elements.
        :rtype: IDataFrame(R).

    .. method:: groupBy(src, numPartitions)
    
        Groups elements that share the same key, which is obtained from the return of the function.
    
        :param src: Function argument.
        :type src: IFunction(T, R)) or ISource.
        :param Integer numPartitions: (Optional) Number of resulting partitions.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(R, List(T)).

    .. method:: sort(ascending, numPartitions)
    
        Sort the elements using their natural order.
    
        :param Boolean ascending: Allows you to choose between ascending and descending order.
        :param Integer numPartitions: (Optional) Number of resulting partitions.
        :return: A Dataframe  with result elements.
        :rtype: IDataFrame(T).

    .. method:: sortBy(src, ascending, numPartitions)
    
        Sort the elements using a custom function, that checks if the first argument is less than the second.
    
        :param src: Function argument.
        :type src: IFunction2(T, T, Boolean)) or ISource.   
        :param Boolean ascending: Allows you to choose between ascending and descending order.
        :param Integer numPartitions: (Optional) Number of resulting partitions.
        :return: A Dataframe  with result elements.
        :rtype: IDataFrame(T).

    .. method:: union(other, preserveOrder, src)
    
        Merges elements of two dataframes.
    
        :param IDataFrame(T) other: other dataframe.
        :param Boolean preserveOrder: If true, the second dataframe is concatenated to the first, otherwise they are
         mixed.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at east :class:`IBeforeFunction` interface.  
        :return: A Dataframe  with result elements of the two dataframes.
        :rtype: IDataFrame(T).

    .. method:: distinct(numPartitions, src)
    
        Duplicate elements are eliminated.
    
        :param Integer numPartitions: Number of resulting partitions.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at east :class:`IBeforeFunction` interface.  
        :return: A Dataframe  with result elements.
        :rtype: IDataFrame(T).

    .. method:: reduce(src)
    
        Accumulate the elements using a custom function, which must be associative and commutative.  
        Like :class:`IDataFrame.treeReduce` but final accumulation is performed in a single executor.
    
        :param src: Function argument.
        :type src: IFunction2(T, T, T)) or ISource.  
        :return: Element resulting from accumulation.
        :rtype: T

    .. method:: treeReduce(src)
    
        Accumulate the elements using a custom function, which must be associative and commutative.  
        Like :class:`IDataFrame.reduce` but final accumulation is performed in parallel using multiple executors.
    
        :param src: Function argument.
        :type src: IFunction2(T, T, T)) or ISource.  
        :return: Element resulting from accumulation.
        :rtype: T

    .. method:: collect()
    
        Retrieve all the elements.
    
        :return: All the elements.
        :rtype: List(T)

    .. method:: aggregate(zero, seqOp, combOp)
    
        Accumulate the elements using two functions, which must be associative and commutative.  
        Like :class: IDataFrame.treeAggregate` but final accumulation is performed in a single executor.
    
        :param zero: Function argument to generate initial value of target type.
        :type zero: IFunction0(R)) or ISource.  
        :param seqOp: Function argument to accumulate the elements of each partition.
        :type seqOp: IFunction2(T, R, R)) or ISource.  
        :param combOp: Function argument to accumulate the results of all partitions .
        :type combOp: IFunction2(R, R, R)) or ISource.  
        :return: Element resulting from accumulation.
        :rtype: R

    .. method:: treeAggregate(zero, seqOp, combOp)
    
        Accumulate the elements using two functions, which must be associative and commutative.  
        Like :class:`IDataFrame.aggregate` but final accumulation is performed in parallel using multiple executors.
    
        :param zero: Function argument to generate initial value of target type.
        :type zero: IFunction0(R)) or ISource.  
        :param seqOp: Function argument to accumulate the elements of each partition.
        :type seqOp: IFunction2(T, R, R)) or ISource.  
        :param combOp: Function argument to accumulate the results of all partitions .
        :type combOp: IFunction2(R, R, R)) or ISource.  
        :return: Element resulting from accumulation.
        :rtype: R
    .. method:: fold(zero, src)
    
        Accumulate the elements using a initial value and custom function, which must be associative and commutative.  
        Like :class:`IDataFrame.treeFold` but final accumulation is performed in a single executor.
    
        :param zero: Function argument to generate initial value of target type.
        :type zero: IFunction0(R)) or ISource.  
        :param src: Function argument to accumulate.
        :type src: IFunction2(T, T, T)) or ISource.  
        :return: Element resulting from accumulation.
        :rtype: T

    .. method:: treeFold(zero, src)
    
        Accumulate the elements using a initial value and custom function, which must be associative and commutative.  
        Like :class:`IDataFrame.treeFold` but final accumulation is performed in parallel using multiple executors.
    
        :param zero: Function argument to generate initial value of target type.
        :type zero: IFunction0(R)) or ISource.  
        :param src: Function argument to accumulate.
        :type src: IFunction2(T, T, T)) or ISource.  
        :return: Element resulting from accumulation.
        :rtype: T

    .. method:: take(num)
    
        Retrieves the first ``num`` elements.
    
        :param Integer num: Number of elements.
        :return: First ``num`` elements.
        :rtype: List(T).

    .. method:: foreach(src)
    
        Calls a custom function once for each element.
    
        :param src: Function argument.
        :type src: IVoidFunction(T) or ISource.

    .. method:: foreachPartition(src)
    
        Calls a custom function once for each partition, elements can be accessed using an iterator.
    
        :param src: Function argument.
        :type src: IVoidFunction(IReadIterator(T)) or ISource.

    .. method:: foreachExecutor(src)
    
        Calls a custom function once for each executor, elements can be accessed using a list of lists where first list
        represents each partition.
    
        :param src: Function argument.
        :type src: IVoidFunction(List(List(T))) or ISource.

    .. method:: top(num, cmp)
    
        Retrieves the first ``num`` elements in descending order. A custom function can be used to checks if the first
        argument is less than the second
        
        :param Integer num: Number of elements.
        :param cmp: (Optional) Comparator to be used instead of the natural order.
        :type cmp: IFunction2(T, T, Boolean)) or ISource.  
        :return: First ``num`` elements.
        :rtype: List(T)

    .. method:: takeOrdered(num, cmp)
    
        Retrieves the first ``num`` elements in ascending order. A custom function can be used to checks if the first
        argument is less than the second
        
        :param Integer num: Number of elements.
        :param cmp: (Optional) Comparator to be used instead of the natural order.
        :type cmp: IFunction2(T, T, Boolean)) or ISource.
        :return: First ``num`` elements.
        :rtype: List(T)

    .. method:: sample(withReplacement, fraction, seed)
    
        Generates a random sample records from the original elements.
    
        :param Boolean withReplacement: An element can be selected more than once.
        :param Float fraction: Percentage of the sample.
        :param Integer seed: Initializes the random number generator.
        :return: A Dataframe  with result elements.
        :rtype: IDataFrame(T).

    .. method:: takeSample(withReplacement, num, seed)
    
        Generates and Retrieves a random sample of ``num`` records from the original elements.
    
        :param Boolean withReplacement: An element can be selected more than once.
        :param Integer num: Number of elements.
        :param Integer seed: Initializes the random number generator.
        :return: A Dataframe  with result elements.
        :rtype: IDataFrame(T).

    .. method:: count()
    
        Count the elements.
    
        :return: Number of elements.
        :rtype: Integer

    .. method:: max(cmp)
    
        Retrieves the element with the maximum value. A custom function can be used to checks if the first argument is
        less than the second. Like :class:`Dataframe.top` with ``num=1``
        
        :param Integer num: Number of elements.
        :param cmp: (Optional) Comparator to be used instead of the natural order.
        :type cmp: IFunction2(T, T, Boolean)) or ISource.
        :return: Element with the maximum value.
        :rtype: T

    .. method:: min(cmp)
    
        Retrieves the element with the minimal value. A custom function can be used to checks if the first argument is
        less than the second. Like :class:`Dataframe.takeOrdered` with ``num=1``
        
        :param Integer num: Number of elements.
        :param cmp: (Optional) Comparator to be used instead of the natural order.
        :type cmp: IFunction2(T, T, Boolean)) or ISource  .
        :return: Element with the minimal value.
        :rtype: T

    .. method:: toPair()
    
        Converts :class:`IDataFrame` to `IPairDataFrame` when :class:`IDataFrame.T` is a :class:`Pair` of
        :class:`IPairDataFrame.K` and :class:`IPairDataFrame.V`.        
    
        :return: A Dataframe of pairs
        :rtype: IPairDataFrame(K, V)
        
.. class:: IPairDataFrame(K, V)

    Extends :class:`IDataFrame` funtionality when :class:`IDataFrame.T` is a :class:`Pair`

    .. class:: K
        
        Represents the value type associated with the parallel collection. Dynamic languages do not have to make it visible 
        to the user, it is the key input value type for most of the functions defined in :class:`IPairDataFrame`.
        
    .. class:: V
        
        Represents the value type associated with the parallel collection. Dynamic languages do not have to make it visible 
        to the user, it is the value input value type for most of the functions defined in :class:`IPairDataFrame`.
    


    .. method:: join(other, preserveOrder, numPartitions, src)
    
        Joins an element of this collection with an element of ``other`` that share the same key.
    
        :param IPairDataFrame(K, V) other: other dataframe.
        :param Integer numPartitions: Number of resulting partitions.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at east :class:`IBeforeFunction` interface.  
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, Pair(V, V)).

    .. method:: flatMapValues(src)
        
        Performs a map function only on the values while preserving the key. Like :class:`IPairDataFrame.mapValues` but each 
        element can generate any number of results, key is duplicated or deleted if necessary.

        :param src: Function argument.
        :type src: IFunction(V, R) or ISource.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, R).

    .. method:: mapValues(src)
    
        Performs a map function only on the values while preserving the key.

        :param src: Function argument.
        :type src: IFunction(V, R) or ISource.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, R).

    .. method:: groupByKey(numPartitions, src)
    
        Groups elements that share the same key.
    
        :param Integer numPartitions: Number of resulting partitions.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at east :class:`IBeforeFunction` interface.  
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, List(V)).

    .. method:: reduceByKey(src, numPartitions, localReduce)
    
        Accumulate the values that share the same key using a custom function, which must be associative and 
        commutative. 
    
        :param src: Function argument.
        :type src: IFunction2(V, V, V)) or ISource.  
        :param Integer numPartitions: Number of resulting partitions.
        :param Boolean localReduce: Accumulate the values that share the same key in a executor before global 
         accumulation. Reduces the size of the exchange if there are duplicated keys in multiple partitions.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, V).

    .. method:: aggregateByKey(zero, seqOp, combOp, numPartitions)
    
        Accumulate the values that share the same key using two functions, which must be associative and commutative. 
    
        :param zero: Function argument to generate initial value of target type.
        :type zero: IFunction0(R)) or ISource.  
        :param seqOp: Function argument to accumulate the values that share the same key of each partition.
        :type seqOp: IFunction2(V, R, R)) or ISource.  
        :param combOp: Function argument to accumulate the results that share the same key of all partitions .
        :type combOp: IFunction2(R, R, R)) or ISource.  
        :param Integer numPartitions: Number of resulting partitions.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, V).

    .. method:: foldByKey(zero, src, numPartitions, localFold)
    
        Accumulate the values that share the same key using a initial value and custom function, which must be 
        associative and commutative. 
    
        :param zero: Function argument to generate initial value of target type.
        :type zero: IFunction0(R)) or ISource.  
        :param src: Function argument to accumulate.
        :type src: IFunction2(V, V, V)) or ISource. 
        :param Integer numPartitions: Number of resulting partitions.
        :param Boolean localFold: Accumulate the values that share the same key in a executor before global 
         accumulation. Reduces the size of the exchange if there are duplicated keys in multiple partitions.
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, V).

    .. method:: sortByKey(ascending, numPartitions, src)
    
        Sort the keys using their natural order. 
    
        :param Boolean ascending: Allows you to choose between ascending and descending order.
        :param Integer numPartitions: Number of resulting partitions.
        :param ISource src: (Optional) Auxiliary function to configure executor, its use may vary between languages. 
         Must implement at east :class:`IBeforeFunction` interface.  
        :return: A Dataframe of pairs with result elements.
        :rtype: IPairDataFrame(K, V).

    .. method:: keys()
    
        Retrieve unique keys.
    
        :return: The unique keys.
        :rtype: List(K)

    .. method:: values()
    
        Retrieve unique values.
    
        :return: The unique values.
        :rtype: List(V)

    .. method:: sampleByKey(withReplacement, fractions, seed, native)
    
        Generates a random sample records from the values that share the same key.
    
        :param Boolean withReplacement: An element can be selected more than once.
        :param Map(K, Float) fraction: Percentage of the sample by key. Absences are taken as zero.
        :param Integer seed: Initializes the random number generator.
        :param Boolean native: (Optional) sends ``fractions`` with native serialization.
        :return: A Dataframe  with result elements.
        :rtype: IDataFrame(T).  

    .. method:: countByKey()
    
        Count unique keys.
    
        :return: Number unique of values.
        :rtype: Integer

    .. method:: countByValue()
    
        Count unique keys.
    
        :return: Number unique of values.
        :rtype: Integer

        
.. class:: ICacheLevel

    .. py:data:: NO_CACHE
        :type: Integer
        :value: 0
        
        Elements cache is disabled.

    .. py:data:: PRESERVE
        :type: Integer
        :value: 1
        
        Elements will be cached in the same storage in which it is stored.

    .. py:data:: MEMORY
        :type: Integer
        :value: 2
        
        Elements will be cached on memory storage.

    .. py:data:: RAW_MEMORY
        :type: Integer
        :value: 3
        
        Elements will be cached on raw memory storage.

    .. py:data:: DISK
        :type: Integer
        :value: 4
        
        Elements will be cached on disk storage.

IDriverException
^^^^^^^^^^^^^^^^

The class :class:`IDriverException` represents an execution error. Exceptions are defined together with the function that
generates them, but they are actually thrown by the function that causes the execution. 

.. class:: IDriverException()


--------
Executor
--------



.. class:: IContext()
    
    The executor context allows the API functions to interact with the rest of the IgnisHPC system.
    
     .. method:: cores()
     
        :return: Number of cores assigned to the executor. 
        :rtype: Integer 
        
     .. method:: executors()
     
        :return: Number of executors. 
        :rtype: Integer 
        
     .. method:: executorId()
         
        :return: Unique identifier of the executor, a number greater than or equal to zero and less than the number
          of executors.
        :rtype: Integer 
        
        
    .. method:: threadId()
         
        :return: Unique identifier of the current thread, a number greater than or equal to zero and less than the
         than the number of cores.
        :rtype: Integer 
        
    .. method:: mpiGroup()
       
        :return: Returns the mpi group of the executors. 
        
    .. method:: props()
    
        :return: Driver :class:`IProperties` as :class:`Map` object.
        :rtype: Map(String, String) 
        
    .. method:: vars()
    
        (This function may vary depending on the implementation.)
    
        :return: Variables sent by :class:`ISource.addParam` as :class:`Map` object. 
        :rtype: Map(String, Any) 
    



.. class:: IReadIterator()

    Transverse through elements of a partition.

    .. method:: hasNext()
        
        :return: True if elements remain
        :rtype: Boolean 
    
    
    .. method:: next()

        :return: Next element.


.. class:: IBeforeFunction()

    .. method:: before(context)
    
        :param IContext context: The executor context.


.. class:: IVoidFunction0()

    .. method:: before(context)
    
        :param IContext context: The executor context.
        
    .. method:: call(context)
    
        :param IContext context: The executor context.
        
    .. method:: after(context)
    
        :param IContext context: The executor context.


.. class:: IVoidFunction()

    .. method:: before(context)
    
        :param IContext context: The executor context.
        
    .. method:: call(context, v)
    
        :param IContext context: The executor context.
        :param v: Argument
        
    .. method:: after(context)
    
        :param IContext context: The executor context.


.. class:: IVoidFunction2()

    .. method:: before(context)
    
        :param IContext context: The executor context.
        
    .. method:: call(context, v1, v2)
    
        :param IContext context: The executor context.
        :param v1: Argument 1
        :param v2: Argument 2
        
    .. method:: after(context)
    
        :param IContext context: The executor context.


.. class:: IFunction0()

    .. method:: before(context)
    
        :param IContext context: The executor context.
        
    .. method:: call(context)
    
        :param IContext context: The executor context.
        :return: This function must return a value.
        
    .. method:: after(context)
    
        :param IContext context: The executor context.


.. class:: IFunction()

    .. method:: before(context)
    
        :param IContext context: The executor context.
        
    .. method:: call(context, v)
    
        :param IContext context: The executor context.
        :param v: Argument
        :return: This function must return a value.
        
    .. method:: after(context)
    
        :param IContext context: The executor context.

.. class:: IFunction2()

    .. method:: before(context)
    
        :param IContext context: The executor context.
        
    .. method:: call(context, v1, v2)
    
        :param IContext context: The executor context.
        :param v1: Argument 1
        :param v2: Argument 2
        :return: This function must return a value.
        
    .. method:: after(context)
    
        :param IContext context: The executor context.

