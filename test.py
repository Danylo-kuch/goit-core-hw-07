class Duplicate_Song(ValueError):
    def __init__(self):
        super().__init__("This song is already in your playlist!")


class Song:
    def __init__(self, title: str, artist: str, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration

    def __str__(self):
        return f"{self.title} by {self.artist}, duration: {self.duration}"
    
    def __repr__(self):
        return f"{self.title} by {self.artist}, duration: {self.duration}"

class Playlist:
    def __init__(self, title: str, songs: list = []):
        self.title = title
        self.songs = songs
        self.index = 0

    def add_song(self, song: Song):
        if song in self.songs:
            raise Duplicate_Song()
        self.songs.append(song)

    def __iter__(self):
        return self

    def __next__(self):
        if 

    def __str__(self):
        return f"Playlist: {self.title}: {self.songs}"
    
    def __repr__(self):
        return f"Playlist: {self.title}: {self.songs}"


    

song = Song("Song One", "Bee Jone", 300)
print(song)


playlist_one = Playlist("Classics")
playlist_one.add_song(song)
print(playlist_one)

