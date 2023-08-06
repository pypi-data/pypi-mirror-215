import os
import subprocess
import sys
import threading
import time
from typing import Any, Callable, Iterable, List, Optional

import joblib
from dash_extensions.enrich import Dash, DashBlueprint
from sklearn.pipeline import Pipeline

from topicwizard.blueprints.app import create_blueprint
from topicwizard.blueprints.template import prepare_blueprint


def is_notebook() -> bool:
    return "ipykernel" in sys.modules


def is_colab() -> bool:
    return "google.colab" in sys.modules


def get_app_blueprint(
    vectorizer: Any,
    topic_model: Any,
    corpus: Iterable[str],
    document_names: Optional[List[str]] = None,
    topic_names: Optional[List[str]] = None,
) -> DashBlueprint:
    blueprint = prepare_blueprint(
        vectorizer=vectorizer,
        topic_model=topic_model,
        corpus=corpus,
        document_names=document_names,
        topic_names=topic_names,
        create_blueprint=create_blueprint,
    )
    return blueprint


def get_dash_app(
    vectorizer: Any,
    topic_model: Any,
    corpus: Iterable[str],
    document_names: Optional[List[str]] = None,
    topic_names: Optional[List[str]] = None,
) -> Dash:
    """Returns topicwizard Dash application.

    Parameters
    ----------
    vectorizer: Vectorizer
        Sklearn compatible vectorizer, that turns texts into
        bag-of-words representations.
    topic_model: TopicModel
        Sklearn compatible topic model, that can transform documents
        into topic distributions.
    corpus: iterable of str
        List of all works in the corpus you intend to visualize.
    document_names: list of str, default None
        List of document names in the corpus, if not provided documents will
        be labeled 'Document <index>'.
    topic_names: list of str, default None
        List of topic names in the corpus, if not provided topics will initially
        be labeled 'Topic <index>'.

    Returns
    -------
    Dash
        Dash application object for topicwizard.
    """
    blueprint = get_app_blueprint(
        vectorizer=vectorizer,
        topic_model=topic_model,
        corpus=corpus,
        document_names=document_names,
        topic_names=topic_names,
    )
    app = Dash(
        __name__,
        blueprint=blueprint,
        title="topicwizard",
        external_scripts=[
            {
                "src": "https://cdn.tailwindcss.com",
            },
            {
                "src": "https://kit.fontawesome.com/9640e5cd85.js",
                "crossorigin": "anonymous",
            },
        ],
    )
    return app


def load_app(filename: str) -> Dash:
    """Loads and prepares saved app from disk.

    Parameters
    ----------
    filename: str
        Path to the file where the data is stored.

    Returns
    -------
    Dash
        Dash application.
    """
    data = joblib.load(filename)
    return get_dash_app(**data)


def open_url(url: str) -> None:
    if sys.platform == "win32":
        os.startfile(url)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", url])
    else:
        try:
            subprocess.Popen(["xdg-open", url])
        except OSError:
            print("Please open a browser on: " + url)


def run_silent(app: Dash, port: int) -> Callable:
    def _run_silent():
        import logging
        import warnings

        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            app.run_server(port=port)

    return _run_silent


def run_app(
    app: Dash,
    port: int = 8050,
) -> Optional[threading.Thread]:
    url = f"http://127.0.0.1:{port}/"
    if is_colab():
        from google.colab import output  # type: ignore

        thread = threading.Thread(target=run_silent(app, port))
        thread.start()
        time.sleep(4)

        print("Open in browser:")
        output.serve_kernel_port_as_window(
            port, anchor_text="Click this link to open topicwizard."
        )
        return thread

    # elif is_notebook():
    #     from IPython.display import IFrame, display
    #
    #     thread = threading.Thread(target=run_silent(app, port))
    #     thread.start()
    #     time.sleep(4)
    #     display(IFrame(src=url, width="1200", height="1000"))
    #     return thread
    else:
        open_url(url)
        app.run_server(port=port)


def load(
    filename: str,
    port: int = 8050,
) -> Optional[threading.Thread]:
    """Visualizes topic model data loaded from disk.

    Parameters
    ----------
    filename: str
        Path to the file where the data is stored.
    port: int, default 8050
        Port where the application should run in localhost. Defaults to 8050.
    enable_notebook: bool, default False
        Specifies whether topicwizard should run in a Jupyter notebook.

    Returns
    -------
    Thread or None
        Returns a Thread if running in a Jupyter notebook (so you can close the server)
        returns None otherwise.
    """
    print("Preparing data")
    app = load_app(filename)
    return run_app(app, port=port)


def visualize(
    corpus: Iterable[str],
    vectorizer: Optional[Any] = None,
    topic_model: Optional[Any] = None,
    pipeline: Optional[Pipeline] = None,
    document_names: Optional[List[str]] = None,
    topic_names: Optional[List[str]] = None,
    port: int = 8050,
    enable_notebook: bool = False,
) -> Optional[threading.Thread]:
    """Visualizes your topic model with topicwizard.

    Parameters
    ----------
    corpus: iterable of str
        List of all works in the corpus you intend to visualize.
    vectorizer: Vectorizer, default None
        Sklearn compatible vectorizer, that turns texts into
        bag-of-words representations.
    topic_model: TopicModel, default None
        Sklearn compatible topic model, that can transform documents
        into topic distributions.
    pipeline: Pipeline, default None
        Sklearn compatible pipeline, that has two components:
        a vectorizer and a topic model.
        Ignored if vectorizer and topic_model are provided.
    document_names: list of str, default None
        List of document names in the corpus, if not provided documents will
        be labeled 'Document <index>'.
    topic_names: list of str, default None
        List of topic names in the corpus, if not provided topics will initially
        be labeled 'Topic <index>'.
    port: int, default 8050
        Port where the application should run in localhost. Defaults to 8050.

    Returns
    -------
    Thread or None
        Returns a Thread if running in a Jupyter notebook (so you can close the server)
        returns None otherwise.
    """
    if (vectorizer is None) and (topic_model is None):
        assert (
            pipeline is not None
        ), "Either pipeline or vectorizer and topic model have to be provided"
        (_, vectorizer), (_, topic_model) = pipeline.steps

    print("Preprocessing")
    app = get_dash_app(
        vectorizer=vectorizer,
        topic_model=topic_model,
        corpus=corpus,
        document_names=document_names,
        topic_names=topic_names,
    )
    return run_app(app, port=port)
