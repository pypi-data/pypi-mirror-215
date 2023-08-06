# Copyright 2022 Chi-kwan Chan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Extra helper functions"""


from inspect import signature
from astropy import units


def get_argnames(f):
    """Get Argument Names from Function Signature

    Using the `inspect` module, it is possible to obtain the names of
    position arguments `a1`, `a2`, ..., from a function

        def f(a1, a2, ...):
            ...

    This helper function return these names in a tuple.

    """
    return tuple(k for k, v in signature(f).parameters.items() if v.default is v.empty)


def get_keywords(f):
    """Get Keywords from Function Signature

    Using the `inspect` module, it is possible to obtain the names of
    keyworded arguments `k1`, `k2`, ..., from a function

        def f(..., k1=..., k2=..., ...):
            ...

    This helper function return these names in a tuple.

    """
    return tuple(k for k, v in signature(f).parameters.items() if v.default is not v.empty)


def get_default(kwargs, name, f):
    """Get Keyworded Argument

    Return the default keyworded argument of function `f()` if that
    value is not set in `kwargs`.

    """
    return kwargs.get(name, signature(f).parameters[name].default)


def get_unit(unit, default):
    """Select Unit"""

    if isinstance(unit, units.UnitBase):
        return unit
    elif isinstance(default, units.UnitBase):
        return default
    else:
        return default[unit]


def get_backend(backend):
    """Deduce Backend from Loaded Module"""

    if backend is None:
        import sys
        if 'jax' in sys.modules:
            import jax.numpy as backend
        else:
            import numpy as backend
    return backend
