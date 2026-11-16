import os

from flask import current_app, jsonify, send_from_directory

from models.download_model import DownloadModel


class DownloadController:
    @staticmethod
    def download_file(filename):
        registro = DownloadModel.find_by_filename(filename)
        if registro is None:
            return jsonify({"erro": "Arquivo não encontrado."}), 404

        pasta_upload = current_app.config["UPLOAD_FOLDER"]
        nome_arquivo = os.path.basename(registro["filepath"])
        caminho_arquivo = os.path.join(pasta_upload, nome_arquivo)
        if not os.path.isfile(caminho_arquivo):
            return jsonify({"erro": "O registro existe, mas o arquivo não está disponível."}), 404

        return send_from_directory(pasta_upload, nome_arquivo, as_attachment=True)
