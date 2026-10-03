import matplotlib.pyplot as plt
import numpy as np

# Generate a hypothetical cumulative regret curve
n = 1000
x = np.linspace(1, n, n)
y = np.log(x)  # The regret increases initially but then slows down

# Plot the curve
plt.plot(x, y)
plt.xlabel('Time step')
plt.ylabel('Cumulative regret')
plt.title('Hypothetical cumulative regret curve for Thompson Sampling')
plt.grid(True)
plt.show()
