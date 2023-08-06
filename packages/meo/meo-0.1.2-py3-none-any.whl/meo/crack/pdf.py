import pikepdf
import meo

class PDFCracker:
    def __init__(self, path: str) -> None:
        self.path = path

    def drop_psw_and_save(self, output_path='./unlock.pdf'):
        with pikepdf.open(self.path) as f:
            print(f.allow)
            # meo.checkout_file_path(output_path)
            # f.save(output_path)

if __name__ == '__main__':
    pdf = PDFCracker("./examples/data/cannot_open.pdf")
    pdf.drop_psw_and_save("./test/unlock.pdf")