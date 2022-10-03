import os
import yaml


def read_yaml(file_path: str) -> dict:
    with open(file_path, 'r', encoding="utf-8") as f:
        res = yaml.load(f, Loader=yaml.SafeLoader)
        return res


def write_yaml(file_path: str, file_data: dict):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(yaml.dump(file_data, sort_keys=False, default_flow_style=False, allow_unicode=True))


def replace_value(yaml_data: dict, keys: list, value: str):
    dic = yaml_data
    for k in keys[:-1]:
        dic = yaml_data[k]
    dic[keys[-1]] = value


if __name__ == '__main__':
    GITALK_CLIENT_ID = os.environ["GITALK_CLIENT_ID"]
    GITALK_CLIENT_SECRET = os.environ["GITALK_CLIENT_SECRET"]
    SHARE_THIS_URL = os.environ["SHARE_THIS_URL"]

    yaml_name = '_config.icarus.yml'
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), yaml_name)

    data = read_yaml(yaml_path)
    replace_value(data, ['comment', 'client_id'], GITALK_CLIENT_ID)
    replace_value(data, ['comment', 'client_secret'], GITALK_CLIENT_SECRET)
    replace_value(data, ['share', 'install_url'], SHARE_THIS_URL)
    write_yaml(yaml_path, data)
