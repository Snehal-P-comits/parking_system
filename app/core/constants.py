"""Core constants and enums shared across modules."""

from enum import Enum
#What is enum?
'''Enum is a built-in Python module that provides a way to define a set of named values.
It allows you to create a collection of related constants that can be accessed by name,
improving code readability and maintainability. Enums are often used to represent a fixed set of options or states in a program.
For example, you can define an enum for the days of the week like this:
from enum import Enum
class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    In this example, DayOfWeek is an enum that represents the days of the week, 
    with each day assigned a unique integer value. You can access the enum members using their names,
    such as DayOfWeek.MONDAY, 
    which would return the value 1. 
    Enums help to make your code more self-explanatory and reduce the likelihood of errors caused by using arbitrary values.'''

class ParkingSessionStatus(str, Enum):
    # ACTIVE: vehicle currently inside parking lot.
    ACTIVE = "ACTIVE"
    # EXITED: session closed after vehicle exit.
    EXITED = "EXITED"


DEFAULT_PASSKEY_LENGTH = 4
DEFAULT_PASSKEY_MAX_RETRIES = 25
DEFAULT_API_PREFIX = "/api/v1"
