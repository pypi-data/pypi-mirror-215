from dataclasses import dataclass

from cmon import Executor, requests


@dataclass
class DummyExecutor(Executor):
    @requests
    def foo(self, docs, **kwargs):
        docs[0].text = 'dummy'
