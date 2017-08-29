cdef class _CheckReceiversSignalMixin:
    cdef public dict receivers

    cdef inline object __not_receivers(self):
        return not self.receivers

    def _not_receivers(self):
        return self.__not_receivers()
