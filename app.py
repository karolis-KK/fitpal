import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))

firebase_admin.initialize_app(cred)

db = firestore.client()
UPLOAD_FOLDER = 'uploads' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add-clothing", methods=["POST"])
def add_clothing():
    clothing_type = request.form['clothing_type']
    clothing_text = request.form["clothing_text"]
    clothing_brand = request.form["clothing_brand"]
    image = request.files['image']

    if clothing_type == "Hoodie" or clothing_type == "Crewneck" or clothing_type == "Sweater/Knit" or clothing_type == "T-Shirt" or clothing_type == "Shirt" or clothing_type == "Jacket" or clothing_type == "Longsleeve":
        clothing_section = "top"
    elif clothing_type == "Pants":
        clothing_section = "middle"
    elif clothing_type == "Shoes":
        clothing_section = "bottom"

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    if clothing_brand.strip() == "":
        clothing_brand = None

    clothing_data = {
        'type': clothing_type,
        'text' : clothing_text,
        "brand": clothing_brand,
        'image_url': url_for('uploaded_file', filename=image.filename),
        'section': clothing_section,
        'timestamp': datetime.utcnow()
    }
    db.collection('clothing').add(clothing_data)
    return redirect(url_for('my_closet'))

@app.route("/my-closet", methods=["GET", "POST"])
def my_closet():
    page = request.args.get('page', 1, type=int)  # Get the current page number
    per_page = 5  # Number of items per page

    # Fetch clothing items based on filters
    clothing_items_query = db.collection('clothing').limit(per_page).offset((page - 1) * per_page).stream()
    clothing_items_list = [
        {
            'id': item.id,
            'type': item.to_dict().get('type'),
            'text': item.to_dict().get('text'),
            'brand': item.to_dict().get('brand'),
            'image_url': item.to_dict().get('image_url'),
            'timestamp': item.to_dict().get('timestamp', 0)
        } for item in clothing_items_query
    ]

    # Fetch total count for pagination
    total_items = len(list(db.collection('clothing').stream()))  
    total_pages = (total_items + per_page - 1) // per_page 

    return render_template("closet.html", clothing_items=clothing_items_list, page=page, total_pages=total_pages)

@app.route("/my-outfits", methods=["GET"])
def my_outfits():
    page = request.args.get('page', 1, type=int)  # current page
    per_page = 30 # Number of outfits per page

    outfits_query = db.collection('outfits').limit(per_page).offset((page - 1) * per_page).stream()
    outfits_list = [
        {
            'id': outfit.id,
            'name': outfit.to_dict().get('name'),
            'top': outfit.to_dict().get('top'),
            'middle': outfit.to_dict().get('middle'),
            'bottom': outfit.to_dict().get('bottom'),
        } for outfit in outfits_query
    ]

    total_items = len(list(db.collection('outfits').stream()))
    total_pages = (total_items + per_page - 1) // per_page  # total pages

    return render_template("myoutfits.html", outfits=outfits_list, page=page, total_pages=total_pages)

@app.route("/make-outfit")
def make_outfit():
    top_items = db.collection('clothing').where('section', '==', 'top').stream()
    middle_items = db.collection('clothing').where('section', '==', 'middle').stream()
    bottom_items = db.collection('clothing').where('section', '==', 'bottom').stream()

    top_items_list = [
        {
            'id': item.id,
            'type': item.to_dict().get('type'),
            'text': item.to_dict().get('text'),
            'brand': item.to_dict().get('brand'),
            'image_url': item.to_dict().get('image_url'),
        } for item in top_items
    ]

    middle_items_list = [
        {
            'id': item.id,
            'type': item.to_dict().get('type'),
            'text': item.to_dict().get('text'),
            'brand': item.to_dict().get('brand'),
            'image_url': item.to_dict().get('image_url'),
        } for item in middle_items
    ]

    bottom_items_list = [
        {
            'id': item.id,
            'type': item.to_dict().get('type'),
            'text': item.to_dict().get('text'),
            'brand': item.to_dict().get('brand'),
            'image_url': item.to_dict().get('image_url'),
        } for item in bottom_items
    ]

    return render_template("outfitc.html", top_items=top_items_list, middle_items=middle_items_list, bottom_items=bottom_items_list)

@app.route("/remove-clothing/<item_id>", methods=["POST"])
def remove_clothing(item_id):
    db.collection('clothing').document(item_id).delete()
    flash("Clothing item removed successfully!")
    return redirect(url_for('my_closet'))

@app.route("/edit-clothing/<item_id>", methods=["GET", "POST"])
def edit_clothing(item_id):
    if request.method == "POST":
        clothing_text = request.form["clothing_text"]
        clothing_brand = request.form["clothing_brand"]
        db.collection('clothing').document(item_id).update({
            'text': clothing_text,
            'brand': clothing_brand,
        })
        return redirect(url_for('my_closet'))

    item = db.collection('clothing').document(item_id).get()
    if item.exists:
        clothing_data = item.to_dict()
        return render_template("closet.html", clothing_data=clothing_data, item_id=item_id)
    else:
        flash("Clothing item not found.")
        return redirect(url_for('my_closet'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/save-outfit", methods=["POST"])
def save_outfit():
    data = request.get_json()
    outfit_name = data.get('name')
    top_image = data.get('top')
    middle_image = data.get('middle')
    bottom_image = data.get('bottom')

    db.collection('outfits').add({
        'name': outfit_name,
        'top': top_image,
        'middle': middle_image,
        'bottom': bottom_image
    })

    return jsonify(success=True)

@app.route("/delete-outfit/<outfit_id>", methods=["POST"])
def delete_outfit(outfit_id):
    db.collection('outfits').document(outfit_id).delete()
    return redirect(url_for('my_outfits')) 

if __name__ == "__main__":
    app.run(debug=True)