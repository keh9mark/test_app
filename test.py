from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.pyplot as plt


dog = [10, 20, 15, 10]
activity = [5, 30, 150, 5]

fig, ax = plt.subplots()
ax.plot(activity, dog)
ax.grid(True)

ax.scatter([5, 30, 150], [10, 20, 15])

ax.text(
  5,
  10,
  "А \nS1=10,5+j30 \nI=30%, II=40%, III=30% \nUном=10, Кз=1.6",
  {},
  rotation=0,
)

ax.legend()


plt.show()
