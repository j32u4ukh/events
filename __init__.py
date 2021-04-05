"""
Events
~~~~~~

Implements C#-Style Events.

Derived from the original work by Zoran Isailovski:
http://code.activestate.com/recipes/410686/ - Copyright (c) 2005

:copyright: (c) 2014-2017 by Nicola Iarocci.
:license: BSD, see LICENSE for more details.
"""


class Event:
    """
    一個 Events 可以添加多個 EventSlot，而一個 EventSlot 又可添加多個 Listener
    >> event = Events()
    >> event.onClicked += onClickedListener1
    >> event.onClicked += onClickedListener2
    >> event.onChanged += onChangedListener1
    >> event.onChanged += onChangedListener2
    """

    def __init__(self):
        pass

    # 當要存取這個物件沒有的屬性時，會呼叫這個函式
    def __getattr__(self, item):
        # __XXX__ 為 Python 內建函式的形式，盡可能避免
        if item.startswith('__'):
            raise AttributeError(f"Avoid using the form like {item}.")
        else:
            # 建立這個屬性，其內涵為 EventSlot 物件
            self.__dict__[item] = ev = EventSlot(item)
            return ev

    def __repr__(self):
        keys = []
        for key in self.__dict__.keys():
            keys.append(key)

        length = len(keys)
        if length == 0:
            output = ""
        else:
            output = "{}".format(keys[0])

            for i in range(1, length):
                output = "{}, {}".format(output, keys[i])

        return "Listener: [{}]".format(output)

    """ 
    調用了print function，其輸出是 __str__ 返回的字串，若是直接輸入變數，輸出則為 __repr__ 返回的字串
    >>> print(usage)
    呼叫 __str__

    >>> usage
    呼叫 __repr__
    """
    __str__ = __repr__

    def __len__(self):
        return len(self.__dict__.items())

    def __iter__(self):
        def gen(dictitems=self.__dict__.items()):
            for attr, val in dictitems:
                if isinstance(val, EventSlot):
                    yield val

        return gen()

    def clearEventSlot(self):
        self.__dict__ = dict()

    def clearListener(self, slot):
        event_slot = self.__dict__[slot]
        event_slot.clearListener()


class EventSlot:
    def __init__(self, name):
        self.__name__ = name
        self.func_container = []

    def __call__(self, *args, **kwargs):
        """ EventSlot 被呼叫時，會被呼叫的函式，可輸入參數 *args, **kwargs"""
        for func in tuple(self.func_container):
            func(*args, **kwargs)

    def __iadd__(self, func):
        """ Override += 符號
        使用 += 相當於呼叫 __iadd__ """
        self.func_container.append(func)
        return self

    def __isub__(self, func):
        """ Override -= 符號
        使用 -= 相當於呼叫 __isub__ """
        # 使用 while 而非 if 的原因為: 同樣的元素或函式可以重複加入，不一定只有一個
        while func in self.func_container:
            self.func_container.remove(func)
        return self

    # region 代迭 EventSlot 時的 Iterable 物件
    """
    Iteration:  走訪/迭代/遍歷一個 object 裡面被要求的所有元素之「過程」或「機制」。是一個概念性的詞。
    Iterable:   可執行 Iteration 的 objects 都稱為 Iterable(可當專有名詞)。
                參照 官方文件 提及，是指可以被 for loop 遍歷的 objects。
                以程式碼來說，只要具有 __iter__ 或__getitem__ 的 objects 就是 Iterable。
    Iterator:   遵照 Python Iterator Protocol 的 objects。
                以 Python3 而言，參照 官方文件，只要具有 __iter__ 和 __next__ 的 objects 皆為 Iterator。
                Iterator 是 Iterable 的 subset。

    for item in x >> x 只需有 __iter__ 就可以

    # 補充一點 __getitem__ 是常見的 magic function (即 Python 預設自訂帶有 double underscores 的 function)，
      所以並不是只有在處理 iteration 時會使用到，如 index 和 slice 等功能都會需要使用到此 function，
      若在創建較為複雜的 object 時，要記得根據 __getitem__ 的 arguments 兼容處理各種況狀。
    # 可能有人會問說為何 Iteration 要設計 __next__ 和__getitem__ 這兩種 pattern 呢？
      實作面來說，用 __next__ 這種方式寫會更適合在處理、生成前後值相依或是與 streaming 概念相似的資料，
      例如「生成 Fibonacci Sequence」；
      而 __getitem__ 一般使用情境是已經將所有資料儲存在某處、某變數中，然後透過 key 來取值。
    """

    # 同時有 __iter__ 和 __getitem__ 時，似乎會優先執行 __iter__
    def __iter__(self):
        return iter(self.func_container)

    def __getitem__(self, key):
        return self.func_container[key]

    # endregion

    # 定義直接輸入變數時，會輸出字串
    def __repr__(self):
        length = len(self.func_container)
        if length == 0:
            output = ""
        else:
            output = "{}".format(self.func_container[0].__name__)

            for i in range(1, length):
                output = "{}, {}".format(output, self.func_container[i].__name__)

        return "EventSlot {}: [{}]".format(self.__name__, output)

    # 取得長度
    def __len__(self):
        """ 呼叫 len(self) 時會返回的數值 """
        return len(self.func_container)

    def clearListener(self):
        self.func_container = []


class EventsException(Exception):
    def __init__(self, msg):
        print(f"EventsException | {msg}")


# TODO: 嘗試做出一個事件的全部監聽器都執行完，才執行下一個的效果(如果是第一個監聽器觸發下一個事件的情況時)
class SequentialEvent:
    def __init__(self):
        pass


if __name__ == "__main__":
    def onClickedListener():
        print("onClickedListener")


    def onChangedValueListener(value):
        print(f"onChangedValueListener value: {value}")


    event = Event()
    event.on_click += onClickedListener
    event.on_change += onChangedValueListener
    event.on_change += onChangedValueListener

    event.clearListener(slot="on_change")
    event.on_change += onChangedValueListener

    event.on_click()
    event.on_change(7)
    event.clearEventSlot()

    print(event)

    event.on_click()
    event.on_change(7)
    print(event)
