# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class element_parked(object):
    """An expectation for checking that an element is parked.

    Parked means that the element has not recently changed position or size.

    :param HTMLElement element: target element
    :param int precision: previous states to check for motion
    :returns: True if element has settled, False otherwise
    """

    def __init__(self, element, precision=3):
        self.element = element
        self.precision = precision
        self.state = []

    def __call__(self, selenium):
        self.state.append('{0.location} {0.size}'.format(self.element))
        history = self.state[-self.precision:]
        return len(history) == self.precision and len(set(history)) == 1
