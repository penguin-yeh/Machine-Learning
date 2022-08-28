# -*- coding: utf-8 -*-
"""resnet18.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pIOVgq9A-W9KTGI1HyDd2sUQ-pyBUgK4

## initial setup
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive')

# %cd /content/drive/MyDrive/Colab Notebooks/ai cup

"""## import """

from __future__ import print_function, division

!pip install --upgrade numpy

from torch.optim import lr_scheduler
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
import pandas as pd
from tqdm import tqdm

"""##  image pre-processing"""

# 資料轉換函數
data_transforms = {
    # 訓練資料集採用資料增強與標準化轉換
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224), # 隨機剪裁並縮放
        transforms.RandomHorizontalFlip(), # 隨機水平翻轉
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) # 標準化
    ]),
    # 驗證資料集僅採用資料標準化轉換
    'val': transforms.Compose([
        transforms.Resize(256),  # 縮放
        transforms.CenterCrop(224), # 中央剪裁
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) # 標準化
    ]),
}

!pwd

"""## get filename"""

class ImageFolderWithPaths(datasets.ImageFolder):
    """Custom dataset that includes image file paths. Extends
    torchvision.datasets.ImageFolder
    """

    # override the __getitem__ method. this is the method that dataloader calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns 
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # the image file path
        path = self.imgs[index][0]
        # make a new tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path

!pwd

"""## load data"""

# 資料集載入 =======================================================================
data_dir = './dataset/training'

image_datasets = {        
  x: ImageFolderWithPaths(    #默認已經將不同類型的image分成不同的folder
    os.path.join(data_dir, x), #path
    data_transforms[x]
  ) 
  for x in ['train', 'val']
}

#print(image_datasets['train'].imgs[22][0])  #class:train底下的已經分類好的img, type
                        # imgs[1][0] => 1st img's filename
                        # imgs[1][1] => 1st img's type 
#print(image_datasets['train'].imgs[22][1])
#print(image_datasets['train'].classes) #class:train底下的已經分類好的folder的name
#print(image_datasets['train'][7][1])  #1st: [7]=>7th img(from start)
                    #2nd: [0]=>img information
                    #   [1]=>label(folder name)

dataloaders = {    
  x: torch.utils.data.DataLoader(  #define how to sampling(batch...)
    image_datasets[x],       #dataset
    batch_size=8,         #how many samples per batch to load 
    shuffle=True,         #資料打亂 reshuffle at every epoch
    num_workers=2         #how many subprocess to load dataset
                    #0 => only main function => slow
                    #1 => only one subprocess => slow too
  )
  for x in ['train', 'val']
}
#print(dataloaders['train'])

## 取得訓練資料集與驗證資料集的資料量
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']} #how many img in train/val
print(dataset_sizes)

# 取得各類別的名稱
class_names = image_datasets['train'].classes
print(class_names)

#get data of batch size
inputs, classes, paths = next(iter(dataloaders['train']))
#classes_names = classes.tolist()
for i in range(5):
    #print(classes[i])
    #print(paths[i])
    idx = classes[i].item()
    #print(idx)
    #idx_string = str(idx)
    #print(idx_string)
    print(class_names[idx])

# 若 CUDA 環境可用，則使用 GPU 計算，否則使用 CPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

"""## look data"""

def tensor2img(inp):
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    return inp

col = {'filename':[], 'category':[]}

"""
col['filename'].append('apple')
col['filename'].append('banana')

col['category'].append(1)
col['category'].append(2)

col_df = pd.DataFrame(col)
col_df.to_csv('label.csv', index=False)
"""

#print(col['filename'])



"""## train model"""

# 將多張圖片拼成一張 grid 圖
#out = torchvision.utils.make_grid(inputs)

# 顯示圖片
#img = tensor2img(out)
#plt.imshow(img)
#plt.title([class_names[x] for x in classes])

# 訓練模型用函數
def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    since = time.time() # 記錄開始時間

    # 記錄最佳模型
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    best_1 = []
    best_2 = []

    # 訓練模型主迴圈
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # 對於每個 epoch，分別進行訓練模型與驗證模型
        for phase in ['train', 'val']:

            temp_1 = []
            temp_2 = []

            if phase == 'train':
                model.train()  # 將模型設定為訓練模式
            else:
                model.eval()   # 將模型設定為驗證模式

            running_loss = 0.0
            running_corrects = 0
            # 以 DataLoader 載入 batch 資料
            for inputs, labels, paths in tqdm(dataloaders[phase]):
                # 將資料放置於 GPU 或 CPU
                inputs = inputs.to(device)
                labels = labels.to(device)

                # 重設參數梯度（gradient）
                optimizer.zero_grad()

                # 只在訓練模式計算參數梯度
                with torch.set_grad_enabled(phase == 'train'):
                    # 正向傳播（forward）
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()  # 反向傳播（backward）
                        optimizer.step() # 更新參數
                '''    
                for item in paths:
                  path = os.path.dirname(item)
                  #print(path)
                  path = os.path.basename(path)
                  #print(path)
                '''
                
                # 計算統計值
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

                #temp = dict(zip(paths, preds))
                '''
                for item, x in zip(paths, labels):
                    print('filename : ' + item, end = ' ')
                    idx = x.item()
                    idx_string = str(idx)
                    print('labels : ',x.item(), end = ' ')
                    print('class : ',class_names.index(idx_string))
                '''

                #zip
                
                if phase == 'val':
                  for item, x in zip(paths, preds):
                    #print(item)
                    temp_1.append(os.path.basename(item))
                    #print(preds[0])
                    #print(x)
                    idx = x.item()
                    temp_2.append(class_names[idx])
                    #col_df = pd.DataFrame(col)
                    #col_df.to_csv('label.csv', index=False)
                    #print('filename = ' + os.path.basename(item), end=' ')
                    #print('class = ',x.item())
                
                """
                if phase == 'val':
                  for item in paths:
                    arr = ""
                    if item != ',':
                      arr = arr + item
                    arr = os.path.basename(arr)
                    print('filename = ' + arr, end='  ')
                """

            if phase == 'train':
                # 更新 scheduler
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # 記錄最佳模型
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                best_1 = temp_1
                best_2 = temp_2


    # 計算耗費時間
    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))

    # 輸出最佳準確度
    print('Best val Acc: {:4f}'.format(best_acc))

    # 載入最佳模型參數
    model.load_state_dict(best_model_wts)
    torch.save(model.state_dict(),"model.pt")

    #output csv
    col['filename'] = best_1
    col['category'] = best_2
    col_df = pd.DataFrame(col)
    col_df.to_csv('label.csv', index=False)
    return model

"""## fine-tuning model"""

# 載入 ResNet18 預訓練模型
model_ft = models.resnet18(pretrained=True)

# 取得 ResNet18 最後一層的輸入特徵數量
num_ftrs = model_ft.fc.in_features

# 將 ResNet18 的最後一層改為只有兩個輸出線性層
# 更一般化的寫法為 nn.Linear(num_ftrs, len(class_names))
model_ft.fc = nn.Linear(num_ftrs, 219)

# 將模型放置於 GPU 或 CPU
model_ft = model_ft.to(device)

# 使用 cross entropy loss
criterion = nn.CrossEntropyLoss()

# 學習優化器
optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

# 每 7 個 epochs 將 learning rate 降為原本的 0.1 倍
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

"""## start training"""

# 訓練模型
model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=25)

"""## predict model"""

# 使用模型進行預測，並顯示結果
def visualize_model(model, num_images=6):
    was_training = model.training # 記錄模型之前的模式
    model.eval() # 將模型設定為驗證模式

    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        # 以 DataLoader 載入 batch 資料
        for i, (inputs, labels) in enumerate(dataloaders['val']):
            # 將資料放置於 GPU 或 CPU
            inputs = inputs.to(device)
            labels = labels.to(device)

            # 使用模型進行預測
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            # 顯示預測結果與圖片
            for j in range(inputs.size()[0]):      #inputs.size() => torch.Size([4, 3, 224, 224])
                images_so_far += 1
                ax = plt.subplot(num_images//2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[preds[j]]))

                # 將 Tensor 轉為原始圖片
                img = tensor2img(inputs.cpu().data[j])

                ax.imshow(img)

                if images_so_far == num_images:
                    model.train(mode=was_training) # 恢復模型之前的模式
                    return

        model.train(mode=was_training) # 恢復模型之前的模式

# 以模型進行預測
#visualize_model(model_ft)