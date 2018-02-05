import re

from collections import defaultdict
from pagereport.examplerequests import example_requests
from pagereport.exampleresponses import http_requests
from sys import argv, stderr


class Auxiliary():

    """Auxiliary class with set of function that will be used in page_report function
    """

    @staticmethod
    def data(name_of_file=None):
        """Reading data from the file
        """
        if not name_of_file:
             name_of_file = argv[1]

        # preparing data
        try:
            with open(name_of_file, 'rb') as f:
                data = f.read().decode("utf-8")
        except UnicodeDecodeError:
            try:
                with open(name_of_file, 'rb') as f:
                    data = f.read().decode("ISO-8859-1")
            except UnicodeDecodeError:
                print("Change the standard of file to UTF-8")

        return data

    @staticmethod
    def pattern(example_requests, http_requests):
        """Setting regex patterns to be searched in the text
        """
        IPv4 = "(\d+\.\d+\.\d+\.\d+).+" # Intentional violation of PEP8 in naming "IPv4"
        datetime = "(\[.*\]).+"

        def pattern_handler(list_of_keywords, pattern):
            # Returns string with regex keyword "|"
            temp = list_of_keywords[0]
            for i in list_of_keywords[0]:
                temp += ("|" + i)
            return pattern.format(temp)

        request = pattern_handler(example_requests, "(?:{}) .*?(//|/)(.+?)(?=\?|/ |/\?| ).+")
        response = pattern_handler(http_requests, "({}) ")

        bytes_sent = "(\d+|-)$"
        return re.compile(IPv4 + datetime + request + response + bytes_sent)


def page_report(name_of_file=None):
    """Converts log file to the database containing visited urls and number of its occurrences,
    ordered lexicographically. Log file may be put from the shell command line.
    
    Parameters
    -----------
    name_of_file : str (optional argument); 
         Name of log file; 
       
    Return
    -----------
    None
    
    Raises
    -----------
    UnicodeDecodeError: if the file is not written in utf-8 standard. 
    """

    data = Auxiliary.data(name_of_file)
    pattern = Auxiliary.pattern(example_requests, http_requests)

    # Counting and sorting  occurrences
    counts = defaultdict(lambda: 0)
    for line in data.splitlines():
        try:
            result = pattern.findall(line)[0]
            if all(result):
                counts[result[3]] += 1
                continue
            raise IndexError
        except IndexError:
            counts["Invalid log lines"] += 1
            continue
    data = sorted(counts.items(), key=lambda x: (-x[1], x[0].lower()))

    # Printing results
    invalids = counts.get("Invalid log lines")
    stderr.write("Invalid log lines: {}\n".format(invalids if invalids else 0))
    for line in data:
        print('''"{}",{}'''.format(*line))

if __name__ == "__main__":
    page_report(name_of_file=None)
