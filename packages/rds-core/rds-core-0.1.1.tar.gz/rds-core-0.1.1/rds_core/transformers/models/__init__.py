from typing import Union, Dict, Any
import inspect
from rds_core.transformers.fields import Field


class ModelTransformer:
    __fields = None

    @classmethod
    def transform_to_dict(
        cls, source_dict: Union[Dict, None]
    ) -> Union[Dict[str, Any], None]:
        destination_dict = {}
        for destination_fieldname, transformer_field in cls.get_fields().items():
            transformer_field.transform_to_dict(
                source_dict, destination_dict, destination_fieldname
            )
        return destination_dict

    @classmethod
    def get_fields(cls) -> dict:
        if cls.__fields is None:
            cls.__fields = {}
            for k, v in inspect.getmembers(cls):
                if isinstance(v, Field):
                    cls.__fields[k] = v
        return cls.__fields
