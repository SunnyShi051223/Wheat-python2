import os
import random
import numpy as np
import joblib
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import lightgbm as lgb
import tensorflow as tf


seed_value = 42
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

img_height, img_width = 200, 200

def build_feature_extractor(input_shape):
    inputs = Input(shape=input_shape)
    x = Conv2D(16, (3, 3), strides=1, padding='same', activation='relu')(inputs)
    x = MaxPooling2D((2, 2), strides=2)(x)
    x = Conv2D(32, (3, 3), strides=1, padding='same', activation='relu')(x)
    x = MaxPooling2D((2, 2), strides=2)(x)
    features = Flatten()(x)
    model = Model(inputs=inputs, outputs=features)
    return model

feature_extractor = build_feature_extractor((img_height, img_width, 3))

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(img_height, img_width))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# ===== 对外接口函数 =====
def predict_image(image_path):
    """输入图片路径，返回(预测类别, 各类别概率列表)"""
    # 1. 预处理
    img_array = load_and_preprocess_image(image_path)
    features = feature_extractor.predict(img_array)

    # 2. 加载模型（可以考虑提前 load 一次，或改为全局变量）
    scaler = joblib.load('model/scaler.pkl')
    pca = joblib.load('model/pca.pkl')
    gbm = lgb.Booster(model_file='model/lgb_model.txt')

    # 3. 转换 & 预测
    features_scaled = scaler.transform(features)
    features_pca = pca.transform(features_scaled)
    pred_probs = gbm.predict(features_pca)[0]
    pred_class_index = np.argmax(pred_probs)

    class_labels = ['0', '1', '2', '3', '4']
    return class_labels[pred_class_index], list(pred_probs)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", type=str, required=True)
    args = parser.parse_args()
    cls, probs = predict_image(args.image)
    print("预测类别：", cls)
    for idx, p in enumerate(probs):
        print(f"  类别 {idx}：{p:.4f}")
