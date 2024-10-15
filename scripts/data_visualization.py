import pandas as pd
import matplotlib.pyplot as plt

# Load Data
abnormal_temps = pd.read_csv('s3://your-bucket/iot_data/output/abnormal_temps.csv')

plt.figure(figsize=(10, 5))
plt.hist(abnormal_temps['temperature'], bins=30)
plt.title('Distribution of Abnormal Temperatures')
plt.xlabel('Temperature')
plt.ylabel('Frequency')
plt.show()
