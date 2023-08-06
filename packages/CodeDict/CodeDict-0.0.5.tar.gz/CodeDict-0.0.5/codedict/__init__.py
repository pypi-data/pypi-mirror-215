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
    line = fopen.readline()
    while line:
        if _line := line.strip():
            yield _line
        line = fopen.readline()
    fopen.close()

class CodeLoader:
    def __init__(self, *path, unique=True, use_bytes=False, encoding='utf8') -> None:
        self.path = set(path)
        self._unique = unique
        self.use_bytes = use_bytes
        self.encoding = encoding
    
    def bytes(self):
        self.use_bytes = True
        return self
    
    def str(self):
        self.use_bytes = False
        return self
        
    def unique(self):
        self._unique = True
        return self
    
    def not_unique(self):
        self._unique = False
        return self

    @property
    def iter(self):
        if self._unique:
            res = []
            for path in self.path:
                res += list(get_lines(path, encoding=self.encoding))
            return iter(set(res))
        return itertools.chain.from_iterable([
            get_lines(path)
            for path in self.path
        ])
        
    def __iter__(self):
        if self.use_bytes:
            return map(lambda x: x.encode(self.encoding), self.iter)
        return self.iter
    
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
    allin = Codes.all_in()
    for i in allin:
        # print(i)
        cnt += 1
    print(cnt)