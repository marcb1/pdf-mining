import pyPdf
import re
import string

def all_names_in_pdf(pdf):
  all_names = []
  for page in pdf.pages:
    cur_page = page.extractText()
    names = parse_names_from_text(cur_page)
    all_names.extend(names)
  return all_names   

def compare_pdf(first_pdf, *other_pdfs):
  first_pdf_names = all_names_in_pdf(first_pdf)
  first_pdf_names = [x.strip(string.whitespace) for x in first_pdf_names]
  for other_pdf in other_pdfs:
    other_pdf_names = all_names_in_pdf(other_pdf)
    other_pdf_names = [x.strip(string.whitespace) for x in other_pdf_names]
    in_first_not_in_other = [x for x in first_pdf_names if x not in other_pdf_names]
    print "names in first pdf but not in second" 
    print in_first_not_in_other
    print ""
  

def parse_names_from_text(cur_page):
      deans_list_regex = 'Dean.*\s+List'
      page_regex = 'Page.*\s+\d+'

      #split page of text by three or more spaces
      names = re.split('\s{3,}', cur_page)

      for name in names:
          if name.find('\n')!=-1:
            names.remove(name)
            split_names = name.split('\n')
            names.extend(split_names)
            continue

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
      print "Found: " + name
  return matches;

pdf1 = pyPdf.PdfFileReader(open("dean-list1.pdf", "rb"))
year1 = all_names_in_pdf(pdf1)

pdf2 = pyPdf.PdfFileReader(open("dean-list2.pdf", "rb"))
year2 = all_names_in_pdf(pdf2)

print find_name_in_list('Neal', 'T', year1);

print find_name_in_list('Neal', 'T', year2);

compare_pdf(pdf1, pdf2)
