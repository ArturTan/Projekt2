# Traffic report

## Requirements. Technology and python libraries
Libraries: Python Standard Library, python3

## Installation

Download repo
```
git clone 
```

## Using the script:
```
The script converts log file to the database containing visited urls and number of its occurrences, ordered lexicographically. Log file may be put from the shell command line.

'''
$ python page_report.py log.file > report.csv
'''
    
Optionally it may be used as the function to be imported

__Example__
'''
>>> from page_report import page_report
>>> page_report("file.log")
'''



