from collections import UserDict


class MyCollection(UserDict):
    def __repr__(self):
        return "<{module}.{name}: {data}>".format(
            module=self.__class__.__module__,
            name=self.__class__.__name__,
            data=list(self.data.values()),
        )

    def __getitem__(self, item):
        if type(item) is str:
            return super().__getitem__(item)
        return list(self.data.values())[item]

    def __iter__(self):
        for item in self.data.values():
            yield item


class ResponseCollection(MyCollection):
    ...


class BatchCollection(MyCollection):
    ...
