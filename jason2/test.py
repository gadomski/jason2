from jason2.project import Project


def test_project2_constructor():
    project = Project(".", ["gdr"], [195])
    assert project.data_directory == "."
    assert project.products == ["gdr"]
