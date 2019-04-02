
class NVCCError(Exception):
    pass


class NVCCUnsupportedInputFile(NVCCError):
    pass

class NVCCUnspecifiedCompiler(NVCCError):
    pass
