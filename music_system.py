from typing import Dict, Any, Optional, List

from music_queue.utils import utils
from queue.music_queue import MusicQueue
from queue.playback_manager import PlaybackManager


class MusicSystem:
    """
    A class that orchestrates MusicQueue, PlaybackManager, and QueueManager.
    Provides a consistent interface to the user.
    """

    def __init__(self, capacity: int = 3):
        """
        Initialize the MusicSystem.

        :param capacity: Initial queue capacity
        """
        self.music_queue = MusicQueue(capacity=capacity)
        self.playback_manager = PlaybackManager(self.music_queue)

    def add_song(self, song: Dict[str, Any]) -> None:
        """
        Add a new song to the queue.

        :param song: Song information dictionary
        """
        self.music_queue.add_song(song)

    def play_first_song(self) -> bool:
        """
        Start playing the first song in the queue.

        :return: Success status
        """
        if len(self.music_queue) == 0:
            return False
        self.playback_manager.current_index = 0
        return True

    def current_song(self) -> Optional[Dict[str, Any]]:
        """
        Return the currently playing song.

        :return: Current song or None
        """
        return self.playback_manager.current_song()

    def next_song(self) -> bool:
        """
        Move to the next song.

        :return: Success status of the operation
        """
        return self.playback_manager.play_next()

    def previous_song(self) -> bool:
        """
        Go back to the previous song.

        :return: Success status of the operation
        """
        return self.playback_manager.play_previous()

    def set_loop(self, loop_type: str, value: bool = None) -> bool:
        """
        Set the repeat playback mode.

        :param loop_type: 'single' or 'album'
        :param value: True/False or None (None toggles current state)
        :return: Loop status after setting
        """
        return self.playback_manager.set_loop(loop_type, value)

    def get_loop_status(self) -> Dict[str, bool]:
        """
        Return the repeat playback status.
        """
        return self.playback_manager.get_loop_status()

    def shuffle_queue(self) -> None:
        """
        Shuffle the queue.
        """
        shuffled = utils.shuffle_list(self.music_queue.get_all_items())
        self.music_queue = MusicQueue(items = shuffled)

    def get_current_queue(self) -> List[Dict[str, Any]]:
        """
        Return all songs in the current queue.

        :return: List of songs
        """
        return self.music_queue.get_all_items()

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        :return: True if empty, False otherwise
        """
        return self.music_queue.is_empty()

    def __getitem__(self, idx: int) -> Optional[Dict[str, Any]]:
        """
        Enable access to songs in the queue through indexing.

        :param idx: 0-based index
        :return: Song information at the specified index
        """
        return self.music_queue[idx]

    def __setitem__(self, idx: int, value: Dict[str, Any]) -> None:
        """
        Enable updating songs in the queue through indexing.

        :param idx: 0-based index
        :param value: Updated song information
        """
        self.music_queue[idx] = value

    def __len__(self) -> int:
        """
        Return the size of the queue.

        :return: Current queue size
        """
        return len(self.music_queue)

    def __bool__(self) -> bool:
        """
        Return whether the MusicSystem is empty.

        :return: True if not empty, False if empty
        """
        return len(self.music_queue) > 0
