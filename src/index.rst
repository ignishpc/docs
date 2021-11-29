IgnisHPC
==============

.. only:: html or man

   :Authors:   César Pomar, Juan Carlos Pichel
   :Contact:  cesaralfredo.pineiro@usc.es, juancarlos.pichel@usc.es
   :Date:     |today|
   
.. image:: _static/img/ignis-hpc.svg
   :target: index.html
   :width: 128
   :alt: IgnisHPC logo

.. topic:: Abstract

   One of the most important issues in the path to the convergence of HPC and Big Data is caused by the differences in
   their software stacks. Despite some research efforts, the interoperability between their programming models and 
   languages is still limited. To deal with this problem we introduce a new computing framework called IgnisHPC, whose 
   main objective is to unify the execution of Big Data and HPC workloads in the same framework. IgnisHPC has native support 
   for multi-language applications using JVM and non-JVM-based languages. Since MPI was used as its backbone technology
   , IgnisHPC takes advantage of many communication models and network architectures. Moreover, MPI applications can be 
   directly executed in a efficient way in the framework. The main consequence is that users could combine in the same 
   multi-language code HPC tasks (using MPI) with Big Data tasks (using MapReduce operations). The experimental evaluation
   demonstrates the benefits of our proposal in terms of performance and productivity with respect to other frameworks. 
   IgnisHPC is publicly available for the Big Data and HPC research community.

.. toctree::
   :caption: Contents
   :maxdepth: 2

   started
   deploy
   schedulers
   properties