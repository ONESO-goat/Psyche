import numpy as np

def brain_geometry(scale: float):
    theta = np.linspace(0, 2*np.pi, 400)

    left = (
        scale * 0.9 * np.cos(theta) - scale * 0.5,
        scale * np.sin(theta)
    )
    right = (
        scale * 0.9 * np.cos(theta) + scale * 0.5,
        scale * np.sin(theta)
    )

    folds = []
    for i in np.linspace(-0.6, 0.6, 6):
        folds.append((
            scale * (0.4 * np.cos(theta) + i),
            scale * (0.2 * np.sin(2 * theta))
        ))

    return left, right, folds

import matplotlib.pyplot as plt

def draw_brain(geometry):
    left, right, folds = geometry

    plt.figure(figsize=(4, 4))
    plt.plot(*left, color="black")
    plt.plot(*right, color="black")

    for f in folds:
        plt.plot(*f, color="gray", alpha=0.6)

    plt.axis("equal")
    plt.axis("off")
    plt.show()
size = 1.5   # try 0.5, 1.0, 2.0
import os
import sys
print(os.getcwd())
print(sys.path)
import numpy as np
import json_numpy
from datetime import datetime
stuff = {
    "hey": "hi there",
    "numpy": np.empty(5),
    "works": "works"
}
arr = np.array([0, 1, 2])
stuff = {
    "news": "I love eating cheese",
    "emoption": 'happy',
    "motivation": arr,
    "timestamp": datetime.utcnow().isoformat()
}
test = 'testJson.json'
with open(test, 'w') as f:
    json_numpy.dump(stuff, f, indent=2)


with open(test, 'r') as f:
    gang = json_numpy.load(f)
print(gang)

test33 = {'hi':5}
print(len(test33))