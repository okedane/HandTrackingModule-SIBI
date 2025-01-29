# -*- coding: utf-8 -*-
"""SIBI1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Dgt5zW1RMVrY_o6MxFHIdVG0KFweF3D
"""

from google.colab import drive
drive.mount('/content/drive')

!pip uninstall -y tensorflow fsspec mediapipe-model-maker

!pip install tensorflow==2.15.0
!pip install fsspec==2023.9.2
!pip install mediapipe-model-maker

from google.colab import files
import os
import tensorflow as tf
from mediapipe_model_maker import gesture_recognizer
import matplotlib.pyplot as plt

dataset_path = "/content/drive/MyDrive/Dataset_SIBIV2/training"

print(dataset_path)
labels = []
for i in os.listdir(dataset_path):
  if os.path.isdir(os.path.join(dataset_path, i)):
    labels.append(i)
labels.sort()
print(labels)

NUM_EXAMPLES = 5

for label in labels:
    label_dir = os.path.join(dataset_path, label)
    example_filenames = os.listdir(label_dir)

    # Dapatkan jumlah gambar yang tersedia
    available_examples = min(len(example_filenames), NUM_EXAMPLES)

    if available_examples == 0:
        print(f"Tidak ada gambar di folder {label}")
        continue

    # Buat subplot sesuai jumlah gambar yang ada
    fig, axs = plt.subplots(1, available_examples, figsize=(2*available_examples, 2))

    # Pastikan axs selalu berbentuk array
    if available_examples == 1:
        axs = [axs]

    # Loop sesuai jumlah gambar yang tersedia
    for i in range(available_examples):
        img_path = os.path.join(label_dir, example_filenames[i])
        try:
            axs[i].imshow(plt.imread(img_path))
            axs[i].get_xaxis().set_visible(False)
            axs[i].get_yaxis().set_visible(False)
        except Exception as e:
            print(f"Error membaca gambar {img_path}: {str(e)}")

    fig.suptitle(f'Showing {available_examples} examples for {label}')
    plt.show()

data = gesture_recognizer.Dataset.from_folder(
    dirname=dataset_path,
    hparams=gesture_recognizer.HandDataPreprocessingParams()
)
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

hParams = gesture_recognizer.HParams(epochs=250, batch_size=16, export_dir="exported_model")

options = gesture_recognizer.GestureRecognizerOptions(hparams=hParams)

model = gesture_recognizer.GestureRecognizer.create(
    train_data= train_data,
    validation_data=validation_data,
    options=options
)

model.export_model()
!ls exported_model

loss, acc = model.evaluate(test_data, batch_size=16)
print("[INFO] accuracy : {:.2f}%".format(acc*100))
print("[INFO] Loss:{}".format(loss))

files.download('exported_model/gesture_recognizer.task')

!zip -r /content/exported_model/