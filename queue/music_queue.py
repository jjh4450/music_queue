from typing import Dict, Any, Optional, List, overload
from .circular_queue import CircularQueue


class MusicQueue(CircularQueue[Dict[str, Any]]):
    """
    음악 정보를 담은 원형 큐를 상속받아 관리하는 클래스.
    """

    def __init__(self, capacity: Optional[int] = None, items: Optional[List[Any]] = None):
        """
        MusicQueue를 초기화합니다.

        :param capacity: 초기 용량
        """
        super().__init__(capacity, items)

    def add_song(self, song: Dict[str, Any]) -> None:
        """
        새로운 곡을 큐에 추가합니다.

        :param song: {'title': str, 'artist': str} 형태의 곡 정보
        """
        self._validate_song_dict(song)
        self.enqueue(song)

    def __iadd__(self, song: Dict[str, Any]) -> None:
        self.add_song(song)

    def update_song(self, idx: int, value: Dict[str, Any]) -> None:
        """
        특정 인덱스의 곡 정보를 업데이트합니다.

        :param idx: 0-based 인덱스
        :param value: 업데이트할 곡 정보
        """
        self._validate_song_dict(value)
        self[idx] = value

    def __setitem__(self, idx: int, value: Dict[str, Any]) -> None:
        self.update_song(idx, value)

    @staticmethod
    def _validate_song_dict(song: Dict[str, Any]) -> None:
        """
        곡 정보가 필요한 필드를 갖췄는지 검증합니다.

        :param song: 곡 정보 딕셔너리
        :raises ValueError: title 또는 artist가 없을 경우
        """
        if 'title' not in song or 'artist' not in song:
            raise ValueError("곡 정보는 'title'과 'artist'를 포함해야 합니다.")