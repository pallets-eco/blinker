cdef class _CheckReceiversSignalMixin:
    cdef public dict receivers

    cdef __check_receivers(self):
        return len(self.receivers) > 0

    def _check_receivers(self):
        return self.__check_receivers()
