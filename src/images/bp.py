import uuid

from flask import Blueprint, render_template, redirect, url_for, request, Response

from . import blob_storage
from .dao import ImageDAO


image_dao = ImageDAO()

bp = Blueprint("images", __name__, url_prefix="/images")


@bp.get("/")
def list_all_images():
    images = list(image_dao.get_all_images())
    return render_template("image_list.html", images=images)


@bp.post("/")
def add_image():
    f = request.files.get("image")
    if not f:
        return "Upload file"
    img_data = {
        "name": f.filename or uuid.uuid4().hex + ".png",
        "type": f.content_type,
    }
    blob_storage.upload_file(f.stream, img_data["name"])
    metadata = blob_storage.get_file_metadata(img_data["name"])
    img_data["size"] = metadata["size"]
    image = image_dao.create_image(img_data)
    return redirect(url_for("images.get_image_by_name", image_id=image.image_id))


@bp.get("/<int:image_id>")
def get_image_by_name(image_id):
    image = image_dao.get_image_by_id(image_id)
    if not image:
        return Response("Not found", status=404)
    url = blob_storage.get_file_by_name(image.name)
    return render_template("image_detail.html", image=image, url=url)


@bp.post("/<int:image_id>")
def delete_image(image_id):
    image = image_dao.get_image_by_id(image_id)
    if not image:
        return Response("Not found", status=404)
    image_dao.delete_image(image_id)
    blob_storage.delete_file(image.name)
    return redirect(url_for("images.list_all_images"))
