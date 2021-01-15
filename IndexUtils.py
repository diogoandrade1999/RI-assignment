from TokenInfo import TokenInfo


def build_token(info:str) -> TokenInfo:
    """
    Build token info.

    Parameters
    ----------
    info : str
        The token info formated.

    Returns
    -------
    TokenInfo
        The token info class.
    """
    splited_info = info.split(":")
    if len(splited_info) == 3:
        doc, weight, list_positions = splited_info
        return TokenInfo(doc, float(weight), positions=[int(i) for i in list_positions.split(",")])

    doc, doc_weight = splited_info
    return TokenInfo(doc, float(doc_weight)) 
