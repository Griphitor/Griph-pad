import yaml
with open('config.yaml', 'r') as infile:
    config = yaml.safe_load(infile)
def get_config(conf) -> any:
    return config[conf]