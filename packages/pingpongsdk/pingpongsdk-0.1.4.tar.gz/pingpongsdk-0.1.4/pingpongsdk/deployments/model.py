from dataclasses import dataclass

@dataclass
class Job:
    id: str
    credits_used: str
    results: list[str]


@dataclass
class Deployment:
    id: str
    model_id: str
    job: Job


@dataclass
class CreateDeployment:
    model_id: str
    args: dict
    name: str

    def dict(self):
        return super().dict()


def dto(m: dict) -> Deployment:
    return Deployment(
        id=m.get('id'),
        model_id=m.get('model_id'),
        job=m.get('job'),
    )
