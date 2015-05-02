from jason2.project import Project


class TestProject:

    def test_constructor(self):
        project = Project(".", ["gdr"])
        assert project.data_directory == "."
        assert project.products == ["gdr"]
