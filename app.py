import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import os 
from dotenv import load_dotenv

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
    image = request.files['image']

    if clothing_type == "Hoodie" or clothing_type == "Crewneck" or clothing_type == "Sweater/Knit" or clothing_type == "T-Shirt":
        clothing_section = "top"
    elif clothing_type == "Pants":
        clothing_section = "middle"
    elif clothing_type == "Shoes":
        clothing_section = "bottom"

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    clothing_data = {
        'type': clothing_type,
        'text' : clothing_text,
        'image_url': url_for('uploaded_file', filename=image.filename),
        'section': clothing_section
    }
    db.collection('clothing').add(clothing_data)
    flash("Clothing item added successfully!")
    return redirect(url_for('my_closet'))

@app.route("/my-closet", methods=["GET", "POST"])
def my_closet():
    if request.method == "POST":
        filter_types = request.form.getlist('filter_type[]')
        sort_by = request.form.get('sort_by')

        # Fetch clothing items based on filters
        if "All" in filter_types:
            clothing_items = db.collection('clothing').stream()
        else:
            clothing_items = db.collection('clothing').where('type', 'in', filter_types).stream()

        # Convert to list for sorting
        clothing_items_list = [
            {
                'id': item.id,
                'type': item.to_dict().get('type'),
                'text': item.to_dict().get('text'),
                'image_url': item.to_dict().get('image_url'),
                'timestamp': item.to_dict().get('timestamp', 0)
            } for item in clothing_items
        ]

        if sort_by == "newest":
            clothing_items_list.sort(key=lambda x: x['timestamp'], reverse=True)
        elif sort_by == "oldest":
            clothing_items_list.sort(key=lambda x: x['timestamp'])

    else:
        clothing_items = db.collection('clothing').stream()
        clothing_items_list = [
            {
                'id': item.id,
                'type': item.to_dict().get('type'),
                'text': item.to_dict().get('text'),
                'image_url': item.to_dict().get('image_url'),
                'timestamp': item.to_dict().get('timestamp', 0)
            } for item in clothing_items
        ]

    return render_template("closet.html", clothing_items=clothing_items_list)

@app.route("/my-outfits")
def my_outfits():
    outfits = db.collection('outfits').stream()
    outfits_list = [
        {
            'id': outfit.id,
            'name': outfit.to_dict().get('name'),
            'top': outfit.to_dict().get('top'),
            'middle': outfit.to_dict().get('middle'),
            'bottom': outfit.to_dict().get('bottom'),
        } for outfit in outfits
    ]
    return render_template("myoutfits.html", outfits=outfits_list)

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
            'image_url': item.to_dict().get('image_url'),
        } for item in top_items
    ]

    middle_items_list = [
        {
            'id': item.id,
            'type': item.to_dict().get('type'),
            'text': item.to_dict().get('text'),
            'image_url': item.to_dict().get('image_url'),
        } for item in middle_items
    ]

    bottom_items_list = [
        {
            'id': item.id,
            'type': item.to_dict().get('type'),
            'text': item.to_dict().get('text'),
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
        db.collection('clothing').document(item_id).update({
            'text': clothing_text
        })
        flash("Clothing item updated successfully!")
        return redirect(url_for('my_closet'))

    # If GET request, fetch the current item data
    item = db.collection('clothing').document(item_id).get()
    if item.exists:
        clothing_data = item.to_dict()
        return render_template("edit_clothing.html", clothing_data=clothing_data, item_id=item_id)
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
    flash("Outfit deleted successfully!")
    return redirect(url_for('my_outfits')) 

if __name__ == "__main__":
    app.run(debug=True)