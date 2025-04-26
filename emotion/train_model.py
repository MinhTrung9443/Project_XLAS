import os
import cv2
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, EarlyStopping

# Thông số
IMG_SIZE = (48, 48)
BATCH_SIZE = 32
EPOCHS = 50

# Đường dẫn đến thư mục data
data_dir = 'data'  # Thay đổi nếu cần
train_dir = os.path.join(data_dir, 'train')
test_dir = os.path.join(data_dir, 'test')

# Các lớp cảm xúc
emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

def load_data(directory):
    images = []
    labels = []
    
    for idx, emotion in enumerate(emotions):
        emotion_dir = os.path.join(directory, emotion)
        for img_name in os.listdir(emotion_dir):
            img_path = os.path.join(emotion_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, IMG_SIZE)
            images.append(img)
            labels.append(idx)
    
    return np.array(images), np.array(labels)

# Load dữ liệu
X_train, y_train = load_data(train_dir)
X_test, y_test = load_data(test_dir)

# Reshape và chuẩn hóa
X_train = X_train.reshape((-1, *IMG_SIZE, 1)) / 255.0
X_test = X_test.reshape((-1, *IMG_SIZE, 1)) / 255.0

# Chuyển labels sang one-hot encoding
y_train = to_categorical(y_train, num_classes=len(emotions))
y_test = to_categorical(y_test, num_classes=len(emotions))

# Data augmentation
train_datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Xây dựng model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(*IMG_SIZE, 1)),
    BatchNormalization(),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    Conv2D(64, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    Conv2D(128, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    Conv2D(256, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(emotions), activation='softmax')
])

model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# Callbacks
checkpoint = ModelCheckpoint('best_model.h5', 
                            monitor='val_accuracy', 
                            save_best_only=True, 
                            mode='max')
early_stop = EarlyStopping(monitor='val_accuracy', 
                          patience=10, 
                          restore_best_weights=True)

# Train model
history = model.fit(
    train_datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
    steps_per_epoch=len(X_train) // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(X_test, y_test),
    callbacks=[checkpoint, early_stop]
)

# Lưu model cuối cùng
model.save('emotion_detection_model.h5')
print("Model đã được lưu thành công!")