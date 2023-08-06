import os
import requests
import json

from .exceptions import *


class VAPI:
    def __init__(
        self,
        addr: str = None,
        cacert: str = None,
        token: str = None,
        namespace: str = None,
        token_file: str = None,
    ):
        self.addr = addr or os.environ.get("VAULT_ADDR", None)
        self.cacert = cacert or os.environ.get("VAULT_CACERT", None)
        self.namespace = namespace or os.environ.get("VAULT_NAMESPACE", "")

        if token and token_file:
            raise VAPIConfigError(
                "May not set token and token_file.  Please choose one."
            )
        elif token:
            self.token = token
        elif token_file:
            with open(token_file, "r") as f:
                self.token = f.read().strip()
        elif os.environ.get("VAULT_TOKEN", None):
            self.token = os.environ["VAULT_TOKEN"]
        elif os.environ.get("VAULT_TOKEN_FILE", None):
            with open(os.environ["VAULT_TOKEN_FILE"], "r") as f:
                self.token = f.read().strip()
        else:
            raise VAPIConfigError(
                "Vault Token not set", "Please check Env variables or pass directly"
            )

        if self.addr is None:
            raise VAPIConfigError(
                "Vault Address not passed or set as environmetn variable",
                "Please check Env variables or pass directly",
            )
        if self.token is None:
            raise VAPIConfigError(
                "Vault Token not passed or set as environment variable",
                "Please check Env variables or pass directly",
            )

        self.api_version = "v1"
        self.current_path = ""

        token_test = self.token_lookup()

    def _validate_wrap_value(self, wrap_response):
        error_message = f"Wrap Response value {wrap_response} is not in valid VAPI format XXs, XXm, or XXh"

        try:
            number = int(wrap_response[:-1])
        except ValueError:
            raise VAPIConfigError(error_message)

        if (
            wrap_response.endswith("s")
            or wrap_response.endswith("m")
            or wrap_response.endswith("h")
        ):
            pass
        else:
            raise VAPIConfigError(error_message)

        return wrap_response

    def _set_headers(self, wrap_response):
        headers = {
            "Content-type": "application/json",
            "X-Vault-Token": self.token,
            "X-Vault-Namespace": self.namespace,
        }

        if wrap_response:
            try:
                headers["X-Vault-Wrap-Ttl"] = self._validate_wrap_value(wrap_response)
            except VAPIConfigError as e:
                raise

        return headers

    def _format_url(self, path):
        self.current_path = path
        url = f"{self.api_version}/{path}".replace("//", "/")
        url = f"{self.addr.rstrip('/')}/{url}"
        return url

    def _format_response(self, response, accepted_status_codes):
        if response.status_code in accepted_status_codes:
            try:
                json_response = response.json()
                if "data" in json_response.keys():
                    return json_response["data"]
                else:
                    return json_response
            except ValueError:
                return {}
        else:
            if response.status_code == 403:
                raise VAPIPermissionDeniedError(
                    f"Vault returned 403 for path {self.current_path} indicating permission issues",
                    response.status_code,
                    errors=response.json()["errors"],
                )
            if response.status_code == 404:
                raise VAPIPathError(
                    f"Vault returned 404 for path {self.current_path} indicating an issue with the path",
                    response.status_code,
                    errors=response.json()["errors"],
                )
            if response.status_code == 503:
                raise VAPISealedError(
                    f"Vault returned 503 for path {self.current_path} and is likely sealed",
                    response.status_code,
                    errors=response.json()["errors"],
                )
            if response.status_code in [200, 204]:
                raise VAPIAcceptedStatusCodeError(
                    f"Vault Response Status Code {response.status_code} for path {self.current_path} not in Accepted Range {', '.join(item) for item in accepted_status_codes}",
                    response.status_code,
                )
            raise VAPIVaultError(response.text, response.status_code)

        try:
            return response.json()
        except ValueError:
            return {}

    def token_lookup(self, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers(None)
        url = self._format_url("/auth/token/lookup-self")
        response = requests.get(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def get(
        self,
        path,
        raw=False,
        accepted_status_codes=[204, 200],
        wrap_response: str = None,
    ):
        headers = self._set_headers(wrap_response)
        url = self._format_url(path)
        response = requests.get(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def list(
        self,
        path,
        raw=False,
        accepted_status_codes=[204, 200],
        wrap_response: str = None,
    ):
        headers = self._set_headers(wrap_response)
        url = f"{self._format_url(path)}?list=true"
        response = requests.get(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def post(
        self,
        path,
        data={},
        raw=False,
        accepted_status_codes=[204, 200],
        wrap_response: str = None,
    ):
        headers = self._set_headers(wrap_response)
        url = self._format_url(path)
        response = requests.post(url, json=data, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)

    def delete(self, path, raw=False, accepted_status_codes=[204, 200]):
        headers = self._set_headers(None)
        url = self._format_url(path)
        response = requests.delete(url, headers=headers, verify=self.cacert)

        if raw:
            return response
        else:
            return self._format_response(response, accepted_status_codes)
