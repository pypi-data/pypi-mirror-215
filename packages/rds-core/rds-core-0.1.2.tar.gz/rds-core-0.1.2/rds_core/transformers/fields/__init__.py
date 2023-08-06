import logging
from typing import Union, Dict, Any, List
from datetime import datetime
from rds_core.helpers import get_dict_by_pathname

strptime = datetime.strptime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Field:
    def __init__(self, source_field: Union[str, object, None]):
        self.source_field = source_field

    def transform_to_dict(
        self,
        source_dict: Dict[str, Any],
        dest_dict: Dict[str, Any],
        dest_fieldname: str,
    ):
        if self.source_field is None:
            dest_dict[dest_fieldname] = None
        else:
            dest_dict[dest_fieldname] = self.cast_source_value(
                get_dict_by_pathname(source_dict, self.source_field)
            )

    def cast_source_value(self, source_value: Union[str, int, bool, float]):
        return source_value


class CharField(Field):
    pass


class DateField(Field):
    def __init__(self, source_field: str, format: str = "%d/%m/%Y"):
        super().__init__(source_field)
        self.format = format

    def cast_source_value(
        self, source_value: Union[None, str, int, bool, float]
    ) -> datetime.date:
        return strptime(source_value, self.format) if source_value is not None else None


class DateTimeField(Field):
    def __init__(self, source_field: str, format: str = "%d/%m/%Y %H:%M:%S"):
        super().__init__(source_field)
        self.format = format

    def cast_source_value(self, source_value: Union[str, int, bool, float]) -> datetime:
        return strptime(source_value, self.format) if source_value is not None else None


class SimpleConcatField(Field):
    def __init__(self, fields: Union[List[str], None] = None, separator: str = ""):
        super().__init__(None)
        self.fields = fields
        self.separator = separator

    def transform_to_dict(
        self,
        source_dict: Dict[str, Any],
        dest_dict: Dict[str, Any],
        dest_fieldname: str,
    ) -> str:
        if self.fields is not None:
            dest_dict[dest_fieldname] = self.separator.join(
                [
                    self.cast_source_value(get_dict_by_pathname(source_dict, f))
                    for f in self.fields
                ]
            )


class SubModelField(Field):
    def transform_to_dict(
        self,
        source_dict: Dict[str, Any],
        dest_dict: Dict[str, Any],
        dest_fieldname: str,
    ):
        dest_dict[dest_fieldname] = self.source_field.transform_to_dict(source_dict)
