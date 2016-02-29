from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pickle

# Open a PDF file.
fp = open('full.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
document = PDFDocument(parser)
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
device = PDFDevice(rsrcmgr)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)

# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = list(enumerate(PDFPage.create_pages(document)))
pages_length = len(pages)
print 'Created page list of ' + str(pages_length) + ' pages'

def sort_text (text):
    return (height - text.y1) * 1000000 + text.x0

all_boxes = []
for index, page in pages:
    print 'Parsing page ' + str(index) + ' of ' + str(pages_length)
    height = page.mediabox[3]
    interpreter.process_page(page)
    layout = device.get_result()
    textboxes = [obj for obj in layout._objs if type(obj).__name__ == 'LTTextBoxHorizontal']
    sorted_text_boxes = sorted([text for text in textboxes], key=sort_text)
    all_boxes += sorted_text_boxes

output = open('data.pkl', 'wb')
all_text = [text.get_text().replace('\n', '') for text in all_boxes]
pickle.dump(all_text, output)
