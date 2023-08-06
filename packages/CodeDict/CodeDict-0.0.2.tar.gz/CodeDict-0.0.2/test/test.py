class Squares:
    def __init__(self, start, stop):  # 迭代起始、终止位
        self.value = start
        self.stop = stop

    def __iter__(self):     # 返回自身的迭代器
        return self

    def __next__(self):     # 返回下一个元素
        if self.value > self.stop:   # 结尾时抛出异常
            raise (StopIteration)
        item = self.value**2
        self.value += 1
        return item

if __name__ == "__main__":
    for i in Squares(1, 5):
        print(i, end=" ")

    s = Squares(1,5)
    print()
    print(9 in s)