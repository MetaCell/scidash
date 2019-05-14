import sciunit.models.backends as backends
import neuronunit.models.backends as nu_backends


class ScidashCacheBackend(nu_backends.jNeuroMLBackend):

    name = 'ScidashCache'

    def init_backend(self, *args, **kwargs):
        """Initialize the Geppetto backend."""
        super().init_backend(*args, **kwargs)

    class FakeAttr:
        def __call__(self, *args, **kwargs):
            return None

    def __getattr__(self, name):
        return self.FakeAttr()

    def _backend_run(self) -> dict:

        cache = self.get_memory_cache(self.model.hash)

        if cache is not None:
            return cache
        elif self.memory_cache is not None:
            _hash, cache = self.memory_cache.popitem()
            return cache

        return {}


backends.register_backends({'ScidashCacheBackend': ScidashCacheBackend})
