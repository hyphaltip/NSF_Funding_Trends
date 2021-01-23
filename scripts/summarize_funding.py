#!/usr/bin/env python3

import zipfile
from lxml import etree

#print etree.tostring(root)

import xml.etree.ElementTree as ET
import os
import csv

# support XML pretty print

def indent(elem, level=0):
    i = "\n" + level * "  "
    j = "\n" + (level - 1) * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


folder = "download"
outfolder="report"
if not os.path.isdir(outfolder):
    os.mkdir(outfolder)

OrgType = set(['Directorate', 'Division'])
Columns = ['AwardEffectiveDate','AwardExpirationDate','MinAmdLetterDate','MaxAmdLetterDate',
             'AwardInstrument', 'AwardAmount', 'AwardID']
qtypes = set(Columns)

Columns.extend(OrgType)
Columns.insert(0,'Year')
for fname in os.listdir(folder):
    if not fname.endswith('.zip'):
        print("skipping {} not a zipfile".format(fname))
        continue
    print(fname)
    Year = os.path.splitext(fname)[0]
    with open(os.path.join(outfolder,"{}.csv".format(Year)),"w") as ofh:
        csvout = csv.writer(ofh,delimiter=",")
        csvout.writerow(Columns)
        # schema
        # year, Duration (months), AwardInstrument, AwardAmount, Directorate,Division, AwardID
        with zipfile.ZipFile(os.path.join(folder, fname), 'r') as myzip:
            for xmlfile in myzip.namelist():
                #print(xmlfile)
                record = {'Year': Year}
#                try:
                with myzip.open(xmlfile,"r") as xmlfh:
                    parser = etree.XMLParser(recover=True) # recover from bad characters.
                    #tree = ET.parse(xmlfh)
                    root = etree.parse(xmlfh, parser=parser)
                    #root = tree.getroot()
                    for award in root.findall('Award'):
                        for field in award:
                            if field.tag == 'Organization':
                                for subfield in field:
                                    if subfield.tag in OrgType:
                                        for name in subfield:
                                            if name.tag == "LongName":
                                                #print(subfield.tag, name.text)
                                                record[subfield.tag] = name.text
                            elif field.tag in qtypes:
                                if field.tag == "AwardInstrument":
                                    for val in field:
                                        if val.tag == "Value":
                                            record[field.tag] = val.text
                                else:
                                    record[field.tag] = field.text
                line = []
                for col in Columns:
                    line.append(record[col])
                csvout.writerow(line)
                        #ET.dump(root)
                        #print(root)
#                except ET.ParseError as err:
#                    print("caught an error with {}/{} {}".format(fname,xmlfile,err))
#                    indent(root)
#                    str = ET.tostring(root)
#                    print(str)
#                    pass
