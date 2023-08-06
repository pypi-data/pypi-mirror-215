from ..shared.client.client import Client
from .model import Deployment, dto, CreateDeployment

from dataclasses import asdict


class Deployments(Client):
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key)


    def get_by_id(self, id: str) -> Deployment:
        """
        get_by_id - get a deployment by its ID
        """
        deployment = super().get("/api/v1/deployments/%s" % id)
        return dto(deployment)
    

    def create(self, deployment: CreateDeployment) -> Deployment:
        """
        create - create a new Deployment
        """
        try:
            deployment = super().post("/api/v1/deployments", asdict(deployment))
            return dto(deployment)
        except Exception as e:
            raise Exception('error creating deployment %s' % e)


    def list(self, start: int, to: int) -> list[Deployment]:
        """
        list - list all of your deployments
        """
        deployments = super().get("/api/v1/deployments", start, to)

        result = []
        for d in deployments:
            result.append(dto(d))

        return result
