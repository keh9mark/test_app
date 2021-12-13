import os
import csv
import random

FOLDER_NAME = 'static'


def generate():
    category_list = ["category_%s" % order for order in range(0, 10)]
    catalog_structure = []
    for image in os.listdir(FOLDER_NAME):
        catalog_structure.append([
            "http://localhost:8080/%s/%s" % (FOLDER_NAME, image),
            random.randint(2, 10),
            *random.sample(category_list, random.randint(1, 5))
        ])

    with open('catalog.csv', 'w') as myfile:
        wr = csv.writer(myfile, delimiter=';')
        for k in catalog_structure:
            wr.writerow(k)
    return


if __name__ == '__main__':
    generate()
