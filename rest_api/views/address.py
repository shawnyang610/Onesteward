from flask import Blueprint, render_template, redirect, url_for
from rest_api.forms.address import AddressCreateForm
from rest_api.models.address import AddressModel
address_bp = Blueprint("address", __name__)




@address_bp.route("/create/<int:company_id><int:user_id>", methods=["GET", "POST"])
def address_create(company_id, user_id):

    form = AddressCreateForm()

    if form.validate_on_submit():
        address = AddressModel(
            line1=form.line1.data,
            line2=form.line2.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data,
            company_id=company_id,
            user_id =user_id
        )
        address.save_to_db()

        return redirect(url_for("company.company_info"))

    return render_template("address_create.html", form=form)


@address_bp.route("/update/<int:address_id>", methods=["GET","POST"])
def address_update(address_id):
    form = AddressCreateForm()

    address = AddressModel.find_by_id(address_id)

    if form.validate_on_submit():
        address.line1 = form.line1.data
        address.line2 = form.line2.data
        address.city =  form.city.data
        address.state= form.state.data
        address.zip = form.zip.data

        address.save_to_db()

        return redirect(url_for("company.company_info"))

    form.line1.data = address.line1
    form.line2.data = address.line2
    form.city.data = address.city
    form.state.data = address.state
    form.zip.data = address.zip

    return render_template("address_create.html", form = form)



# @address_bp.route("/info")
# def address_info():
#     pass

@address_bp.route("/delete/<int:address_id>", methods=["GET","POST"])
def address_delete(address_id):
    
    address = AddressModel.find_by_id(address_id)
    
    if address:
        address.delete_from_db()
    
    return redirect(url_for("company.company_info"))