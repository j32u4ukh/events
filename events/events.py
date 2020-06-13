"""
Events
~~~~~~

Implements C#-Style Events.

Derived from the original work by Zoran Isailovski:
http://code.activestate.com/recipes/410686/ - Copyright (c) 2005

:copyright: (c) 2014-2017 by Nicola Iarocci.
:license: BSD, see LICENSE for more details.
"""


class Events:
    """
    Encapsulates the core to event subscription and event firing, and feels
    like a "natural" part of the language.

    The class Events is there mainly for 3 reasons:

        - Events (Slots) are added automatically, so there is no need to
        declare/create them separately. This is great for prototyping. (Note
        that `__events__` is optional and should primarilly help detect
        misspelled event names.)
        - To provide (and encapsulate) some level of introspection.
        - To "steel the name" and hereby remove unneeded redundancy in a call
        like:

            xxx.OnChange = event('OnChange')
    """
    def __init__(self, events=None):

        if events is not None:
            # 檢查 events 是否為 iterable
            try:
                for _ in events:
                    break
            except:
                raise AttributeError("type object %s is not iterable" % (type(events)))
            else:
                self.__events__ = events

    def __getattr__(self, name):
        print("__getattr__, name: ", name)
        if name.startswith('__'):
            raise AttributeError("type object '%s' has no attribute '%s'" %
                                 (self.__class__.__name__, name))

        if hasattr(self, '__events__'):
            if name not in self.__events__:
                raise EventsException("Event '%s' is not declared" % name)

        elif hasattr(self.__class__, '__events__'):
            if name not in self.__class__.__events__:
                raise EventsException("Event '%s' is not declared" % name)

        print("Add new attr ", name)
        self.__dict__[name] = ev = EventSlot(name)
        return ev

    def __repr__(self):
        return '<%s.%s object at %s>' % (self.__class__.__module__,
                                         self.__class__.__name__,
                                         hex(id(self)))

    __str__ = __repr__

    def __len__(self):
        return len(self.__dict__.items())

    def __iter__(self):
        def gen(dictitems=self.__dict__.items()):
            for attr, val in dictitems:
                if isinstance(val, EventSlot):
                    yield val
        return gen()


class EventSlot:
    def __init__(self, name):
        self.targets = []
        self.__name__ = name

    def __repr__(self):
        return "event '%s'" % self.__name__

    def __call__(self, *a, **kw):
        """ Events 的 on_change() 呼叫時，會被呼叫的函式，可輸入參數 *a, **kw"""
        for f in tuple(self.targets):
            f(*a, **kw)

    def __iadd__(self, f):
        """ Override += 符號
        使用 += 相當於呼叫 __iadd__ """
        self.targets.append(f)
        return self

    def __isub__(self, f):
        """ Override -= 符號
        使用 -= 相當於呼叫 __isub__ """
        # 使用 while 而非 if 的原因為: 同樣的元素或函式可以重複加入，不一定只有一個
        while f in self.targets:
            self.targets.remove(f)
        return self

    def __len__(self):
        # 取得長度
        return len(self.targets)

    # region 代迭 EventSlot 時的 Iterable 物件
    def __iter__(self):
        def gen():
            for target in self.targets:
                yield target
        return gen()

    def __getitem__(self, key):
        return self.targets[key]
    # endregion


class EventsException(Exception):
    def __init__(self, msg):
        print(f"[EventsException] {msg}")


if __name__ == "__main__":
    def onClickedListener():
        print("onClickedListener")

    def onChangedValueListener(value):
        print(f"onChangedValueListener value: {value}")

    event = Events()
    event.on_click += onClickedListener
    event.on_change += onChangedValueListener

    for i in range(50):
        if i % 7 == 0:
            event.on_click()
            event.on_change(i)
