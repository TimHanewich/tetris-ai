import numpy as np
import tetris
import keras


# Example dimensions
board_height = 8
board_width = 4
piece_height = 2
piece_width = 2
channels = 1  # Single channel input

# Define the model (using the previous example)
input_board = keras.layers.Input(shape=(board_height, board_width, channels))
x_board = keras.layers.Conv2D(8, (2, 2), activation='relu')(input_board)
x_board = keras.layers.Flatten()(x_board)
x_board = keras.layers.Dense(128, activation='relu')(x_board)

input_piece = keras.layers.Input(shape=(piece_height, piece_width, channels))
x_piece = keras.layers.Conv2D(1, (2, 2), activation='relu')(input_piece)
x_piece = keras.layers.Flatten()(x_piece)
x_piece = keras.layers.Dense(128, activation='relu')(x_piece)

combined = keras.layers.concatenate([x_board, x_piece])
x = keras.layers.Dense(256, activation='relu')(combined)
output = keras.layers.Dense(4, activation='softmax')(x)

model = keras.Model(inputs=[input_board, input_piece], outputs=output)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

gs = tetris.GameState()
p = tetris.Piece()

# convert board and pieces to 0's and 1's
board:list[list[int]] = []
for row in gs.board:
    irow:list[int] = []
    for column in row:
        irow.append(int(column))
    board.append(irow)
piece:list[list[int]] = []
for row in p.squares:
    irow:list[int] = []
    for column in row:
        irow.append(int(column))
    piece.append(irow)

i_board = np.array([board])
i_piece = np.array([piece])

print(i_board)
print(i_piece)
input()

# Forward pass
predictions = model.predict([i_board, i_piece])
print(predictions)
print(str(type(predictions)))
