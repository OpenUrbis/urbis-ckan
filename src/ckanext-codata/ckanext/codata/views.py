import logging

from flask import Blueprint, request

log = logging.getLogger(__name__)

# Endpoints do CKAN que servem o arquivo de um recurso enviado por upload.
# O core chama `flask.send_file()` sem `as_attachment=True`, o que resulta em
# `Content-Disposition: inline` e faz o navegador renderizar o arquivo
# (GeoJSON, JSON, TXT, XML...) em vez de baixá-lo.
DOWNLOAD_ENDPOINTS = frozenset([
    'dataset_resource.download',
    'resource.download',
])

codata = Blueprint('codata', __name__)


@codata.after_app_request
def force_resource_download(response):
    """
    Força o download direto do arquivo na rota de download de recursos.

    Reescreve o `Content-Disposition: inline` enviado pelo CKAN para
    `attachment`, preservando o `filename` original. Respostas sem esse
    cabeçalho (ex.: o redirect de recursos de URL externa) não são alteradas.

    :param response: Resposta do Flask.
    :return: Resposta com o cabeçalho ajustado.
    """
    if request.endpoint not in DOWNLOAD_ENDPOINTS:
        return response

    disposition = response.headers.get('Content-Disposition', '')
    if disposition.startswith('inline'):
        response.headers['Content-Disposition'] = (
            'attachment' + disposition[len('inline'):]
        )

    return response


def get_blueprints():
    return [codata]
