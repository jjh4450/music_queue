from typing import Dict, Any, Optional, List

from music_queue.utils import utils
from queue.music_queue import MusicQueue
from queue.playback_manager import PlaybackManager


class MusicSystem:
    """
    MusicQueue, PlaybackManager, QueueManager를 오케스트레이션하는 클래스.
    사용자에게 일관된 인터페이스를 제공한다.
    """

    def __init__(self, capacity: int = 3):
        """
        MusicSystem을 초기화한다.

        :param capacity: 초기 큐 용량
        """
        self.music_queue = MusicQueue(capacity=capacity)
        self.playback_manager = PlaybackManager(self.music_queue)

    def add_song(self, song: Dict[str, Any]) -> None:
        """
        새 곡을 큐에 추가한다.

        :param song: 곡 정보 딕셔너리
        """
        self.music_queue.add_song(song)

    def play_first_song(self) -> bool:
        """
        첫 번째 곡을 재생 상태로 만든다.

        :return: 성공 여부
        """
        if len(self.music_queue) == 0:
            return False
        self.playback_manager.current_index = 0
        return True

    def current_song(self) -> Optional[Dict[str, Any]]:
        """
        현재 재생 중인 곡을 반환한다.

        :return: 현재 곡 또는 None
        """
        return self.playback_manager.current_song()

    def next_song(self) -> bool:
        """
        다음 곡으로 넘어간다.

        :return: 이동 성공 여부
        """
        return self.playback_manager.play_next()

    def previous_song(self) -> bool:
        """
        이전 곡으로 돌아간다.

        :return: 이동 성공 여부
        """
        return self.playback_manager.play_previous()

    def set_loop(self, loop_type: str, value: bool = None) -> bool:
        """
        반복 재생 모드를 설정한다.

        :param loop_type: 'single' 또는 'album'
        :param value: True/False 또는 None(None이면 토글)
        :return: 설정 후 반복 상태
        """
        return self.playback_manager.set_loop(loop_type, value)

    def get_loop_status(self) -> Dict[str, bool]:
        """
        반복 재생 상태를 반환한다.
        """
        return self.playback_manager.get_loop_status()

    def shuffle_queue(self) -> None:
        """
        대기열을 셔플한다.
        """
        shuffled = utils.shuffle_list(self.music_queue.get_all_items())
        self.music_queue = MusicQueue(items = shuffled)

    def get_current_queue(self) -> List[Dict[str, Any]]:
        """
        현재 큐에 담긴 곡을 모두 반환한다.

        :return: 곡 목록 리스트
        """
        return self.music_queue.get_all_items()

    def is_empty(self) -> bool:
        """
        큐가 비었는지 확인한다.

        :return: 비었으면 True, 아니면 False
        """
        return self.music_queue.is_empty()

    def __getitem__(self, idx: int) -> Optional[Dict[str, Any]]:
        """
        인덱스를 통해 대기열의 곡에 접근할 수 있게 한다.

        :param idx: 0-based 인덱스
        :return: 해당 인덱스의 곡 정보
        """
        return self.music_queue[idx]

    def __setitem__(self, idx: int, value: Dict[str, Any]) -> None:
        """
        인덱스를 통해 대기열의 곡을 업데이트할 수 있게 한다.

        :param idx: 0-based 인덱스
        :param value: 업데이트할 곡 정보
        """
        self.music_queue[idx] = value

    def __len__(self) -> int:
        """
        대기열의 크기를 반환한다.

        :return: 현재 큐 크기
        """
        return len(self.music_queue)

    def __bool__(self) -> bool:
        """
        MusicSystem이 비어있는지 여부를 반환한다.

        :return: 비어있지 않으면 True, 비어있으면 False
        """
        return len(self.music_queue) > 0
