import sys
import os

sys.path.insert(0, os.path.curdir)

from meo.crack import Crack

# pdf = Crack.pdf("./examples/data/cannot_edit.pdf")
# pdf.remove_pdf_password("./output.pdf")
pdf = Crack.pdf("./examples/data/cannot_open.pdf")
# pdf.remove_pdf_password("./output.pdf")

res = pdf.only_number()
print(res)