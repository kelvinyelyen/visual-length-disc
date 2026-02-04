"""
THE INSIGHT
Goal: Find the PSE (Bias) and JND (Sensitivity)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. Load Data
df = pd.read_csv('my_psychophysics_data.csv')

# 2. Calculate Probabilities
# We group by the Ratio (x-axis) and get the mean of responses (y-axis).
# Since response is 0 or 1, the mean is the "Probability of saying Longer".
summary = df.groupby('ratio')['response'].mean().reset_index()
x_data = summary['ratio']
y_data = summary['response']

# 3. Define the Model (The Psychometric Function)
# We model the brain's decision as a Cumulative Distribution Function (CDF)
# of a Gaussian distribution.
# x = stimulus intensity
# mu = point of subjective equality (PSE)
# sigma = inverse of sensitivity (related to JND)
from scipy.stats import norm

def psychometric_function(x, mu, sigma):
    return norm.cdf(x, loc=mu, scale=sigma)

# 4. Fit the Model (Curve Fitting)
# We ask scipy: "Find the mu and sigma that best explain this data."
# initial guesses: mu=1.0 (no bias), sigma=0.1 (some noise)
popt, pcov = curve_fit(psychometric_function, x_data, y_data, p0=[1.0, 0.1])
pse, sigma = popt

# 5. Calculate Metrics
# JND is often defined as sigma * 0.6745 (the distance from 50% to 75% on a CDF)
jnd = sigma * 0.6745

print(f"--- RESULTS ---")
print(f"PSE (Bias): {pse:.4f} (Ideal is 1.0)")
print(f"JND (Sensitivity): {jnd:.4f} (Lower is better)")

# 6. Plotting
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, 'o', label='Raw Data', color='black')

# Generate smooth curve for plotting
x_smooth = np.linspace(min(x_data), max(x_data), 100)
y_smooth = psychometric_function(x_smooth, pse, sigma)
plt.plot(x_smooth, y_smooth, '-', label='Fitted Model', color='red')

# Visual markers
plt.axvline(pse, color='blue', linestyle='--', label=f'PSE = {pse:.3f}')
plt.axvline(pse + jnd, color='green', linestyle=':', label=f'JND = {jnd:.3f}')

plt.title('My Visual Length Discrimination')
plt.xlabel('Ratio (Test / Standard)')
plt.ylabel('Probability of responding "Test is Longer"')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()