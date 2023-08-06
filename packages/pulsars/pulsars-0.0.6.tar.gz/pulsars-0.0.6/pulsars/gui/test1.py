import tomli

def readtemplate(file):

    with open(file, "rb") as f:
        toml_dict = tomli.load(f)
    return toml_dict


template = readtemplate("test.toml")




keys = list(template["geometry_parameters"].keys())
values = list(template["geometry_parameters"].values())

print("Keys:", keys)
print("Values:", values)

