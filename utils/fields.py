from models import State
from py_models.location import state_pydantic, state_pydantic_list
from schemas.fields import State as StatePydantic

async def get_db_states():
    return await state_pydantic.from_queryset(State.all())

