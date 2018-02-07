
import logging
from pyRacetrack import Racetrack


class RacetrackHandler(logging.Handler):

    def __init__(self, racetrack=None, *args, **kwargs):
        super(RacetrackHandler, self).__init__(*args, **kwargs)
        self.racetrack = racetrack

    def emit(self, record):
        if record.levelname in ['ERROR']:
            self.racetrack.verify(record.msg, actual=False, expected=True)
        elif record.levelname in ['WARN', 'CRITICAL']:
            self.racetrack.warning(record.msg)
        else:
            self.racetrack.comment(record.msg)


if __name__ == "__main__":
    rt = Racetrack(server="racetrack-dev.eng.vmware.com", port=80)
    rt.test_set_begin(buildid=12345,
                      user="rramchandani",
                      product="dummy",
                      description="some desc",
                      hostos="10.112.19.19",
                      server_buildid="1234",
                      branch="master")

    console = logging.StreamHandler()
    racetrackh = RacetrackHandler(racetrack=rt)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    logger.addHandler(racetrackh)

    rt.test_case_begin("testcase", "feature", "some des", "machine", tcmsid=98765)
    count = 0
    words = {
        0: "Zero",
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five"
    }

    for i in ["debug", "info", "warn", "error", "critical"]:
        getattr(logger, i)(words[count])
        count += 1

    rt.test_case_end()
    rt.test_set_end()
