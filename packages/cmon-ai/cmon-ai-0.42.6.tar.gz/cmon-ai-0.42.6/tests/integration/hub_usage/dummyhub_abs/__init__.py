from utils import foo

from cmon import Executor


class DummyHubExecutorAbs(Executor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        foo()
