class Layer:
    def __init__(self):
        self.rows = []

    def make_blank(self, width: int, height: int):
        row = []
        for i in range(height):
            for j in range(width):
                row.append('-1')
            self.rows.append(row)
            row = []

    def get_pixel(self, row: int, col: int) -> str:
        return self.rows[row][col]

    def set_pixel(self, val: str, row: int, col: int) -> None:
        self.rows[row][col] = val

    def show(self):
        layer = '\n'
        for row in self.rows:
            layer += ','.join(row) + '\n'
        return layer

    def count(self, to_count: str):
        count = 0
        for row in self.rows:
            for pixel in row:
                if pixel == to_count:
                    count += 1
        return count


class Image:
    def __init__(self, data: str, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.num_layers: float = len(data) / (width * height)
        self.layers = []
        self.make_layers(data)

    @property
    def image(self):
        final_image = Layer()
        final_image.make_blank(self.width, self.height)
        for layer in self.layers:
            for i, row in enumerate(layer.rows):
                for j, pixel in enumerate(row):
                    if final_image.get_pixel(i, j) == '-1' and pixel != '2':
                        final_image.set_pixel(pixel, i, j)

        return final_image

    def find_min_layer(self, to_minimize: str) -> int:
        min = 999999
        min_i = 0
        for i, layer in enumerate(self.layers):
            cnt = layer.count(to_minimize)
            if cnt < min:
                min = cnt
                min_i = i
        return min_i

    def make_layers(self, data: str) -> None:
        layer = Layer()
        current_row = []
        for i, pixel in enumerate(data):
            if i % self.width == 0 and i != 0:
                layer.rows.append(current_row)
                current_row = [pixel]
            else:
                current_row.append(pixel)

            # Make new layer
            if len(layer.rows) == self.height:
                self.layers.append(layer)
                layer = Layer()
        layer.rows.append(current_row)
        self.layers.append(layer)


with open('input.txt', 'r') as file:
    img = Image(file.readline(), 25, 6)
    min_zeros = img.find_min_layer('0')
    a = img.layers[min_zeros].count('1') * img.layers[min_zeros].count('2')
    print(a)
    # Part 2
    with open('output.csv', 'w') as f_out:
        f_out.write(img.image.show())
        print(img.image.show())