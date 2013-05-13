from flask import Flask, url_for, render_template, redirect
import json
app = Flask(__name__)
data_file = "list_annotation.json"

@app.route("/")
def hello():
    return "Welcome!\n"

@app.route("/show/<entity_id>")
def show(entity_id):
    features = _get_features(entity_id)
    return render_template(
        'show.html', 
        entity_id=entity_id,
        status=features["status"],
        confirm_url=url_for("confirm", entity_id = entity_id),
        reject_url=url_for("reject", entity_id = entity_id))

@app.route("/confirm/<entity_id>")
def confirm(entity_id):
    _save_annotation(entity_id, "confirmed")
    return redirect(url_for('show', entity_id = entity_id))

@app.route("/reject/<entity_id>")
def reject(entity_id):
    _save_annotation(entity_id, "reject")
    return redirect(url_for('show', entity_id = entity_id))

def _get_features(entity_id):
    entities = _entities()
    return entities.get(entity_id, {"status" : "Undefined"})

def _entities():
    try:
        with open(data_file) as fh:
            return(json.load(fh))
    except IOError:
        with open(data_file, "w") as fh:
            fh.write("{}")
            return {}

def _save_annotation(entity_id, status):
    entities = _entities()
    entities[entity_id] = {"status" : status, "mod_time" : ""}
    with open(data_file, "w") as fh:
        json.dump(entities, fh)

if __name__ == "__main__":
    app.debug = True
    app.run()
