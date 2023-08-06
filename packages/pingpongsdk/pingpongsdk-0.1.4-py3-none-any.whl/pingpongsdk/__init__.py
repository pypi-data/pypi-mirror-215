import os

from .deployments.deployments import Deployments
from .models.models import Models


_API_KEY = os.getenv('X_MEDIAMAGIC_KEY')


class PingPong():
    """
    PingPong - is a vanity class, which simply
    combined the underlying libraries into one
    object with the api configured for each etc.
    """

    models: Models
    deployments: Deployments

    def __init__(self, api_key=_API_KEY):
        self.models = Models(api_key=api_key)
        self.deployments = Deployments(api_key=api_key)
