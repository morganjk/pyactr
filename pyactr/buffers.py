"""
General class on buffers.
"""

import collections

import pyactr.chunks as chunks
import pyactr.utilities as utilities

class Buffer(collections.MutableSet):
    """
    Buffer module.
    """

    _BUSY = utilities._BUSY
    _FREE = utilities._FREE
    _ERROR = utilities._ERROR

    def __init__(self, dm=None, data=None):
        self.dm = dm
        self.state = self._FREE
        if data == None:
            self._data = set([])
        else:
            self._data = data
        assert len(self) <= 1, "Buffer can carry at most one element"

    def __contains__(self, elem):
        return elem in self._data

    def __iter__(self):
        for elem in self._data:
            yield elem

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def add(self, elem):
        """
        Adds a chunk into the buffer.
        """
        self._data = set()
        
        if isinstance(elem, chunks.Chunk):
            self._data.add(elem)
        else:
            raise TypeError("Only chunks can be added to Buffer")

    def discard(self, elem):
        """
        Discard an element without clearing it into a memory.
        """
        self._data.discard(elem)

    def test_buffer(self, inquiry):
        """
        Is buffer full/empty?
        """
        if self._data:
            if inquiry == "full": return True
        else:
            if inquiry == "empty": return True
        return False

    def modify(self, otherchunk, actrvariables=None):
        """
        Modify the chunk in Buffer according to the info in otherchunk.
        """
        if actrvariables == None:
            actrvariables = {}
        elem = self._data.pop()
        mod_attr_val = {x[0]: utilities.check_bound_vars(actrvariables, x[1]) for x in otherchunk.removeunused()} #creates dict of attr-val pairs according to otherchunk

        elem_attr_val = {x[0]: x[1] for x in elem}
        elem_attr_val.update(mod_attr_val) #updates original chunk with attr-val from otherchunk
        mod_chunk = chunks.Chunk(otherchunk.typename, **elem_attr_val) #creates new chunk

        self._data.add(mod_chunk) #put chunk directly into buffer