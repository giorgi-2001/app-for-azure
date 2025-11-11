import uuid

from flask import Blueprint, render_template, redirect, url_for, request

from . import blob_storage


bp = Blueprint("images", __name__, url_prefix="/images")


@bp.get("/")
def list_all_images():
    images = blob_storage.list_files()
    return render_template("image_list.html", images=images)


@bp.post("/")
def add_image():
    f = request.files.get("image")
    if not f:
        return "Upload file"
    file_name = f.filename or uuid.uuid4().hex + ".png"
    blob_storage.upload_file(f.stream, file_name)
    return redirect(url_for("images.get_image_by_name", image_name=file_name))


@bp.get("/<string:image_name>")
def get_image_by_name(image_name):
    url = blob_storage.get_file_by_name(image_name)
    return render_template("image_detail.html", image_name=image_name, url=url)


@bp.post("/<string:image_name>")
def delete_image(image_name):
    blob_storage.delete_file(image_name)
    return redirect(url_for("images.list_all_images"))
