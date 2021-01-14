from TokenInfo import TokenInfo


def build_token(info:str) -> TokenInfo:
    doc, doc_weight = info.split(":")
    if "[" in doc_weight:
        weight, list_positions = doc_weight[:-1].split("[")
        return TokenInfo(doc, float(weight), positions=[int(i) for i in list_positions.split(",")])
    return TokenInfo(doc, float(doc_weight)) 
