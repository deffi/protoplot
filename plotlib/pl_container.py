from plotlib import OptionsContainer

class Container(list):
    '''
    * A list
    * Has an 'options' property, which is an OptionsContainer representing
      default options for all contained items
    * Has an add method whigh creates and adds an instance of a pre-defined
      class (klass) 
    '''
    def __init__(self, klass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._klass = klass
        self.options = OptionsContainer()
        
    def add(self, *args, **kwargs):
        content = self._klass(*args, **kwargs)
        self.append(content)
        return content
