from dataclasses import dataclass

@dataclass
class Job:
    id: str
    credits_used: str
    results: list[str]


@dataclass
class Deployment:
    id: str
    model: str
    job: Job


@dataclass
class CreateDeployment:
    model: str
    args: dict
    name: str

    def dict(self):
        return super().dict()

def request_dto(id: str, m: CreateDeployment) -> dict:
    return {
        'model_id': id,
        'args': m.args,
        'name': m.name,
    }

def dto(m: dict) -> Deployment:
    return Deployment(
        id=m.get('id'),
        model=m.get('alias'),
        job=m.get('job'),
    )
