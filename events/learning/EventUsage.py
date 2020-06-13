class Usage:
    def __init__(self):
        self.count = 0
        self.limit = 20

    def has(self, attr):
        """ hasattr() 函數用於判斷對象是否包含對應的屬性。
        如果對象有該屬性返回 True，否則返回 False。"""

        return hasattr(self, attr)

    """
    （1）__getattr__(self, item):
    在訪問對象的 item 屬性的時候，如果對象並沒有這個相應的屬性，方法，那麽將會調用這個方法來處理。。。
    這裏要註意的時，假如一個對象叫 fjs,  他有一個屬性：fjs.name = "fjs"，
    那麽在訪問 fjs.name 的時候因為當前對象有這個屬性，那麽將不會調用 __getattr__() 方法，
    而是直接返回了擁有的 name 屬性了
    
    （2）__setattr__(self, item, value): 
    當試圖對象的 item 特性賦值的時候將會被調用。。
    
    （3）__getattribute__(self, item): 
    這個只有在新式類中才有的，對於對象的所有特性的訪問，都將會調用這個方法來處理。。。
    可以理解為在 __getattr__ 之前
    """

    # 當要存取這個物件沒有的屬性時，會呼叫這個函式
    def __getattr__(self, item):
        print("__getattr__, item:", item)
        raise AttributeError(f"No {item} attribute.")


usage = Usage()
print(usage.has('__getattr__'))
print(usage.has('__events__'))
print(usage.has('count'))
