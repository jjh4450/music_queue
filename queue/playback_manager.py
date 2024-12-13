from typing import Dict, Any, Optional


class PlaybackManager:
    """
    Playback management class. Manages current playing song index and repeat settings.
    """

    def __init__(self, music_queue):
        """
        Initialize PlaybackManager.

        :param music_queue: MusicQueue instance
        """
        self.music_queue = music_queue
        self.loop: Dict[str, bool] = {"single": False, "album": True}

    def current_song(self) -> Optional[Dict[str, Any]]:
        """
        Returns the currently playing song.

        :return: Current song info or None
        """
        return self.music_queue[0] if not self.music_queue.is_empty() else None

    def next_song(self) -> Optional[Dict[str, Any]]:
        """
        Returns the next song information.

        :return: Next song info or None
        """
        return self.music_queue[1] if len(self.music_queue) > 1 else None

    def previous_song(self) -> Optional[Dict[str, Any]]:
        """
        Returns the previous song information.

        :return: Previous song info or None
        """
        if len(self.music_queue) < 2:
            return None

        # Returns the last element of the queue
        return self.music_queue[-1]

    def play_next(self) -> bool:
        """
        Moves to the next song from the current song.

        :return: Success status of the operation
        """
        if self.music_queue.is_empty():
            return False

        if self.loop['single']:
            return True

        if self.loop['album']:
            # Move the first element to the end of queue
            self.music_queue.enqueue(self.music_queue.dequeue())
            return True

        # In non-loop mode, remove the first element
        self.music_queue.dequeue()
        return True

    def play_previous(self) -> bool:
        """
        Moves to the previous song from the current song.

        :return: Success status of the operation
        """
        if self.music_queue.is_empty():
            return False

        # Move the last element to the front of queue
        self.music_queue.enqueue(self.music_queue.dequeue())
        return True

    def set_loop(self, loop_type: str, value: bool = None) -> bool:
        """
        Changes the repeat playback settings.

        :param loop_type: 'single' or 'album'
        :param value: Value to set (True/False), toggles if None
        :return: The set loop status
        :raises ValueError: If loop_type is invalid
        """
        if loop_type not in self.loop:
            raise ValueError(f"Invalid loop type: {loop_type}")
        if value is not None:
            self.loop[loop_type] = value
        else:
            self.loop[loop_type] = not self.loop[loop_type]
        return self.loop[loop_type]

    def get_loop_status(self) -> Dict[str, bool]:
        """
        Returns the current repeat playback settings.

        :return: {'single': bool, 'album': bool}
        """
        return self.loop.copy()