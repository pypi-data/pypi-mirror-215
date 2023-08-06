import os

from cmon import Executor, requests


class DummyExec(Executor):
    @requests
    def foo(self, **kwargs):
        pass
