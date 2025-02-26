from text_node import TextType, TextNode
from extract_markdown import extract_markdown_links, extract_markdown_images
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
     

def split_nodes_link(old_nodes):
    result = []
    
    for node in old_nodes:
        if len(extract_markdown_links(node.text)) == 0:
            result.append(node)
            continue
            
        current_text = node.text
        for link_text, url in extract_markdown_links(current_text):
            parts = current_text.split(f"[{link_text}]({url})", 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            result.append(TextNode(link_text, TextType.LINK, url))
            
            current_text = parts[1]
        
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
            
    return result


def split_nodes_image(old_nodes):
    result = []
    
    for node in old_nodes:
        if len(extract_markdown_images(node.text)) == 0:
            result.append(node)
            continue
            
        current_text = node.text
        for image_alt, image_link in extract_markdown_images(current_text):
            parts = current_text.split(f"![{image_alt}]({image_link})", 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            result.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            current_text = parts[1]
        
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
            
    return result

def text_to_textnode(text):

    nodes = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([nodes])
    
    nodes = split_nodes_link([nodes][0])
    
    nodes = split_nodes_delimiter([nodes][0], "**", TextType.BOLD)
    
    nodes = split_nodes_delimiter([nodes][0], "*", TextType.ITALIC)
    
    nodes = split_nodes_delimiter([nodes][0], "`", TextType.CODE)
    

    return nodes


