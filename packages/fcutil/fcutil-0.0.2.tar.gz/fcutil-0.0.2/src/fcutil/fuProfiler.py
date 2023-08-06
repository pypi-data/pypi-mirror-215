import cProfile
import pstats
import io

class fuProfiler:

    _result = ""

    def __init__(self):
        self._profiler = cProfile.Profile()

    def getResults(self):
        return self._result
    
    def start(self):
        self._profiler.enable()

    def stop(self):
        self._profiler.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(self._profiler, stream=s).sort_stats(sortby)
        stats = ps.print_stats()
        self._result = s.getvalue()

