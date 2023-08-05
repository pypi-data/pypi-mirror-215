from mixy.models.base import BaseModel


class JinjaSettings(BaseModel):
    block_start_string: str = "{*"
    block_end_string: str = "*}"
    variable_start_string: str = "{@"
    variable_end_string: str = "@}"
