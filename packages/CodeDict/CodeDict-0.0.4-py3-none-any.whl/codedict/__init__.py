import meo
import zipfile
import os
import itertools

__CUR_PATH = meo.utils.script_path(__file__)
# unzip
BOOKS_DIR_PATH = os.path.join(__CUR_PATH, "books")
if not os.path.exists(BOOKS_DIR_PATH):
    # cat slices
    _SLICES_PATH = os.path.join(__CUR_PATH, "slices")
    file_bytes = bytes()
    for slice_name in os.listdir(_SLICES_PATH):
        path = os.path.join(_SLICES_PATH, slice_name)
        if os.path.isfile(path):
            file_bytes += meo.load_file(path)
    BOOKS_ZIP_FILE_PATH = os.path.join(__CUR_PATH, "books.zip")
    meo.to_file(BOOKS_ZIP_FILE_PATH, file_bytes, mode='wb+')
    # unzip
    zipfile.ZipFile(BOOKS_ZIP_FILE_PATH).extractall(BOOKS_DIR_PATH)
    os.remove(BOOKS_ZIP_FILE_PATH)

def get_book_dir(_type):
    book_dir = os.path.join(__CUR_PATH, "books", _type)
    return lambda name: os.path.join(book_dir, name)

get_codes_path = get_book_dir("codes")

class CodeBookPath:
    FIVE_MILLION_PATH = get_codes_path("5M.txt")
    TOP1000_PATH = get_codes_path("top1000.txt")
    WPA_PATH = get_codes_path("wpa.txt")
    ROOTPHANTOMER_PATH = get_codes_path('rootphantomer.txt')

def get_lines(path, encoding='utf8'):
    fopen = open(path, 'r', encoding=encoding)
    while True:
        line = fopen.readline()
        if line := line.strip():
            yield line
        else: break
    fopen.close()

class CodeLoader:
    def __init__(self, *path, unique=True) -> None:
        self.path = set(path)
        self._unique = True
        
    def unique(self):
        self._unique = True
        return self
    
    def not_unique(self):
        self._unique = False
        return self

    def __iter__(self):
        if len(self.path) == 1:
            return get_lines(self.path[0])
        if self._unique:
            res = set()
            for path in self.path:
                lines = set(get_lines(path))
                res = res or lines
            return iter(res)
        return itertools.chain.from_iterable([
            get_lines(path)
            for path in self.path
        ])
    
    def __add__(self, v):
        if isinstance(v, CodeLoader):
            return CodeLoader(*self.path, *v.path)
        elif isinstance(v, str):
            return CodeLoader(*self.path, v)
        else:
            raise ValueError("except str or CodeLoader")

class Codes:
    def top1000():
        return CodeLoader(CodeBookPath.TOP1000_PATH)
    def wpa():
        return CodeLoader(CodeBookPath.WPA_PATH)
    def five_million():
        return CodeLoader(CodeBookPath.FIVE_MILLION_PATH)
    def rootphantomer():
        return CodeLoader(CodeBookPath.ROOTPHANTOMER_PATH)
    def some(*path):
        return CodeLoader(*path)
    def all_in():
        names = [ ]
        for k in dir(CodeBookPath):
            v = getattr(CodeBookPath, k)
            if isinstance(v, str) and not (k.startswith("__") or k.endswith("__")):
                names.append(v)
        return Codes.some(*names)

if __name__ == '__main__':
    cnt = 0
    it = Codes.five_million() + Codes.rootphantomer()
    for cell in it.not_unique():
        cnt +=1
    print(cnt)
    cnt = 0
    for cell in it.unique():
        cnt +=1
    print(cnt)
    for pwd in Codes.all_in():
        print(pwd)
        exit()