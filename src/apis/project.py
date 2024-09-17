from flask import blueprints, request, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
from src.logger import Logger, route_logger
from src.config import Config
from src.project import ProjectManager
from ..state import AgentState

import os

project_bp = blueprints.Blueprint("project", __name__)

logger = Logger()
manager = ProjectManager()


# Project APIs

@project_bp.route("/api/get-project-files", methods=["GET"])
@route_logger(logger)
def project_files():
    """Get the list of files for a given project.

    Args:
        project_name (str): The name of the project to get the files for.

    Returns:
        dict: A JSON dict containing a single key, "files", which is a list of
            strings representing the file paths in the project.
    """

    project_name = secure_filename(request.args.get("project_name"))
    files = manager.get_project_files(project_name)  
    return jsonify({"files": files})

@project_bp.route("/api/create-project", methods=["POST"])
@route_logger(logger)
def create_project():
    data = request.json
    project_name = data.get("project_name")
    manager.create_project(secure_filename(project_name))
    return jsonify({"message": "Project created"})


@project_bp.route("/api/delete-project", methods=["POST"])
@route_logger(logger)
def delete_project():
    """Delete a project by name.

    Args:
        project_name (str): The name of the project to delete.

    Returns:
        dict: A JSON dict containing a single key, "message", which is a string
            indicating that the project was deleted.
    """
    data = request.json
    project_name = secure_filename(data.get("project_name"))
    manager.delete_project(project_name)
    AgentState().delete_state(project_name)
    return jsonify({"message": "Project deleted"})


@project_bp.route("/api/download-project", methods=["GET"])
@route_logger(logger)
def download_project():
    """Download a project by name.

    Args:
        project_name (str): The name of the project to download.

    Returns:
        file: The zipped project as a file.
    """
    project_name = secure_filename(request.args.get("project_name"))
    manager.project_to_zip(project_name)
    project_path = manager.get_zip_path(project_name)
    return send_file(project_path, as_attachment=False)


@project_bp.route("/api/download-project-pdf", methods=["GET"])
@route_logger(logger)
def download_project_pdf():
    """Download a project's PDF report by name.

    Args:
        project_name (str): The name of the project to download.

    Returns:
        file: The PDF report as a file.
    """
    project_name = secure_filename(request.args.get("project_name"))
    pdf_dir = Config().get_pdfs_dir()
    pdf_path = os.path.join(pdf_dir, f"{project_name}.pdf")

    response = make_response(send_file(pdf_path))
    response.headers['Content-Type'] = 'project_bplication/pdf'
    return response
