import pytest

def test_pydnatic_model_monkeypath():
    from pydantic import BaseModel, Extra

    class MockModel(BaseModel):
        a: str = 'a'
    with pytest.raises(ValueError, match='no field "b"'):
        MockModel().b = 'b'