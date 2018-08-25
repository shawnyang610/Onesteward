from datetime import datetime
import random
import qrcode
import os
from flask import current_app
from rest_api.models.order import OrderModel
from pyzbar import pyzbar
from PIL import Image
def generate_order_number():
    date = datetime.utcnow()
    return str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.microsecond)+str(random.randint(10, 100))

def generate_qrcode(str_order_number):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=1
    )

    qr.add_data(str_order_number)
    qr.make(fit=True)

    filename = str_order_number+".jpg"

    filepath = os.path.join(current_app.root_path, "static", "order_qr",filename)


    img = qr.make_image()
    img.save(filepath)


    return filename

def generate_and_validate_order_number(generate_order_number):
    order_number = generate_order_number()

    order = OrderModel.find_by_ur_code(order_number)

    while order:
        order_number = generate_order_number()
        order = OrderModel.find_by_ur_code(order_number)

    return order_number

def decode_qrcode(img_file):

    pil_image = Image.open(img_file)

    decoded_data = pyzbar.decode(pil_image)
    
    return decoded_data[0].data.decode("utf-8")
