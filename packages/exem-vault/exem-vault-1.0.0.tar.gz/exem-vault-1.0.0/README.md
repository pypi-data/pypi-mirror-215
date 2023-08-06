# Vault

This project provides a simple, object-oriented Python API for interacting with an HashiCorp's Vault 
using the hvac library.

## How to

### Usage
#### Init

Init the vault api with:

```
vault = Vault("your.token")
```

By default the vault access is set to the local vault server.

If the vault is distant you can specify the url with:

```
vault = Vault("your.token", "http://your.vault.url:port")
```

#### Token

You can create a token with:

```
vault.create_token("token_name", "policy_name")
```

#### Interact

You can interact with the vault with the following methods:

```
vault.read("engine_mount_path", "data_path")
vault.write("engine_mount_path", "data_path", {"key": "value"})
vault.delete("engine_mount_path", "data_path", "key_to_delete")
```


#### Policies

You can create a policy with:

```
path_guest = Path("/path/to/secret", Right.GUEST)
path_write = Path("/path/to/other_secret", Right.WRITE)

policy = Policy(path_guest, path_write)
```

And add it to the vault with:

```
vault.add_policy("your_policy_name", policy)
```
