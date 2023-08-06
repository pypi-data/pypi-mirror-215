
import unittest

from gungnir.project import Project

class TestProject(unittest.TestCase):
    def test_version(self):
        project = Project("test", version="1")
        self.assertEqual(project.name, "test")
        self.assertEqual(project.version, "1")
        self.assertEqual(project.full_version, "1")

        project.parent = Project("parent", version="ABC")
        self.assertEqual(project.full_version, "1-parent")



