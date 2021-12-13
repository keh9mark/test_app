import csv


class IMGSimple(object):

    def __init__(self, catalog, name=''):
        self._id = id(self)
        self._catalog = catalog
        self._name = name if name != '' else 'IMG %s' % self.get_id()

    def __str__(self):
        return '<%s => %s>' % (self.__class__.__name__, self.get_id())

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_catalog(self):
        return self._catalog


class IMGCategory(IMGSimple):

    def __init__(self, catalog, name):
        super().__init__(catalog, name)
        self._images = {}

    def set_image(self, image_obj):
        self._images[image_obj.get_id()] = image_obj
        return

    def images(self):
        return self._images.values()

    def get_balance(self):
        balance = 0
        for image_obj in self.images():
            balance += image_obj.get_balance()
        return balance

    def calc_probability_images(self):
        _table = {}
        balance = self.get_balance()
        for image in self.images():
            if balance == 0.0:
                value = 0.0
            else:
                value = float(image.get_balance()) / float(balance)
            _table[image.get_id()] = value
        return _table


class IMGimage(IMGSimple):

    def __init__(self, catalog, name, path_to_item, number_of_view):
        super().__init__(catalog, name)
        self._path = path_to_item
        self._number_of_view = number_of_view
        self._balance = number_of_view
        self._categories = {}

    def set_category(self, category_obj):
        self._categories[category_obj.get_name()] = category_obj
        category_obj.set_image(self)
        return

    def get_balance(self):
        return self._balance

    def decrease_display(self):
        self._balance -= 1
        return

    def get_path(self):
        return self._path


class IMGCatalog(object):

    def __init__(self, catalog_file_name='catalog.csv'):
        self.catalog_file_name = catalog_file_name
        self._table_image = {}
        self._table_category = {}
        self._create_images_table()
        self.previous_pictures = None

    def __str__(self):
        result = 'Оставшиеся картинки:'
        for category_obj in self.categories():
            statistic = ''
            for image in category_obj.images():
                statistic = "%s\n Показов осталось: _%s Изображение:_%s" % (
                    statistic, image.get_name(), image.get_balance()
                )
            result = "%s\n Категория:_ %s: %s\n" % (
                result, category_obj.get_name(), statistic
            )
        return result

    def categories(self):
        return self._table_category.values()

    def _create_images_table(self):
        with open(self.catalog_file_name, newline='') as catalog_data:
            for image_row in csv.reader(catalog_data):
                self.create_image(image_row[0].split(';'))
        return

    def decrease_display_image(self, image_id):
        image = self.get_image(image_id)
        image.decrease_display()
        return image

    def create_image(self, image_item):
        path_to_item = image_item[0]
        image_obj = IMGimage(
            catalog=self,
            name=path_to_item.split('/')[-1],
            path_to_item=image_item[0],
            number_of_view=int(image_item[1])
        )
        self._table_image[image_obj.get_id()] = image_obj
        for position in range(2, len(image_item)):
            category = image_item[position]
            if category not in self._table_category:
                category_obj = self.create_category(category)
            else:
                category_obj = self.get_category(category)
            image_obj.set_category(category_obj)
        return

    def get_category(self, category_name):
        return self._table_category.get(category_name)

    def get_image(self, image_id):
        return self._table_image.get(image_id)

    def images(self):
        return self._table_image.values()

    def create_category(self, category_name):
        category_obj = IMGCategory(
            catalog=self,
            name=category_name
        )
        self._table_category[category_obj.get_name()] = category_obj
        return category_obj

    def get_numerous_item(self):
        _for_numerous = {}
        for image in self.images():
            _for_numerous[image.get_id()] = image.get_balance()
        _images_sort = sorted(_for_numerous.items(), key=lambda item: item[1])
        last_value = _images_sort[-1]
        image_id = _images_sort[-1][0]
        if last_value[1] == 0.0:
            return
        if last_value[0] == self.previous_pictures:
            if len(_images_sort) > 1:
                alternative = _images_sort[-2]
                if alternative[1] == 0.0 and last_value[1] != 0.0:
                    image_id = alternative[0]
                else:
                    image_id = last_value[0]
        return image_id

    def request_image(self, list_of_categories=[]):
        if len(list_of_categories) == 0:
            image = self.get_numerous_item()
        else:
            image = self.caclculate_probability_images(list_of_categories)
        if image is None:
            return
        else:
            image = self.decrease_display_image(image)
            self.previous_pictures = image.get_id()
            return image.get_path()

    def caclculate_probability_images(self, list_of_categories):
        _table_probability = {}
        order = 0.0
        for category in list_of_categories:
            category_obj = self.get_category(category)
            order += 1
            _table_probability[
                category
            ] = category_obj.calc_probability_images()
        _images = set()
        for images_structure in _table_probability.values():
            _images = _images | set(images_structure.keys())
        _results_probability = {}
        for image_id in _images:
            _image_value = 0.0
            for category_value in _table_probability.values():
                _image_value += category_value.get(image_id, 0.0)
            _results_probability[image_id] = _image_value * (1 / order)
        single_images, return_image, alternative = [], None, None
        for_sorted = {}
        for image, value in _results_probability.items():
            if value == 1.0:
                single_images.append(image)
            elif value == 0.0:
                continue
            else:
                for_sorted[image] = value
        sorted_tuples = sorted(for_sorted.items(), key=lambda item: item[1])
        if len(sorted_tuples) > 1:
            return_image = sorted_tuples[-1]
            alternative = sorted_tuples[-2]
        elif len(sorted_tuples) == 1:
            return_image = sorted_tuples[-1]
        if return_image is None:
            for single_exp in single_images:
                if single_exp != self.previous_pictures:
                    return single_exp
            if (self.previous_pictures is None and len(single_images) > 0) or \
                    single_images:
                return single_images[0]
        else:
            if return_image[0] != self.previous_pictures:
                return return_image[0]
            else:
                return alternative[0]
