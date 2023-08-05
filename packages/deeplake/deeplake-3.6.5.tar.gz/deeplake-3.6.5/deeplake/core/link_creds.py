import json
from typing import Optional
import warnings
from deeplake.constants import ALL_CLOUD_PREFIXES
from deeplake.core.storage.deeplake_memory_object import DeepLakeMemoryObject
from deeplake.core.storage import StorageProvider, storage_factory
from deeplake.core.storage.s3 import S3Provider
from deeplake.util.exceptions import (
    ManagedCredentialsNotFoundError,
    MissingCredsError,
    MissingManagedCredsError,
)
from deeplake.util.token import expires_in_to_expires_at, is_expired_token
from deeplake.client.log import logger
from datetime import datetime, timezone


def _is_expired_creds(creds: dict) -> bool:
    if "expiration" not in creds:
        return False

    return creds["expiration"] < datetime.now(timezone.utc).timestamp()


class LinkCreds(DeepLakeMemoryObject):
    def __init__(self):
        self.creds_keys = []
        self.creds_dict = {}  # keys to actual creds dictionary
        self.creds_mapping = {}  # keys to numbers, for encoding
        self.managed_creds_keys = set()  # keys which are managed
        self.used_creds_keys = set()  # keys which are used by one or more samples
        self.storage_providers = {}
        self.default_s3_provider = None
        self.default_gcs_provider = None
        self.default_azure_provider = None
        self.client = None
        self.org_id = None

    def get_creds(self, key: Optional[str]):
        if key is None:
            return {}
        if key not in self.creds_keys:
            raise MissingCredsError(f"Creds key {key} does not exist")
        if key not in self.creds_dict:
            if key not in self.managed_creds_keys:
                raise MissingCredsError(
                    f"Creds key {key} hasn't been populated. Populate it using ds.populate_creds()"
                )
            else:
                raise MissingManagedCredsError(
                    f"Managed creds key {key} hasn't been fetched."
                )
        if (
            self.client is not None
            and key in self.managed_creds_keys
            and (
                is_expired_token(self.creds_dict[key])
                or _is_expired_creds(self.creds_dict[key])
            )
        ):
            self.refresh_managed_creds(key)  # type: ignore
        return self.creds_dict[key]

    def refresh_managed_creds(self, creds_key: str):
        if creds_key not in self.managed_creds_keys:
            return False
        creds = self.fetch_managed_creds(creds_key)
        self.populate_creds(creds_key, creds)
        return True

    def get_default_provider(self, provider_type: str):
        if provider_type == "s3":
            if self.default_s3_provider is None:
                self.default_s3_provider = storage_factory(
                    S3Provider, "s3://bucket/path"
                )
            return self.default_s3_provider
        elif provider_type == "gcs":
            if self.default_gcs_provider is None:
                from deeplake.core.storage.gcs import GCSProvider

                self.default_gcs_provider = storage_factory(
                    GCSProvider, "gcs://bucket/path"
                )
            return self.default_gcs_provider
        elif provider_type == "azure":
            if self.default_azure_provider is None:
                from deeplake.core.storage.azure import AzureProvider

                self.default_azure_provider = storage_factory(
                    AzureProvider, "az://account/container"
                )
            return self.default_azure_provider

    def get_storage_provider(self, key: Optional[str], provider_type: str):
        assert provider_type in {"s3", "gcs", "azure"}
        if key is None:
            return self.get_default_provider(provider_type)

        provider: StorageProvider
        creds = self.get_creds(key)

        if provider_type == "s3":
            if key in self.storage_providers:
                provider = self.storage_providers[key]
                if isinstance(provider, S3Provider):
                    return provider

            provider = storage_factory(S3Provider, "s3://bucket/path", **creds)
        elif provider_type == "gcs":
            from deeplake.core.storage.gcs import GCSProvider

            if key in self.storage_providers:
                provider = self.storage_providers[key]
                if isinstance(provider, GCSProvider):
                    return provider

            provider = storage_factory(GCSProvider, "gcs://bucket/path", **creds)
        elif provider_type == "azure":
            from deeplake.core.storage.azure import AzureProvider

            if key in self.storage_providers:
                provider = self.storage_providers[key]
                if isinstance(provider, AzureProvider):
                    return provider

            provider = storage_factory(
                AzureProvider, "az://account/container", creds=creds
            )
        self.storage_providers[key] = provider
        return provider

    def add_creds_key(self, creds_key: str, managed: bool = False):
        if creds_key in self.creds_keys:
            raise ValueError(f"Creds key {creds_key} already exists")
        if managed:
            creds = self.fetch_managed_creds(creds_key)
        self.creds_keys.append(creds_key)
        self.creds_mapping[creds_key] = len(self.creds_keys)
        if managed:
            self.managed_creds_keys.add(creds_key)
            self.populate_creds(creds_key, creds)

    def _replace_with_existing_creds(self, old_creds_key: str, new_creds_key: str):
        replaced_indices = []
        for i in range(len(self.creds_keys)):
            if self.creds_keys[i] == old_creds_key:
                self.creds_keys[i] = new_creds_key
                replaced_indices.append(i)

        self.creds_dict.pop(old_creds_key, None)
        self.creds_mapping.pop(old_creds_key, None)

        self.managed_creds_keys.discard(old_creds_key)
        self.used_creds_keys.discard(old_creds_key)

        self.storage_providers.pop(old_creds_key, None)

        return replaced_indices

    def replace_creds(self, old_creds_key: str, new_creds_key: str):
        if old_creds_key not in self.creds_keys:
            raise KeyError(f"Creds key {old_creds_key} does not exist")
        if new_creds_key in self.creds_keys:
            return self._replace_with_existing_creds(old_creds_key, new_creds_key)
        replaced_indices = []
        for i in range(len(self.creds_keys)):
            if self.creds_keys[i] == old_creds_key:
                self.creds_keys[i] = new_creds_key
                replaced_indices.append(i)

        if old_creds_key in self.creds_dict:
            self.creds_dict[new_creds_key] = self.creds_dict[old_creds_key]
            del self.creds_dict[old_creds_key]

        self.creds_mapping[new_creds_key] = self.creds_mapping[old_creds_key]
        del self.creds_mapping[old_creds_key]

        if old_creds_key in self.managed_creds_keys:
            self.managed_creds_keys.remove(old_creds_key)
            self.managed_creds_keys.add(new_creds_key)

        if old_creds_key in self.used_creds_keys:
            self.used_creds_keys.remove(old_creds_key)
            self.used_creds_keys.add(new_creds_key)

        if old_creds_key in self.storage_providers:
            self.storage_providers[new_creds_key] = self.storage_providers[
                old_creds_key
            ]
            del self.storage_providers[old_creds_key]
        return replaced_indices

    def populate_creds(self, creds_key: str, creds):
        if creds_key not in self.creds_keys:
            raise MissingCredsError(f"Creds key {creds_key} does not exist")
        expires_in_to_expires_at(creds)
        self.creds_dict[creds_key] = creds
        self.storage_providers.pop(creds_key, None)

    def add_to_used_creds(self, creds_key: Optional[str]):
        if creds_key is None or creds_key in self.used_creds_keys:
            return False
        self.used_creds_keys.add(creds_key)
        return True

    def tobytes(self) -> bytes:
        d = {
            "creds_keys": self.creds_keys,
            "managed_creds_keys": list(self.managed_creds_keys),
            "used_creds_keys": list(self.used_creds_keys),
        }
        return json.dumps(d).encode("utf-8")

    @classmethod
    def frombuffer(cls, buffer: bytes):
        obj = cls()
        if buffer:
            d = json.loads(buffer.decode("utf-8"))
            obj.creds_keys = list(d["creds_keys"])
            obj.creds_mapping = {k: i + 1 for i, k in enumerate(obj.creds_keys)}
            obj.managed_creds_keys = set(d["managed_creds_keys"])
            obj.used_creds_keys = set(d["used_creds_keys"])
            if "ENV" in obj.used_creds_keys and "ENV" not in obj.creds_keys:
                obj.creds_keys = ["ENV"] + obj.creds_keys
                obj.creds_mapping["ENV"] = 0
        obj.is_dirty = False
        return obj

    def get_encoding(self, key: Optional[str] = None, path: Optional[str] = None):
        if key is None:
            if path and path.startswith(ALL_CLOUD_PREFIXES):
                raise ValueError("Creds key must always be specified for cloud storage")
            return 0

        if key not in self.creds_keys:
            raise MissingCredsError(f"Creds key {key} does not exist")
        return self.creds_mapping[key]

    def get_creds_key(self, encoding):
        if encoding > len(self.creds_keys):
            raise KeyError(f"Encoding {encoding} not found.")
        return None if encoding == 0 else self.creds_keys[encoding - 1]

    @property
    def nbytes(self):
        return len(self.tobytes())

    def __getstate__(self):
        return {
            "creds_keys": self.creds_keys,
            "creds_dict": self.creds_dict,
            "managed_creds_keys": self.managed_creds_keys,
            "used_creds_keys": self.used_creds_keys,
        }

    def __setstate__(self, state):
        self.creds_keys = state["creds_keys"]
        self.creds_dict = state["creds_dict"]
        self.managed_creds_keys = state["managed_creds_keys"]
        self.used_creds_keys = state["used_creds_keys"]
        self.creds_mapping = {key: i + 1 for i, key in enumerate(self.creds_keys)}
        self.storage_providers = {}
        self.default_s3_provider = None
        self.default_gcs_provider = None
        self.client = None
        self.org_id = None

    def __len__(self):
        return len(self.creds_keys)

    @property
    def missing_keys(self) -> list:
        return [key for key in self.creds_keys if key not in self.creds_dict]

    def populate_all_managed_creds(self, verbose: bool = True):
        assert self.client is not None
        assert self.org_id is not None
        for creds_key in self.managed_creds_keys:
            try:
                self.populate_single_managed_creds(creds_key, verbose=verbose)
            except ManagedCredentialsNotFoundError:
                logger.warning(
                    f"Credentials '{creds_key}' not found in Activeloop platform. "
                    f"Please make sure the credentials are added to the platform and reload the dataset. "
                    f"Alternatively, use ds.update_creds_key(key_name, managed=False) to disable the managed credentials.)"
                )

    def populate_single_managed_creds(self, creds_key: str, verbose: bool = True):
        assert self.client is not None
        assert self.org_id is not None
        creds = self.fetch_managed_creds(creds_key, verbose=verbose)
        self.populate_creds(creds_key, creds)

    def fetch_managed_creds(self, creds_key: str, verbose: bool = True):
        creds = self.client.get_managed_creds(self.org_id, creds_key)
        if verbose:
            logger.info(f"Loaded credentials '{creds_key}' from Activeloop platform.")
        return creds

    def change_creds_management(self, creds_key: str, managed: bool) -> bool:
        if creds_key not in self.creds_keys:
            raise KeyError(f"Creds key {creds_key} not found.")
        is_managed = creds_key in self.managed_creds_keys
        if is_managed == managed:
            return False
        if managed:
            creds = self.fetch_managed_creds(creds_key)
            self.managed_creds_keys.add(creds_key)
            self.populate_creds(creds_key, creds)
        else:
            self.managed_creds_keys.discard(creds_key)
            self.creds_dict.pop(creds_key, None)
            self.storage_providers.pop(creds_key, None)
        return True

    def warn_missing_managed_creds(self):
        """Warns about any missing managed creds that were added in parallel by someone else."""
        missing_creds = self.missing_keys

        missing_managed_creds = [
            creds for creds in missing_creds if creds in self.managed_creds_keys
        ]
        if missing_managed_creds:
            warnings.warn(
                f"There are some managed creds missing ({missing_managed_creds}) that were added after the dataset was loaded. Reload the dataset to load them."
            )
