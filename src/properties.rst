===================
Properties
===================

IgnisHPC properties control most of the application settings and are configured separately for each application. Properties can be defined dynamically in the driver code, in the submitter script or as an environment variable. Default values are stored in both cases in ``/opt/ignis/etc/ignis.conf``.

All the system variables start with the prefix *ignis*. They can be of different types:

-  Read-Only variables: contain information about the current job (``ignis.home``, ``ignis.job.name``, ``ignis.job.directory``, …)

-  Driver/submitter variables: must be defined before launching the driver, any later modification will have no effect on the system (``ignis.driver.image``, ``ignis.driver.port``, ``ignis.driver.cores``, …)

-  Executors variables: can be defined by all the available methods. Once the execution environment is created, modifications will have no effect (``ignis.executor.cores``, ``ignis.partition.type``, ``ignis.modules.io.compression``, …)

----------------------
How to set properties?
----------------------

Driver code
^^^^^^^^^^^

Driver has a Properties object available that allows users to read and write properties. The default values can be overwritten but will recover their value if the property is deleted.

See the driver section for more details.

Enviroment variable
^^^^^^^^^^^^^^^^^^^

Driver and submitter scan the environment variables for properties at startup. Environment variables starting with ``IGNIS_`` will be treated as properties. The variable names will be converted to lowercase and the ``_`` will be converted to ``.``. For example, ``IGNIS_FOO_BAR`` will be stored as ``ignis.foo.bar``, whose value will remain unchanged.

Submitter script
^^^^^^^^^^^^^^^^

The submitter sets the properties values using the ``-p`` or ``--properties`` parameter when a job is launched.

See submitter section for more details.

File
^^^^

Default values are stored in ``/opt/ignis/etc/ignis.conf`` using Java Properties with a ``key=value`` format.


Mixed definition
^^^^^^^^^^^^^^^^

In case of multiple definitions of the same variable, the following priority list will be used:

  1. Driver Properties Object (highest priority)
  2. Driver Container enviroment variable
  3. Submitter script argument
  4. Submitter Container enviroment variable
  5. File ``/opt/ignis/etc/ignis.conf``\ \*

\* There are two different files in the driver and submitter, and each one only stores the default values for its module. Note that IgnisHPC does not define any default value outside the configuration files, which allows users to know the values of all the system variables. Therefore, values can be modified but never deleted.


-----------------
Property list
-----------------

Base Properties
^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.debug                   | Boolean | False   | All      | Enables debugging messages.                          |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.home                    | Path    | ``auto``| Driver   | Path where IgnisHPC is installed, IgnisHPC images    |
|                               |         |         | Executor | set this value to ``/opt/ignis``.                    |
+-------------------------------+---------+---------+----------+------+-----------------------------------------------+
| ignis.options                 | Raw     | ``auto``| Driver   | Raw value used by the submitter to send options to   |
|                               |         |         |          | the driver.                                          |
+-------------------------------+---------+---------+----------+------+-----------------------------------------------+
| ignis.working.directory       | Path    | ``auto``| Driver   | Working directory of the current Job, it is used to  |
|                               |         |         | Executor | resolve all relative paths.                          |
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Job Properties
^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.job.id                  | String  | ``auto``| Driver   | Job identifier, generated and used by the scheduler. |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.job.name                | String  | ``auto``| Driver   | Job name, can be sent as a submitter parameter,      |
|                               |         |         |          | otherwise it will be generated automatically. The    |
|                               |         |         |          | final job name may vary depending on the scheduler   |
|                               |         |         |          | used.                                                |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.job.directory           | Path    | ``auto``| Executor | Directory where the job data is stored, it is        |
|                               |         |         |          | generated as a subdirectory of the working directory.|
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.job.worker              | Integer | ``auto``| Executor | Identifies the worker whose instance is the executor.|
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Distributed Filesystem (DFS) Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.dfs.id                  | String  | ``auto``| Driver   | DFS identifier, it identifies DFS in the scheduler.  |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.dfs.home                | Path    | ``auto``| Driver   | Directory where the DFS is mounted on.               |
|                               |         |         | Executor |                                                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Scheduler Properties
^^^^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.scheduler.url           | URL[]   | ``auto``| Driver   | One or more Scheduler API URL, syntax is             |
|                               |         |         |          | Scheduler-dependent.                                 |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.scheduler.type          | String  | ``auto``| Driver   | Scheduler implementation name. See Scheduler section |
|                               |         |         |          | for value names.                                     |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.scheduler.dns           | String[]| ``auto``| Driver   | Hostnames to resolve in the container network.       |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.scheduler.param.{name}  | String  |         | Driver   | It sets <name> parameter for the Scheduler,          |
|                               |         |         |          | each Scheduler has its own parameters.               |
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Driver Properties
^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.driver.image            | String  |``empty``| Driver   | Driver: container image                              |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.cores            | Interger| 1       | Driver   | Driver: number of cores                              |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.memory           | String  | 1GB     | Driver   | Driver: memory limit in Bytes, might use prefixes    |
|                               |         |         |          | (K, M, G, ...) or (Ki, Mi, Gi, ...).                 |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.rpc.port         | Port    | 4000    | Driver   | Backend service listening port.                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.rpc.compression  | Integer | 6       | Driver   | Backend service RPC zlib compression level. (0-9)    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.swappiness       | Integer |``empty``| Driver   | Driver: Container swappiness rate. (0-100)           |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.pool             | Integer | 8       | Driver   | Minimum number of workers on standby when the Backend|
|                               |         |         |          | is idle.                                             |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.port.{tcp\|udp}. | Port    |         | Driver   | Driver: exposes a container port to a host port.     |
| {cport}                       |         |         |          | Value ``0`` generates a random host port.            |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.ports.{tcp\|udp} | Integer |         | Driver   | Driver: exposes a specific number of random ports to |
|                               |         |         |          | the host, ports are exposed to the same value on host|
|                               |         |         |          | .                                                    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.bind.{cpath}     | Path    |         | Driver   | Driver: binds a container path ``cpath`` to a host   |
|                               |         |         |          | path. Add ':ro' for read-only.              |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.volume.{cpath}   | String  |         | Driver   | Driver: Creates a volume in the path with value size |
|                               |         |         |          | in Bytes, might use prefixes (K, M, G, ...) or       |
|                               |         |         |          | (Ki, Mi, Gi, ...).                                   |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.hosts            | String[]|``empty``| Driver   | Driver: the container must be launched on one of the |
|                               |         |         |          | hosts in order of preference.                        |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.env.{name}       | String  |``empty``| Driver   | Driver: creates an environment variable in the       |
|                               |         |         |          | container.                                           |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.public.key       | String  | ``auto``| Driver   | SSH tunnel public key.                               |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.private.key      | String  | ``auto``| Driver   | SSH tunnel private key.                              |
|                               |         |         | Executor |                                                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.healthcheck.port | String  | 1963    | Driver   | Backend healthcheck listening port.                  |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.healthcheck.url  | String  | ``auto``| Driver   | Backend healthcheck URL.                             |
|                               |         |         | Executor |                                                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.healthcheck.     | Integer | 60      | Driver   | How often the driver is checked to see if it is still|
| interval                      |         |         | Executor | alive.                                               |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.healthcheck.     | Integer | 20      | Driver   | Backend healthcheck response timeout.                |
| timeout                       |         |         | Executor |                                                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.driver.healthcheck.     | Integer | 5       | Driver   | Number of healthcheck failures before aborting.      |
| retries                       |         |         | Executor |                                                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+



Executor Properties
^^^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.executor.instances      | Integer | 1       | Executor | Number of executors.                                 |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.attempts       | Integer | 2       | Executor | Number of execution attempts before failure.         |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.image          | String  | ignishpc| Executor | Executor: container image.                           |
|                               |         | /full   |          |                                                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.cores          | Interger| 1       | Executor | Executor: number of cores.                           |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.cores.single   | String[]| python  | Executor | Executors that do not support multithreading. Threads|
|                               |         |         |          | are transformed into processes.                      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.memory         | String  | 1GB     | Executor | Executor: memory limit in Bytes, might use prefixes  |
|                               |         |         |          | (K, M, G, ...) or (Ki, Mi, Gi, ...).                 |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.rpc.port       | Port    | 5000    | Executor | Executor service listening port.                     |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.rpc.compression| Integer | 6       | Executor | Executor service RPC zlib compression level. (0-9)   |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.swappiness     | Integer | 0       | Executor | Executor: container swappiness rate. (0-100)         |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.isolation      | Boolean | True    | Executor | Prevents different workers from running in the same  |
|                               |         |         |          | container at the same time.                          |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.directory      | Path    | ``auto``| Executor | Directory where the job data is stored, it is        |
|                               |         |         |          | generated as a subdirectory of job directory.        |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.port.{tcp\|udp}| Port    |         | Executor | Executor: exposes a container port to a host port.   |
| .{cport}                      |         |         |          | Value ``0`` generates a random host port.            |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.ports.         | Integer |         | Executor | Executor: exposes a specific number of random ports  |
| {tcp\|udp}                    |         |         |          | to the host, ports are exposed to the same value on  |
|                               |         |         |          | host.                                                |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.bind.{cpath}   | Path    |         | Executor | Executor: binds a container path ``cpath`` to a host |
|                               |         |         |          | path. Add ':ro' to value for read-only.              |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.volume.{cpath} | String  |         | Executor | Executor: creates a volume in the path with value    |
|                               |         |         |          | size in Bytes, might use prefixes (K, M, G, ...) or  |
|                               |         |         |          | (Ki, Mi, Gi, ...).                                   |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.hosts          | String[]|``empty``| Executor | Executor: the container must be launched on one of   |
|                               |         |         |          | the hosts in order of preference.                    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.executor.env.{name}     | String  |``empty``| Executor | Executor: creates an environment variable in the     |
|                               |         |         |          | container.                                           |
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Partition Properties
^^^^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.partition.type          | String  | Memory  | Executor | Storage type for partitions, must be ``Memory``,     |
|                               |         |         |          | ``RawMemory`` or ``Disk``.                           |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.partition.minimal       | String  | 128MB   | Executor | Minimum partition size from file.                    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.partition.compression   | Integer | 0       | Executor | Storage zlib compresion level. Available for         |
|                               |         |         |          | ``RawMemory`` and ``Disk``. (0-9)                     |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.partition.serialization | String  | native  | Executor | Type of serialization with executors of the same     |
|                               |         |         |          | language.                                            |
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Transport Properties
^^^^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.transport.cores         | Float   | 0.0     | Executor | Number of threads used to execute a transport action |
|                               |         |         |          | at the same time. If the value is less than 1, the   |
|                               |         |         |          | value will be multiplied by ``ignis.executor.cores``.|
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.transport.compression   | Integer | 0       | Executor | Transport zlib compresion level. (0-9)               |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.transport.ports         | Integer | 20      | Executor | Number of ports reserved for data exchanges.         |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.transport.minimal       | String  | 100KB   | Executor | Minimum size to open a data transport channel,       |
|                               |         |         |          | otherwise it will be sent by RPC.                    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.transport.element.size  | String  | 256B    | Executor | Average size per element to use as a reference when  |
|                               |         |         |          | it cannot be calculated.                             |
+-------------------------------+---------+---------+----------+------------------------------------------------------+


Module Properties
^^^^^^^^^^^^^^^^^
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| Name                          | Type    | Default | Context  | Description                                          |
+===============================+=========+=========+==========+======================================================+
| ignis.modules.io.compression  | Integer | 0       | Executor | File zlib compresion level. (0-9)                    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.modules.io.cores        | Float   | 0.0     | Executor | Number of threads used to read/write files at the    |
|                               |         |         |          | same time. If the value is less than 1, the value    |
|                               |         |         |          | will be multiplied by ``ignis.executor.cores``.      |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.transport.compression   | Integer | 0       | Executor | Transport zlib compresion level. (0-9)               |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.modules.io.overwrite    | Boolean | False   | Executor | Output files are overwritten if they already exist.  |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.modules.sort.samples    | Float   | 0.001   | Executor | Sampling size in the sort algorithm. Number of       |
|                               |         |         |          | samples is calculated using this value and the number|
|                               |         |         |          | of elements. If the value is greater than 1, it will |
|                               |         |         |          | be used as the number of samples.                    |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.modules.sort.resampling | Boolean | False   | Executor | Samples from the sort algorithm are resampled for    |
|                               |         |         |          | parallel processing. It is only useful if large      |
|                               |         |         |          | amounts of data are sorted or if the sample size is  |
|                               |         |         |          | very high.                                           |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
| ignis.modules.exchange.type   | String  | auto    | Executor | Algorithm used for data exchange, can be sync or     |
|                               |         |         |          | async. Any other value selects the method that best  |
|                               |         |         |          | fits.                                                |
+-------------------------------+---------+---------+----------+------------------------------------------------------+
