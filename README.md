# genome-liftover
This script is to enhance the UCSC genome liftover program. 

Key features are:
- automate the liftover of any number of files
- search for the closest liftable position when a point liftover fails
- liftover both single postions and segments
- detailed logs 
- resume from interruption

### File structure
```
- ./arraymapLiftOver.py  The python script
- ./chains/              Home of the chain files
- ./liftOver             The UCSC liftOver program
- ./logs/                Not in github, but will show up after running the script once.
                      Home of all log files.
- ./tmp/                 For temporary files during liftover.
```

### Getting the UCSC liftOver
This script depends on the UCSC liftOver program, you can find it [here](https://genome-store.ucsc.edu/).

### Getting more chain files
The chain files for hg18 to hg19, hg18 to hg38 and hg19 to hg38 are provided.

You can get other chain files [here](http://hgdownload.cse.ucsc.edu/downloads.html)

### Python dependency
The script is deveoped in python3.6, it should work for any verison later than python3.5
With minor modifications, it can also work for verison eralier than 3.5

It uses packages: click6.7, pandas0.20.1

## Usage
Tyical usage:
```
>python3 arraymapLiftover.py -i /Volumes/data/hg18/ -o /Volumes/data/hg19/ -c hg18ToHg19.over.chain -si segments.tsv -so seg.tsv -pi probes.tsv -po prob.tsv 
```
General usage:
```
>python3 arraymapLiftover.py [OPTIONS]

Options:
  -i, --input_dir TEXT            The direcotry to start processing.
  -o, --output_dir TEXT           The direcotry to write new files.
  -c, --chain_file TEXT           Specify the chain file name.
  --clean                         Clean up log files.
  -t, --test_mode INTEGER RANGE   Only process a limited number of files.
  -f, --file_indexing             Only generate the indexing file.
  -si, --segment_input_file TEXT  Specify the segment input file name.
  -so, --segment_output_file TEXT
                                  Specify the segment output file name.
  -pi, --probe_input_file TEXT    Specify the probe input file name.
  -po, --probe_output_file TEXT   Specify the probe output file name.
  --step_size INTEGER             The step size of remapping.
  --steps INTEGER                 The number of steps of remapping.
  -x, --index_file FILENAME       Specify an indexing file cotaining file
                                  paths.
  -r, --remap_file FILENAME       Specify an remapping list file.
  --help                          Show this message and exit.
```

- **input_dir, output_dir** and **chain_file** are required options.
- if **index_file** is specified, **input_dir** will be ignored.
- use **segment** if you have ranged data, see *format* section for more info.
- use **probe** if you have single position data, see *format* section for more info.



### Outputs
1. The liftover output files are in corresponding sub directories in "output_dir"
2. ./logs/filelist.log    This is the indexing file for input_dir.
                          It can dramtically speed up file processing, if you have a lot.
                          It can be used to specify what files to process.
                          If the file is present, the script will igonore the inpu_dir.
3. ./logs/liftover.log    The main log file, keeps records for all the works done and errors encountered.
4. ./logs/progress.log    It lists the sucessfully processed files.
5. ./logs/unmapped.log    It lists all the coordinates failed to be lifted.
6. ./logs/remapped.log    It lists all the approximated mappings (when liftover fails to map).

### Overwriting behaviour
1. The script WILL overwrite output_dir
2. The script WILL overwrite all log files


## File format for input
If you have a list of single positions, use the **prob_input_file** and **prob_output_file** options.

- the file should be tab seperated, with at least 3 columns. 
- the first 3 columns should be **id**, **chromosome** and **position**. The name does not matter, but the order does.
- after the liftover, the first 3 column names will be renamed, and the rest will not be changed.
- data other than the first 3 columns will be kept and not touched.

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

If you have a list of segments/range, use the **segment_input_file** and **segment_output_file** options.

- the file should be tab seperated, with at least 4 columns. 
- the first 3 columns should be **id**, **chromosome**, **start** and **stop**. The name does not matter, but the order does.
- after the liftover, the first 4 column names will be renamed, and the rest will not be changed.
- data other than the first 4 columns will be kept and not touched.
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
## More funcionalities

### Start from a file
With the **index_file** option, you can provide a file containing files you want to process. One file name per line and use full path.

After each run, a **fileList.log** file can be found in **./logs/** which can be used as quick start for next time.

### Reuse approximated mapping results
With the **remap_file** option, you can reuse previously generated log file to speed up processing.

After each run, a **remapped.log** file can be found in **./logs/**.

### Specify parameters of approximated mapping
With **setp_size** and **steps**, you can control the resolution and scope of searching for the closest liftable position when a position can not be lifted. The default values are *500* and *4000*

### Parallel runing
The simplest way is to first generate a file containing files to process, split it into serval files, than use **index_file** option to start multiple sessions.
