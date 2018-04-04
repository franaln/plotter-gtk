class History:

    def __init__(self, maxlen=100):
        self._history = []
        self._index = 0
        self._maxlen = maxlen

    def add(self, item):
        # Remove everything after index
        # if self._index < len(self._history) - 2:
        #     del self._history[:self._index+1]
        # Remove Duplicates
        try:
            self._history.remove(item)
        except:
            pass
        #     else:
        #         if self._history and self._history[-1] == item:
        #             del self._history[-1]

        # Remove first if list is too long
        if len(self._history) > max(self._maxlen-1, 0):
            del self._history[0]

        # Append the item and fast forward
        self._history.append(item)
        self._index = len(self._history) - 1

    def __len__(self):
        return len(self._history)

    def index(self):
        return self._index

    def current(self):
        if self._history:
            return self._history[self._index]
        else:
            return None

    def top(self):
        try:
            return self._history[-1]
        except IndexError:
            return None

    def bottom(self):
        try:
            return self._history[0]
        except IndexError:
            return None

    def back(self):
        self._index -= 1
        if self._index < 0:
            self._index = 0
        return self.current()

    def forward(self):
        if self._history:
            self._index += 1
            if self._index > len(self._history) - 1:
                self._index = len(self._history) - 1
        else:
            self._index = 0
        return self.current()

    # def search(self, string, n):
    #     if n != 0 and string:
    #         step = n > 0 and 1 or -1
    #         i = self._index
    #         steps_left = steps_left_at_start = int(abs(n))
    #         while steps_left:
    #             i += step
    #             if i >= len(self._history) or i < 0:
    #                 break
    #             if self._history[i].startswith(string):
    #                 steps_left -= 1
    #         if steps_left != steps_left_at_start:
    #             self._index = i
    #     return self.current()
