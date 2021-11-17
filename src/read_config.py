import yaml
with open('config.yaml', 'r') as infile:
    config = yaml.safe_load(infile)
    print(yaml.dump(config, default_flow_style=False))
def get_config(conf):
    return config[conf]