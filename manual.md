#segmentLiftover Manual

segmentLiftover is a Python tool for converting segments between genome assemblies without break them apart. See the main [README](https://github.com/baudisgroup/segment-liftover/blob/master/README.md) for introduction and installation.

## Options
```
Usage: segmentLiftover.py [OPTIONS]

Options:
  -i, --input_dir TEXT            The directory to start processing.
  -o, --output_dir TEXT           The directory to write new files.
  -c, --chain_file TEXT           Specify the chain file name.
  --clean                         Clean up log files.
  -t, --test_mode INTEGER RANGE   Only process a limited number of files.
  -f, --file_indexing             Only generate the index file.
  -si, --segment_input_file TEXT  Specify the segment input file name.
  -so, --segment_output_file TEXT
                                  Specify the segment output file name.
  -pi, --probe_input_file TEXT    Specify the probe input file name.
  -po, --probe_output_file TEXT   Specify the probe output file name.
  --step_size INTEGER             The step size of remapping (in bases,
                                  default:400).
  --range INTEGER                 The range of remapping search (in kilo
                                  bases, default:10).
  -x, --index_file FILENAME       Specify an index file containing file paths.
  -r, --remap_file FILENAME       Specify an remapping list file.
  --no_remapping                  No remapping, only original liftover.
  --new_segment_header TEXT...    Specify 4 new column names for new segment
                                  files.
  --new_probe_header TEXT...      Specify 3 new column names for new probe
                                  files.
  --resume TEXT...                Specify a index file and a progress file to
                                  resume               an interrupted job.
  --help                          Show this message and exit.
```

## Required options
segmentLiftover is designed for batch processing, therefore, it requires the user to provide both input and output directories, and a pattern of the input file.

### input directory

```
-i, --input_dir TEXT
```
The root directory of all the files that need to be processed. The program will traverse all the sub-directories and index all the files that match the user-defined pattern.

### output directory

```
-o, --output_dir TEXT 
```
Where the converted files should be stored. It keeps the same directory structure as ```input direcotry```. 

### chain file 
```
-c, --chain_file TEXT
```
segmentLiftover uses the UCSC Liftover program to perform the basic conversion. Because a file chain is required by Liftover, so does the segmentLiftover.

Common human chain files are provided by segmentLiftover as key words: _hg18ToHg19, hg18ToHg38, hg19ToHg38, hg19ToHg18, hg38ToHg19_.

You can find other chain files [here](http://hgdownload.cse.ucsc.edu/downloads.html).

### segment input file & probe input file
```
-si, --segment_input_file TEXT
-pi, --probe_input_file TEXT
```
At lease one input file need to be given. It will be used for the automatic file traversal and discovery in the input directory.

The ```TEXT``` is interpreted as a regular expression. 

As a regular expression, the input ```segment.tsv``` actually means ```segment?tsv```. But most of the time, this should not be a problem.

## Other options

### segment output file & probe output file
```
-so, --segment_output_file TEXT
-po, --probe_output_file TEXT
```
When specified, the output files will be renamed, otherwise, the input file name will be adopted.

### generate an index file
```
-f, --file_indexing
```
Traversing a large or complex directry may take hours to complete. With this option, the program will stop after generating the indexing file which is saved as ```./logs/fileList.log```. This is particularly useful for paralell running.

### start from an index file
```
-x, --index_file FILENAME
```
Instead of begin with file traversal, which may be unnecessary to repeat, segmentLiftover can also start from a pre-defined or generate file.

Each line of the file should be the path of an input file, nothing else should be in this file.

All the required options are still needed to generated the direcotry stucture and distinguish segment/probe files.

### test mode
```
-t, --test_mode INTEGER RANGE
```
When this option is given, the program will only process a limited number of files. 

### no remapping
```
--no_remapping
```
When this option is given, the program will only use convertion results from Liftovet. No proximal re-convertion.

### specify a remapping file
```
-r, --remap_file FILENAME
```
After each suceessful execution, segmentLiftover will generate a log file containing all the re-converted segments and probes at ```./logs/remapped.log```.

It can be re-used to dramaticly improve the processing time, if the segments/probes are from the same/similar pipeline or platform.

### step size & range
```
--step_size INTEGER
--range INTEGER
```
When Liftover fails to convert a segment or probe, segmentLiftover will try to re-convert by approximation. The arounding region of the failed postion will be searched, and the closed convertable position will be used as substitute. The distance between two searched positions and the maximam distance of the search are defined by ```step_size``` and ```range```, respectively.

The default settings is ```step_size = 400```, ```range = 10```. The counting unit is _base_ for ```step_size``` and _kilo bases_ for ```range```.

These options have significant impact on the process time of re-convertion. Read our [publication]() for the detailed discussion of tuning for the best performence.

### new header names
```
--new_segment_header TEXT
--new_probe_header TEXT
```
When specified, the output files will use the given new column names in the header.

### resume from interruption
```
--resume TEXT
```
Two files are needed to resume from an interruption: the indexing file and the progress files. They are log files generated by segmentLiftover and saved as ```./logs/fileList.log``` and ```./logs/progress.log```.

### clean log files
```
--clean
```
This option will remove all the log files in ```./logs/``` directory.