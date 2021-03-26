import cv2
import numpy as np
import sys
import tensorflow as tf

IMG_WIDTH = 30
IMG_HEIGHT = 30

def load_test(file):
    images = []
    img = cv2.imread(file)
    rimg = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    images.append(rimg)
    return np.array(images)

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python test.py img_file model")

    model = tf.keras.models.load_model(sys.argv[2])
    test = load_test(sys.argv[1])
    #probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    prediction = model.predict(test)
    print(prediction)
    print(f'the picture is classified to {np.argmax(prediction)}')

if __name__ == '__main__':
    main()