import os, shutil
from blocks_markdown import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)
        if item.endswith(".md"):
            if dest_path.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
            generate_page(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_markdown = f.read()
    with open(template_path) as f:
        template_markdown = f.read()
    node = markdown_to_html_node(from_markdown)
    html = node.to_html()
    title = extract_title(from_markdown)

    full_html = template_markdown.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)

def extract_title(markdown):
    markdown_list = markdown.split("\n")
    for markdown_string in markdown_list:
        if markdown_string.startswith("# "):
            return markdown_string.lstrip("#").strip()
    raise Exception("No h1 header.")

def copy_dir(src, dst):
    files = os.listdir(src)
    for file in files:
        src_path = os.path.join(src, file)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        else:
            dst_path = os.path.join(dst, file)
            os.mkdir(dst_path)
            copy_dir(src_path, dst_path)

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()