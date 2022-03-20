# This import should be at the top of the file because we need to apply monkey patch
# before executing any other code.
# We want to revert this change: https://github.com/python/cpython/pull/1030
# Additional context is here: https://github.com/aio-libs/aiopg/issues/837
import selectors  # isort:skip # noqa: F401

selectors._PollLikeSelector.modify = (  # type: ignore
    selectors._BaseSelectorImpl.modify  # type: ignore
)  # noqa: E402
