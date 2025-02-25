def markdown_to_blocks(markdown):
    block = []
    
    previous_delimiter = " "

    if markdown == "":
        raise ValueError("Empty markdown")
    
    for index,  value in enumerate(markdown.split("\n")):
        if index + 1 == len(markdown.split("\n")):
            break
        if value != "":
            string = value.strip()
            current_delimiter = string[0]
            if previous_delimiter != current_delimiter:
                block.append(string)
            else:
                block[-1] = block[-1] + "\n" + string
            previous_delimiter = current_delimiter
    
    return block

