import cabina


class Config(cabina.Config):
    class GitLab(cabina.Section):
        URL: str = "http://localhost:8080"

    class PyPi(cabina.Section):
        URL: str = "http://localhost:8080/simple"
