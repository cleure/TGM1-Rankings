
class Sortable(object):
    """ User-sortable type """
    
    def __init__(self, value=0, sortby=0):
        self.sortby = sortby
        self.value = value
    
    def __eq__(a, b): return a.sortby == b.sortby
    def __ne__(a, b): return a.sortby != b.sortby
    def __lt__(a, b): return a.sortby  < b.sortby
    def __le__(a, b): return a.sortby <= b.sortby
    def __gt__(a, b): return a.sortby  > b.sortby
    def __ge__(a, b): return a.sortby >= b.sortby
