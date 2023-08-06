import logging
import os

# pyxecm packages
from .main import *
from .k8s import *
from .otac import *
from .otcs import *
from .otds import *
from .otiv import *
from .otpd import *
from .payload import *
from .translate import *
from .web import *

logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(os.path.basename(__file__))