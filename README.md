# genome-liftover
This script is designed to lift over the CNprobes.tab and segments.tab files from hg18 to hg19 or hg 38.

But with a simple renaming, it can also be used to lift any file from any genome edition to any edition.

## File structure
```
- ./arraymapLiftOver.py  The python script
- ./chains/              Home of the chain files
- ./liftOver             The UCSC liftOver program
- ./logs/                Not in github, but will show up after running the script once.
                      Home of all log files.
```

## Getting the UCSC liftOver
This script depends on the UCSC liftOver program, you can find it [here](https://genome-store.ucsc.edu/).

## Getting more chain files
The chain files for hg18 to hg19, and hg18 to hg38 are provided.

You can get other chain files [here](http://hgdownload.cse.ucsc.edu/downloads.html)

## Python dependency
The script is in python3.6

It uses packages: click6.7, pandas0.20.1

## Usage
```
>python3 arraymapLiftover.py [OPTIONS]

Options:
  -i, --input_dir TEXT            The direcotry to start processing.
  -o, --output_dir TEXT           The direcotry to write new files.
  -g, --genome_editions [18to19|18to38]
                                  The genome editions of liftover.
  -c, --clean                     Clean up log files.
  -t, --test_mode INTEGER RANGE   Only process a limited number of files.
  -f, --file_indexing             Only generate the indexing file.
  --help                          Show this message and exit.
```

### Outputs
1. The corresponding CNprobes.tab and segments.tab files in "output_dir"
2. ./logs/filelist.log    This is the indexing file for input_dir.
                          It can dramtically speed up file processing, if you have a lot.
                          It can be used to specify what files to process.
                          If the file is present, the script will igonore the inpu_dir.
3. ./logs/liftover.log    The main log file, keeps records for all the works done and errors encountered.
4. ./logs/progress.log    It lists the sucessfully processed files.
5. ./unmapped.log         It lists all the coordinates failed to be lifted.

### Overwriting behaviour
1. The script WILL overwrite output_dir
2. The script WILL overwrite all log files, excpet filelist.log
3. The script will NOT overwrite filelist.log

## To liftover other files
If you have a list of single positions, rename it as "CNprobes.tab".

The file must be tab seperated, with the following format:
```
PROBEID	CHRO	BASEPOS	VALUE
ID_2_1	1	51599	-0.6846
ID_3_2	1	51672	-0.2546
ID_4_3	1	51687	0.0833
ID_5_4	1	52016	-0.5201
ID_6_5	1	52784	0.1997
ID_7_6	1	52801	-0.3800
ID_8_7	1	62568	-0.2435
ID_9_8	1	62640	0.3516
ID_10_9	1	72034	-0.5687
```

If you have a list of segments/range, rename it as "segments.tab".

The file must be tab seperated, with the following format:
```
id	        chro	start	    stop	      value_1	  value_2
GSM378022	  1	  775852	  143752373	  0.025	    9992
GSM378022	  1	  143782024	214220966	  0.1607	  6381
GSM378022	  1	  214224452	247110269	  -0.0463	  3437
GSM378022	  2	  24049	      88551883	  -0.0213	  8985
GSM378022	  2	  88585000	144628991	  0.0131	  4256
GSM378022	  2	  144635510	146290468	  0.1432	  146
GSM378022	  2	  146298722	242650580	  0.0079	  8791
GSM378022	  3	  48603	    8994748	    0.0544	  1469
```
