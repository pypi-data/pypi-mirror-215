def _ignore_warnings():
    import logging
    import warnings

    logging.captureWarnings(True)
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="Deprecated call to `pkg_resources.declare_namespace('google')`.",
    )


_ignore_warnings()

from .backend import serving, download_df, upload_df

__version__ = '0.0.46'
