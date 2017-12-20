segment_liftover
================

Converting genome coordinates between different genome assemblies is a
common task in bioinformatics. Services and tools such as UCSC Liftover,
NCBI Remap and CrossMap are available to perform such conversion. When
converting a segment, all tools will break the segment into a few
smaller segments, if the segment is not continuous anymore in the new
assembly. However, in some circumstances such as copy number studies,
the integrity of the segment needs to be kept.

The segment_liftover is a python program that can convert segments
between genome assemblies without breaking them apart. Furthermore, it
also tries to re-convert by approximation when precise conversion fails.

Key features: - convert segments in whole - do approximate conversion
when direct conversion fails - batch process any number of files -
automatic folder traversal and file discovery - detailed logs - resume
from interruption - work for both segment and probe data

Program dependency
~~~~~~~~~~~~~~~~~~

The segment_liftover depends on the UCSC Liftover program to work.You
can find it `here <https://genome-store.ucsc.edu/>`__. Please note,
Liftover is only free for non-commercial use. Despite the inconvenience
of licensing, Liftover offers some very convenient features: - it is a
stand-along command-line tool - it can convert assemblies of any
species, even between species - it runs locally and does not require
network

How to install
--------------

The easies way is to install through pip:

::

    pip install segment_liftover
    segment_liftover --help

Another way is to copy ``segment_liftover/segmentLiftover.py`` and
``segment_liftover/chains/*`` from
`github <https://github.com/baudisgroup/segment-liftover>`__.
Dependencies need to be installed manually.

::

    python3 segmentLiftover.py --help

How to use
----------

See the
`maunal <https://github.com/baudisgroup/segment-liftover/blob/master/manual.md>`__
for details.

Quick start
~~~~~~~~~~~

Typical usage:

::

    >python3 segment_liftover.py -i /Volumes/data/hg18/ -o /Volumes/data/hg19/ -c hg18ToHg19 -si segments.tsv -so seg.tsv

General Usage
~~~~~~~~~~~~~

::

    Usage: segment_liftover.py [OPTIONS]

    Options:
      -i, --input_dir TEXT            The directory to start processing.
      -o, --output_dir TEXT           The directory to write new files.
      -c, --chain_file TEXT           Specify the chain file name.
      -si, --segment_input_file TEXT  Specify the segment input file name.
      -so, --segment_output_file TEXT
                                      Specify the segment output file name.
      -pi, --probe_input_file TEXT    Specify the probe input file name.
      -po, --probe_output_file TEXT   Specify the probe output file name.
      -l, --liftover TEXT             Specify the location of the UCSC liftover
                                      program.
      -t, --test_mode INTEGER RANGE   Only process a limited number of files.
      -f, --file_indexing             Only generate the index file.
      -x, --index_file FILENAME       Specify an index file containing file paths.
      -r, --remap_file FILENAME       Specify an remapping list file.
      --step_size INTEGER             The step size of remapping (in bases,
                                      default:400).
      --range INTEGER                 The range of remapping search (in kilo
                                      bases, default:10).
      --no_remapping                  No remapping, only original liftover.
      --new_segment_header TEXT...    Specify 4 new column names for new segment
                                      files.
      --new_probe_header TEXT...      Specify 3 new column names for new probe
                                      files.
      --resume TEXT...                Specify a index file and a progress file to
                                      resume an interrupted job.
      --clean                         Clean up log files.
      --help                          Show this message and exit.

Required options are:

-  ``-i, --input_dir TEXT``
-  ``-o, --output_dir TEXT``
-  ``-c, --chain_file TEXT``
-  either of both of ``-si, --segment_input_file TEXT`` and
   ``-pi, --probe_input_file TEXT``

File structure
~~~~~~~~~~~~~~

source directory:

::

    ./segment_liftover.py       The python script.
    ./chains/                   Home of the chain files.

working directory:

::

    ./liftOver             Put the UCSC LiftOver program here.
    ./logs/                Will show up after running the script once. Home of all log files.
    ./tmp/                 For temporary files during liftover.

Start with your input file
~~~~~~~~~~~~~~~~~~~~~~~~~~

segment_liftover is designed to process a large number of files in one
run.

-  It requires ***an input directory***, and will traverse through all
   subfolders to index all files that matching ***the input file
   name***.
-  It requires ***an output directory***, and will keep the original
   folder structure in the output folder.
-  Segment and probe files are treated differently, therefore, you need
   to use different options to pass the input file name.
-  You can also create a list of input files to start, please see
   `manual <https://github.com/baudisgroup/segment-liftover/blob/master/manual.md>`__
   for more details.
-  Regular expression is supported for input names.

Input file format
~~~~~~~~~~~~~~~~~

Use ``-si filename`` for segment file names. All files should:

-  be **tab separated**,
-  have at least **4** columns as id, chromosome, start and end (names
   do not matter, order does).

Extra columns will be kept over.

An example:

::

    id  chro    start   stop    value_1 value_2
    GSM378022   1   775852  143752373   0.025   9992
    GSM378022   1   143782024   214220966   0.1607  6381
    GSM378022   2   88585000    144628991   0.0131  4256
    GSM378022   2   144635510   146290468   0.1432  146
    GSM378022   3   48603   8994748 0.0544  1469

Use ``-pi filename`` for probe file names. All files should:

-  be **tab separated**,
-  have at least **3** columns as id, chromosome and position (names do
   not matter, order does).

Extra columns will be kept over.

An example:

::

    PROBEID CHRO    BASEPOS VALUE
    ID_2_1  1   51599   -0.6846
    ID_3_2  1   51672   -0.2546
    ID_4_3  1   51687   0.0833
    ID_5_4  1   52016   -0.5201
    ID_6_5  1   52784   0.1997
    ID_7_6  1   52801   -0.3800
    ID_8_7  1   62568   -0.2435
    ID_9_8  1   62640   0.3516
    ID_10_9 1   72034   -0.5687

Chain files
~~~~~~~~~~~

A chain file is required by the UCSC LiftOver program to convert from
one assemble to another, therefore, it is also **required** by
segment_liftover.

Common chain files for human are provider by segment_liftover, please
check
`manual <https://github.com/baudisgroup/segment-liftover/blob/master/manual.md>`__
for details.

You can get other chain files
`here <http://hgdownload.cse.ucsc.edu/downloads.html>`__

Outputs
~~~~~~~

-  The file structure of input directory will be kept in output
   directory
-  Output files can be renamed with ``-so, --segment_output_file TEXT``
   or ``-po, --probe_output_file TEXT``

Log files
~~~~~~~~~

::

    ./logs/filelist.log    The indexing file from traversing input_dir.
    ./logs/liftover.log    The main log file, keeps records for all the works done and errors encountered.
    ./logs/progress.log    A list of successfully processed files.
    ./logs/unmapped.log    A list of all positions that could not be lifted and re-converted.
    ./logs/remapped.log    A list of all the approximated conversion (when LiftOver fails).

Overwriting behaviour
~~~~~~~~~~~~~~~~~~~~~

The script **WILL overwrite ``output_dir``**

Python dependency
~~~~~~~~~~~~~~~~~

The script is developed in python3.6

Packages: click6.7, pandas0.20.1

Advanced use
------------

Start from a file
~~~~~~~~~~~~~~~~~

With the **index_file** option, you can provide a file containing files
you want to process. One file name per line and use full path.

After each run, a **fileList.log** file can be found in **./logs/**
which can be used as quick start for next time.

Reuse approximated mapping results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the **remap_file** option, you can reuse previously generated log
file to speed up processing.

After each run, a **remapped.log** file can be found in **./logs/**.

Specify parameters of approximated mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``--step_size`` and ``--range``, you can control the resolution and
scope of searching for the closest liftable position when a position can
not be lifted. The default values are *500* (base) and *10* (kilo-bases)

Choose good parameters
~~~~~~~~~~~~~~~~~~~~~~

Resume from interruption
~~~~~~~~~~~~~~~~~~~~~~~~

Parallel running
~~~~~~~~~~~~~~~~

The simplest way is to first generate a file containing files to
process, split it into serval files, than use **index_file** option to
start multiple sessions.