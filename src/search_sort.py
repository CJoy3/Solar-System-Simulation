import datetime


class Search_Sort:
    def merge(data):
        if len(data) == 1:
            return data
        # recursion to split array
        left = Search_Sort.merge(data[: len(data) // 2])
        right = Search_Sort.merge(data[len(data) // 2 :])
        # empty array
        sorted_data = [[0 for i in range(2)] for j in range(len(data))]
        l = 0
        r = 0
        s = 0
        while l < len(left) and r < len(right):
            if datetime.datetime.strptime(
                left[l][0], r"%d/%m/%Y"
            ) > datetime.datetime.strptime(right[r][0], r"%d/%m/%Y"):
                sorted_data[s] = right[r]
                r += 1
                s += 1
            else:
                sorted_data[s] = left[l]
                l += 1
                s += 1
        # extra while loops after comparisons with left AND right
        while l < len(left):
            sorted_data[s] = left[l]
            l += 1
            s += 1
        while r < len(right):
            sorted_data[s] = right[r]
            r += 1
            s += 1
        return sorted_data

    def binary(dataset, to_find):
        if len(dataset) == 0:
            return -1
        left = 0
        right = len(dataset) - 1
        centre = (left + right) // 2
        # 2d list first part date comparison datetime.datetime.strptime(dataset[centre][0], r"%d/%m/%Y")
        while (
            datetime.datetime.strptime(dataset[centre][0], r"%d/%m/%Y") != to_find
            and left != right
        ):
            if datetime.datetime.strptime(dataset[centre][0], r"%d/%m/%Y") < to_find:
                left = centre + 1
            else:
                right = centre - 1
            centre = (left + right) // 2
        if datetime.datetime.strptime(dataset[centre][0], r"%d/%m/%Y") == to_find:
            return centre
        else:
            return -1


class Stack:
    def __init__(self):
        self.frame_stack = [0 for i in range(5)]
        self.pointer = -1

    def push(self, item):
        self.pointer += 1
        self.frame_stack[self.pointer] = item

    def pop(self):
        if self.pointer > 0:
            self.pointer -= 1

    def peek(self):
        top_item = self.frame_stack[self.pointer]
        return top_item
