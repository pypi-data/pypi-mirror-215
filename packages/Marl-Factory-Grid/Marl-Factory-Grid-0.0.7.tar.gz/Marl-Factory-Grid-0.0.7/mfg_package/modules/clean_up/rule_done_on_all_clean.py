from mfg_package.environment import constants as c
from mfg_package.environment.rules import Rule
from mfg_package.utils.results import DoneResult
from mfg_package.modules.clean_up import constants as d, rewards as r


class DirtAllCleanDone(Rule):

    def __init__(self):
        super().__init__()

    def on_check_done(self, state) -> [DoneResult]:
        if len(state[d.DIRT]) == 0 and state.curr_step:
            return [DoneResult(validity=c.VALID, identifier=self.name, reward=r.CLEAN_UP_ALL)]
        return [DoneResult(validity=c.NOT_VALID, identifier=self.name, reward=0)]
