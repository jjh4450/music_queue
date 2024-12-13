# Music Queue System

A Python-based music queue system that manages music playback, including queue management, playback control, and looping functionality.

## Features

- **Circular Queue Implementation**: Efficient queue management using a circular queue data structure.
- **Music Queue**: Specialized queue for handling music tracks.
- **Playback Manager**: Controls playback functionalities like play, pause, next, previous, and looping modes.
- **Looping Support**: Supports single track repeat and album repeat modes.
- **Shuffle Functionality**: Ability to shuffle the music queue.

## Installation

```bash
git clone https://github.com/yourusername/music_queue.git
cd music_queue
```

## Usage

- Initialize the `MusicSystem` with an optional capacity.
- Add songs to the queue by providing song dictionaries with `'title'` and `'artist'`.
- Control playback using methods like `play_first_song()`, `next_song()`, and `previous_song()`.
- Set looping modes using `set_loop('single', True)` or `set_loop('album', True)`.

## Example

```python
from music_system import MusicSystem

# Initialize Music System
music_system = MusicSystem(capacity=5)

# Add songs to the queue
music_system.add_song({'title': 'Song 1', 'artist': 'Artist A'})
music_system.add_song({'title': 'Song 2', 'artist': 'Artist B'})

# Play first song
music_system.play_first_song()

# Get current song
current = music_system.current_song()
print(f"Now playing: {current['title']} by {current['artist']}")
```

## License

This project is licensed under the MIT License.