+++
title = "Data Decryption"
weight = 18
[menu.main]
    parent = "deploy"
+++

You might need to decrypt data from an encrypted Dgraph cluster for a variety of reasons, including:

* Migration of data from an encrypted cluster to a non-encrypted cluster
* Changing your data or schema by directly editing an RDF file or schema file

To support these scenarios, Dgraph includes a `decrypt` command that decrypts encrypted RDF and schema files. To learn how to export RDF
and schema files from Dgraph, see:
[Dgraph Administration: Export database](/deploy/dgraph-administration/#exporting-database).

The `decrypt` command supports a variety of symmetric key lengths, which
determine the AES cypher used for encryption and decryption, as follows:


| Symmetric key length | AES encryption cypher |
|----------------------|-----------------------|
| 128 bits (16-bytes)  |  AES-128              |
| 192 bits (24-bytes)  |  AES-192              |
| 256 bits (32-bytes)  |  AES-256              |


The `decrypt` command also supports the use of [Hashicorp Vault](https://www.vaultproject.io/) to store secrets, including support for Vault's
[AppRole authentication](https://www.vaultproject.io/docs/auth/approle.html).

## Decryption options

The following decryption options (or *flags*) are available for the `decrypt` command:


| Flag or Superflag       | Superflag Option | Notes                                                                                         |
|-------------------------|------------------|-----------------------------------------------------------------------------------------------|
| `--encryption`          | `key-file`       | Encryption key filename                                                                       |
| `-f`, `--file`          |                  | Path to file for the encrypted RDF or schema **.gz** file                                     |
| `-h`, `--help`          |                  | Help for the decrypt command                                                                  |
| `-o`, `--out`           |                  | Path to file for the decrypted **.gz** file that decrypt creates                                  |
| `--vault`               | `addr`           | Vault server address, in **http://&lt;*ip-address*&gt;:&lt;*port*&gt;** format (default: `http://localhost:8200` ) |
|                         | `enc-field`      | Name of the Vault server's key/value store field that holds the Base64 encryption key         |
|                         | `enc-format`     | Vault server field format; can be `raw` or `base64` (default: `base64`)                           |
|                         | `path`           | Vault server key/value store path (default: `secret/data/dgraph`)                             |
|                         | `role-id-file`   | File containing the [Vault](https://www.vaultproject.io/) `role_id` used for AppRole authentication                             |
|                         | `secret-id-file` | File containing the [Vault](https://www.vaultproject.io/) `secret_id` used for AppRole authentication                           |

To learn more about the `--vault` superflag and its options that have replaced the `--vault_*` options in release v20.11 and earlier, see
[Dgraph CLI Command Reference]({{< relref "deploy/cli-command-reference.md" >}}).

## Data decryption examples 

For example, you could use the following command with an encrypted RDF file
(**encrypted.rdf.gz**) and an encryption key file (**enc_key_file**), to
create a decrypted RDF file:

```bash
# Encryption Key from the file path
dgraph decrypt --file "encrypted.rdf.gz" --out "decrypted_rdf.gz" --encryption key-file="enc-key-file"

# Encryption Key from HashiCorp Vault
dgraph decrypt --file "encrypted.rdf.gz" --out "decrypted_rdf.gz" \
  --vault addr="http://localhost:8200";enc-field="enc_key";enc-format="raw";path="secret/data/dgraph/alpha";role-id-file="./role_id";secret-id-file="./secret_id"
```

You can use similar syntax to create a decrypted schema file:

```bash
# Encryption Key from the file path
dgraph decrypt --file "encrypted.schema.gz" --out "decrypted_schema.gz" --encryption key-file="enc-key-file"

# Encryption Key from HashiCorp Vault
dgraph decrypt --file "encrypted.schema.gz" --out "decrypted_schema.gz" \
  --vault addr="http://localhost:8200";enc-field="enc_key";enc-format="raw";path="secret/data/dgraph/alpha";role-id-file="./role_id";secret-id-file="./secret_id"
```
