import asyncio
from typing import AsyncGenerator, TypeVar, Sequence, Optional, Tuple

_T = TypeVar('_T')
_T_gen = AsyncGenerator[_T, None]
_T_seq_gen = AsyncGenerator[Sequence[_T], None]

__all__ = ['aenumerate', 'limit_yields', 'limit_sub_yields']


def limit_yields(
        agen: _T_gen,
        limit: Optional[int]
) -> _T_gen:
    """limits count of `agen`'s results"""
    if limit is None:
        return agen
    else:
        return _limit_yields(agen, limit=limit)


async def _limit_yields(
        agen: _T_gen,
        limit: int
) -> _T_gen:
    async for count, obj in aenumerate(agen):
        if count >= limit:
            return
        yield obj


def limit_sub_yields(
        agen: _T_seq_gen,
        limit: Optional[int]
) -> _T_seq_gen:
    """
    Limits amount of sub results of `agen`.

    If `limit` is `100`, and `agen` yields each time 20-length result ->
    the func will yield it only 5 times, then it's stopped.

    Also, if `agen` each time yields 30-length result ->
    the func will yield it 4 times but last one will be sliced, so it contains only 10 sub-results.

    Args:
        agen: AsyncGenerator, must yield objects supporting `len` and `slicing`: str, list, etc.
        limit: int | None, None -> no limit, int -> max

    Examples:
        >>> base = ['part']*5  # summary len = 20

        >>> async def agen_():
        ...     for part in base:
        ...         yield part

        >>> async def main():
        ...     async for parts in limit_sub_yields(agen_(), limit=14):
        ...         print(parts)

        >>> asyncio.run(main())
        part
        part
        part
        pa
    """
    if limit is None:
        return agen
    else:
        return _limit_sub_yields(agen, limit=limit)


async def _limit_sub_yields(
        agen: _T_seq_gen,
        limit: int
) -> _T_seq_gen:
    count = 0
    async for seq in agen:
        count += len(seq)
        if count >= limit:
            yield seq[:-(count-limit)]
            return
        yield seq


async def aenumerate(
        agen: _T_gen,
        start: int = 0
) -> AsyncGenerator[Tuple[int, _T], None]:
    """async enumerate"""
    count = start
    async for obj in agen:
        yield count, obj
        count += 1
