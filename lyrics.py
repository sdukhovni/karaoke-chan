#! /usr/bin/python2

import copy
import bisect

METADATA_FIELDS = ["artist", "album", "title", "length"]

class Lyrics:
    """Data type for representing karaoke lyrics"""

    def __init__(self):
        """Create a new, empty Lyrics instance """
        self.phrases = []
        self.times = []
        self.metadata = {}

    def getMetadata(self):
        """Get a dictionary of song metadata

        Returns:
            dict. May contain some, all, or none of the following keys::
                "artist" (str): Name of the artist
                "album" (str): Name of the album
                "title" (str): Title of the song
                "length" (int): Length of the song in seconds
        """
        return copy.copy(self.metadata)

    def getPhrases(self):
        """Get the lyrics as a list of phrases

        Returns: list. A representation of the lyrics as a list of
            strings.  Each string is a separate "phrase": a substring
            of the lyrics delimited by timestamps or start/end of
            file. The phrases contain no timestamps or escape
            sequences, but may contain newlines or trailing
            spaces. All newlines will be '\n' characters.

        """
        return copy.copy(self.phrases)

    def getTimes(self):
        """Get all timing data

        Returns:
            list. A list of pairs (time, phrase), ordered by time::
                time (int): start time of a lyric in hundredths of a second
                phrase (int): index of a phrase in the list returned by
                    self.getPhrases()
        """
        return copy.copy(self.times)

    def getCurrentIndex(self, time):
        """Get the index of the current phrase of the song

        Args:
            time (int): time in hundredths of a second

        Returns:
            int. index of the phrase in self.getPhrases() that is being
            sung at time time. If there's no phrase at time time (it's before
            the vocals start), return -1.
        """
        # Search for last entry in self.times that has a time <= time
        idx = bisect.bisect(self.times, (time, len(self.phrases))) - 1

        if idx >= 0:
            return self.times[idx][1]
        else:
            # the time we were given comes before any timestamps
            return -1

    def setMetadata(self, **metadata):
        """Set the metadata for this song

        Kwargs:
            artist (str): Name of the artist
            album (str): Name of the album
            title (str): Title of the song
            length (int): Length of the song, in seconds
        Other Kwargs will be ignored.
        """
        metadata = {k: v for (k,v) in metadata.iteritems()
                    if k in METADATA_FIELDS}
        self.metadata.update(metadata)

    def addPhrase(self, phrase, times):
        """Add a phrase to this song

        Args:
            phrase (str): Phrase to append to the end of the song; may contain
                newlines and trailing spaces.
            times (list): List of integer timestamps, in hundredths of a
                second, when the phrase is to be sung. The list must not be
                empty.
        """
        phrase = '\n'.join(phrase.splitlines())
        self.phrases.append(phrase)
        for time in times:
            bisect.insort(self.times, (time, len(self.phrases)-1))
