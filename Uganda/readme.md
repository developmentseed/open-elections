## Uganda 2016 Presidential Elections

Results data provided by the Uganda Election Commission - http://www.ec.or.ug/ecresults/0-Final_Presidential_Results_Polling%20Station.pdf

## Data extraction
The PDF was converted to a csv using:
- read.py to extract the cntent of the PDF and write it to a python .pkl file, and
- parse.py to process the .pkl file and convert it to a structured .csv

**Note that the Constituency information may not be accurate. The PDF provided by the election commission lists one constituency at the top of each page. There appear to be cases where a page contains data from multiple constituencies, but the document still only lists a singe constituency. For completeness we include the data as provided by the EC.**
