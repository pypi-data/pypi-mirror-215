import meo
import zipfile
import os

__CUR_PATH = meo.utils.script_path(__file__)
# unzip
BOOKS_DIR_PATH = os.path.join(__CUR_PATH, "books")
if not os.path.exists(BOOKS_DIR_PATH):
    BOOKS_ZIP_FILE_PATH = os.path.join(__CUR_PATH, "books.zip")
    zipfile.ZipFile(BOOKS_ZIP_FILE_PATH).extractall(BOOKS_DIR_PATH)

def get_book_path(name):
    return os.path.join(__CUR_PATH, "books", name)

class CodeNames:
    FIVE_MILLION_PATH = get_book_path("5M.txt")
    TOP1000_PATH = get_book_path("top1000.txt")
    WPA_PATH = get_book_path("wpa.txt")

def get_lines(path, encoding='utf8'):
    fopen = open(path, 'r', encoding=encoding)
    while True:
        line = fopen.readline()
        if line:
            yield line.strip()
        else: break
    fopen.close()

class CodeLoader:
    def __init__(self, path) -> None:
        self.path = path

    def __iter__(self):
        return get_lines(self.path)
    
class Codes:
    def top1000():
        return CodeLoader(CodeNames.TOP1000_PATH)
    def wpa():
        return CodeLoader(CodeNames.WPA_PATH)
    def five_million():
        return CodeLoader(CodeNames.FIVE_MILLION_PATH)
    def some(*path):
        for p in path:
            for wd in CodeLoader(p):
                yield wd
    def all_in():
        names = [ ]
        for k in dir(CodeNames):
            v = getattr(CodeNames, k)
            if isinstance(v, str) and os.path.exists(v):
                names.append(v)
        return Codes.some(*names)

if __name__ == '__main__':
    for cell in Codes.all_in():
        print(cell)