# segment_liftover Manual

segment_liftover is a Python tool for converting segments between genome assemblies without break them apart. See the main [README](https://github.com/baudisgroup/segment-liftover/blob/master/README.md) for introduction and installation.

## Options
```
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
  --beta FLOAT                    Parameter in quality control.                                
  --no_approximate_conversion     Do not perform approximate conversion.
  --new_segment_header TEXT...    Specify 4 new column names for new segment
                                  files.
  --new_probe_header TEXT...      Specify 3 new column names for new probe
                                  files.
  --resume TEXT...                Specify a index file and a progress file to
                                  resume an interrupted job.
  --clean                         Clean up log files.
  --help                          Show this message and exit.
```

## Required options
segment_liftover is designed for batch processing, therefore, it requires the user to provide both input and output directories, and a pattern of the input file.

### input directory

```
-i, --input_dir TEXT
```
The root directory of all the files that need to be processed. The program will traverse all the sub-directories and index all the files that match the user-defined pattern.

### output directory

```
-o, --output_dir TEXT 
```
Where the converted files should be stored. It keeps the same directory structure as ```input directory```. 

### chain file 
```
-c, --chain_file TEXT
```
segment_liftover uses the UCSC Liftover program to perform the basic conversion. Because a file chain is required by Liftover, so does the segment_liftover.

Common human chain files are provided by segment_liftover as key words: _hg18ToHg19, hg18ToHg38, hg19ToHg38, hg19ToHg18, hg38ToHg19_.

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
Traversing a large or complex directory may take hours to complete. With this option, the program will stop after generating the indexing file which is saved as ```./logs/fileList.log```. This is particularly useful for parallel running.

### start from an index file
```
-x, --index_file FILENAME
```
Instead of begin with file traversal, which may be unnecessary to repeat, segment_liftover can also start from a pre-defined or generate file.

Each line of the file should be the path of an input file, nothing else should be in this file.

All the required options are still needed to generated the directory structure and distinguish segment/probe files.

### test mode
```
-t, --test_mode INTEGER RANGE
```
When this option is given, the program will only process a limited number of files. 

### no approximate conversion
```
--no_approximate_conversion
```
When this option is given, the program will only use conversion results from Liftovet. 

### re-use a mapping file
```
-m, --mapping_file FILENAME
```
After each successful execution, segment_liftover will generate a log file containing all the re-converted segments and probes in ```./logs/approximate_conversion.log```.

It can be re-used to dramatically improve the processing time, if the segments/probes are from the same/similar pipeline or platform.

### step size & range
```
--step_size INTEGER
--range INTEGER
```
When Liftover fails to convert a segment or probe, segment_liftover will try to re-convert by approximation. The surrounding region of the failed position will be searched, and the closed convertible position will be used as substitute. The distance between two searched positions and the maximum distance of the search are defined by ```step_size``` and ```range```, respectively.

The default settings is ```step_size = 400```, ```range = 10```. The counting unit is _base_ for ```step_size``` and _kilo bases_ for ```range```.

These options have significant impact on the process time of re-conversion. In general they should be related to the average distance between adjacent probes of the experiment platform.

### beta 
```
--beta FLOAT
```
This parameter controls the strictness of one of the quality control condition, the defaut value is 2. Please refer to the paper for more details.

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
Two files are needed to resume from an interruption: the indexing file and the progress files. They are log files generated by segment_liftover and saved as ```./logs/fileList.log``` and ```./logs/progress.log```.

### clean log files
```
--clean
```
This option will remove all the log files in ```./logs/``` directory.
