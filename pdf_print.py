import PyPDF2, re, datetime, os
import tkinter as tk
from tkinter import filedialog, messagebox

pdf_input_name = ''
root = tk.Tk()
root.withdraw()

################################## Modify here ##########################################################
#Enter path + PDF & txt file name

default_path = r'' #For better user experience
pdf_output_name = r''
txt_input_name = r''
txt_output_name = r''

################################## Modify here ##########################################################

home = os.path.expanduser(default_path)
pdf_input_name = filedialog.askopenfilename(initialdir = home)

if pdf_input_name == '':
    print('user cancelled')
    raise SystemExit

retries = 1
while pdf_input_name.lower().endswith('.pdf') == False:
    print('you must select a pdf file only')
    pdf_input_name = filedialog.askopenfilename(initialdir = home)
    retries = retries - 1
    if retries == 0:
        raise ValueError('invalid user response')

with open(txt_input_name, 'r') as f:
    list_strings = []
    lines = [line.rstrip('\n') for line in f]
    list_strings += lines
    pdfFileObj = open(pdf_input_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter = PyPDF2.PdfFileWriter()

    pageFound = -1
    Count = 0
    for i in range(0, pdfReader.numPages):
        content = ""
        content += pdfReader.getPage(i).extractText() + "\n"
        content1 = content.encode('ascii', 'ignore').lower().decode('utf-8')
        for Number_string in list_strings:
            ResSearch = re.search(Number_string, content1)
            if ResSearch is not None:
               pageFound = i
               pageObj = pdfReader.getPage(pageFound)
               pdfWriter.addPage(pageObj)
               Count += 1
               break

pdfOutput = open(pdf_output_name, 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()
f.close()

print("Done! Total = %s" % Count)

with open (txt_output_name, 'w') as f1:
    pdfFileObj = open(pdf_output_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for pageNumber in range(0, pdfReader.numPages):
        page_content_for_txt = pdfReader.getPage(pageNumber).extractText()
        f1.write(page_content_for_txt)
    f1.close()
