


def hashtag(topic):
    print("#" * 50)
    print(f"# {topic}")
    print("#" * 50)
    print()


index = 0
def debug(message):
    global index
    print(f"[DEBUG] {index}: {message}")
    index += 1
    
def reset_debug():
    global index
    index = 0