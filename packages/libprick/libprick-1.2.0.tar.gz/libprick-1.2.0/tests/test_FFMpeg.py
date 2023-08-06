import os
import unittest

from libprick import FFMpeg


class TestFFMpeg(unittest.TestCase):

    def test_ffmpeg(self):
        ffmpeg = FFMpeg()

        ffmpeg.open(os.path.join("fixtures", "example-mp4-file-small.mp4"))

        num_frames = 0
        while ffmpeg.read_frame():
            num_frames += 1

        ffmpeg.close()

        assert num_frames == 1905
