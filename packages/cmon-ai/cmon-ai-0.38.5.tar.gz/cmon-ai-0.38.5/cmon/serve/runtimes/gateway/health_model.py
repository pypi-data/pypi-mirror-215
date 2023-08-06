from pydantic import BaseModel
from typing import Dict


def _to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


class CmonHealthModel(BaseModel):
    """Pydantic BaseModel for Cmon health check, used as the response model in REST app."""

    ...


class CmonInfoModel(BaseModel):
    """Pydantic BaseModel for Cmon status, used as the response model in REST app."""

    cmon: Dict
    envs: Dict

    class Config:
        alias_generator = _to_camel_case
        allow_population_by_field_name = True
