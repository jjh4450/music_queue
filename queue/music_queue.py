from typing import Dict, Any, Optional, List, overload
from .circular_queue import CircularQueue


class MusicQueue(CircularQueue[Dict[str, Any]]):
    """
    A class that manages a circular queue containing music information.
    """

    def __init__(self, capacity: Optional[int] = None, items: Optional[List[Any]] = None):
        """
        Initialize MusicQueue.

        :param capacity: Initial capacity
        """
        super().__init__(capacity, items)

    def add_song(self, song: Dict[str, Any]) -> None:
        """
        Add a new song to the queue.

        :param song: Song information in the format {'title': str, 'artist': str}
        """
        self._validate_song_dict(song)
        self.enqueue(song)

    def __iadd__(self, song: Dict[str, Any]) -> None:
        self.add_song(song)

    def update_song(self, idx: int, value: Dict[str, Any]) -> None:
        """
        Update song information at a specific index.

        :param idx: 0-based index
        :param value: Updated song information
        """
        self._validate_song_dict(value)
        self[idx] = value

    def __setitem__(self, idx: int, value: Dict[str, Any]) -> None:
        self.update_song(idx, value)

    @staticmethod
    def _validate_song_dict(song: Dict[str, Any]) -> None:
        """
        Validate if the song information contains the required fields.

        :param song: Song information dictionary
        :raises ValueError: If title or artist is missing
        """
        if 'title' not in song or 'artist' not in song:
            raise ValueError("Song information must include 'title' and 'artist'")