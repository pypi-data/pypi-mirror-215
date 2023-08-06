import tomli
# parse toml configuration file
def readconfig(file):
    
    with open(file, "rb") as f:
        toml_dict = tomli.load(f)
    return toml_dict


