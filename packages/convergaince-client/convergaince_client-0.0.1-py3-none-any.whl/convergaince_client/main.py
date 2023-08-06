from __future__ import print_function
import os
from . import retrieve
from .lib import get_default_logger


class APIClient(object):
    """API client with stateful authentication for lib functions and extra convenience methods."""

    def __init__(self, api_host, access_token=None):
        """Construct a GroClient instance.

        Parameters
        ----------
        api_host : string, optional
            The API server hostname.
        access_token : string, optional
            Your Gro API authentication token. If not specified, the
            :code:`$GROAPI_TOKEN` environment variable is used. See
            :doc:`authentication`.
        proxy_host : string, optional
            If you're instantiating the GroClient behind a proxy, you'll need to
            provide the proxy_host to properly send requests using the groclient
            library.
        proxy_port : int, optional
            If you're instantiating the GroClient behind a proxy, you'll need to
            provide the proxy_port to properly send requests using the groclient
            library.
        proxy_username : string, optional
            If you're instantiating the GroClient behind a proxy, and your proxy
            requires a username and password, you'll need to provide the proxy_username.
        proxy_pass : string optional
            Password for your proxy username.

        Raises
        ------
            RuntimeError
                Raised when neither the :code:`access_token` parameter nor
                :code:`$GROAPI_TOKEN` environment variable are set.

        Examples
        --------
            >>> client = GroClient()  # token stored in $GROAPI_TOKEN

            >>> client = GroClient(access_token="your_token_here")

            # example useage when accessed via a proxy
            >>> client = GroClient(access_token="your_token_here", proxy_host="0.0.0.0", proxy_port=8080,
            proxy_username="user_name", proxy_pass="secret_password")
        """
        # Initialize early since they're referenced in the destructor and
        # access_token checking may cause constructor to exit early.

        if access_token is None:
            access_token = os.environ.get("APICLIENT_TOKEN")
            if access_token is None:
                raise RuntimeError(
                    "$APICLIENT_TOKEN environment variable must be set when "
                    "APIClient is constructed without the access_token argument"
                )
        self.api_host = api_host
        self.access_token = access_token
        self._logger = get_default_logger()

    def get_logger(self):
        return self._logger

    def get_dataframe(self, entity):
        """ """
        return retrieve.get_dataframe(
            access_token=self.access_token, api_host=self.api_host, entity=entity
        )
