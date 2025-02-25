from text_node import TextNode, TextType

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/cdae7fca-a7dc-4706-b2c5-7a03d66db1c9")
    print(node)

if __name__ == "__main__":
    main()