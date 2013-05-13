from flask import Flask, url_for, render_template, redirect
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome!\n"

@app.route("/show/<entity_id>")
def show(entity_id):
    return render_template(
        'show.html', 
        entity_id=entity_id,
        confirm_url=url_for("confirm", entity_id = entity_id),
        reject_url=url_for("reject", entity_id = entity_id))

@app.route("/confirm/<entity_id>")
def confirm(entity_id):
    return "%s confirmed<br/><a href='%s'>back</a>" % (
        entity_id, url_for("show", entity_id = entity_id))

@app.route("/reject/<entity_id>")
def reject(entity_id):
    return "%s rejected<br/><a href='%s'>back</a>" % (
        entity_id, url_for("show", entity_id = entity_id))

if __name__ == "__main__":
    app.debug = True
    app.run()
