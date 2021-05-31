import cv2
import glob
import os
import numpy as np

def load_data():
    filenames = glob.glob(r"./train/data/*.txt")
    # filenames=glob.glob(r"./test/data/*.txt")  # 获取文件名
    for i in range(0,len(filenames)):
        f=open(filenames[i])
        data = []
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            # print(line)
            data.append(line)
        data=get_boxes(data,filenames[i].split('/')[2].split('\\')[1].split('.')[0])
        rename=filenames[i].split('/')[2].split('\\') # 获取新文件名
        # print(rename)
        f = open("./train/dataset_label_boxes/{}.txt".format(rename[1].split('.')[0]), 'w')
        # f=open("./test/dataset_label_boxes/{}.txt".format(rename[1].split('.')[0]),'w')
        f.write(''.join(data))
        # print(i,filenames[i])
    return data

# 通过中心点获取边框坐标，便于检测分类
def get_boxes(data,filename):
    x=[]
    y=[]
    update_data=[]
    for line in data:
        temp=line.split(',')
        x.append(int(temp[0]))
        y.append(int(temp[1]))
    y_sort=sorted(y)  # 从上到下绘制边框
    for i in range(0,len(data)):  # 中心点坐标x[index_x],y_sorted[i]
        index=y.index(y_sort[i])  # 排序后y对应的data列表和x列表下标
        if i==0:
            height = y_sort[i+1] - y_sort[i]  # 一半高度
        elif i==len(data)-1:
            height=y_sort[i]-y_sort[i-1]
        else:
            height=(y_sort[i+1]-y_sort[i-1])/2
        width=int(height*1.4)  # 一半宽度
        # 矩形边框左上角坐标和右下角坐标
        left_top_x=x[index]-width
        left_top_y=y_sort[i]-height
        right_bottom_x=x[index]+width
        right_bottom_y=y_sort[i]+height
        # print(i,x[index_x],y_sort[i],left_top_x,left_top_y,right_bottom_x,right_bottom_y,width,height)
        # 画图检验边框
        # import matplotlib.pyplot as plt
        # image_array=cv2.imread('./test/data/'+filename+'.jpg')
        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        # plt.plot(x[index],y_sort[i],'om')
        # plt.plot(left_top_x,left_top_y,'ob')
        # plt.plot(right_bottom_x,right_bottom_y,'oy')
        # rect = plt.Rectangle((left_top_x, left_top_y), width*2, height*2, fill=False, edgecolor='red', linewidth=1)
        # ax.add_patch(rect)
        # plt.imshow(image_array)  # 图像数组
        # plt.show()
        new=data[index].split(',')
        print(new)
        new[0]=str(int(left_top_x))+','+str(int(left_top_y))
        new[1]=str(int(right_bottom_x))+','+str(int(right_bottom_y))
        update_data.append(','.join(new)+'\n')
        # 椎间盘label调整顺序
        # print(i,index)
        # if i%2==0:
        #     update_data = change_order(i,update_data)
    return update_data

# 调整label顺序，目的为使label以{'identification'：''，'disc/vertebra'：''}形式呈现，但是效果不佳，需要进一步修改
def change_order(index,data):
    update_new=data
    # print(data,index)
    split=update_new[index].split('{')
    xy=split[0]
    temp=split[1].strip('}\n').split('\'')
    # print(temp)
    new_label='{\''+temp[5]+'\''+temp[6]+'\''+temp[7]+'\', \''+temp[1]+'\''+temp[2]+'\''+temp[3]+'\'}\n'
    # print(new_label)
    update_new[index]=xy+new_label
    # print(update_new)
    return update_new

if __name__ == '__main__':
    load_data()
