segment_liftover
================

Converting genome coordinates between different genome assemblies is a
common task in bioinformatics. Services and tools such as UCSC Liftover,
NCBI Remap and CrossMap are available to perform such conversion.

When converting a genomic segment, those conversion tools will break the
segment into smaller parts if the segment is not continuous in the new
assembly. However, in some circumstances such as copy number analyses,
where the quantitative representation of a genomic range takes
precedence over base-specific representation, the integrity of a single
segment needs to be kept.

Moreover, all those tools are designed for single file processing, and
offer nothing to facilitate batch processing. But in Bioinformatic
studies, it is very often that people need to deal with hundreds and
even thousands of files at a time.

*segment_liftover* is a Python program that can convert segments between
genome assemblies, without breaking them apart. Part of its
functionality is based on re-conversion by locus approximation, in
instances where a precise conversion of genomic positions fails.

Key features: - converts continuous segments - performs approximate
conversion when direct conversion fails - batch processing of any number
of files - automatic folder traversal and file discovery - detailed logs
- resuming from interruption - accept both segment (i.e. start => end)
and probe (i.e., single position) data

Program dependency
~~~~~~~~~~~~~~~~~~

*segment_liftover* depends on the *UCSC Liftover program*, which can be
found `here <https://genome-store.ucsc.edu/>`__. Please note that the
UCSC Liftover is only free for non-commercial use. Despite the
inconvenience of licensing, Liftover offers some very convenient
features: - it is a stand-alone command-line tool - it can convert
assemblies of any species, even between species - it runs locally and
does not require network access

How to install
--------------

The easiest way is to install through pip:

::

    pip install segment_liftover
    segment_liftover --help

Another option is to copy ``segment_liftover/segmentLiftover.py`` and
``segment_liftover/chains/*`` from
`github <https://github.com/baudisgroup/segment-liftover>`__.
Dependencies need to be installed manually.

::

    python3 segmentLiftover.py --help

**Important: Add the UCSC ``liftOver`` program to your working
directory, or use -l to specify its location.**

How to use
----------

See the
`maunal <https://github.com/baudisgroup/segment-liftover/blob/master/manual.md>`__
for details.

Quick start
~~~~~~~~~~~

Typical usage:

::

    >segment_liftover -i /Volumes/data/hg18/ -o /Volumes/data/hg19/ -c hg18ToHg19 -si segments.tsv -so seg.tsv

General Usage
~~~~~~~~~~~~~

::

    Usage: segment_liftover [OPTIONS]

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
      -t, --test_mode INTEGER         Only process a limited number of files.
      -f, --file_indexing             Only generate the index file.
      -x, --index_file FILENAME       Specify an index file containing file paths.
      -m, --mapping_file FILENAME     Specify a pre-defined file of position
                                      mappings.
      --step_size INTEGER             The step size of approximate conversion (in
                                      bases, default:400).
      --range INTEGER                 The searching range of approximate conversion
                                      (in kilo bases, default:10).
      --no_approximate_conversion     Do not perform approximate conversion.
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

    ./segmentLiftover.py    The python script.
    ./chains/               Home of the chain files.

working directory:

::

    ./liftOver             The UCSC LiftOver program.
    ./logs/                Will show up after running the script once. Home of all log files.
    ./tmp/                 Will show up during processing.

Start with your input file
~~~~~~~~~~~~~~~~~~~~~~~~~~

*segment_liftover* is designed to process a large number of files in one
run.

-  It requires ***an input directory***, and will traverse through all
   sub-directories to index all files matching ***the input file
   name***.
-  It requires ***an output directory***, and will keep the original
   directory structure in the output directory.
-  Segment and probe files are treated differently - therefore, you need
   to use different options to pass the input file name.
-  You can also create a list of input files to start. Please see
   `manual <https://github.com/baudisgroup/segment-liftover/blob/master/manual.md>`__
   for more details.
-  Regular expressions are supported for input names.

Input file format
~~~~~~~~~~~~~~~~~

Use ``-si filename`` for segment file names. All files should:

-  be **tab separated**, without quoted values
-  have at least **4** columns as id, chromosome, start and end (names
   do not matter, order does).

Extra columns will be copied over.

An example:

::

    id  chro    start   stop    value_1 value_2
    GSM378022   1   775852  143752373   0.025   9992
    GSM378022   1   143782024   214220966   0.1607  6381
    GSM378022   2   88585000    144628991   0.0131  4256
    GSM378022   2   144635510   146290468   0.1432  146
    GSM378022   3   48603   8994748 0.0544  1469

Use ``-pi filename`` for probe file names. All files should:

-  be **tab separated**, without quoted values
-  have at least **3** columns as id, chromosome and position (names do
   not matter, order does).

Extra columns will be copied over.

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

A chain file is required by the *UCSC LiftOver* program to convert from
one assembly to another and therefore also **required** by
*segment_liftover*.

Common chain files for human genome editions (from UCSC) are provider as
part of *segment_liftover*. Please check the
`manual <https://github.com/baudisgroup/segment-liftover/blob/master/manual.md>`__
for details.

Other chain files can be accessed `at the UCSC dowload
area <http://hgdownload.cse.ucsc.edu/downloads.html>`__

Output files
~~~~~~~~~~~~

-  The file structure of the input directory will be kept in output
   directory.
-  Output files can be renamed with ``-so, --segment_output_file TEXT``
   or ``-po, --probe_output_file TEXT``

Understanding results
~~~~~~~~~~~~~~~~~~~~~

Five different numbers will be reported after the execution. For
example:

::

    Total segments:                 a count of all segments in all files.
    - directly converted:           conversions by UCSC liftOver.
    - approximately converted:      successful approximate conversions.
    - converted but rejected:       although converted, but failed the quality check.
    - unconvertible:                cannot be converted at all.

Quality check
~~~~~~~~~~~~~

The usefulness of a converted probe or segment will be checked by a few
criteria.

For a probe:

-  the new chromosome must be the same as the old chromosome.

For a segment:

-  the new start position and new end position are on the same
   chromosome,
-  0.5 < length(new_segment)/length(old_segment) < 2.

Log files
~~~~~~~~~

::

    ./logs/fileList.log    The indexing file from traversing input_dir.
    ./logs/general.log    The main log file, keeps records for all the works done and errors encountered.
    ./logs/progress.log    A list of successfully processed files.
    ./logs/unconverted.log    A list of all positions that could not be lifted and re-converted.
    ./logs/approximate_conversion.log    A list of all the approximately converted positions (when LiftOver fails).

If *segment_liftover* does not work as expected, you can check
**general.log** for execution details.

If you are interested in unique re-converted or unconverted results, you
can check **approximate_conversion.log**.

If you want to get information of rejection or conversion result of a
specific file, you can check **unconverted.log**.

Overwriting behaviour
~~~~~~~~~~~~~~~~~~~~~

The script **WILL overwrite ``output_dir``**

Python dependencies
~~~~~~~~~~~~~~~~~~~

The script is developed in python3.6

Packages: click6.7, pandas0.20.1

Advanced use
------------

Start from a file
~~~~~~~~~~~~~~~~~

With the **index_file** option, you can provide a file containing files
you want to process. One file name per line, using the file’s full path.

After each run, a **fileList.log** file can be found in **./logs/**,
which can be used as quick start for next time. You can also generate a
*file list* using the following command:

::

    >segment_liftover -i /Volumes/data/hg18/ -o /Volumes/data/hg19/ -c hg18ToHg19 -si segments.tsv -x ./myfilelist.txt

Reuse approximate conversion results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the **–mapping_file** option, you can reuse a previously generated
log file to speed up processing.

After each run, a **approximate_conversion.log** file can be found in
**./logs/**.

Specify parameters of approximate conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``--step_size`` and ``--range``, you can control the resolution and
scope of searching for the closest liftable position when a position can
not be lifted. The default values are *500* (bases) and *10*
(kilo-bases).

.. raw:: html

   <!--### Choose good parameters
   -->

Resume from interruption
~~~~~~~~~~~~~~~~~~~~~~~~

If the execution of the script is interrupted, it can be resumed using
**–resume** as following:

::

    >segment_liftover --resume ./logs/fileList.log ./logs/progress.log -i /Volumes/data/hg18/ -o /Volumes/data/hg19/ -c hg18ToHg19 -si segments.tsv 

Parallel processing
~~~~~~~~~~~~~~~~~~~

*segment_liftover* does not support multiprocessing directly, but very
tasks can be divided into smaller tasks and run parallel with ease.

-  First, generate a **fileList** as instructed in *Start from a file*
   section.
-  Then (optional), shuffle the lines in the **fileList**.
-  Next, split **fileList** into smaller files and put them in separated
   folders.
-  Finally, run *lift_over* with option **–index_file** in each folder.
