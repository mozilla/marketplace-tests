# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class element_moving(object):
    """An expectation for checking that an element is moving.

    Moving means that the element has recently changed position or size.

    :param HTMLElement element: target element
    :param int precision: previous states to check for motion
    :returns: True if element is moving, False otherwise
    """

    def __init__(self, element, precision=3):
        self.element = element
        self.precision = precision
        self.history = []

    def __call__(self, selenium):
        while len(self.history) < self.precision:
            self.history.append((
                str(self.element.location),
                str(self.element.size)))
        return len(set(self.history[-self.precision:])) == 1


class element_not_moving(element_moving):
    """An expectation for checking that an element is not moving.

    Moving means that the element has recently changed position or size.

    :param HTMLElement element: target element
    :param int precision: previous states to check for motion
    :returns: True if element is not moving, False otherwise
    """

    def __init__(self, element, precision=3):
        super(element_not_moving, self).__init__(element, precision)

    def __call__(self, selenium):
        return not super(element_not_moving, self).__call__(selenium)
