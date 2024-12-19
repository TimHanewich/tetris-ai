import numpy as np
import keras

input_board = keras.layers.Input(shape=(2, 2, 1))
carry = keras.layers.Conv2D(1, (2,2), activation="relu")(input_board)
carry = keras.layers.Flatten()(carry)
carry = keras.layers.Dense(20, activation="relu")(carry)

model = keras.Model(inputs=input_board, outputs=carry)

x_data = [[0,0],[0,0]]
x_data = np.array([x_data])

v = model.predict(x_data)