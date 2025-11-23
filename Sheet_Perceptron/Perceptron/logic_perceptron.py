import numpy as np


class Perceptron:

    def __init__(self, weights: list[int], bias: float) -> None:
        self.weights = np.array(weights)
        self.bias = bias

    def activation_function(self, x_vector: np.ndarray) -> int:
        return 1 if x_vector > 0 else 0

    def predict(self, inputs: list[int]) -> int:
        linear_output: np.ndarray = np.dot(inputs, self.weights) + self.bias
        return self.activation_function(linear_output)


# 1. Logisches UND (AND)
# Beide Eingaben muessen 1 sein, damit die Summe (1+1) den Bias (-1.5) ueberwindet.
perceptron_and: Perceptron = Perceptron(weights=[1, 1], bias=-1.5)

# 2. Logisches ODER (OR)
# Eine Eingabe von 1 reicht, um den niedrigen Bias (-0.5) zu ueberwinden.
perceptron_or: Perceptron = Perceptron(weights=[1, 1], bias=-0.5)

# 3. Logisches Komplement (NOT)
# Hat nur einen Input. Das Gewicht ist negativ, um das Signal umzukehren.
# Wenn Input 0: 0*-1 + 0.5 = 0.5 -> 1
# Wenn Input 1: 1*-1 + 0.5 = -0.5 -> 0
perceptron_not: Perceptron = Perceptron(weights=[-1], bias=0.5)


print("--- Test: Logisches UND (AND) ---")
test_data: list[tuple] = [(0, 0), (0, 1), (1, 0), (1, 1)]
for x1, x2 in test_data:
    output: float = perceptron_and.predict([x1, x2])
    print(f"Input: {x1}, {x2} -> Output: {output}")

print("\n--- Test: Logisches ODER (OR) ---")
for x1, x2 in test_data:
    output: float = perceptron_or.predict([x1, x2])
    print(f"Input: {x1}, {x2} -> Output: {output}")

print("\n--- Test: Komplement (NOT) ---")
test_data_not: list[int] = [0, 1]
for x in test_data_not:
    # Hinweis: Input muss als Array/Liste uebergeben werden
    output: float = perceptron_not.predict([x])
    print(f"Input: {x}    -> Output: {output}")
