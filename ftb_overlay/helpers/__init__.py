import ftb_overlay.core.parser as Parser


def get_title(url):
    return Parser.Parser(url).title


def getName(projectID):
    pR = get_title("https://minecraft.curseforge.com/projects/{}".format(projectID))
    pT = pR.split(" - ")[1]
    return pT


def getVersion(projectID, fileID):
    pR = get_title("https://minecraft.curseforge.com/projects/{}/files/{}".format(projectID, fileID))
    pT = pR.split(" - ")[0]
    return pT


def mod_index(modlist, modid):
    """
    Find the first instance of the specified mod in the provided list.

    Args:
        modlist (:obj:`list` of :obj:`dict`): List of mods as defined by the FTB manifest
        modid (str): Numeric string of the mod project ID to search for

    Returns:
        (int) Index of first match, if any. Returns `None` if no match.
    """

    for i in range(0, len(modlist)):
        if modlist[i]['projectID'] == modid:
            return i
    return None
