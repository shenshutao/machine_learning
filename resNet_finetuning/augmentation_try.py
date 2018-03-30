# import custom_image as image
import os
from custom_preprocess import preprocess_input, custom_load_img_padding, custom_load_img_random_crop
from keras.preprocessing import image

os.chdir('/Users/shutao/Desktop/image_classify_test/')


datagen = image.ImageDataGenerator(
        preprocessing_function=preprocess_input,
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        # samplewise_std_normalization=True,  # divide each input by its std
        # zca_whitening=True,  # apply ZCA whitening
        channel_shift_range=100,
        # rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.01,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.01,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False,
        # shear_range=0.05,
        # zoom_range=0.05,
        fill_mode='nearest')

# Customize image resize logic: padding / random crop
image.load_img = custom_load_img_padding
# image.load_img = custom_load_img_random_crop

for f in os.listdir('preview'):
    os.remove(os.path.join('preview', f))

i = 0
for batch in datagen.flow_from_directory(
        'train_all',
        target_size=(224, 224),
        batch_size=4,
        classes=['womenpeashoes'],
        class_mode='categorical',
        save_to_dir='preview', save_prefix='augment_result', save_format='jpeg'):
    i += 1
    if i > 1:
        break