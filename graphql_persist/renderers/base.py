
class BaseRenderer(object):

    def render(self, data, context=None):
        raise NotImplementedError('.render() must be implemented')
