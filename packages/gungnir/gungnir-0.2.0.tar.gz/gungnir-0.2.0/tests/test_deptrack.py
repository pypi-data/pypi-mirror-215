
import unittest

from gungnir.dependencytrack import Project


class TestDepTrack(unittest.TestCase):
    def test_version_check(self):
        project = Project("test")


