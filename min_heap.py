
class MinHeap:
    def __init__(self):
        self.heap = [None]
        self.count = 0

    def parent_idx(self, idx):
        return idx // 2 

    def left_child_idx(self, idx):
        return idx * 2
    
    def right_child_idx(self, idx):
        return idx * 2 + 1

    def child_present(self, idx):
        return self.left_child_idx(idx) <= self.count
    
    def get_smaller_child(self, idx):
        if self.right_child_idx(idx) > self.count:
            return self.left_child_idx(idx)
        else:
            if self.heap[self.right_child_idx(idx)][2] < self.heap[self.left_child_idx(idx)][2]:
                return self.right_child_idx(idx)
            else:
                return self.left_child_idx(idx)
    
    def add(self, item):
        self.count += 1
        self.heap.append(item)
        self.heapify_up()

    def heapify_up(self):
        idx = self.count
        while self.parent_idx(idx) > 0:
            parent = self.heap[self.parent_idx(idx)]
            child = self.heap[idx]
            if parent[2] > child[2]:
                self.heap[self.parent_idx(idx)] = child
                self.heap[idx] = parent
            idx = self.parent_idx(idx)
    
    def retrieve_min(self):
        if self.count <= 0:
            return None
        min = self.heap[1]
        self.heap[1] = self.heap[self.count]
        self.count -= 1
        self.heap.pop(-1)
        self.heapify_down()
        return min
    
    def heapify_down(self):
        idx = 1
        while self.child_present(idx):
            smaller_child_idx = self.get_smaller_child(idx)
            child = self.heap[smaller_child_idx]
            parent = self.heap[idx]
            if parent[2] > child[2]:
                self.heap[idx] = child
                self.heap[smaller_child_idx] = parent
            idx = smaller_child_idx