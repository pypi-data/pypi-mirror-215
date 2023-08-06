class Policy:
    def __init__(self, *paths):
        self.paths = paths

    def __str__(self):
        paths = ""
        for path in self.paths:
            paths += f"{path}\n\n"
        return paths.strip()


class Path:
    def __init__(self, path, rights):
        self.path = path
        self.rights = rights

    def __str__(self):
        return f"path \"{self.path}\" {{\n  capabilities = {str(self.rights)}\n}}"


class Right:
    READ = ["read"]
    LIST = ["list"]
    CREATE = ["create"]
    UPDATE = ["update"]
    PATCH = ["patch"]
    DELETE = ["delete"]

    GUEST = READ + LIST
    MAINTAINER = GUEST + CREATE + UPDATE + PATCH
    ADMIN = MAINTAINER + DELETE
