import csv
import os.path
from pprint import pprint
import xml.etree.ElementTree as ET
import re

# TODO : Open the CSV file in read mode.
# Example: C:\\Portico-Project\\SAE Standards\\SETUP-21241\\PQ-3844_Standards_NO_XML.csv
CSV_File_PATH = 'C:\\Portico-Project\\IBFR-PUMED\\Content-for-XML_SETUP-21924.csv'

# TODO: Convert dictionary into XML file and save it on the disk.
# Example: C:\\Portico-Project\\SAE Standards\\SETUP-21241\\Python-Generated-XML\\
output_file_location = "C:\\Portico-Project\\IBFR-PUMED\\Off-System-Portico-GeneratedXML\\"

if os.path.exists(output_file_location):
    pass
else:
    os.mkdir(output_file_location)

# Reading CSV file
csv_file = open(CSV_File_PATH,'r', encoding='utf-8')
csv_file_reader = csv.reader(csv_file)

# print(next(csv_file_reader))

header_row = [col.replace('ï»¿','') for col in next(csv_file_reader)]

# print(header_row)

# TODO: Read each row and store it in dictionary data structure

data_dict = {}

no_of_rows_in_csv = 0

for row in csv_file_reader:
    if row[0] not in data_dict:
        data_dict[row[0]] = row
    else:
        duplicate_row = row[0] + '-row-no-'+ str(csv_file_reader.line_num)
        data_dict[duplicate_row] = row
    no_of_rows_in_csv += 1


#pprint(data_dict)

# TODO: store XML file in output location.
no_of_xml_created = 0

def convert_csv_2_nlm_xml():
    global no_of_xml_created
    for k in data_dict:
        root = ET.Element('article',attrib=dict((('xmlns:xlink','http://www.w3.org/1999/xlink'),('xml:lang','en'),('article-type','technical-paper'))))
        tree = ET.ElementTree(root)

        front = ET.SubElement(root,'front')
        JM = ET.SubElement(front,'journal-meta')
        JID = ET.SubElement(JM,'journal-id')
        JID.text = data_dict[k][0]

        # ISSN = ET.SubElement(JM,'issn')

        EISSN = ET.SubElement(JM, 'issn', attrib=dict((('publication-format', 'electronic'),)))
        EISSN.text = data_dict[k][4]

        PISSN = ET.SubElement(JM, 'issn', attrib=dict((('publication-format', 'print'),)))
        PISSN.text = data_dict[k][5]

        PUBLISHER = ET.SubElement(JM,'publisher')
        PUBNAME = ET.SubElement(PUBLISHER,'publisher-name')
        PUBNAME.text = data_dict[k][3]
        PUBLOC = ET.SubElement(PUBLISHER,'publisher-loc')

        AM = ET.SubElement(front,'article-meta')
        ARTID = ET.SubElement(AM, 'article-id', attrib=dict((('pub-id-type','publisher-id'),)))
        ARTID.text=data_dict[k][0]
        TG = ET.SubElement(AM,'title-group')
        AT = ET.SubElement(TG,'article-title')
        AT.text = data_dict[k][2]

        CG = ET.SubElement(AM,'contrib-group')
        AUTHORS = data_dict[k][6].split(',')
        for AUTHOR in AUTHORS:
            CN = ET.SubElement(CG, 'contrib', attrib=dict((('contrib-type', 'AUTHOR'),)))
            SN = ET.SubElement(CN,'string-name')
            SN.text = AUTHOR

        PD = ET.SubElement(AM,'pub-date')

        if re.match("\\d{2}-\\d{2}-\\d{4}",data_dict[k][1]):
            groups = re.fullmatch("(\\d{2})-(\\d{2})-(\\d{4})",data_dict[k][1]).groups()
            PDAY = ET.SubElement(PD, 'day')
            PDAY.text = groups[1]
            PMON = ET.SubElement(PD, 'month')
            PMON.text = groups[0]
            PYEAR = ET.SubElement(PD, 'year')
            PYEAR.text = groups[2]

        if len(data_dict[k][9]) > 0:
            SELFURI = ET.SubElement(AM,'self-uri',attrib=dict((('xlink:href',data_dict[k][9]),)))

        if len(data_dict[k][7]) > 0:
            ABSTRACT = ET.SubElement(AM, 'abstract')
            ABP = ET.SubElement(ABSTRACT, 'p')
            ABP.text = data_dict[k][7]

        if len(data_dict[k][8]) > 0:
            CMG = ET.SubElement(AM, 'custom-meta-group')
            CM = ET.SubElement(CMG, 'custom-meta')
            MN = ET.SubElement(CM, 'meta-name')
            MN.text = header_row[8]
            MV = ET.SubElement(CM,'meta-value')
            MV.text = data_dict[k][8]

        ET.indent(tree,space=' ',level=0)
        # ET.dump(root)
        # Example: PQ-3844_Standards_NO_XML-XLSX-PTC
        source_csv_file_name='PQ-3745_Tech_Papers_NO_XML-XLSX-PTC'
        output_file = open(output_file_location + source_csv_file_name + '-' + k + '.xml', 'wb')

        tree.write(output_file, encoding='utf-8', xml_declaration=True)

        no_of_xml_created += 1
        output_file.close()



def generate_csv_2_pubmed_xml():
    for key_col in data_dict:
        articleset = ET.Element("ArticleSet")
        tree = ET.ElementTree(articleset)
        article = ET.SubElement(articleset, 'Article')
        journal = ET.SubElement(article,"Journal")
        publishername = ET.SubElement(journal,"PublisherName")
        publishername.text = data_dict[key_col][1]

        # Journal start
        journaltitle  = ET.SubElement(journal,"JournalTitle")
        journaltitle.text = data_dict[key_col][2]
        pissn = ET.SubElement(journal,"PIssn")
        pissn.text = data_dict[key_col][3]

        eissn = ET.SubElement(journal,"EIssn")
        eissn.text = data_dict[key_col][4]
        volume = ET.SubElement(journal,"Volume")
        volume.text = data_dict[key_col][5]
        issue = ET.SubElement(journal,"Issue")
        issue.text = data_dict[key_col][6]

        pubdate = ET.SubElement(journal, "PubDate", attrib=dict((('PubStatus','ppublish'),)))
        year = ET.SubElement(pubdate, "Year")
        year.text = data_dict[key_col][7]
        # Journal end

        articletitle = ET.SubElement(article, "ArticleTitle")
        articletitle.text = data_dict[key_col][8]

        firstpage = ET.SubElement(article, "FirstPage")
        firstpage.text = data_dict[key_col][9]

        lastpage = ET.SubElement(article, "LastPage")
        lastpage.text = data_dict[key_col][10]

        pdffilename = ET.SubElement(article, "PDFFileName")
        pdffilename.text = data_dict[key_col][11]

        language = ET.SubElement(article, "Language")
        language.text = data_dict[key_col][12]

        authorlist = ET.SubElement(article, "AuthorList")
        author_list = [items.replace('\naff:',', aff:').replace('\nauthor','author') for items in  data_dict[key_col][13].split(',\n')]
        author_list_list = [re.split('\nauthor:',items) for items in author_list]
        #print(author_list_list)

        for items in author_list_list:
            for item in items:
                #print(item)
                author_affiliation = re.match(pattern='(author: .*),\\s*(aff: .*)',string=item).groups()
                author_name = author_affiliation[0].replace('author: ','').split(' ')
                #print(author_affiliation[0])
                author = ET.SubElement(authorlist, "Author")
                firstname = ET.SubElement(author, "FirstName")
                firstname.text = author_name[0]
                if len(author_affiliation[0])==2:
                    middlename = ET.SubElement(author, "MiddleName")
                    middlename.text = author_name[1]
                    lastname = ET.SubElement(author, "LastName")
                    lastname.text = author_name[2]
                else:
                    lastname = ET.SubElement(author, "LastName")
                    lastname.text = author_name[1]

                affiliation = ET.SubElement(author, "Affiliation")
                affiliation.text =  author_affiliation[1].replace('aff: ','')

        abstract = ET.SubElement(article, "Abstract")
        abstract.text = data_dict[key_col][14]
        copyrightinformation = ET.SubElement(article, "CopyrightInformation")
        copyrightinformation.text = data_dict[key_col][15]

        objectlist = ET.SubElement(article, "ObjectList")
        keywords_list = data_dict[key_col][16].split(',')
        for keyword in keywords_list:
            object = ET.SubElement(objectlist, "Object", attrib=dict((("Type", 'keyword'),)))
            param  = ET.SubElement(object, "Param", attrib=dict((("Name", 'value'),)))
            param.text = keyword.replace(' Param: ','').replace('Param: ','')

        urls = ET.SubElement(article, "URLs")
        urls_list = data_dict[key_col][17].split(',')
        urls_abstract = ET.SubElement(urls, "abstract")
        urls_abstract.text = urls_list[0].replace('abstract: ','')
        fulltext = ET.SubElement(urls, "Fulltext")
        for item in urls_list[1:]:
            pdf = ET.SubElement(fulltext, "pdf")
            pdf.text = item.replace(' Fulltext: ','')

        ET.indent(tree,space=' ',level=0)
        # ET.dump(root)
        # Example: PQ-3844_Standards_NO_XML-XLSX-PTC
        source_csv_file_name='Off-System-Portico-Generated-Metadata'
        output_file = open(output_file_location + source_csv_file_name + '-' + key_col, 'wb')

        tree.write(output_file, encoding='utf-8', xml_declaration=True)


generate_csv_2_pubmed_xml()

# TODO: Close open files
print(f"Total number of records in CSV file are {no_of_rows_in_csv}")

print(f"Total number of XML files created {no_of_xml_created}")
csv_file.close()