from jason2.project import Project


def test_constructor():
    Project(data_directory=".",
            email="me@example.com",
            products=[],
            passes=[]
            )
