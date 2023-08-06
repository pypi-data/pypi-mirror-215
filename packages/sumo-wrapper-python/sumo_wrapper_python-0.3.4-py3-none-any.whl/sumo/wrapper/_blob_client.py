import requests
from ._request_error import raise_request_error_exception


class BlobClient:
    """Upload blobs to blob store using pre-authorized URLs"""

    def upload_blob(self, blob: bytes, url: str):
        """Upload a blob.

        Parameters:
            blob: byte string to upload
            url: pre-authorized URL to blob store
        """

        headers = {
            "Content-Type": "application/octet-stream",
            "Content-Length": str(len(blob)),
            "x-ms-blob-type": "BlockBlob",
        }

        try:
            response = requests.put(url, data=blob, headers=headers)
        except requests.exceptions.ProxyError as err:
            raise_request_error_exception(503, err)

        if not response.ok:
            raise_request_error_exception(response.status_code, response.text)

        return response
