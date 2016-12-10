# TODO we should also allow accessing by name, i. e.
#     oc = OptionsContainer()
#     oc(foo=11, bar=22)
#     oc.baz=33
#     print(oc.baz)
class OptionsContainer(dict):
    '''
    A dict that can be updated by calling it.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._by_tag = dict()
 
    def __call__(self, **kwargs):
        self.update(kwargs)

    def by_tag(self, tag_selector):
        '''tag_selector must be a single string tag for now'''
        # TODO allow functions
        # TODO allow combinations of tags (and-list)
        
        # TODO right now, by_tag itself is an OptionsContainer, so it can be
        # recursive (i. e. can have a by_tag again). Is this what we want? 
        # TODO use a defaultdict instead?
        if tag_selector not in self._by_tag:
            self._by_tag[tag_selector] = OptionsContainer()
        
        return self._by_tag[tag_selector]

    # TODO should also accept single tags?
    # TODO should be tag selectors 
    def for_tags(self, tags_list):
        result = dict()
        
        result.update(self)
        
        for tag in tags_list:
            # TODO when we allow functions as selectors, there will have to be
            # more elaborate matching.
            if tag in self._by_tag:
                result.update(self._by_tag[tag])

        return result