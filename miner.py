import pyPdf
import re

def all_names_in_pdf(pdf):
  all_names = []
  for page in pdf.pages:
    cur_page = page.extractText()
    names = parse_names_from_text(cur_page)
    all_names.extend(names)
  return all_names   

def parse_names_from_text(cur_page):
      deans_list_regex = 'Dean.*\s+List'
      page_regex = 'Page.*\s+\d+'

      #split page of text by three or more spaces
      names = re.split('\s{3,}', cur_page)

      for name in names:

          #Look for 'Dean's List'
          res = re.search(deans_list_regex, name, re.IGNORECASE)

          if res != None:
            #remove Dean's List from 'Dean's List Fall/Spring 20xx'
            match = re.sub(deans_list_regex, "", name)
            names.remove(name)
            if len(match) > 15:
                names.extend(match)


          #Look for Page x
          res = re.search(page_regex, name, re.IGNORECASE)

          if res != None:
            #remove Page digit* from 'Page digit* xxxx'
            match = re.sub(page_regex, "", name)
            names.remove(name)
            if len(match) > 4:
              names.extend(match)
      return names


def find_name_in_list(first, last, list):
  matches = 0
  for name in list:
    res = re.search(first + '.*\s+.*' + last, name, re.IGNORECASE)
    if res != None:
      matches += 1
  return matches;

pdf = pyPdf.PdfFileReader(open("dean-list1.pdf", "rb"))
year1 = all_names_in_pdf(pdf)

pdf = pyPdf.PdfFileReader(open("dean-list2.pdf", "rb"))
year2 = all_names_in_pdf(pdf)

print find_name_in_list('Neal', 'T', year1);

print find_name_in_list('Neal', 'T', year2);
