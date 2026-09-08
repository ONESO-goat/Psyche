


def hashtag(topic):
    print("=" * 50)
    print(f"# {topic}")
    print("=" * 50)
    print()


index = 0
def debug(message:str, tier:int=5):
    global index
    E = f"[DEBUG {tier}] {index}: {message}"
    print(E)
    index += 1
    return E
    
def reset_debug()->None:
    global index
    index = 0