from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class CircularQueue(Generic[T]):
    """
    Circular Queue implementation class.
    """

    def __init__(self, capacity: Optional[int] = None, items: Optional[List[T]] = None):
        """
        Initialize the queue.

        :param capacity: Maximum capacity of the queue (used when items is None)
        :param items: Initial queue elements (optional)
        :raises ValueError: When both items and capacity are None
        """
        if items is not None:
            self.capacity = len(items)
            self._queue: List[Optional[T]] = [None] * self.capacity

            self._queue[:len(items)] = items

            self.front = 0
            self.rear = len(items) - 1
            self.size = len(items)

        elif capacity is not None:
            self.capacity = capacity
            self._queue: List[Optional[T]] = [None] * capacity

            self.front = -1
            self.rear = -1
            self.size = 0

        else:
            raise ValueError("Either items or capacity must be specified.")

    def is_full(self) -> bool:
        """
        Check if the queue is full.

        :return: True if full, False otherwise
        """
        return self.size == self.capacity

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        :return: True if empty, False otherwise
        """
        return self.size == 0

    def _resize(self) -> None:
        """
        Double the queue capacity and copy existing elements.
        """
        new_capacity = self.capacity * 2
        new_queue = [None] * new_capacity

        for i in range(self.size):
            new_queue[i] = self._queue[(self.front + i) % self.capacity]

        self._queue = new_queue
        self.capacity = new_capacity
        self.front = 0
        self.rear = self.size - 1

    def enqueue(self, item: T) -> None:
        """
        Insert an item into the queue. Automatically resizes if necessary.

        :param item: Item to insert
        """
        if self.is_full():
            self._resize()
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self._queue[self.rear] = item
        self.size += 1

    def dequeue(self) -> Optional[T]:
        """
        Remove and return an item from the queue.

        :return: Removed item, None if queue is empty
        """
        if self.is_empty():
            return None
        item = self._queue[self.front]
        self._queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        if self.size == 0:
            self.front = -1
            self.rear = -1
        return item

    def get_item(self, idx: int) -> Optional[T]:
        """
        Return item at specific index in the queue.

        :param idx: 0-based index
        :return: Item at the index, None if out of range
        """
        if idx < 0 or idx >= self.size:
            return None
        return self._queue[(self.front + idx) % self.capacity]

    def __len__(self) -> int:
        """
        Return the current size of the queue.
        """
        return self.size

    def __iter__(self):
        """
        Provide iterator for queue traversal.
        """
        idx = self.front
        for _ in range(self.size):
            yield self._queue[idx]
            idx = (idx + 1) % self.capacity

    def __getitem__(self, idx: int) -> Optional[T]:
        """
        Allow access to items through queue indexing.

        :param idx: 0-based index
        :return: Item at the index
        """
        return self.get_item(idx)

    def __setitem__(self, idx: int, value: T) -> None:
        """
        Set item at specific index.

        :param idx: 0-based index
        :param value: Value to set
        """
        if idx < 0 or idx >= self.size:
            raise IndexError("Queue index out of range")
        real_idx = (self.front + idx) % self.capacity
        self._queue[real_idx] = value

    def __delitem__(self, idx: int) -> None:
        """
        Delete item at specific index and rearrange the queue.

        :param idx: 0-based index
        """
        if idx < 0 or idx >= self.size:
            raise IndexError("Queue index out of range")

        new_queue = [None] * self.capacity
        new_size = 0
        new_rear = -1

        for i in range(self.size):
            if i == idx:
                continue
            new_rear = (new_rear + 1) % self.capacity
            new_queue[new_rear] = self._queue[(self.front + i) % self.capacity]
            new_size += 1

        self._queue = new_queue
        self.size = new_size
        self.front = 0 if new_size > 0 else -1
        self.rear = new_rear if new_size > 0 else -1

    def __contains__(self, item: T) -> bool:
        return item in self._queue

    def __bool__(self) -> bool:
        """
        Return whether MusicSystem is empty.

        :return: True if not empty, False if empty
        """
        return self.size > 0

    def clear(self) -> None:
        """
        Initialize the queue.
        """
        self._queue = [None] * self.capacity
        self.front = -1
        self.rear = -1
        self.size = 0

    def get_all_items(self) -> List[Optional[T]]:
        """
        Return all items in the queue as a list.

        :return: List of items
        """
        return [self.get_item(i) for i in range(self.size)]
