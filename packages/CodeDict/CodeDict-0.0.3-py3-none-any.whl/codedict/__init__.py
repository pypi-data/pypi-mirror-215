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
    ROOTPHANTOMER_PATH = get_book_path('rootphantomer.txt')

def get_lines(path, encoding='utf8'):
    fopen = open(path, 'r', encoding=encoding)
    while True:
        line = fopen.readline()
        if line:
            yield line.strip()
        else: break
    fopen.close()

class CodeLoader:
    def __init__(self, *path) -> None:
        self.path = set(path)

    def __iter__(self):
        if len(self.path) == 1:
            return get_lines(self.path[0])
        res = set()
        for path in self.path:
            lines = set(get_lines(path))
            res = res or lines
        return iter(res)
    
    def __add__(self, v):
        if isinstance(v, CodeLoader):
            return CodeLoader(*self.path, *v.path)
        elif isinstance(v, str):
            return CodeLoader(*self.path, v)
        else:
            raise ValueError("except str or CodeLoader")

class Codes:
    def top1000():
        return CodeLoader(CodeNames.TOP1000_PATH)
    def wpa():
        return CodeLoader(CodeNames.WPA_PATH)
    def five_million():
        return CodeLoader(CodeNames.FIVE_MILLION_PATH)
    def rootphantomer():
        return CodeLoader(CodeNames.ROOTPHANTOMER_PATH)
    def some(*path):
        return CodeLoader(*path)
    def all_in():
        names = [ ]
        for k in dir(CodeNames):
            v = getattr(CodeNames, k)
            if isinstance(v, str) and os.path.exists(v):
                names.append(v)
        return Codes.some(*names)

if __name__ == '__main__':
    cnt = 0
    for cell in Codes.five_million() + Codes.rootphantomer():
    # for cell in Codes.all_in():
        # print(cell)
        cnt +=1
    print(cnt)