from TokenInfo import TokenInfo

def build_token(info:str) -> TokenInfo:
    doc, doc_weight = info.split(":")
    return TokenInfo(doc, float(doc_weight)) 