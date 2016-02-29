import pickle
import csv
import re

pkl_file = open('data.pkl', 'rb')
all_boxes = pickle.load(pkl_file)

district = 'NULL'
constit = 'NULL'
sub_county = 'NULL'
rows = []
row = []
## Regex helpers
parish = '\d{3}(?:\s[A-Za-z]+)+'
station = '\d{2}(?:\s+\S+)+'

## Create new lines with single blanks or Parishes
pattern = re.compile('^\s$|' + parish)
full_list = list(enumerate(all_boxes))

for index, text in full_list:
    ## current text replaces new lines and percentages
    current_text = re.sub('\s[\d|\.]+%', '', text)
    ## save the sub country match object in case it matched too much
    sub_county_test = re.match('\s*Sub-county:\s(\d+(?:\s[A-Z]+)+)(\s+' + parish + ')?(\s+' + station +')?(.+?\d{2,})?', current_text)
    ## save the extra info match to keep vote numbers off the station names
    extra_info_test = re.match('(' + station + ')(.+?\d{2,})', current_text)
    if re.match('DISTRICT:', current_text):
        district = full_list[index + 1][1]
    if re.match('CONSTITUENCY:', current_text):
        constit = full_list[index + 1][1]
    if pattern.match(current_text) or sub_county_test:
        if len(row) > 4 and not re.search('Tuesday|Parish|Total|Page|TALLY|CONSTITUENCY|^\s{3}$', row[4]) and not re.search('Tuesday|Parish|Total|Page|TALLY|CONSTITUENCY|^\s{3}$', row[3]):
            ## before we append the row, check if there are three digit numbers
            ## trailing the 5th column, we don't catch them earlier because of
            ## how broad we need to be with station matching
            trailing_triple = re.match('(?:\s+)?(' + station + ')\s+(\d{3})', row[4])
            if trailing_triple:
                row[4] = trailing_triple.group(1)
                row = row[0:4] + [trailing_triple.group(2)] + row[4:]
            ## also if station is in the 6th column, swap it back
            if re.match(station, row[5]):
                row[5], row[4] = row[4], row[5]
            rows.append(row)
        if sub_county_test:
            sub_county = sub_county_test.group(1)
        row = [district, constit, sub_county]
        if sub_county_test:
            for group in sub_county_test.groups()[1:]:
                if group:
                    row.append(group)
        else:
            parish_plus = re.match('(' + parish + ').+?(' + station + ')(.+?\d{2,})?', current_text)
            if parish_plus:
                for group in parish_plus.groups():
                    if group:
                        row.append(group)
            else:
                row.append(current_text)
    elif extra_info_test:
        for group in extra_info_test.groups():
            if group:
                row.append(group)
    else:
        row.append(current_text)

with open('output_pickle.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        writer.writerow(row)
