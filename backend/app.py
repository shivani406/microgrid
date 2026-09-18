import os
from flask import Flask, render_template, jsonify
from backend.routes.api import api_bp

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "templates"))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "static"))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)