import os
import re

import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing import image

from custom_preprocess import preprocess_input, custom_load_img_padding


def do_predict(model_h5, weights_h5, img_width, img_height, input_folder, output_file):
    model = load_model(model_h5)
    if weights_h5 is not None:
        model.load_weights(weights_h5)

    rows = []
    column_names = ['id', 'category']
    for f in os.listdir(input_folder):
        if not f.startswith('.'):
            img = image.load_img(os.path.join(input_folder, f))
            # do padding
            img = custom_load_img_padding(img, target_size=[img_width, img_height])

            img_array = image.img_to_array(img)
            x = np.expand_dims(img_array, axis=0)
            x = preprocess_input(x)
            y_prob = model.predict(x)
            y_classes = y_prob.argmax(axis=-1)

            matchObj = re.match(r'Test_(.*).jpg', f, re.M | re.I)
            row = [str(matchObj.group(1)), str(y_classes[0])]
            rows.append(row)

    df = pd.DataFrame(rows, columns=column_names)
    df['id'] = df['id'].astype('int')
    df = df.sort_values('id')
    df.to_csv(output_file, index=False, header=True)


# if __name__ == "__main__":
#     os.chdir('/Users/shutao/Desktop/image_classify_test/')
#    # os.chdir('/home/users/nus/e0015130/shopee/')
#     do_predict('resNet/resnet_224_ft.h5', None, 224, 224, 'predict', 'result/output_result_random_20180325001.csv')
