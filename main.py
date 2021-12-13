from flask import Flask, request, render_template

from img_catalog import IMGCatalog

app = Flask(__name__)
images_catalog = IMGCatalog()

msg = 'No images found!'
# debug
# in start
# print(images_catalog)


@app.route('/', methods=['GET'])
def get_images_for_user():
    image_path = images_catalog.request_image(
        request.args.getlist('category[]'))
    # debug
    # after request image
    # print(images_catalog)
    if image_path is None:
        return msg
    return render_template('index.html', image=image_path)


if __name__ == "__main__":
    app.run(port=8080)
