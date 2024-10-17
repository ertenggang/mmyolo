import json
import random


k=256
with open('/mnt/d/projects/mmyolo/data/mmengine_format_5000.json') as f:
    data = json.load(f) 

print(data.keys())
data['data_list'] = random.sample(data['data_list'], k=k)
data['data_list'] = [v for v in data['data_list'] if not v['img_path'].endswith('gt.jpg')]

print(len(data['data_list']))

for idx, d in enumerate(data['data_list']):
    d['img_id'] = idx


with open(f'/mnt/d/projects/mmyolo/data/mmengine_format_{k}.json', 'w') as f:
    json.dump(data, f)