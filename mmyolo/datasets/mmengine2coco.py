import json 

input_file = '/mnt/e/ours_annotation/annotations/mmengine_format_256.json'
output_file = '/mnt/e/ours_annotation/annotations/coco_format_256.json'

def convert(input_file, output_file):
    with open(input_file) as f:
        anno_mmdet = json.load(f)

    anno_coco = dict()
    anno_coco['categories'] = []
    for idx, c in enumerate(anno_mmdet['metainfo']['classes']):
        anno_coco['categories'].append({'id': idx, 'name': c})

    print(len(anno_coco['categories']))

    anno_coco['images'] = []
    anno_coco['annotations'] = []

    anno_idx = 0
    sample_categories = set()
    for img_id, data in enumerate(anno_mmdet['data_list']):
        width, height = 640, 360
        anno_coco['images'].append({'id': img_id, 
                                    'file_name': data['img_path'], 
                                    'width':width, 
                                    'height':height})
        for obj in data['objects']:
            anno_coco['annotations'].append({
                'id': anno_idx,
                'image_id': img_id,
                'category_id': obj['defect_name'],
                'area': obj['bncbox']['width']*obj['bncbox']['height']*width*height/10000,
                'bbox': [obj['bncbox']['x']*width/100, 
                         obj['bncbox']['y']*height/100, 
                         obj['bncbox']['width']*width/100, 
                         obj['bncbox']['height']*height/100],
                'iscrowd' :0
            })
            anno_idx += 1
            sample_categories.add(obj['defect_name'])

    print(len(sample_categories))
    anno_coco['categories'] = [c for c in anno_coco['categories'] if c['id'] in sample_categories]
    for instance in anno_coco['annotations']:
        instance['category_id'] = anno_coco['categories'].index([c for c in anno_coco['categories'] if c['id'] == instance['category_id']][0])
    for idx, c in enumerate(anno_coco['categories']):
        c['id'] = idx
    print(len(anno_coco['categories']))
    with open(output_file, 'w') as f:
        json.dump(anno_coco, f)
    


convert(input_file, output_file)
