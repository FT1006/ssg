def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks