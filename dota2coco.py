import os
from dataset2coco import Dataset2COCO
import cv2
from shapely.geometry import Polygon

"""
将DOTA1.5数据集转换为COCO instance数据集格式
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


class DOTA2COCO:
    def __init__(self, image_path, label_path, categories):
        self.image_path = image_path
        self.label_path = label_path
        self.categories = categories

    def _load_files(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError(file_path + " not exists")
        return os.listdir(file_path)

    def _txt2anno(self, label_name):
        txt_anno = []
        with open(os.path.join(self.label_path, label_name), 'r', encoding='utf-8') as f:
            for line in f:
                anno = {}
                items = line.strip().split(' ')
                segmentation = [int(float(x)) for x in items[:8]]
                points = [(float(items[i]), float(items[i + 1])) for i in range(0, 8, 2)]
                category = items[8]
                category_id = self.categories.index(category) + 1
                area = Polygon(points).area
                xmin, ymin, xmax, ymax = min(segmentation[::2]), min(segmentation[1::2]), \
                                         max(segmentation[::2]), max(segmentation[1::2])
                bbox = [xmin, ymin, xmax - xmin, ymax - ymin]
                anno['segmentation'] = [segmentation]
                anno['area'] = area
                anno['bbox'] = bbox
                anno['iscrowd'] = 0
                anno['category_id'] = category_id
                txt_anno.append(anno)
        return txt_anno

    def _image2anno(self, file_name):
        image_anno = {}
        img = cv2.imread(os.path.join(self.image_path, file_name))
        h, w = img.shape[:2]
        image_anno['file_name'] = file_name
        image_anno['height'] = h
        image_anno['width'] = w
        return image_anno

    def _generate_data(self, cut):
        images = self._load_files(self.image_path)
        if cut:
            images = images[cut[0]: cut[1]]
        results = []
        for image in images:
            print('current image: ', image)
            image_anno = self._image2anno(image)
            label = image.split('.')[0] + '.txt'
            txt_anno = self._txt2anno(label)
            image_anno['annos'] = txt_anno
            results.append(image_anno)
        return results

    def dota2coco(self, info, output_path, cut=None):
        print('start converting.')
        results = self._generate_data(cut)
        d2c = Dataset2COCO()
        d2c.dataset2coco(results, categories, info, output_path)
        print('convert successful.')


if __name__ == '__main__':
    categories = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle',
                  'ship', 'tennis-court',
                  'basketball-court', 'storage-tank', 'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool',
                  'helicopter', 'container-crane']
    image_path = r'D:\BaiduNetdiskDownload\DOTA\train-split\images'
    label_path = r'D:\BaiduNetdiskDownload\DOTA\train-split\labelTxt'
    output_path = r'D:\BaiduNetdiskDownload\DOTA\train-split'
    info = {
        "description": "Dataset2COCO example ",
        "version": "1.0",
        "year": 2020,
        "contributor": "fishawd",
        "date_created": "2020/08/08"
    }
    d2c = DOTA2COCO(image_path, label_path, categories)
    # cut为空表示转换全部数据
    # 只需要转换部分数据,cut可以指定下标范围m~n
    d2c.dota2coco(info, output_path, cut=[12348, 14348])
