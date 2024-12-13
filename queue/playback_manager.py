from typing import Dict, Any, Optional


class PlaybackManager:
    """
    재생 관리 클래스. 현재 재생 곡 인덱스와 반복 설정을 관리합니다.
    """

    def __init__(self, music_queue):
        """
        PlaybackManager를 초기화합니다.

        :param music_queue: MusicQueue 인스턴스
        """
        self.music_queue = music_queue
        self.loop: Dict[str, bool] = {"single": False, "album": True}

    def current_song(self) -> Optional[Dict[str, Any]]:
        """
        현재 재생 중인 곡을 반환합니다.

        :return: 현재 곡 정보 또는 None
        """
        return self.music_queue[0] if not self.music_queue.is_empty() else None

    def next_song(self) -> Optional[Dict[str, Any]]:
        """
        다음 곡 정보를 반환합니다.

        :return: 다음 곡 정보 또는 None
        """
        return self.music_queue[1] if len(self.music_queue) > 1 else None

    def previous_song(self) -> Optional[Dict[str, Any]]:
        """
        이전 곡 정보를 반환합니다.

        :return: 이전 곡 정보 또는 None
        """
        if len(self.music_queue) < 2:
            return None

        # 큐의 마지막 요소를 돌려줍니다
        return self.music_queue[-1]

    def play_next(self) -> bool:
        """
        현재 곡을 다음 곡으로 이동합니다.

        :return: 이동 성공 여부
        """
        if self.music_queue.is_empty():
            return False

        if self.loop['single']:
            return True

        if self.loop['album']:
            # 첫 번째 요소를 큐의 끝으로 이동
            self.music_queue.enqueue(self.music_queue.dequeue())
            return True

        # 비순환 모드에서는 첫 번째 요소를 제거
        self.music_queue.dequeue()
        return True

    def play_previous(self) -> bool:
        """
        현재 곡을 이전 곡으로 이동합니다.

        :return: 이동 성공 여부
        """
        if self.music_queue.is_empty():
            return False

        # 마지막 요소를 큐의 맨 앞으로 이동
        self.music_queue.enqueue(self.music_queue.dequeue())
        return True

    def set_loop(self, loop_type: str, value: bool = None) -> bool:
        """
        반복 재생 설정을 변경합니다.

        :param loop_type: 'single' 또는 'album'
        :param value: True/False로 설정할 값, None이면 토글
        :return: 설정된 반복 상태
        :raises ValueError: 잘못된 loop_type일 경우
        """
        if loop_type not in self.loop:
            raise ValueError(f"잘못된 반복 유형입니다: {loop_type}")
        if value is not None:
            self.loop[loop_type] = value
        else:
            self.loop[loop_type] = not self.loop[loop_type]
        return self.loop[loop_type]

    def get_loop_status(self) -> Dict[str, bool]:
        """
        현재 반복 재생 설정 상태를 반환합니다.

        :return: {'single': bool, 'album': bool}
        """
        return self.loop.copy()