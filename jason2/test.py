from jason2.project import Project


class TestProject:

    def test_constructor(self):
        project = Project(".")
        assert project.data_directory == "."
