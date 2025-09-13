
def create():
    """
    Create a speaker object
        :return:  appropriate object for the platform
    """
    from .macos import SpeakerMacos
    return SpeakerMacos()

