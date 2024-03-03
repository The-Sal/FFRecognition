class FFRError(Exception):
    pass

class NoBindingsError(FFRError):
    pass


class NoDylibError(FFRError):
    pass


class UnableToCompareFacesError(FFRError):
    pass
