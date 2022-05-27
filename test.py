import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def make_graph_image(items, merge_info):
  x_ = []
  y_ = []
  points_x = []
  points_y = []

  sorted_merge = []

  for merge in merge_info:
    first = merge[0]
    second = merge[1]
    sorted_merge.append(first)
    x_.append(items[first]["x"])
    y_.append(items[first]["y"])
    points_x.append(items[first]["x"])
    points_y.append(items[first]["y"])

  x_.append(items[second]["x"])
  y_.append(items[second]["y"])

  fig = plt.figure()
  gs = gridspec.GridSpec(1, 3)
  ax = fig.add_subplot(gs[0, :2])

  ax.plot(x_, y_, color="k")

  ax.grid(True)

  ax.scatter(points_x, points_y, color="k")

  for x, y, point in zip(points_x, points_y, sorted_merge):
    ax.text(
      x - 10,
      y + 2.5,
      f"{point}({x},{y})",
      {},
      rotation=0,
      bbox=dict(
        boxstyle="square",
        ec=(0, 0, 0),
        fc=(1, 1, 1),
      ),
    )

  x_coord = 0
  y_coord = 1
  if len(items) == 6:
    y_coord = 0.9

  ax = fig.add_subplot(gs[0, 2])

  for point, info in items.items():
    ax.text(
      x_coord,
      y_coord,
      f"({point}) {info['S']} \n{info['proc']} \nU={info['Unom']}, кз=1.6",
      {},
      rotation=0,
      bbox=dict(
        boxstyle="square",
        ec=(0, 0, 0),
        fc=(1, 1, 1),
      ),
    )
    y_coord -= 0.18

  ax.set_axis_off()

  plt.xticks([])
  plt.yticks([])

  image_name = "myimage.png"
  plt.savefig(image_name)
  return image_name


def create_power_flow_image(merge_info):
  # предполагаем что начинается и заканчивается на Источник А
  x_start = 1
  y_start = 0.5
  fig, ax = plt.subplots()

  # расставим точки
  points = {}
  x_list = []
  y_list = []
  for attached in merge_info:
    first = attached[0]
    second = attached[1]
    if first == "A":
      points[first] = {"x": x_start, "y": y_start}
      x_list.append(x_start)
      y_list.append(y_start)
      ax.text(
        x_start,
        y_start + 0.03,
        f"{first}",
        {},
        rotation=0,
        bbox=dict(
          boxstyle="square",
          ec=(0, 0, 0),
          fc=(1, 1, 1),
        ),
      )
      x_start += 2
    points[second] = {"x": x_start, "y": y_start}
    ax.text(
      x_start,
      y_start + 0.03,
      f"{second}",
      {},
      rotation=0,
      bbox=dict(
        boxstyle="square",
        ec=(0, 0, 0),
        fc=(1, 1, 1),
      ),
    )
    x_list.append(x_start)
    y_list.append(y_start)
    if second in ["B", "1", "2", "3", "4", "5"]:
      load_x = x_start
      load_y = y_start - 0.2
      x_list.append(load_x)
      y_list.append(load_y)
    x_start += 2
  ax.scatter(x_list, y_list, color="k")

  axes = plt.gca()
  axes.set_xlim([0, x_start])
  axes.set_ylim([0, 1])
  plt.show()


if __name__ == "__main__":
  items = {
    "A": {
      "x": 10,
      "y": 40,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=30%, II=40%, III=30%",
      "Unom": 6,
    },
    "B": {
      "x": 70,
      "y": 20,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=0%, II=70%, III=30%",
      "Unom": 6,
    },
    "1": {
      "x": 30,
      "y": 80,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=30%, II=40%, III=30%",
      "Unom": 6,
    },
    "2": {
      "x": 90,
      "y": 60,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=30%, II=40%, III=30%",
      "Unom": 6,
    },
    "3": {
      "x": 40,
      "y": 10,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=30%, II=40%, III=30%",
      "Unom": 6,
    },
    "4": {
      "x": 90,
      "y": 10,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=30%, II=40%, III=30%",
      "Unom": 6,
    },
    "5": {
      "x": 40,
      "y": 40,
      "S": "S=10+j40",
      "coef": "Кз=1,3",
      "proc": "I=30%, II=40%, III=30%",
      "Unom": 6,
    },
  }

  merge_info = ["A1", "12", "2B", "B4", "43", "35", "5A"]

  # make_graph_image(items=items, merge_info=merge_info)
  create_power_flow_image(merge_info)
