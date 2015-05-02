from jason2.project import Project
from jason2.ftp import jason2_glob


def test_project2_constructor():
    project = Project(".", ["gdr"], [195])
    assert project.data_directory == "."
    assert project.products == ["gdr"]

def test_jason2_glob():
    assert "JA2_GPN_2PdP012_034_*.nc" == jason2_glob("gdr_d", 12, 34)
    assert "JA2_GPS_2PdP056_078_*.zip" == jason2_glob("sgdr_d", 56, 78)
