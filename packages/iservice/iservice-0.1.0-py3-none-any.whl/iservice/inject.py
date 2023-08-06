import functools
import typing

import iservice

P = typing.ParamSpec("P")
R = typing.TypeVar("R")
S1 = typing.TypeVar("S1", bound=iservice.Service)
S2 = typing.TypeVar("S2", bound=iservice.Service)
S3 = typing.TypeVar("S3", bound=iservice.Service)
S4 = typing.TypeVar("S4", bound=iservice.Service)


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[type[S1], P], R],
    service1: type[S1],
    /,
) -> typing.Callable[P, R]:
    ...


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[type[S1], type[S2], P], R],
    service1: type[S1],
    service2: type[S2],
    /,
) -> typing.Callable[P, R]:
    ...


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[type[S1], type[S2], type[S3], P], R],
    service1: type[S1],
    service2: type[S2],
    service3: type[S3],
    /,
) -> typing.Callable[P, R]:
    ...


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[type[S1], type[S2], type[S3], type[S4], P], R],
    service1: type[S1],
    service2: type[S2],
    service3: type[S3],
    service4: type[S4],
    /,
) -> typing.Callable[P, R]:
    ...


def inject(
    func: typing.Callable[..., R],
    /,
    *services: type[iservice.Service],
) -> typing.Callable[..., R]:
    """Read implementation accept any number of services."""
    return functools.partial(func, *services)
