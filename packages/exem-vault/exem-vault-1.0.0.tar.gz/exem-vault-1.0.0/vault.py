import hvac


class Vault:

    @staticmethod
    def unseal(host="http://localhost:8200", keys=None):
        client = hvac.Client(url=host)
        if isinstance(keys, list):
            for key in keys:
                client.sys.submit_unseal_key(key)
        else:
            raise TypeError(f"keys must be a list but is {type(keys)}")
        return not client.sys.is_sealed()

    def __init__(self, token, host="http://localhost:8200"):
        self.token = token
        self.client = hvac.Client(url=host, token=token, timeout=120)

    def read(self, mount_point, path):
        return self.client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount_point)["data"]["data"]

    def write(self, mount_point, path, data):
        return self.client.secrets.kv.v2.patch(mount_point, path, data)

    def delete(self, mount_point, path, key):
        data = self.read(mount_point, path).pop(key)
        return self.client.secrets.kv.v2.create_or_update_secret(mount_point, path, data)

    def create_token(self, display_name, *policies_names):
        return self.client.auth.token.create(policies=policies_names, ttl="3650d", display_name=display_name)

    def add_policy(self, name, policy):
        return self.client.sys.create_or_update_policy(name, policy)

    def get_policy(self, name):
        return self.client.get_policy(name)
