import os
os.environ['KERAS_HOME'] = 'C:/Users/Dell/.keras/models/'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Giảm verbosity của TensorFlow

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import MobileNetV2
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.optimizers import Adam

# Thông số
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50  # Tăng epochs để có không gian cho fine-tuning
NUM_CLASSES = 6
INIT_LR = 1e-4  # Learning rate ban đầu

# Đường dẫn dataset
dataset_path = "dataset"

# Data augmentation mạnh hơn
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

# Tăng số lượng augmentation
train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Kiểm tra class imbalance
class_counts = np.bincount(train_generator.labels)
class_weights = {i: 1./count for i, count in enumerate(class_counts) if count > 0}
class_weights = {k: v / min(class_weights.values()) for k, v in class_weights.items()}

def build_model():
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
    
    base_model.trainable = False
    
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    
    return model

model = build_model()

# Sử dụng learning rate nhỏ hơn
optimizer = Adam(learning_rate=INIT_LR)
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Callbacks được cải tiến
callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=15,  # Tăng patience
        min_delta=0.001,
        mode='max',
        restore_best_weights=True,
        verbose=1
    ),
    ModelCheckpoint(
        "best_model.h5",
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )
]

print("[INFO] Training base model...")
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=val_generator,
    validation_steps=val_generator.samples // BATCH_SIZE,
    epochs=EPOCHS // 2,  # Chỉ train một nửa epochs cho base model
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
)

# Fine-tuning
print("[INFO] Fine-tuning model...")
base_model = model.layers[0]
base_model.trainable = True

# Chỉ unfreeze các layer cuối
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Biên dịch lại với learning rate nhỏ hơn
model.compile(
    optimizer=Adam(learning_rate=INIT_LR/10),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Tiếp tục training
history_fine = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=val_generator,
    validation_steps=val_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    initial_epoch=history.epoch[-1] + 1,
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
)

# Lưu model cuối cùng
model.save('final_model.h5')
np.save('class_indices.npy', train_generator.class_indices)
print("[INFO] Training completed and models saved!")