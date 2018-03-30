import os

from keras import backend as K
from keras import callbacks
from keras.applications.resnet50 import ResNet50, Flatten
from keras.layers import Dense
from keras.models import Model
from keras.optimizers import Nadam
from keras.preprocessing import image

from custom_split_data import split_data
from custom_predict_padding import do_predict
from custom_preprocess import preprocess_input, custom_load_img_padding


def train_resNet(train_data_dir, validate_data_dir, res_dir, model_file_name, weight_file_name, img_width=224,
                 img_height=224):
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    batch_size = 40

    train_datagen = image.ImageDataGenerator(
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

    validate_datagen = image.ImageDataGenerator(
        preprocessing_function=preprocess_input
        # zca_whitening=True
    )

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        classes=['BabyBibs', 'BabyHat', 'BabyPants', 'BabyShirt', 'PackageFart', 'womanshirtsleeve', 'womencasualshoes',
                 'womenchiffontop', 'womendollshoes', 'womenknittedtop', 'womenlazyshoes', 'womenlongsleevetop',
                 'womenpeashoes', 'womenplussizedtop', 'womenpointedflatshoes', 'womensleevelesstop', 'womenstripedtop',
                 'wrapsnslings'],
        class_mode='categorical')

    validate_generator = validate_datagen.flow_from_directory(
        validate_data_dir,
        target_size=(img_width, img_height),
        classes=['BabyBibs', 'BabyHat', 'BabyPants', 'BabyShirt', 'PackageFart', 'womanshirtsleeve', 'womencasualshoes',
                 'womenchiffontop', 'womendollshoes', 'womenknittedtop', 'womenlazyshoes', 'womenlongsleevetop',
                 'womenpeashoes', 'womenplussizedtop', 'womenpointedflatshoes', 'womensleevelesstop', 'womenstripedtop',
                 'wrapsnslings'],
        batch_size=batch_size,
        class_mode='categorical')

    # Use Padding
    image.load_img = custom_load_img_padding

    # # 3.model structure
    # # Base model Conv layers + Customize FC layers
    # # create the base pre-trained model with weights
    if K.image_data_format() == 'channels_first':
        the_input_shape = (3, img_width, img_height)
    else:
        the_input_shape = (img_width, img_height, 3)
    base_model = ResNet50(weights='imagenet', include_top=False,
                          input_shape=the_input_shape)  # don't include the top (final FC) layers.

    x = base_model.output
    x = Flatten(input_shape=base_model.output_shape[1:])(x)
    predictions = Dense(18, activation='softmax', name='fc18')(x)

    # first: train only the FC layers (which were randomly initialized)
    # i.e. freeze all convolutional resnet layers
    for layer in base_model.layers:
        layer.trainable = False

    # this is the final model we will train
    model = Model(inputs=base_model.input, outputs=predictions)
    model.summary()

    # # 4.compile the model (should be done *after* setting layers to non-trainable)
    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # check model layers
    for i, layer in enumerate(base_model.layers):
        print i, layer.name

    model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.n // batch_size,
        epochs=1,
        validation_data=validate_generator,
        validation_steps=validate_generator.n // batch_size)

    # # 6. fine tune.
    NB_IV3_LAYERS_TO_FREEZE = 141
    for layer in model.layers[:NB_IV3_LAYERS_TO_FREEZE]:
        layer.trainable = False
    for layer in model.layers[NB_IV3_LAYERS_TO_FREEZE:]:
        layer.trainable = True

    # fine tune: stochastic gradient descent optimizer
    model.compile(optimizer=Nadam(), loss='categorical_crossentropy', metrics=['accuracy'])

    # fine tune: train again for fine tune
    check_pointer1 = callbacks.ModelCheckpoint(monitor='val_acc', filepath=os.path.join(res_dir, weight_file_name),
                                               verbose=1, save_best_only=True, mode='auto', period=1)
    check_pointer2 = callbacks.ModelCheckpoint(monitor='val_acc', filepath=os.path.join(res_dir, model_file_name) + '.{epoch:02d}-{val_loss:.2f}',
                                               verbose=1, save_best_only=False, save_weights_only=False, mode='auto',
                                               period=1)
    model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.n // batch_size,
        epochs=4,
        validation_data=validate_generator,
        validation_steps=validate_generator.n // batch_size,
        callbacks=[check_pointer1, check_pointer2])

    model.save(os.path.join(res_dir, model_file_name))


if __name__ == "__main__":
    os.chdir('/Users/shutao/Desktop/image_classify_test/')
    # os.chdir('/home/users/nus/e0015130/shopee/')
    try:
        split_data('train_all', 'validate_all', 0.5)
        train_resNet('train_all', 'validate_all', 'resNet', 'resnet_padding.h5',
                    'tmp_weights_resnet_padding.h5', 224, 224)
        do_predict('resNet/resnet_padding.h5', 'resNet/tmp_weights_resnet_padding.h5', 224, 224, 'predict',
                   'resNet/output_result_resnet_padding_best.csv')
        do_predict('resNet/resnet_padding.h5', None, 224, 224,
                   'predict', 'resNet/output_result_resnet_padding_final.csv')

    except Exception as e:
        print e.message
