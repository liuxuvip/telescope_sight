# cut an image into parts by object number from VOC XML.
# apple optical sight on VOC for train
import os
import sys
import random

import numpy as np
import tensorflow as tf
import cv2
import xml.etree.ElementTree as ET

from datasets.dataset_utils import int64_feature, float_feature, bytes_feature
from datasets.pascalvoc_common import VOC_LABELS

from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os, sys
def make_xml(xmwidth, xmheight, label_text, xmin_tuple, ymin_tuple, xmax_tuple, ymax_tuple, image_name):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name + '.jpg'
    node_object_num = SubElement(node_root, 'object_num')
    node_object_num.text = str(len(xmin_tuple))
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = xmwidth
    node_height = SubElement(node_size, 'height')
    node_height.text = xmheight
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for i in xrange(len(xmin_tuple)):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = label_text
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(xmin_tuple[i])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(ymin_tuple[i])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(xmax_tuple[i])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(ymax_tuple[i])
    xml = tostring(node_root, pretty_print = True)
    dom = parseString(xml)
    # print xml
    return dom
data_path = '/home/bidlc/optical_sight/dataexam/'
old_image_path = '/home/bidlc/optical_sight/dataexam/image/'
old_xml_path = '/home/bidl/optical_sight/dataexam/labelxml/'
mumimg = len(os.listdir(old_image_path))
img_Lists = os.listdir(old_image_path)
for findex in range(len(img_Lists)):

    # Read the image file.
    filenameimg = old_image_path+img_Lists[findex]
    # image_data = tf.gfile.FastGFile(filename, 'r').read()
    img = cv2.imread(filenameimg)
    # Read the XML annotation file.
    # filename = os.path.join("/home/bidlc/optical_sight/dataexam/labelxml/006644.xml")
    filename = os.path.join(old_xml_path+img_Lists[findex][0:6]+".xml")

    tree = ET.parse(filename)
    root = tree.getroot()

    # Image shape.
    size = root.find('size')
    shape = [int(size.find('height').text),
             int(size.find('width').text),
             int(size.find('depth').text)]
    # Find annotations.
    bboxes = []
    bboxes_orig = []
    labels = []
    labels_text = []
    difficult = []
    truncated = []
    for obj in root.findall('object'):
        label = obj.find('name').text
        labels.append(int(VOC_LABELS[label][0]))
        labels_text.append(label.encode('ascii'))

        if obj.find('difficult'):
            difficult.append(int(obj.find('difficult').text))
        else:
            difficult.append(0)
        if obj.find('truncated'):
            truncated.append(int(obj.find('truncated').text))
        else:
            truncated.append(0)

        bbox = obj.find('bndbox')
        bboxes.append((float(bbox.find('ymin').text) / shape[0],
                       float(bbox.find('xmin').text) / shape[1],
                       float(bbox.find('ymax').text) / shape[0],
                       float(bbox.find('xmax').text) / shape[1]
                       ))
        bboxes_orig.append((int(bbox.find('ymin').text),
                   int(bbox.find('xmin').text),
                   int(bbox.find('ymax').text),
                   int(bbox.find('xmax').text)
                   ))

    for index in range(len(bboxes_orig)):
        # orignal box in the image
        # imgm = img[bboxes_orig[index][0]:bboxes_orig[index][2],bboxes_orig[index][1]:bboxes_orig[index][3]]
        # cut box with extral pixel
        new_x1 = random.randint(bboxes_orig[index][0]-bboxes_orig[index][0]/4, bboxes_orig[index][0])
        new_x2 = random.randint(bboxes_orig[index][2], (bboxes_orig[index][2]+(shape[0]-bboxes_orig[index][2])/4))

        new_y1 = random.randint(bboxes_orig[index][1]-bboxes_orig[index][1]/4, bboxes_orig[index][1])
        new_y2 = random.randint(bboxes_orig[index][3], (bboxes_orig[index][3]+(shape[1]-bboxes_orig[index][3])/4))
        # box in the new pacth
        real_x1 = bboxes_orig[index][0] - new_x1
        real_x2 = bboxes_orig[index][2] - new_x1
        real_y1 = bboxes_orig[index][1] - new_y1
        real_y2 = bboxes_orig[index][3] - new_y1

        imgm = img[new_x1:new_x2,new_y1:new_y2]

        imgmr = imgm[real_x1:real_x2,real_y1:real_y2]
        label = labels[index]
        label_text = labels_text[index]
        xmwidth = str(imgm.shape[0])
        xmheight = str(imgm.shape[1])

        xmin_tuple = [real_x1]
        xmax_tuple = [real_x2]
        ymin_tuple = [real_y1]
        ymax_tuple = [real_y2]

        image_name = img_Lists[findex][0:6]+'extr'+str(index)

        dom = make_xml(xmwidth, xmheight, label_text, xmin_tuple, ymin_tuple, xmax_tuple, ymax_tuple, image_name)
        imgext_name = os.path.join(data_path + 'extimg/'+image_name + '.jpg')
        cv2.imwrite(imgext_name, imgm)
        xml_name = os.path.join(data_path + 'extxml/'+image_name + '.xml')
        with open(xml_name, 'w') as f:
            f.write(dom.toprettyxml(indent='\t', encoding='utf-8'))

        # resizedimgm =cv2.resize(imgm,dim,interpolation = cv2.INTER_AREA)
        # imgname = "cutbox_rs" + str(index) + ".jpg"
        # cv2.imwrite(imgname, resizedimgm)
        # imgname = "VOCcut" + str(index) + ".jpg"
        # cv2.imwrite(imgname, imgm)
        # cv2.imshow('imgname',imgmr)
        # cv2.waitKey(0)

    print "image num", findex, len(img_Lists)
