"""A video player class."""
import random

from .video_library import VideoLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playing = False
        self._pause = False
        self._playlist = []
        self._flagged = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        print("Here's a list of all available videos: ")
        video = self._video_library.get_all_videos()
        video.sort(key=lambda vid: vid.title, reverse=False)
        for i in video:
            tags = str(i.tags)
            tags2 = tags.replace("'", "")
            tags3 = tags2.replace("(", "[")
            tags4 = tags3.replace(")", "]")
            finaltag = tags4.replace(",", "")
            if (i.video_id in self._flagged):
                print(f"\t{i.title} ({i.video_id}) {finaltag} - FLAGGED (reason: {self._flagged[i.video_id]})")
            else:
                print(f"\t{i.title} ({i.video_id}) {finaltag}")

    def play_video(self, video_id):
        if (video_id in self._flagged):
            print("Cannot play video: Video is currently flagged (reason: " + self._flagged[video_id] + ")")
            return
        if (self._video_library.get_video(video_id) != None):
            if (self._playing != False):
                self.stop_video()
            self._playing = self._video_library.get_video(video_id)
            print(f"Playing video: {self._playing.title}")
        else:
            print("Cannot play video: Video does not exist")
        self._pause = False

    def stop_video(self):
        if self._playing != False:
            print(f"Stopping video: {self._playing.title}")
            self._playing = False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        video = self._video_library.get_all_videos()
        if (len(video) == len(self._flagged)):
            print("No videos available")
            return
        if (self._playing != False):
            print("Stopping video: " + str(self._playing.title))
            self._playing = False

        while True:
            num = random.randint(0, len(video) - len(self._flagged))
            if not (video[num].video_id in self._flagged):
                print("Playing video: " + video[num].title)
                break

        self._pause = False

    def pause_video(self):
        if (self._playing == False):
            print("Cannot pause video: No video is currently playing")

        else:
            if (self._pause == False):
                print("Pausing video: " + str(self._playing.title))
                self._pause = True
            else:
                print("Video already paused: " + str(self._playing.title))

    def continue_video(self):
        if (self._playing == False):
            print("Cannot continue video: No video is currently playing")

        elif (self._pause == False):
            print("Cannot continue video: Video is not paused")

        elif (self._pause == True and self._playing != False):
            print("Continuing video: " + str(self._playing.title))
            self._pause = False

    def show_playing(self):
        if (self._playing == False):
            print("No video is currently playing")

        else:
            title = str(self._video_library.get_video(self._playing.video_id).title)
            id = str(self._video_library.get_video(self._playing.video_id).video_id)
            tags = str(self._video_library.get_video(self._playing.video_id).tags)
            tags2 = tags.replace("'", "")
            tags3 = tags2.replace("(", "[")
            tags4 = tags3.replace(")", "]")
            finaltag = tags4.replace(",", "")
            paused = ""
            if (self._pause == True):
                paused = " - PAUSED"
            print("Currently playing: " + title + " (" + id + ") " + finaltag + paused)

    def create_playlist(self, playlist_name):
        for i in range(len(self._playlist)):
            if (playlist_name.upper() == self._playlist[i][0].upper()):
                print("Cannot create playlist: A playlist with the same name already exists")
                return
        print("Successfully created new playlist: " + playlist_name)
        self._playlist.append([playlist_name])

    def add_to_playlist(self, playlist_name, video_id):
        if (video_id in self._flagged):
            print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + self._flagged[
                video_id] + ")")
            return
        for i in range(len(self._playlist)):
            if (playlist_name.upper() == self._playlist[i][0].upper()):
                if (self._video_library.get_video(video_id) == None):
                    print("Cannot add video to " + playlist_name + ": Video does not exist")
                    return
                else:
                    nested = self._playlist[i]
                    for j in range(len(nested)):
                        if (video_id.upper() == nested[j].upper()):
                            print("Cannot add video to " + playlist_name + ": Video already added")
                            return
                    print("Added video to " + playlist_name + ": " + str(self._video_library.get_video(video_id).title))
                    nested.append(video_id)
                    return

        print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        if (len(self._playlist) == 0):
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        self._playlist.sort()
        for i in range(len(self._playlist)):
            print(str(self._playlist[i][0]))

    def show_playlist(self, playlist_name):
        for i in range(len(self._playlist)):
            if (playlist_name.upper() == self._playlist[i][0].upper()):
                print("Showing playlist: " + playlist_name)
                nested = self._playlist[i]
                if (len(nested) == 1):
                    print("\tNo videos here yet")
                    return
                for j in range(len(nested)):
                    if j == 0:
                        continue
                    i = self._video_library.get_video(nested[j])
                    tags = str(i.tags)
                    tags2 = tags.replace("'", "")
                    tags3 = tags2.replace("(", "[")
                    tags4 = tags3.replace(")", "]")
                    finaltag = tags4.replace(",", "")
                    if (i.video_id in self._flagged):
                        print(f"\t{i.title} ({i.video_id}) {finaltag} - FLAGGED (reason: {self._flagged[i.video_id]})")
                    else:
                        print(f"\t{i.title} ({i.video_id}) {finaltag}")
                return

        print("Cannot show playlist " + playlist_name + ": Playlist does not exists")

    def remove_from_playlist(self, playlist_name, video_id):

        for i in range(len(self._playlist)):
            if (playlist_name.upper() == self._playlist[i][0].upper()):
                if (self._video_library.get_video(video_id) == None):
                    print("Cannot remove video from " + playlist_name + ": Video does not exist")
                    return
                nested = self._playlist[i]
                for j in range(len(nested)):
                    if (nested[j].upper() == video_id.upper()):
                        print("Removed video from " + playlist_name + ": " + str(
                            self._video_library.get_video(nested[j]).title))
                        nested.remove(video_id)
                        return

                print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
                return

        print("Cannot remove video from " + playlist_name + ": Playlist does not exists")

    def clear_playlist(self, playlist_name):
        for i in range(len(self._playlist)):
            if (playlist_name.upper() == self._playlist[i][0].upper()):
                nested = self._playlist[i]
                for j in range(len(nested)):
                    if j == 0:
                        continue
                    del nested[j]
                print("Successfully removed all videos from " + playlist_name)
                return
        print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        for i in range(len(self._playlist)):
            if (playlist_name.upper() == self._playlist[i][0].upper()):
                nested = self._playlist[i]
                for j in range(len(nested)):
                    if j == 0:
                        continue
                    del nested[j]
                del self._playlist[i]
                print("Deleted playlist: " + playlist_name)
                return
        print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        video = self._video_library.get_all_videos()
        video.sort(key=lambda vid: vid.title, reverse=False)
        count = 0
        vid_search = []
        for i in video:
            if (search_term.upper() in i.title.upper()):
                if (i.video_id in self._flagged):
                    continue
                if (count == 0):
                    print("Here are the results for " + search_term + ":")
                count += 1
                tags = str(i.tags)
                tags2 = tags.replace("'", "")
                tags3 = tags2.replace("(", "[")
                tags4 = tags3.replace(")", "]")
                finaltag = tags4.replace(",", "")
                print(f"{count}) {i.title} ({i.video_id}) {finaltag}")
                vid_search.append(i)

        if (count == 0):
            print("No search results for " + search_term)
            return

        try:
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            inp = int(input())
            if (inp > 0 and inp < count + 1):
                self.play_video(vid_search[inp - 1].video_id)
        except:
            return

    def search_videos_tag(self, video_tag):
        video = self._video_library.get_all_videos()
        video.sort(key=lambda vid: vid.title, reverse=False)
        count = 0
        vid_search = []
        for i in video:
            if ("#" not in video_tag):
                break
            for j in i.tags:
                if (video_tag.upper() in j.upper()):
                    if (i.video_id in self._flagged):
                        continue
                    if (count == 0):
                        print("Here are the results for " + video_tag + ":")
                    count += 1
                    tags = str(i.tags)
                    tags2 = tags.replace("'", "")
                    tags3 = tags2.replace("(", "[")
                    tags4 = tags3.replace(")", "]")
                    finaltag = tags4.replace(",", "")
                    print(f"{count}) {i.title} ({i.video_id}) {finaltag}")
                    vid_search.append(i)

        if (count == 0):
            print("No search results for " + video_tag)
            return

        try:
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            inp = int(input())
            if (inp > 0 and inp < count + 1):
                self.play_video(vid_search[inp - 1].video_id)
        except:
            return

    def flag_video(self, video_id, flag_reason=""):
        if (self._video_library.get_video(video_id) == None):
            print("Cannot flag video: Video does not exist")
            return

        if (self._playing != False and self._playing.video_id == video_id):
            self.stop_video()
        for i in self._flagged:
            if (i == video_id):
                print("Cannot flag video: Video is already flagged")
                return

        if (flag_reason == ""):
            self._flagged[video_id] = "Not supplied"
        else:
            self._flagged[video_id] = flag_reason
        print("Successfully flagged video: " + str(self._video_library.get_video(video_id).title) + " (reason: " +
              self._flagged[video_id] + ")")

    def allow_video(self, video_id):
        if (self._video_library.get_video(video_id) == None):
            print("Cannot remove flag from video: Video does not exist")
            return

        if (video_id in self._flagged):
            self._flagged.pop(video_id)
            print("Successfully removed flag from video: " + str(self._video_library.get_video(video_id).title))
            return

        print("Cannot remove flag from video: Video is not flagged")
