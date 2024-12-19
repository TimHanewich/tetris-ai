import keras
import numpy as np


# build the neural net

input_piece = keras.layers.Input(shape=(4,))
carry_piece = keras.layers.Dense(16, "relu")(input_piece)
carry_piece = keras.layers.Dense(16, "relu")(carry_piece)
carry_piece = keras.layers.Dense(16, "relu")(carry_piece)
carry_piece = keras.layers.Dense(16, "relu")(carry_piece)

input_board = keras.layers.Input(shape=(32,))
carry_board = keras.layers.Dense(128, "relu")(input_board)
carry_board = keras.layers.Dense(128, "relu")(carry_board)
carry_board = keras.layers.Dense(128, "relu")(carry_board)
carry_board = keras.layers.Dense(128, "relu")(carry_board)

# combine the two
combined = keras.layers.concatenate([carry_piece, carry_board])
carry = keras.layers.Dense(256, "relu")(combined)
carry = keras.layers.Dense(256, "relu")(carry)
carry = keras.layers.Dense(256, "relu")(carry)
carry = keras.layers.Dense(256, "relu")(carry)
output = keras.layers.Dense(4, "softmax")(carry)

# construct the model
model = keras.Model(inputs=[input_piece, input_board], outputs=output)
model.compile("adam", "categorical_crossentropy")

# sample data
piece = [1,1,1,1]
board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

x1 = np.array([piece])
x2 = np.array([board])

v = model.predict([x1,x2])
print(v)

correct:list[int] = [0,0,1,0]
y = np.array([correct])

model.fit([x1,x2],y)