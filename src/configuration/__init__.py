import re
from typing import TypeVar

T = TypeVar("T")

camel_pattern: re.Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")


class Configuration:
    def get_instance(self, instance_type: type[T]) -> T:
        return getattr(
            self,
            re.sub(camel_pattern, "_", instance_type.__name__).lower(),
        )