import numpy as np
import matplotlib.pyplot as plt


# Generate the data points.
# return X: array containing one data point per column : shape (2,m)
def generate_points(m=100, seed=42):
    rng = np.random.RandomState(seed)

    # Wir nutzen uniform für gleichmäßige Verteilung in [-1, 1]
    # (randint würde nur ganze Zahlen liefern, uniform ist hier präziser)
    X = rng.uniform(-1, 1, (2, m))

    return X


# Generate random decision boundary
# return w: weight vector representing decision boundary, of shape (3,1)
def random_boundary(seed=42):
    rng = np.random.RandomState(seed)

    # generate two random points A and B within [-1, 1]
    p1 = rng.uniform(-1, 1, 2)
    p2 = rng.uniform(-1, 1, 2)

    # calculate vector w
    # Wir nutzen homogene Koordinaten (Bias=1), um w durch Kreuzprodukt zu finden
    # P1_hom = [1, x1, y1], P2_hom = [1, x2, y2]
    vec_p1 = np.array([1, p1[0], p1[1]])
    vec_p2 = np.array([1, p2[0], p2[1]])

    # Das Kreuzprodukt liefert den Normalenvektor der Linie durch p1 und p2
    w = np.cross(vec_p1, vec_p2)

    w = np.reshape(w, (3, 1))
    return w


# Define function that calculates predictions
# input w : weight vector chracterising perceptron model : of shape (3,1)
# input X_ext : data matrix X, extended by a row of ones : of shape (3,m)
# return predictions : sign(w.transpose * x) : of shape (1,m)
def predict(w, X_ext):
    # Berechnung: w^T * X_ext
    # np.matmul(w.T, X_ext) ergibt shape (1, m)
    raw_output = np.matmul(w.T, X_ext)
    predictions = np.sign(raw_output)

    # np.sign gibt 0 zurück bei 0, wir wandeln 0 in 1 um (Konvention)
    predictions = np.where(predictions == 0, 1, predictions)

    predictions = np.reshape(predictions, (1, X_ext.shape[1]))
    return predictions


# Define function for weight update
# input w : current weight vector with shape (3,1)
# input x : misclassified data point (should have shape (3,1))
# input y : label of data point x (scalar)
# return new_w : updated weight vector
def weight_update(w, x, y, learning_rate):
    # Wir berechnen zuerst die aktuelle (falsche) Vorhersage h(x)
    # Hinweis: x muss shape (3,1) haben
    prediction = np.sign(np.dot(w.T, x))
    if prediction == 0:
        prediction = 1

    # Formel: w_new = w + alpha * (y_target - y_predicted) * x
    # (y - prediction) ist entweder +2 oder -2 bei einem Fehler.
    # Manchmal wird auch vereinfacht w = w + alpha * y * x genutzt.
    # Wir nehmen die exakte Formel aus deiner vorherigen Aufgabe:
    update_val = learning_rate * (y - prediction)

    new_w = w + update_val * x

    new_w = np.reshape(new_w, (3, 1))
    return new_w


# --- Setup Code ---
m = 100
X = generate_points(m)
X_ext = np.vstack((np.ones((1, X.shape[1])), X))
w = random_boundary()
Y = predict(w, X_ext)

# Initialize weight vector w_ with 0.
w_ = np.zeros((3, 1))
w_ = np.reshape(w_, (3, 1))

learning_rate = 1.0  # In der Aufgabe war alpha=1
num_iterations = 1000  # Erhöhe Iterationen etwas für Konvergenz

# initialize array to save number of misclassified points in each iteration
num_misses = np.zeros(num_iterations)

for i in range(num_iterations):
    # 1. calculate predictions for all points
    current_predictions = predict(w_, X_ext)  # Shape (1, m)

    # 2. identify indices of misclassified points
    # Vergleich: (1,m) == (1,m). np.where gibt Tuple zurück -> [1] sind die Spaltenindices
    misclassified_indices = np.where(current_predictions != Y)[1]

    # 3. calculate and save number of misclassified points
    miss_count = len(misclassified_indices)
    num_misses[i] = miss_count

    # break if there are none
    if miss_count == 0:
        print(f"Konvergenz erreicht nach {i} Schritten.")
        break

    # 4. select random misclassified index
    random_idx = np.random.choice(misclassified_indices)

    # Extrahiere x und y. WICHTIG: Reshape x zu (3,1) für Matrizenrechnung
    x_mis = X_ext[:, random_idx].reshape(3, 1)
    y_true = Y[0, random_idx]

    # 5. perform one weight update using datapoint at selected index
    w_ = weight_update(w_, x_mis, y_true, learning_rate)

# --- Ergebnis Visualisierung ---
plt.figure(figsize=(6, 6))
plt.plot(range(i + 1), num_misses[:i + 1])
plt.xlabel("Iteration")
plt.ylabel("Anzahl Fehler")
plt.title("Lernkurve")
plt.show()

print("Final Weights w_:\n", w_)

# Visualize
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(X[0, :], X[1, :], marker='o', c=Y.flatten(), s=25, edgecolor='k', cmap='bwr')
xp = np.array((-1, 1))
# Schutz gegen Division durch Null, falls w[2] sehr klein ist
if abs(w[2]) > 1e-10:
    yp = -(w[1] / w[2]) * xp - (w[0] / w[2])
    plt.plot(xp, yp, "g-", label="Target Boundary")

plt.axis([-1.1, 1.1, -1.1, 1.1])
plt.legend()
plt.title("Target Dataset")
plt.show()
