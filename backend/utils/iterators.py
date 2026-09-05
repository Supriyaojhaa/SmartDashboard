class DatasetIterator:

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration

        value = self.data[self.index]
        self.index += 1
        return value

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f"DatasetIterator(rows={len(self.data)}, index={self.index})"
    
    def __add__(self, other):
        return len(self.data) + len(other.data)