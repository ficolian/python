from matplotlib import pyplot as plt
import numpy as np

measurement = [45, 48, 49, 41, 42, 60, 46, 47, 42, 46, 47, 41, 40, 43, 45, 46, 43, 45, 46, 41, 39, 45, 48, 42, 43, 44, 45, 46, 47, 42,
 40, 41, 41, 61, 45, 45, 43, 42, 42, 40]
actual = 45
initial_estimate = 60  # actually this can be anything
initial_error_estimate = 2
error_in_measurement = 4
current_estimate = initial_estimate
current_error_estimate = initial_error_estimate
kalman_output_list = []
kalman_output_list.append(initial_estimate)
for i in range(len(measurement)):
    kalman_gain = (current_error_estimate) / (current_error_estimate + error_in_measurement)
    kalman_output = (current_estimate + (kalman_gain) * (measurement[i] - current_estimate))
    kalman_output_list.append(kalman_output)

    new_error_estimate = (1 - kalman_gain) * (current_error_estimate)
    current_estimate = kalman_output
    current_error_estimate = new_error_estimate
plt.title('One Dimensional Kalman Filter Output')
plt.xlabel('Time')
plt.ylabel('Temperature in degrees')
plt.plot(measurement, label='Measuerements from the thermometer')
plt.axhline(y=actual, color='r', linestyle='-', label='Actual Temperature')
plt.plot(kalman_output_list, '-g', label='kalman output')
plt.axis([0, len(measurement) - 1, 0, 110])
plt.legend()
plt.show()