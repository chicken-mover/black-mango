
class ScrollableLabelSet(object):
    """
    A quick and dirty class for handling sets of scrolling labels.

    - If the anchor points are outside of the set's box, they become hidden.
    - If a label becomes selected that is outside of the box, all labels are
      scrolled until it is inside the box.
    """

    def __init__(self,
        width,
        height,
        anchor_x,
        anchor_y):

        self.width = width
        self.height = height
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

        self.bounds = {
            'left': anchor_x,
            'right': anchor_x + width,
            'top': anchor_y,
            'bottom': anchor_y - height,
        }

        self.labels = []

    def add(self, label):
        self.labels.append(label)

    def remove(self, label):
        self.labels = filter(lambda x: x is not label, self.labels)

    def set_selected(self, i, reset_color):
        selected = self.labels[i]
        while selected.y < self.bounds['bottom']:
            for i in self.labels:
                i.y += 1
        while selected.y > self.bounds['top']:
            for i in self.labels:
                i.y -= 1
        while selected.x < self.bounds['left']:
            for i in self.labels:
                i.x += 1
        while selected.x > self.bounds['right']:
            for i in self.labels:
                i.x -= 1

        for i in self.labels:
            if i.y < self.bounds['bottom']:
                i.visible = False
            elif i.y > self.bounds['top']:
                i.visible = False
            elif i.x < self.bounds['left']:
                i.visible = False
            elif i.x > self.bounds['right']:
                i.visible = False
            else:
                i.visible = True

            # Manually hide labels that are 'visible = False' by setting 100%
            # transparency
            if hasattr(i, 'visible') and not i.visible:
                i.color = i.color[:-1] + (0,)
            elif hasattr(i, 'visible') and i.visible:
                i.color = reset_color
