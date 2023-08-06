import queue
from typing import Collection
from opentelemetry import context, trace
from opentelemetry.context import attach, detach
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_current_span, get_tracer, get_tracer_provider

from .package import _instruments
from .version import __version__


class _InstrumentedQueue(queue.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tracer = get_tracer(__name__, __version__)

    def put(self, item, *args, **kwargs):
        item["_parent_span"] = get_current_span()
        super().put(item, *args, **kwargs)

    def get(self, *args, **kwargs):
        item = super().get(*args, **kwargs)

        # Start a new span for the get operation
        with self._tracer.start_as_current_span("queue.get") as span:
            # Get the parent span context from the item, if it exists
            parent_span = item.get("_parent_span")
            if parent_span is not None:
                # Set the parent span context for this thread
                ctx = trace.set_span_in_context(parent_span)
                token = attach(ctx)
                try:
                    # Call the original function
                    return super().get(*args, **kwargs)
                finally:
                    detach(token)


class QueueInstrumentor(BaseInstrumentor):
    original_queuecls = queue.Queue

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, *args, **kwargs):
        tracer_provider = (
            kwargs.get("tracer_provider", None) or get_tracer_provider()
        )

        tracer = get_tracer(__name__, __version__, tracer_provider)
        queue.Queue = _InstrumentedQueue
        _InstrumentedQueue._tracer = tracer

    def _uninstrument(self, **kwargs):
        queue.Queue = self.original_queuecls
