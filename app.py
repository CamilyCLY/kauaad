import os

from flask import Flask, jsonify

from database.db import init_db
from routes.download_route import download_bp
from routes.upload_route import upload_bp


def create_app():
    app = Flask(__name__)

    # Os caminhos podem ser alterados pelas variáveis de ambiente no Render.
    app.config["UPLOAD_FOLDER"] = os.environ.get(
        "UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "uploads")
    )
    app.config["DATABASE_PATH"] = os.environ.get(
        "DATABASE_PATH", os.path.join(os.path.dirname(__file__), "database.db")
    )
    app.config["MAX_CONTENT_LENGTH"] = 40 * 1024  # margem para os dados do formulário; o arquivo tem limite próprio
    app.config["MAX_FILE_SIZE"] = 30 * 1024  # 30 KB por arquivo

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    init_db(app.config["DATABASE_PATH"])

    app.register_blueprint(upload_bp, url_prefix="/uploads")
    app.register_blueprint(download_bp, url_prefix="/downloads")

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API de upload e download funcionando!",
            "rotas": {
                "upload": "POST /uploads/upload (campo do formulário: file)",
                "download": "GET /downloads/download/<nome_do_arquivo>"
            }
        })

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


app = create_app()


if __name__ == "__main__":
    # Debug fica desativado por padrão. Para desenvolvimento local, use FLASK_DEBUG=1.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=debug)
