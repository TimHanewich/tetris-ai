import keras
import random
import numpy

inputs = keras.layers.Input(shape=(2,))
h1 = keras.layers.Dense(30, "relu")
h2 = keras.layers.Dense(20, "relu")
h3 = keras.layers.Dense(10, "relu")
outputs = keras.layers.Dense(1)

model = keras.Sequential()
model.add(inputs)
model.add(h1)
model.add(h2)
model.add(h3)
model.add(outputs)

model.compile("adam", "mean_squared_error")

for _ in range(0, 500):

    x1:int = random.randint(0, 100)
    x2:int = random.randint(0, 100)
    y:int = x1 * x2

    x_train = [[x1, x2]]
    y_train = [y]

    x_train = numpy.array(x_train)
    y_train = numpy.array(y_train)

    model.fit(x_train, y_train, epochs=10)
