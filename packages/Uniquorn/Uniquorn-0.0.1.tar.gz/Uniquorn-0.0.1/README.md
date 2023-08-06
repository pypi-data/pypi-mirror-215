# Uniquorn

A Python metaclass to create class instances with the same parameters only once.

Sometimes you need to avoid duplicated class instances with the same parameters.
The `Uniquorn` metaclass makes this easy.

## Basic usage

To avoid creating multiple instances with the same instantiation parameters
simply designate `Uniquorn` as your class' metaclass.

```python
from uniquorn import Uniquorn

class ExampleClass(metaclass=Uniquorn):

    def __init__(self, ...):
        ...
```

## List and dict order

By default, the order of items in list and dict parameters is irrelevant to
`Uniquorn`. It sorts the items in an attempt to detect duplicates.

You can tell `Uniquorn` the order of items is relevant to your
class through `uniquorn_list_order_matters` and `uniquorn_dict_order_matters`.
By assigning `True` to you tell `Uniquorn` for all parameters of that type order
of the items is relevant. Alternatively, you can assign the names of the
parameters  as a list, tuple or set to tell `Uniquorn` for those parameters the
order of the items is relevant.

```python
from uniquorn import Uniquorn

class ExampleClass(metaclass=Uniquorn):

    uniquorn_list_order_matters = True
    uniquorn_dict_order_matters = ("param1", "param2", )

    def __init__(self, ...):
        ...
```

## Limitations
- If you change the parameters after instance creation it will not be noted
  by `Uniquorn`.
- Apart from the mechanism described under 'List and dict order' above,
  `Uniquorn` makes no attempt to match parameters based on their internal
  structure.
