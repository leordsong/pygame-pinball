from typing import List


class Listener:

    def yield_events(self, game) -> List[str]:
        raise NotImplementedError("This method needs to be implemented")

