import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.indent(sequence=4, offset=2)
yaml.width = 4096
yaml.preserve_quotes = True

def main():
    name = input("Enter your name: ")
    return f"Hello, {name}!"
