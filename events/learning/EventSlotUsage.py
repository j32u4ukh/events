class Usage:
    def __init__(self, name):
        self.container = []
        self.__name__ = name

    def __iadd__(self, item):
        """ Override += 符號
        使用 += 相當於呼叫 __iadd__ """
        self.container.append(item)
        return self

    def __isub__(self, item):
        """ Override -= 符號
        使用 -= 相當於呼叫 __isub__ """
        # 使用 while 而非 if 的原因為: 同樣的元素或函式可以重複加入，不一定只有一個
        while item in self.container:
            self.container.remove(item)
        return self

    def __len__(self):
        """ 呼叫 len(self) 時會返回的數值 """
        return len(self.container)

    # region Iteration / Iterable / Iterator
    """
    Iteration:  走訪/迭代/遍歷一個 object 裡面被要求的所有元素之「過程」或「機制」。是一個概念性的詞。
    Iterable:   可執行 Iteration 的 objects 都稱為 Iterable(可當專有名詞)。
                參照 官方文件 提及，是指可以被 for loop 遍歷的 objects。
                以程式碼來說，只要具有 __iter__ 或__getitem__ 的 objects 就是 Iterable。
    Iterator:   遵照 Python Iterator Protocol 的 objects。
                以 Python3 而言，參照 官方文件，只要具有 __iter__ 和 __next__ 的 objects 皆為 Iterator。
                Iterator 是 Iterable 的 subset。

    for item in x >> x 只需有 __iter__ 就可以

    # 同時有 __iter__ 和 __getitem__ 時，似乎會優先執行 __iter__
    # 補充一點 __getitem__ 是常見的 magic function (即 Python 預設自訂帶有 double underscores 的 function)，
      所以並不是只有在處理 iteration 時會使用到，如 index 和 slice 等功能都會需要使用到此 function，
      若在創建較為複雜的 object 時，要記得根據 __getitem__ 的 arguments 兼容處理各種況狀。
    # 可能有人會問說為何 Iteration 要設計 __next__ 和__getitem__ 這兩種 pattern 呢？
      實作面來說，用 __next__ 這種方式寫會更適合在處理、生成前後值相依或是與 streaming 概念相似的資料，
      例如「生成 Fibonacci Sequence」；
      而 __getitem__ 一般使用情境是已經將所有資料儲存在某處、某變數中，然後透過 key 來取值。
    """

    def __iter__(self):
        print("__iter__")
        return iter(self.container)

    def __getitem__(self, item):
        # print("__getitem__:", item)
        return self.container[item]

    # endregion

    def __call__(self, *args, **kwargs):
        """ 物件以函式的形式被使用時，會呼叫的函式
        usage = Usage()
        usage() >> 此時會呼叫 __call__ 函式
        """
        print("__call__")

    # region 印出物件，類似於 toString()
    """ 
    調用了print function，其輸出是 __str__ 返回的字串，若是直接輸入變數，輸出則為 __repr__ 返回的字串
    >>> print(usage)
    __str__ event U
    
    >>> usage
    __repr__ event U
    """
    def __repr__(self):
        return f"__repr__ event {self.__name__}"

    def __str__(self):
        return f"__str__ event {self.__name__}"
    # endregion


def func1():
    print("func1")


def func2():
    print("func2")


if __name__ == "__main__":
    usage = Usage("U")
    usage += func1
    usage += func2
    print(usage.container)
    print("__len__:", len(usage))
    usage()
    print(usage)

