import logging
import os

from flask import current_app, jsonify, request
from werkzeug.utils import secure_filename

from models.upload_model import UploadModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "pdf", "txt"}


class UploadController:
    @staticmethod
    def arquivo_permitido(nome_arquivo):
        return (
            "." in nome_arquivo
            and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
        )

    @staticmethod
    def upload_file():
        if "file" not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado. Use o campo 'file'."}), 400

        arquivo = request.files["file"]
        if not arquivo.filename:
            return jsonify({"erro": "Nome do arquivo vazio."}), 400

        nome_arquivo = secure_filename(arquivo.filename)
        if not nome_arquivo:
            return jsonify({"erro": "Nome de arquivo inválido."}), 400

        if not UploadController.arquivo_permitido(nome_arquivo):
            return jsonify({
                "erro": "Tipo de arquivo não permitido.",
                "tipos_permitidos": sorted(EXTENSOES_PERMITIDAS)
            }), 400

        # Lê no máximo 1 byte além do limite para validar o tamanho real do arquivo.
        limite = current_app.config["MAX_FILE_SIZE"]
        conteudo = arquivo.stream.read(limite + 1)
        if len(conteudo) > limite:
            return jsonify({"erro": "Arquivo excede o tamanho máximo permitido (30 KB)."}), 400

        pasta_upload = current_app.config["UPLOAD_FOLDER"]
        caminho_arquivo = os.path.join(pasta_upload, nome_arquivo)

        # Não sobrescreve um arquivo existente com o mesmo nome.
        if os.path.exists(caminho_arquivo):
            return jsonify({"erro": "Já existe um arquivo com esse nome."}), 409

        with open(caminho_arquivo, "wb") as destino:
            destino.write(conteudo)

        salvo = UploadModel.save_file(nome_arquivo, caminho_arquivo)
        if not salvo:
            # Evita deixar um arquivo órfão caso o nome já esteja cadastrado no banco.
            try:
                os.remove(caminho_arquivo)
            except OSError:
                logger.exception("Não foi possível remover um arquivo não cadastrado.")
            return jsonify({"erro": "Já existe um registro com esse nome."}), 409

        logger.info("Upload concluído: %s", nome_arquivo)
        return jsonify({
            "mensagem": "Arquivo salvo com sucesso!",
            "arquivo": nome_arquivo,
            "tamanho_bytes": len(conteudo),
            "url_download": f"/downloads/download/{nome_arquivo}"
        }), 201
