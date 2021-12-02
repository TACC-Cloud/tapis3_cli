import docker as dockerpy


class DockerPy:
    dockerpy = None

    def docker_client_from_env(self):
        setattr(self, "dockerpy", dockerpy.from_env())
