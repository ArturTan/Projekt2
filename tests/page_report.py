import re

from ..page_report
from pagereport.examplerequests import example_requests
from pagereport.exampleresponses import http_requests
from sys import stdout, argv, stderr


class Pattern():

    @staticmethod
    def pattern(example_requests, http_requests):
        IPv4 = "(\d+\.\d+\.\d+\.\d+).+"
        datetime = "(\[.*\]).+"
        request_kinds = example_requests[0]
        for i in example_requests[1:]:
            request_kinds += ("|" + i)
        request = "(?:{}) .*?(//|/)(.+?)(?=\?|/ |/\?| ).+".format(request_kinds)
        responses_kinds = http_requests[0]
        for i in http_requests[1:]:
            responses_kinds += ("|" + i)
        response = "({}) ".format(responses_kinds)
        bytes_sent = "(\d+|-)$"
        return re.compile(IPv4 + datetime + request + response + bytes_sent)

def page_report():
    """Converts log file to the csv database containing visited urls and number of its occurrences,
    ordered lexigraphically.
    -----------
    The function gets file from the command line as the first argument from sys.argv list. 
    Firstly it find the following patterns:
    1) <IPv4 address>  ​- X.X.X.X, where X is the string containing integers;
    2) [<datetime>] - date and hour in brackets;
    3) "​ <HTTP request>​ " - REQUEST with url;
    4) ​<HTTP response code> - response code
    5)  <bytes sent> - number of bytes sent.
    If pattern exists, than the occurrence is registered by the count dictionary. 
    If not the number of "Invalid log lines" increases by 1. 
    Then, the function calculate number of occurrences and sort it by:
    1) number of occurences;
    2) name of the url. 
    
    Results are printed with sys.stdout.write.     
    """

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
            print("Change decoder")

    pattern = Pattern.pattern(example_requests, http_requests)

    # Counting and sorting  occurences
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
        stdout.write("'{}',{}\n".format(*line))


if __name__ == "__main__":
    page_report()

# Tests basing on the example from the task
# Copying the documentation from the files
# Messing the files out ("test2.txt", jupyter notebook, etc.")
# Writing down documentation
# Givng license
# Checking folders
