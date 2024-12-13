from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class CircularQueue(Generic[T]):
    """
    원형 큐 구현 클래스.
    """

    def __init__(self, capacity: Optional[int] = None, items: Optional[List[T]] = None):
        """
        큐를 초기화합니다.

        :param capacity: 큐의 최대 용량 (items가 없을 때 사용)
        :param items: 초기 큐의 요소들 (옵션)
        :raises ValueError: items와 capacity가 모두 None인 경우
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
            raise ValueError("items 또는 capacity 중 하나는 반드시 지정해야 합니다.")

    def is_full(self) -> bool:
        """
        큐가 가득 차 있는지 확인합니다.

        :return: 가득 차 있으면 True, 아니면 False
        """
        return self.size == self.capacity

    def is_empty(self) -> bool:
        """
        큐가 비어있는지 확인합니다.

        :return: 비어있으면 True, 아니면 False
        """
        return self.size == 0

    def _resize(self) -> None:
        """
        큐의 용량을 두 배로 늘리고 기존 요소를 복사합니다.
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
        큐에 아이템을 삽입합니다. 필요하다면 자동으로 큐를 리사이징합니다.

        :param item: 삽입할 아이템
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
        큐에서 아이템을 제거하고 반환합니다.

        :return: 제거된 아이템, 큐가 비었으면 None
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
        큐에서 특정 인덱스의 아이템을 반환합니다.

        :param idx: 0-based 인덱스
        :return: 해당 인덱스의 아이템, 범위를 벗어나면 None
        """
        if idx < 0 or idx >= self.size:
            return None
        return self._queue[(self.front + idx) % self.capacity]

    def __len__(self) -> int:
        """
        큐의 현재 크기를 반환합니다.
        """
        return self.size

    def __iter__(self):
        """
        큐를 순회할 수 있는 이터레이터를 제공합니다.
        """
        idx = self.front
        for _ in range(self.size):
            yield self._queue[idx]
            idx = (idx + 1) % self.capacity

    def __getitem__(self, idx: int) -> Optional[T]:
        """
        큐의 인덱스를 통해 아이템에 접근할 수 있게 합니다.

        :param idx: 0-based 인덱스
        :return: 해당 인덱스의 아이템
        """
        return self.get_item(idx)

    def __setitem__(self, idx: int, value: T) -> None:
        """
        특정 인덱스의 아이템을 설정합니다.

        :param idx: 0-based 인덱스
        :param value: 설정할 값
        """
        if idx < 0 or idx >= self.size:
            raise IndexError("큐 인덱스가 범위를 벗어났습니다")
        real_idx = (self.front + idx) % self.capacity
        self._queue[real_idx] = value

    def __delitem__(self, idx: int) -> None:
        """
        특정 인덱스의 아이템을 삭제하고, 큐를 재배치합니다.

        :param idx: 0-based 인덱스
        """
        if idx < 0 or idx >= self.size:
            raise IndexError("큐 인덱스가 범위를 벗어났습니다")

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
        MusicSystem이 비어있는지 여부를 반환한다.

        :return: 비어있지 않으면 True, 비어있으면 False
        """
        return self.size > 0

    def clear(self) -> None:
        """
        큐를 초기화합니다.
        """
        self._queue = [None] * self.capacity
        self.front = -1
        self.rear = -1
        self.size = 0

    def get_all_items(self) -> List[Optional[T]]:
        """
        큐의 모든 아이템을 리스트로 반환합니다.

        :return: 아이템 리스트
        """
        return [self.get_item(i) for i in range(self.size)]
