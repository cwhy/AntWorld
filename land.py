import physics

class land:
    def __init__(self, length, width=None):
        self.length = length
        if width == None:
            self.width = int(length)
        else:
            self.width = int(width)

    def get_info(self, x, y, info='all'):
        if info == 'all':
            return [['x', x],['y', y]]
        elif info == None:
            return None
        else:
            raise 'You are requesting some nonsense from the land'
