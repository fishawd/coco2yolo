import json
import os

"""
将给定的数据格式转换为COCO instance数据集

代码中要求输入的数据格式如下:
 
    [
        {
            file_name: 图片名称
            width:  宽   
            height:  高
            annos: [
                        {
                            segmentation: 边界
                            area：  面积
                            bbox:   水平矩形框
                            iscrowd:    是否多个目标
                            category_id:    类别id
                        },
                    ]
        },
    ]
            
                
COCO instance数据格式说明如下

info:{
        "description": "COCO 2017 Dataset",
        "url": "http://cocodataset.org",
        "version": "1.0",
        "year": 2017,
        "contributor": "COCO Consortium",
        "date_created": "2017/09/01"
     }
    
licenses(可选):[
        {
            url:
            id:
            name        
        }
    ]

images:[
        {
            license(可选):
            file_name: 图片名称
            coco_url(可选):
            height: 高
            width: 宽
            date_captured(可选):
            flickr_url(可选):
            id: 图片id
        }
    ]

annotations:[
        {
            segmentation: 边界坐标，RLE or [polygon]格式
            area: 标注区域的面积
            image_id：图片id
            bbox：水平框坐标，图片左上角为(0,0)，坐标从左上角开始，依次是[x,y,w,h] x,y是左上角的坐标， w,h是宽高
            iscrowd：单个还是多个目标(0 or 1)，当iccrowd是0采用polygon格式，会有多个多边形
            category_id：类别id
            id: 对象id， 也就是该框的id
        }
    
    ]

categories:[
    {
        id: 类别id
        name: 类别名称
        supercategory: 父类名称
    }
]


"""


class Dataset2COCO:
    """
    images_with_anno格式:
    [
        {
            file_name: 图片名称
            width:  宽
            height:  高
            annos: [
                        {
                            segmentation: 边界
                            area：  面积
                            bbox:   水平矩形框
                            iscrowd:    是否多个目标
                            category_id:    类别id
                        },
                    ]
        },
    ]
    """
    def __init__(self):
        self.images = []
        self.annotations = []
        self.image_id = 1
        self.anno_id = 1

    def dataset2coco(self, images_annos, categories, info, output_path):
        self._generate_images(images_annos)

        result = {
            'info': info,
            'categories': self._generate_categories(categories),
            'images': self.images,
            'annotations': self.annotations
        }
        json.dump(result, open(os.path.join(output_path, 'dataset_train.json'), 'w', encoding='utf-8'))

    def _generate_images(self, images_annos):
        for image_anno in images_annos:
            image = {
                'file_name': image_anno['file_name'],
                'width': image_anno['width'],
                'height': image_anno['height'],
                'id': self.image_id
            }
            self.images.append(image)
            self._generate_annotations(image_anno['annos'])
            self.image_id += 1

    def _generate_annotations(self, annos):
        for anno in annos:
            annotation = {
                'segmentation': anno['segmentation'],
                'area': anno['area'],
                'image_id': self.image_id,
                'bbox': anno['bbox'],
                'iscrowd': anno['iscrowd'],
                'category_id': anno['category_id'],
                'id': self.anno_id
            }
            self.annotations.append(annotation)
            self.anno_id += 1

    def _generate_categories(self, categories):
        categories_anno = []
        for i, category in enumerate(categories):
            id = i + 1
            name = category
            supercategory = category
            cat_anno = {
                'id': id,
                'name': name,
                'supercategory': supercategory
            }
            categories_anno.append(cat_anno)
        return categories_anno
