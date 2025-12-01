from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from config import Config
from models import db, Note

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route("/")
    def index():
        notes = Note.query.order_by(Note.updated_at.desc()).all()
        return render_template("index.html", notes=notes)

    @app.route("/note/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            body = request.form.get("body", "").strip()
            if not title:
                return render_template("new_note.html", error="Title required", title=title, body=body)
            note = Note(title=title, body=body)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("new_note.html")

    @app.route("/note/<int:note_id>")
    def view_note(note_id):
        note = Note.query.get_or_404(note_id)
        return render_template("view_note.html", note=note)

    @app.route("/note/<int:note_id>/edit", methods=["GET", "POST"])
    def edit_note(note_id):
        note = Note.query.get_or_404(note_id)
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            body = request.form.get("body", "").strip()
            if not title:
                return render_template("edit_note.html", note=note, error="Title required")
            note.title = title
            note.body = body
            db.session.commit()
            return redirect(url_for("view_note", note_id=note.id))
        return render_template("edit_note.html", note=note)

    # Simple JSON API to delete a note
    @app.route("/api/note/<int:note_id>", methods=["DELETE"])
    def delete_note_api(note_id):
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "deleted"}), 200

    # Optional: API to list notes as JSON
    @app.route("/api/notes")
    def api_list_notes():
        notes = Note.query.order_by(Note.updated_at.desc()).all()
        return jsonify([n.to_dict() for n in notes])

    return app

if __name__ == "__main__":
    app = create_app()
    # bind to 0.0.0.0 so the app is reachable from Docker / EC2 network
    app.run(host="0.0.0.0", debug=True)
