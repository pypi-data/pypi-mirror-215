"""[Automate OpenText Directory Services (OTDS) and Extended ECM (OTCS) configurations]

Functions:

initM365: initialize the Microsoft 365 object
initOTDS: initialize the OTDS object
initOTAC: initialize the OTAC object
initOTCS: initialize the OTCS (Extended ECM) object
initOTPD: initialize the PowerDocs object
initOTAWP: initialize OTDS settings for AppWorks Platform

restartOTCSPods: restart the OTCS backend and frontend pods -
                 required to make certain configurations effective
restartOTACPod: restart spawner process in Archive Center
consolidateOTDS: consolidate OTDS users / groups (to get to a fully synchronized state)
restartOTAWPPod: restart the AppWorks Platform Pod to make settings effective

importPowerDocsConfiguration: import PowerDocs database

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import sys
import time
import os
import logging
import yaml
import requests

from datetime import datetime

# OpenText specific modules:
import pyxecm.payload as payload
import pyxecm.otds as otds
import pyxecm.otcs as otcs
import pyxecm.otac as otac
import pyxecm.otiv as otiv
import pyxecm.otpd as otpd
import pyxecm.k8s as k8s
import pyxecm.m365 as m365

# Global dict with placeholder values for replacements in LLConfig files:
placeholder_values = {}

# Global variables for OTCS replicas
otcs_replicas_frontend = 0
otcs_replicas_backend = 0

# global Logging LEVEL environment variable
# This produces debug-level output in pod logging
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")

# The following CUST artifacts are created by the main.tf in the python module:
CUST_BASE_DIR = ""  # change this if you run / test locally
CUST_APP_DIR = CUST_BASE_DIR + "/app/"
CUST_SETTINGS_DIR = CUST_BASE_DIR + "/settings/"
CUST_PAYLOAD_DIR = CUST_BASE_DIR + "/payload/"
CUST_PAYLOAD = CUST_PAYLOAD_DIR + "payload.yaml"
CUST_PAYLOAD_EXTERNAL = "/payload-external/"
CUST_LOG_DIR = "/tmp/"
CUST_LOG_FILE = CUST_LOG_DIR + "customizing.log"
CUST_TARGET_FOLDER_NICKNAME = (
    "deployment"  # nickname of folder to upload payload and log files
)
# CUST_RM_SETTINGS_DIR = "/opt/opentext/cs/appData/supportasset/Settings/"
CUST_RM_SETTINGS_DIR = CUST_SETTINGS_DIR

# This script is expecting that the pod has a couple
# of environment variables set. This is typically done in
# the Helm Chart of the deployment or in the Terraform scripts.

# OTDS Constants:
OTDS_PROTOCOL = os.environ.get("OTDS_PROTOCOL", "http")
OTDS_PUBLIC_PROTOCOL = os.environ.get("OTDS_PUBLIC_PROTOCOL", "https")
OTDS_HOSTNAME = os.environ.get("OTDS_HOSTNAME", "otds")
OTDS_PORT = os.environ.get("OTDS_SERVICE_PORT_OTDS", 80)
OTDS_ADMIN = os.environ.get("OTDS_ADMIN", "admin")
OTDS_ADMIN_PARTITION = "otds.admin"
OTDS_PUBLIC_URL = os.environ.get("OTDS_PUBLIC_URL", "otds.xecm.dev")
OTDS_PASSWORD = os.environ.get("OTDS_PASSWORD", "Opentext1!")

# Content Server Constants:
OTCS_PROTOCOL = os.environ.get("OTCS_PROTOCOL", "http")
OTCS_PUBLIC_PROTOCOL = os.environ.get("OTCS_PUBLIC_PROTOCOL", "https")
OTCS_HOSTNAME = OTCS_HOSTNAME_BACKEND = os.environ.get("OTCS_HOSTNAME", "otcs-admin-0")
OTCS_HOSTNAME_FRONTEND = os.environ.get("OTCS_HOSTNAME_FRONTEND", "otcs-frontend")
OTCS_PUBLIC_URL = os.environ.get("OTCS_PUBLIC_URL", "otcs.xecm.dev")
OTCS_PORT = OTCS_PORT_BACKEND = os.environ.get("OTCS_SERVICE_PORT_OTCS", 8080)
OTCS_PORT_FRONTEND = 80
OTCS_ADMIN = os.environ.get("OTCS_ADMIN", "admin")
OTCS_PASSWORD = os.environ.get("OTCS_PASSWORD", "Opentext1!")
OTCS_PARTITION = os.environ.get("OTCS_PARTITION", "Content Server Members")
OTCS_RESOURCE_NAME = "cs"
OTCS_K8S_STATEFUL_SET_FRONTEND = "otcs-frontend"
OTCS_K8S_STATEFUL_SET_BACKEND = "otcs-admin"
OTCS_K8S_INGRESS = "otxecm-ingress"
OTCS_MAINTENANCE_MODE = (
    os.environ.get("OTCS_MAINTENANCE_MODE", "true").lower() == "true"
)
OTCS_LICENSE_FEATURE = "X3"

# K8s service name for maintenance pod
OTCS_MAINTENANCE_SERVICE_NAME = "maintenance"
OTCS_MAINTENANCE_SERVICE_PORT = 80  # K8s service name for maintenance pod

# Archive Center constants:
OTAC_ENABLED = os.environ.get("OTAC_ENABLED", True)
OTAC_HOSTNAME = os.environ.get("OTAC_SERVICE_HOST", "otac-0")
OTAC_PORT = os.environ.get("OTAC_SERVICE_PORT", 8080)
OTAC_PROTOCOL = os.environ.get("OTAC_PROTOCOL", "http")
OTAC_PUBLIC_URL = os.environ.get("OTAC_PUBLIC_URL", "otcs.xecm.dev")
OTAC_ADMIN = os.environ.get("OTAC_ADMIN", "dsadmin")
OTAC_PASSWORD = os.environ.get("OTAC_PASSWORD", "")
OTAC_KNOWN_SERVER = os.environ.get("OTAC_KNOWN_SERVER", "")
OTAC_K8S_POD_NAME = "otac-0"

# PowerDocs constants:
OTPD_ENABLED = os.environ.get("OTPD_ENABLED", False)
OTPD_HOSTNAME = os.environ.get("OTPD_SERVICE_HOST", "otpd")
OTPD_PORT = os.environ.get("OTPD_SERVICE_PORT", 8080)
OTPD_PROTOCOL = os.environ.get("OTPD_PROTOCOL", "http")
OTPD_DBIMPORTFILE = os.environ.get(
    "OTPD_DBIMPORTFILE", "URL://url.download.location/file.zip"
)
OTPD_TENANT = os.environ.get("OTPD_TENANT", "Successfactors")
OTPD_USER = os.environ.get("OTPD_USER", "powerdocsapiuser")
OTPD_PASSWORD = os.environ.get("OTPD_PASSWORD", "Opentext1!")
OTPD_K8S_POD_NAME = "otpd-0"

# Intelligent Viewing constants:
OTIV_ENABLED = os.environ.get("OTIV_ENABLED", False)
OTIV_LICENSE_FILE = CUST_PAYLOAD_DIR + "otiv-license.lic"
OTIV_LICENSE_FEATURE = "FULLTIME_USERS_REGULAR"
OTIV_PRODUCT_NAME = "Viewing"
OTIV_PRODUCT_DESCRIPTION = "OpenText Intelligent Viewing"
OTIV_RESOURCE_NAME = "iv"

# AppWorks Platform constants:
OTAWP_ENABLED = os.environ.get("OTAWP_ENABLED", False)
OTAWP_RESOURCE_NAME = "awp"
OTAWP_ACCESS_ROLE_NAME = "Access to " + OTAWP_RESOURCE_NAME
OTAWP_ADMIN = os.environ.get("OTAWP_ADMIN", "sysadmin")
OTAWP_PASSWORD = os.environ.get("OTAWP_PASSWORD", "Opentext1!")
OTAWP_PUBLIC_PROTOCOL = os.environ.get("OTAWP_PROTOCOL", "https")
OTAWP_PUBLIC_URL = os.environ.get("OTAWP_PUBLIC_URL", "otawp.xecm.dev")
OTAWP_K8S_STATEFUL_SET = "appworks"
OTAWP_K8S_CONFIGMAP = "appworks-config-ymls"

# K8s Mode
K8S_ENABLED = os.environ.get("K8S_ENABLED", "true").lower() == "true"

# Microsoft 365 Environment variables:

O365_ENABLED = os.environ.get("O365_ENABLED", False)
O365_TENANT_ID = os.environ.get("O365_TENANT_ID")
O365_CLIENT_ID = os.environ.get("O365_CLIENT_ID")
O365_CLIENT_SECRET = os.environ.get("O365_CLIENT_SECRET")
O365_USER = os.environ.get("O365_USER", "")
O365_PASSWORD = os.environ.get("O365_PASSWORD", "")
O365_DOMAIN = os.environ.get("O365_DOMAIN")
O365_SKU_ID = os.environ.get(
    "O365_SKU_ID", "c7df2760-2c81-4ef7-b578-5b5392b571df"
)  # Office 365 E5, used as default SKU for users
O365_TEAMS_APP_NAME = "OpenText Extended ECM"

# Configure logging output
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    level=logging.INFO if LOGLEVEL == "INFO" else logging.DEBUG,
    handlers=[
        logging.FileHandler(CUST_LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(os.path.basename(__file__))


def initM365() -> object:
    """Initialize the M365 object we use to talk to the Microsoft Graph API.

    Args:
        None
    Returns:
        object: M365 object or None if the object couldn't be created or
                the authentication fails.
    """

    logger.info("Microsoft 365 Tenant ID             = " + O365_TENANT_ID)
    logger.info("Microsoft 365 Client ID             = " + O365_CLIENT_ID)
    logger.debug("Microsoft 365 Client Secret         = " + O365_CLIENT_SECRET)
    logger.info(
        "Microsoft 365 User                  = "
        + (O365_USER if O365_USER != "" else "<not configured>")
    )
    logger.debug(
        "Microsoft 365 Password              = "
        + (O365_PASSWORD if O365_PASSWORD != "" else "<not configured>")
    )
    logger.info("Microsoft 365 Domain                = " + O365_DOMAIN)
    logger.info("Microsoft 365 Default License SKU   = " + O365_SKU_ID)
    logger.info("Microsoft 365 Teams App             = " + O365_TEAMS_APP_NAME)

    m365_object = m365.M365(
        O365_TENANT_ID,
        O365_CLIENT_ID,
        O365_CLIENT_SECRET,
        O365_DOMAIN,
        O365_SKU_ID,
        O365_TEAMS_APP_NAME,
    )

    if m365_object and m365_object.authenticate():
        logger.info("Connected to Microsoft Graph API.")
        return m365_object
    else:
        logger.error("Failed to connect to Microsoft Graph API.")
        return None

    # end function definition


def initK8s(inCluster: bool = True) -> object:
    """Initialize the Kubernetes object we use to talk to the Kubernetes API.

    Args:
        inCluster (boolean): controls wether the code runs inside a pod (inCluster = True)
                             or locally (access via .kube / kubectl, inCluster = False)
    Return:
        K8s object
        The global variables otcs_replicas_frontend and otcs_replicas_backend are initialized
    """

    global otcs_replicas_frontend
    global otcs_replicas_backend

    logger.info("Connect to Kubernetes, inCluster -> {}".format(inCluster))

    k8s_object = k8s.K8s(inCluster)
    if k8s_object:
        logger.info("Kubernetes API is ready now.")
    else:
        logger.error("Cannot establish connection to Kubernetes.")

    # Get number of replicas for frontend:
    otcs_frontend_scale = k8s_object.getStatefulSetScale(OTCS_K8S_STATEFUL_SET_FRONTEND)
    if not otcs_frontend_scale:
        logger.error(
            "Cannot find Kubernetes Stateful Set for OTCS Frontends -> {}".format(
                OTCS_K8S_STATEFUL_SET_FRONTEND
            )
        )
        return False
    otcs_replicas_frontend = otcs_frontend_scale.spec.replicas
    logger.info(
        "Stateful Set -> {} has -> {} replicas".format(
            OTCS_K8S_STATEFUL_SET_FRONTEND, otcs_replicas_frontend
        )
    )

    # Get number of replicas for backend:
    otcs_backend_scale = k8s_object.getStatefulSetScale(OTCS_K8S_STATEFUL_SET_BACKEND)
    if not otcs_backend_scale:
        logger.error(
            "Cannot find Kubernetes Stateful Set for OTCS Backends -> {}".format(
                OTCS_K8S_STATEFUL_SET_BACKEND
            )
        )
        return False
    otcs_replicas_backend = otcs_backend_scale.spec.replicas
    logger.info(
        "Stateful Set -> {} has -> {} replicas".format(
            OTCS_K8S_STATEFUL_SET_BACKEND, otcs_replicas_backend
        )
    )

    return k8s_object

    # end function definition


def initOTDS():
    """Initialize the OTDS object and parameters and authenticate at OTDS once it is ready.

    Args:
        None
    Returns:
        object: OTDS object
    """

    logger.info("Connection parameters OTDS:")
    logger.info("OTDS Protocol          = " + OTDS_PROTOCOL)
    logger.info("OTDS Public Protocol   = " + OTDS_PUBLIC_PROTOCOL)
    logger.info("OTDS Hostname          = " + OTDS_HOSTNAME)
    logger.info("OTDS Public URL        = " + OTDS_PUBLIC_URL)
    logger.info("OTDS Port              = " + str(OTDS_PORT))
    logger.info("OTDS Admin User        = " + OTDS_ADMIN)
    logger.debug("OTDS Admin Password   = " + OTDS_PASSWORD)
    logger.info("OTDS Admin Partition   = " + OTDS_ADMIN_PARTITION)

    otds_object = otds.OTDS(
        OTDS_PROTOCOL, OTDS_HOSTNAME, OTDS_PORT, OTDS_ADMIN, OTDS_PASSWORD
    )

    logger.info("Authenticating to OTDS...")
    otds_cookie = otds_object.authenticate()
    while otds_cookie is None:
        logger.warning("Waiting 30 seconds for OTDS to become ready...")
        time.sleep(30)
        otds_cookie = otds_object.authenticate()
    logger.info("OTDS is ready now.")

    logger.info("Enable OTDS audit...")
    otds_object.enableAudit()

    return otds_object

    # end function definition


def initOTAC(k8s_object: object) -> object:
    """Initialize the OTAC object and parameters.
       Configure the Archive Server as a known server
       if environment variable OTAC_KNOWN_SERVER is set.

    Args: None
    Return:
        OTAC object
    """

    logger.info("Connection parameters OTAC:")
    logger.info("OTAC Protocol          = " + OTAC_PROTOCOL)
    logger.info("OTAC Hostname          = " + OTAC_HOSTNAME)
    logger.info("OTAC Public URL        = " + OTAC_PUBLIC_URL)
    logger.info("OTAC Port              = " + str(OTAC_PORT))
    logger.info("OTAC Admin User        = " + OTAC_ADMIN)
    logger.debug("OTAC Admin Password   = " + OTAC_PASSWORD)
    logger.info(
        "OTAC Known Server      = "
        + (OTAC_KNOWN_SERVER if OTAC_KNOWN_SERVER != "" else "<not configured>")
    )

    otac_object = otac.OTAC(
        OTAC_PROTOCOL,
        OTAC_HOSTNAME,
        OTAC_PORT,
        OTAC_ADMIN,
        OTAC_PASSWORD,
        OTDS_ADMIN,
        OTDS_PASSWORD,
    )

    # is there a known server configured for Archive Center (to sync content with)
    if otac_object and OTAC_KNOWN_SERVER != "":
        # wait until the OTAC pod is in ready state
        logger.info("Waiting for Archive Center to become ready...")
        k8s_object.waitPodCondition(OTAC_K8S_POD_NAME, "Ready")

        logger.info("Configure known host for Archive Center...")
        response = otac_object.execCommand(
            "cf_create_host {} 0 /archive 8080 8090".format(OTAC_KNOWN_SERVER)
        )
        if not response or not response.ok:
            logger.error("Failed to configure known host for Archive Center!")

        logger.info("Configure host alias for Archive Center...")
        response = otac_object.execCommand(
            "cf_set_variable MY_HOST_ALIASES {},{},otac DS".format(
                OTAC_K8S_POD_NAME, OTAC_PUBLIC_URL
            )
        )
        if not response or not response.ok:
            logger.error("Failed to configure host alias for Archive Center!")

        # Restart the spawner in Archive Center:
        logger.info("Restart Archive Center Spawner...")
        restartOTACPod(k8s_object)
    else:
        logger.info(
            "Skip configuration of known host for Archive Center (OTAC_KNOWN_SERVER is not set)."
        )

    return otac_object

    # end function definition


def initOTCS(
    otds_object: object,
    hostname: str = OTCS_HOSTNAME,
    port: int = OTCS_HOSTNAME,
    partition_name: str = OTCS_PARTITION,
    resource_name: str = OTCS_RESOURCE_NAME,
) -> object:
    """Initialize the OTCS class and parameters and authenticate at OTCS once it is ready.

    Args:
        otds_object (object): OTDS object that has been created before
        hostname (string): OTCS hostname
        port (integer): port number of OTCS
        partition_name: name of OTDS Partition for Extended ECM users
        resource_name: name of OTDS resource for Extended ECM
    Returns:
        object: OTCS object
    """

    global placeholder_values

    logger.info("Connection parameters OTCS (Extended ECM):")
    logger.info("OTCS Protocol              = " + OTCS_PROTOCOL)
    logger.info("OTCS Public Protocol       = " + OTCS_PUBLIC_PROTOCOL)
    logger.info("OTCS Hostname              = " + hostname)
    logger.info("OTCS Public URL            = " + OTCS_PUBLIC_URL)
    logger.info("OTCS Port                  = " + str(port))
    logger.info("OTCS Admin User            = " + OTCS_ADMIN)
    logger.debug("OTCS Admin Password       = " + OTCS_PASSWORD)
    logger.info("OTCS User Partition        = " + partition_name)
    logger.info("OTCS Resource Name         = " + resource_name)
    logger.info("OTCS User Default License  = " + OTCS_LICENSE_FEATURE)
    logger.info("OTCS K8s Frontend Pods     = " + OTCS_K8S_STATEFUL_SET_FRONTEND)
    logger.info("OTCS K8s Backend Pods      = " + OTCS_K8S_STATEFUL_SET_BACKEND)

    otcs_object = otcs.OTCS(
        OTCS_PROTOCOL,
        hostname,
        port,
        OTCS_ADMIN,
        OTCS_PASSWORD,
        partition_name,
        resource_name,
    )

    # It is important to wait for OTCS to be configured - otherwise we
    # may interfere with the OTCS container automation and run into errors
    logger.info("Wait for OTCS to be configured...")
    otcs_configured = otcs_object.isConfigured()
    while not otcs_configured:
        logger.warning("OTCS is not configured yet. Waiting 30 seconds...")
        time.sleep(30)
        otcs_configured = otcs_object.isConfigured()
    logger.info("OTCS is configured now.")

    logger.info("Authenticating to OTCS...")
    otcs_cookie = otcs_object.authenticate()
    while otcs_cookie is None:
        logger.warning("Waiting 30 seconds for OTCS to become ready...")
        time.sleep(30)
        otcs_cookie = otcs_object.authenticate()
    logger.info("OTCS is ready now.")

    # Set first name and last name of Admin user (ID = 1000):
    otcs_object.updateUser(1000, field="first_name", value="Terrarium")
    otcs_object.updateUser(1000, field="last_name", value="Admin")

    if not "OTCS_RESSOURCE_ID" in placeholder_values:
        placeholder_values["OTCS_RESSOURCE_ID"] = otds_object.getResource(
            OTCS_RESOURCE_NAME
        )["resourceID"]
        logger.debug(
            "Placeholder values after OTCS init = {}".format(placeholder_values)
        )

    if OTAWP_ENABLED == "true":
        otcs_resource = otds_object.getResource(OTCS_RESOURCE_NAME)
        otcs_resource[
            "logoutURL"
        ] = f"{OTAWP_PUBLIC_PROTOCOL}://{OTAWP_PUBLIC_URL}/home/system/wcp/sso/sso_logout.htm"
        otcs_resource["logoutMethod"] = "GET"

        otds_object.updateResource(name="cs", resource=otcs_resource)

    # Allow impersonation of the resource for all users:
    otds_object.impersonateResource(resource_name)

    return otcs_object

    # end function definition


def initOTIV(otds_object: object) -> object:
    """Initialize the OTIV (Intelligent Viewing) object and its OTDS settings.

    Args:
        otds_object (object): OTDS object
    Returns:
        objects: OTIV object
    """

    logger.info("Parameters for OTIV (Intelligent Viewing):")
    logger.info("OTDS Resource Name       = " + OTIV_RESOURCE_NAME)
    logger.info("OTIV License File        = " + OTIV_LICENSE_FILE)
    logger.info("OTIV Product Name        = " + OTIV_PRODUCT_NAME)
    logger.info("OTIV Product Description = " + OTIV_PRODUCT_DESCRIPTION)
    logger.info("OTIV License Feature     = " + OTIV_LICENSE_FEATURE)

    otiv_object = otiv.OTIV(
        OTIV_RESOURCE_NAME,
        OTIV_PRODUCT_NAME,
        OTIV_PRODUCT_DESCRIPTION,
        OTIV_LICENSE_FILE,
        OTIV_LICENSE_FEATURE,
    )

    otds_resource = otds_object.getResource(OTIV_RESOURCE_NAME)
    if not otds_resource:
        logger.error("OTDS Resource -> {} for Intelligent Viewing not found.")
        return

    otiv_license = otds_object.addLicenseToResource(
        OTIV_LICENSE_FILE,
        OTIV_PRODUCT_NAME,
        OTIV_PRODUCT_DESCRIPTION,
        otds_resource["resourceID"],
    )
    if not otiv_license:
        logger.info(
            "Couldn't apply license -> {} for product -> {}. Intelligent Viewing may not be deployed!".format(
                OTIV_LICENSE_FILE, OTIV_PRODUCT_NAME
            )
        )
        return None

    return otiv_object

    # end function definition


def initOTPD(k8s_object: object) -> object:
    """Initialize the OTPD (PowerDocs) object and parameters.

    Args:
        None
    Returns:
        object: OTPD (PowerDocs) object
    """

    logger.info("Connection parameters OTPD (PowerDocs):")
    logger.info("OTPD Protocol             = " + OTPD_PROTOCOL)
    logger.info("OTPD Hostname             = " + OTPD_HOSTNAME)
    logger.info("OTPD Port                 = " + str(OTPD_PORT))
    logger.info("OTPD API User             = " + OTPD_USER)
    logger.info("OTPD Tenant               = " + OTPD_TENANT)
    logger.info(
        "OTPD Database Import File = "
        + (OTPD_DBIMPORTFILE if OTPD_DBIMPORTFILE != "" else "<not configured>")
    )
    logger.info("OTPD K8s Pod Name         = " + OTPD_K8S_POD_NAME)

    otpd_object = otpd.OTPD(
        OTPD_PROTOCOL, OTPD_HOSTNAME, OTPD_PORT, OTPD_USER, OTPD_PASSWORD
    )

    # wait until the OTPD pod is in ready state
    k8s_object.waitPodCondition(OTPD_K8S_POD_NAME, "Ready")

    # Fix settings for local Kubernetes deployments.
    # Unclear why this is not the default.
    if otpd_object:
        otpd_object.applySetting("LocalOtdsUrl", "http://otds/otdsws")
        otpd_object.applySetting(
            "LocalApplicationServerUrlForContentManager",
            "http://localhost:8080/c4ApplicationServer",
            OTPD_TENANT,
        )

    return otpd_object

    # end function definition


def initOTAWP(otds_object: object, k8s_object: object):
    """Initialize OTDS for Appworks Platform
    Args:
        otds_object: OTDS object
        k8s_object: Kubernetes object
    Return: None
    """

    global placeholder_values

    logger.info("Connection parameters OTAWP:")
    logger.info("OTAWP Enabled          = " + OTAWP_ENABLED)
    logger.info("OTAWP Resource         = " + OTAWP_RESOURCE_NAME)
    logger.info("OTAWP Access Role      = " + OTAWP_ACCESS_ROLE_NAME)
    logger.info("OTAWP Admin User       = " + OTAWP_ADMIN)
    logger.debug("OTAWP Password         = " + OTAWP_PASSWORD)
    logger.info("OTAWP K8s Stateful Set = " + OTAWP_K8S_STATEFUL_SET)
    logger.info("OTAWP K8s Config Map   = " + OTAWP_K8S_CONFIGMAP)

    logger.info(
        "Wait for OTCS to create its OTDS resource with name -> {}...".format(
            OTCS_RESOURCE_NAME
        )
    )

    # Loop to wait for OTCS to create its OTDS resource
    # (we need it to update the AppWorks K8s Config Map):
    otcs_resource = otds_object.getResource(OTCS_RESOURCE_NAME)
    while otcs_resource is None:
        logger.warning(
            "OTDS resource for Content Server with name -> {} does not exist yet. Waiting...".format(
                OTCS_RESOURCE_NAME
            )
        )
        time.sleep(30)
        otcs_resource = otds_object.getResource(OTCS_RESOURCE_NAME)

    otcs_resource_id = otcs_resource["resourceID"]

    logger.info("OTDS resource ID for Content Server -> {}".format(otcs_resource_id))

    # make sure code is idempotent and only try to add ressource if it doesn't exist already:
    awp_resource = otds_object.getResource(OTAWP_RESOURCE_NAME)
    if not awp_resource:
        logger.info(
            "OTDS resource -> {} for AppWorks Platform does not yet exist. Creating...".format(
                OTAWP_RESOURCE_NAME
            )
        )
        # Create a Python dict with the special payload we need for AppWorks:
        additional_payload = {}
        additional_payload["connectorid"] = "rest"
        additional_payload["resourceType"] = "rest"
        user_attribute_mapping = [
            {
                "sourceAttr": ["oTExternalID1"],
                "destAttr": "__NAME__",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["displayname"],
                "destAttr": "DisplayName",
                "mappingFormat": "%s",
            },
            {"sourceAttr": ["mail"], "destAttr": "Email", "mappingFormat": "%s"},
            {
                "sourceAttr": ["oTTelephoneNumber"],
                "destAttr": "Telephone",
                "mappingFormat": "%s",
            },
            {"sourceAttr": ["oTMobile"], "destAttr": "Mobile", "mappingFormat": "%s"},
            {
                "sourceAttr": ["oTFacsimileTelephoneNumber"],
                "destAttr": "Fax",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTStreetAddress,l,st,postalCode,c"],
                "destAttr": "Address",
                "mappingFormat": "%s%n%s %s %s%n%s",
            },
            {"sourceAttr": ["oTCompany"], "destAttr": "Company", "mappingFormat": "%s"},
            {
                "sourceAttr": ["ds-pwp-account-disabled"],
                "destAttr": "AccountDisabled",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTExtraAttr9"],
                "destAttr": "IsServiceAccount",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["custom:proxyConfiguration"],
                "destAttr": "ProxyConfiguration",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["c"],
                "destAttr": "Identity-CountryOrRegion",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["gender"],
                "destAttr": "Identity-Gender",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["displayName"],
                "destAttr": "Identity-DisplayName",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTStreetAddress"],
                "destAttr": "Identity-Address",
                "mappingFormat": "%s",
            },
            {"sourceAttr": ["l"], "destAttr": "Identity-City", "mappingFormat": "%s"},
            {
                "sourceAttr": ["mail"],
                "destAttr": "Identity-Email",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["givenName"],
                "destAttr": "Identity-FirstName",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["sn"],
                "destAttr": "Identity-LastName",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["initials"],
                "destAttr": "Identity-MiddleNames",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTMobile"],
                "destAttr": "Identity-Mobile",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["postalCode"],
                "destAttr": "Identity-PostalCode",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["st"],
                "destAttr": "Identity-StateOrProvince",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["title"],
                "destAttr": "Identity-title",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["physicalDeliveryOfficeName"],
                "destAttr": "Identity-physicalDeliveryOfficeName",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTFacsimileTelephoneNumber"],
                "destAttr": "Identity-oTFacsimileTelephoneNumber",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["notes"],
                "destAttr": "Identity-notes",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTCompany"],
                "destAttr": "Identity-oTCompany",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTDepartment"],
                "destAttr": "Identity-oTDepartment",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["birthDate"],
                "destAttr": "Identity-Birthday",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["cn"],
                "destAttr": "Identity-UserName",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["Description"],
                "destAttr": "Identity-UserDescription",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["oTTelephoneNumber"],
                "destAttr": "Identity-Phone",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["displayName"],
                "destAttr": "Identity-IdentityDisplayName",
                "mappingFormat": "%s",
            },
        ]
        additional_payload["userAttributeMapping"] = user_attribute_mapping
        group_attribute_mapping = [
            {
                "sourceAttr": ["cn"],
                "destAttr": "__NAME__",
                "mappingFormat": '%js:function format(name) { return name.replace(/&/g,"-and-"); }',
            },
            {
                "sourceAttr": ["description"],
                "destAttr": "Description",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["description"],
                "destAttr": "Identity-Description",
                "mappingFormat": "%s",
            },
            {
                "sourceAttr": ["displayName"],
                "destAttr": "Identity-DisplayName",
                "mappingFormat": "%s",
            },
        ]
        additional_payload["groupAttributeMapping"] = group_attribute_mapping
        additional_payload["connectorName"] = "REST (Generic)"
        additional_payload["pcCreatePermissionAllowed"] = "true"
        additional_payload["pcModifyPermissionAllowed"] = "true"
        additional_payload["pcDeletePermissionAllowed"] = "false"
        additional_payload["connectionParamInfo"] = [
            {
                "name": "fBaseURL",
                "value": "http://appworks:8080/home/system/app/otdspush",
            },
            {"name": "fUsername", "value": OTAWP_ADMIN},
            {"name": "fPassword", "value": OTAWP_PASSWORD},
        ]

        awp_resource = otds_object.addResource(
            OTAWP_RESOURCE_NAME,
            "AppWorks Platform",
            "AppWorks Platform",
            additional_payload,
        )
    else:
        logger.info(
            "OTDS resource -> {} for AppWorks Platform does already exist.".format(
                OTAWP_RESOURCE_NAME
            )
        )

    awp_resource_id = awp_resource["resourceID"]

    logger.info("OTDS resource ID for AppWorks Platform -> {}".format(awp_resource_id))

    placeholder_values["OTAWP_RESOURCE_ID"] = str(awp_resource_id)

    logger.debug("Placeholder values after OTAWP init = {}".format(placeholder_values))

    logger.info("Update AppWorks Kubernetes Config Map with OTDS resource IDs...")

    config_map = k8s_object.getConfigMap(OTAWP_K8S_CONFIGMAP)
    if not config_map:
        logger.error(
            "Failed to retrieve AppWorks Kubernetes Config Map -> {}".format(
                OTAWP_K8S_CONFIGMAP
            )
        )
    else:
        solution = yaml.safe_load(config_map.data["solution.yaml"])

        # Change values as required
        solution["platform"]["organizations"]["system"]["otds"][
            "resourceId"
        ] = awp_resource_id
        solution["platform"]["content"]["ContentServer"][
            "contentServerUrl"
        ] = "{}://{}/cs/cs".format(OTCS_PUBLIC_PROTOCOL, OTCS_PUBLIC_URL)
        solution["platform"]["content"]["ContentServer"][
            "contentServerSupportDirectoryUrl"
        ] = "{}://{}/cssupport".format(OTCS_PUBLIC_PROTOCOL, OTCS_PUBLIC_URL)
        solution["platform"]["content"]["ContentServer"][
            "otdsResourceId"
        ] = otcs_resource_id
        solution["platform"]["authenticators"]["OTDS_auth"]["publicLoginUrl"] = (
            OTDS_PUBLIC_PROTOCOL + "://" + OTDS_PUBLIC_URL + "/otdsws/login"
        )
        solution["platform"]["security"]["contentSecurityPolicy"] = (
            "frame-ancestors 'self' " + OTCS_PUBLIC_PROTOCOL + "://" + OTCS_PUBLIC_URL
        )
        data = {"solution.yaml": yaml.dump(solution)}
        result = k8s_object.replaceConfigMap(OTAWP_K8S_CONFIGMAP, data)
        if result:
            logger.info("Successfully updated AppWorks Solution YAML.")
        else:
            logger.error("Failed to update AppWorks Solution YAML.")
        logger.debug("Solution YAML for AppWorks -> {}".format(solution))

    logger.info("Scale AppWorks Kubernetes Stateful Set to 1...")
    k8s_object.scaleStatefulSet(sts_name=OTAWP_K8S_STATEFUL_SET, scale=1)

    # Add the OTCS Admin user to the AppWorks Access Role in OTDS
    otds_object.addUserToAccessRole(
        "Access to " + OTAWP_RESOURCE_NAME, "otadmin@otds.admin"
    )

    # Loop to wait for OTCS to create its OTDS user partition:
    otcs_partition = otds_object.getPartition(OTCS_PARTITION)
    while otcs_partition is None:
        logger.warning(
            "OTDS user partition for Content Server with name -> {} does not exist yet. Waiting...".format(
                OTCS_PARTITION
            )
        )
        time.sleep(30)
        otcs_partition = otds_object.getPartition(OTCS_PARTITION)

    # Add the OTDS user partition for OTCS to the AppWorks Platform Access Role in OTDS.
    # This will effectvely sync all OTCS users with AppWorks Platform:
    otds_object.addPartitionToAccessRole(OTAWP_ACCESS_ROLE_NAME, OTCS_PARTITION)

    # Add the OTDS admin partition to the AppWorks Platform Access Role in OTDS.
    otds_object.addPartitionToAccessRole(OTAWP_ACCESS_ROLE_NAME, OTDS_ADMIN_PARTITION)

    # Set Group inclusion for Access Role for OTAWP to "True":
    otds_object.updateAccessRoleAttributes(
        OTAWP_ACCESS_ROLE_NAME, [{"name": "pushAllGroups", "values": ["True"]}]
    )

    # Add ResourceID User to OTDSAdmin to allow push
    otds_object.addUserToGroup(
        user=str(awp_resource_id) + "@otds.admin", group="otdsadmins@otds.admin"
    )

    # Allow impersonation for all users:
    otds_object.impersonateResource(OTAWP_RESOURCE_NAME)

    # end function definition


def restartOTCSPods(otcs_object: object, k8s_object: object):
    """Restart the Content Server service in all OTCS pods

    Args:
        otcs_object: OTCS class instance (object)
        k8s_object: Kubernetes object
    Returns:
        None
    """

    global otcs_replicas_frontend
    global otcs_replicas_backend

    logger.info("Restart OTCS frontend and backend pods...")

    # Restart all frontends:
    for x in range(0, otcs_replicas_frontend):
        pod_name = OTCS_K8S_STATEFUL_SET_FRONTEND + "-" + str(x)

        logger.info("Deactivate Liveness probe for pod -> {}".format(pod_name))
        k8s_object.execPodCommand(pod_name, ["/bin/sh", "-c", "touch /tmp/keepalive"])
        logger.info("Restarting pod -> {}".format(pod_name))
        k8s_object.execPodCommand(
            pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/stop_csserver"]
        )
        k8s_object.execPodCommand(
            pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/start_csserver"]
        )

    # Restart all backends:
    for x in range(0, otcs_replicas_backend):
        pod_name = OTCS_K8S_STATEFUL_SET_BACKEND + "-" + str(x)

        logger.info("Deactivate Liveness probe for pod -> {}".format(pod_name))
        k8s_object.execPodCommand(pod_name, ["/bin/sh", "-c", "touch /tmp/keepalive"])
        logger.info("Restarting pod -> {}".format(pod_name))
        k8s_object.execPodCommand(
            pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/stop_csserver"]
        )
        k8s_object.execPodCommand(
            pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/start_csserver"]
        )

    logger.info("Re-Authenticating to OTCS after restart of pods...")
    otcs_cookie = otcs_object.authenticate(revalidate=True)
    while otcs_cookie is None:
        logger.warning("Waiting 30 seconds for OTCS to become ready...")
        time.sleep(30)
        otcs_cookie = otcs_object.authenticate(revalidate=True)
    logger.info("OTCS is ready again.")

    # Reactivate Liveness probes in all pods:
    for x in range(0, otcs_replicas_frontend):
        pod_name = OTCS_K8S_STATEFUL_SET_FRONTEND + "-" + str(x)

        logger.info("Reactivate Liveness probe for pod -> {}".format(pod_name))
        k8s_object.execPodCommand(pod_name, ["/bin/sh", "-c", "rm /tmp/keepalive"])

    for x in range(0, otcs_replicas_backend):
        pod_name = OTCS_K8S_STATEFUL_SET_BACKEND + "-" + str(x)

        logger.info("Reactivate Liveness probe for pod -> {}".format(pod_name))
        k8s_object.execPodCommand(pod_name, ["/bin/sh", "-c", "rm /tmp/keepalive"])

    logger.info("Restart OTCS frontend and backend pods has been completed.")

    # end function definition


def restartOTACPod(k8s_object: object) -> bool:
    """Restart the Archive Center spawner service in OTAC pod

    Args:
        k8s_object (object): Kubernetes object
    Returns:
        boolean: True if restart was done, False if error occured
    """

    if not OTAC_ENABLED:
        return False

    logger.info(
        "Restarting spawner service in Archive Center pod -> {}".format(
            OTAC_K8S_POD_NAME
        )
    )
    # The Archive Center Spawner needs to be run in "interactive" mode - otherwise the command will "hang":
    # The "-c" parameter is not required in this case
    # False is given as parameter as OTAC writes non-errors to stderr
    response = k8s_object.execPodCommandInteractive(
        OTAC_K8S_POD_NAME, ["/bin/sh", "/etc/init.d/spawner restart"], 60, False
    )

    if response:
        return True
    else:
        return False

    # end function definition


def restartOTAWPPod(k8s_object: object):
    """Delete the AppWorks Platform Pod to make Kubernetes restart it.

    Args:
        k8s_object: Kubernetes object
    Returns:
        None
    """

    k8s_object.deletePod(OTAWP_K8S_STATEFUL_SET + "-0")

    # end function definition


def consolidateOTDS(otds_object: object):
    """Consolidate OTDS resources
    Args:
        otds_object: OTDS object
    Return: None
    """

    otds_object.consolidate(OTCS_RESOURCE_NAME)

    if OTAWP_ENABLED == "true":  # is AppWorks Platform deployed?
        otds_object.consolidate(OTAWP_RESOURCE_NAME)

    # end function definition


def importPowerDocsConfiguration(otpd_object: object):
    """Import a database export (zip file) into the PowerDocs database

    Args:
        otpd_object (object): PowerDocs object
    """

    if OTPD_DBIMPORTFILE.startswith("http"):
        # Download file from remote location specified by the OTPD_DBIMPORTFILE
        # this must be a public place without authentication:
        logger.info(
            "Download PowerDocs database file from URL -> {}".format(OTPD_DBIMPORTFILE)
        )

        try:
            package = requests.get(OTPD_DBIMPORTFILE)
            package.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error -> {}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting -> {}".format(errc))
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error -> {}".format(errt))
        except requests.exceptions.RequestException as err:
            logger.error("Request error -> {}".format(err))

        logger.info(
            "Successfully downloaded PowerDocs database file -> {}; status code -> {}".format(
                OTPD_DBIMPORTFILE, package.status_code
            )
        )
        filename = "/tmp/otpd_db_import.zip"
        with open(filename, mode="wb") as localfile:
            localfile.write(package.content)

        logger.info(
            "Starting import on {}://{}:{} of {}".format(
                OTPD_PROTOCOL, OTPD_HOSTNAME, OTPD_PORT, OTPD_DBIMPORTFILE
            )
        )
        response = otpd_object.importDatabase(filename=filename)
        logger.info("Response -> {}".format(response))

    # end function definition


def customization_run():
    # Initialize the OTDS, OTCS and OTPD objects and wait for the
    # pods to be ready. If any of this fails we bail out:

    logger.info("========== Initialize OTDS ==============")

    otds_object = initOTDS()
    if not otds_object:
        logger.error("Failed to initialize OTDS - exiting...")
        sys.exit()

    # Establish in-cluster Kubernetes connection
    logger.info("========== Initialize Kubernetes ============")
    if K8S_ENABLED:
        k8s_object = initK8s(inCluster=True)

        if not k8s_object:
            logger.error("Failed to initialize Kubernetes - exiting...")
            sys.exit()
    else:
        k8s_object = None

    # Put Frontend in Maintenance mode to make sure nobody interferes
    # during customization:
    if OTCS_MAINTENANCE_MODE:
        logger.info("========== Enable Maintenance Mode ==========")
        logger.info(
            "Put OTCS frontends in Maitenance Mode by changing the Kubernetes Ingress backend service..."
        )
        k8s_object.updateIngressBackendServices(
            OTCS_K8S_INGRESS,
            "otcs",
            OTCS_MAINTENANCE_SERVICE_NAME,
            OTCS_MAINTENANCE_SERVICE_PORT,
        )
        logger.info("OTCS frontend is now in Maintenance Mode!")

    if OTAWP_ENABLED == "true":  # is AppWorks Platform deployed?
        logger.info("========== Initialize OTAWP =============")

        # Configure required OTDS resources as AppWorks doesn't do this on its own:
        initOTAWP(otds_object, k8s_object)
    else:
        placeholder_values["OTAWP_RESOURCE_ID"] = ""

    if O365_ENABLED == "true":  # is M365 enabled?
        logger.info("======== Initialize MS Graph API ========")

        # Initialize the M365 object and connection to M365 Graph API:
        m365_object = initM365()
    else:
        m365_object = None

    logger.info("========== Initialize OTCS backend ======")
    otcs_backend_object = initOTCS(
        otds_object, OTCS_HOSTNAME_BACKEND, OTCS_PORT_BACKEND, OTCS_PARTITION
    )
    if not otcs_backend_object:
        logger.error("Failed to initialize OTCS backend - exiting...")
        sys.exit()

    logger.info("========== Initialize OTCS frontend =====")
    otcs_frontend_object = initOTCS(
        otds_object, OTCS_HOSTNAME_FRONTEND, OTCS_PORT_FRONTEND, OTCS_PARTITION
    )
    if not otcs_frontend_object:
        logger.error("Failed to initialize OTCS frontend - exiting...")
        sys.exit()

    if OTAC_ENABLED == "true":  # is Archive Center deployed?
        logger.info("========== Initialize OTAC ==============")

        otac_object = initOTAC(k8s_object)
        if not otac_object:
            logger.error("Failed to initialize OTAC - exiting...")
            sys.exit()
    else:
        otac_object = None

    if OTIV_ENABLED == "true":  # is PowerDocs deployed?
        logger.info("========== Initialize OTIV ==============")

        otiv_object = initOTIV(otds_object)
    else:
        otiv_object = None

    if OTPD_ENABLED == "true":  # is PowerDocs deployed?
        logger.info("========== Initialize OTPD ==============")

        otpd_object = initOTPD(k8s_object)
        if not otpd_object:
            logger.error("Failed to initialize OTPD - exiting...")
            sys.exit()
    else:
        otpd_object = None

    if (
        O365_ENABLED == "true" and O365_USER and O365_PASSWORD
    ):  # is M365 enabled and do we have the required credentials?
        logger.info("======== Upload MS Teams App ============")

        # Download MS Teams App from OTCS (this has with 23.2 a nasty side-effect
        # of unsetting 2 checkboxes on that config page - we reset these checkboxes
        # with the settings file "O365Settings.xml"):
        response = otcs_frontend_object.downloadConfigFile(
            "/cs/cs?func=officegroups.DownloadTeamsPackage", "/tmp/ot.xecm.teams.zip"
        )
        user_access_token = m365_object.authenticateUser(O365_USER, O365_PASSWORD)

        # Check if the app is already installed:
        response = m365_object.getTeamsApps(
            "contains(displayName, '{}')".format(O365_TEAMS_APP_NAME)
        )
        if m365_object.existResultItem(response, "displayName", O365_TEAMS_APP_NAME):
            logger.info(
                "Extended ECM Teams App is already in app catalog. Trying to install an update (may give a warning if it is not a new version)..."
            )
            app_id = m365_object.getResultValue(
                response, "id", 0
            )  # 0 = Index = first item
            logger.info(
                "Extended ECM Teams App is already in app catalog (app ID -> {}). Updating existing app...".format(
                    app_id
                )
            )
            response = m365_object.uploadTeamsApp(
                "/tmp/ot.xecm.teams.zip", update_existing_app=True, app_id=app_id
            )
        else:
            # this upload will be done with the user credentials - this is required:
            logger.info(
                "Extended Teams ECM App is not yet in app catalog. Installing as new app..."
            )
            response = m365_object.uploadTeamsApp("/tmp/ot.xecm.teams.zip")

    # Set totalStartTime for duration calculation
    totalStartTime = datetime.now()

    logger.info("========== Processing Payload ===========")

    cust_payload_list = [CUST_PAYLOAD]

    # do we have additional payload as an external file?
    if os.path.exists(CUST_PAYLOAD_EXTERNAL):
        for filename in os.scandir(CUST_PAYLOAD_EXTERNAL):
            if filename.is_file() and os.path.getsize(filename) > 0:
                logger.info("Found external payload file -> {}".format(filename.path))
                cust_payload_list.append(filename.path)
    else:
        logger.info("No external payload file -> {}".format(CUST_PAYLOAD_EXTERNAL))

    for cust_payload in cust_payload_list:
        # Open the payload file. If this fails we bail out:
        logger.info("Starting processing of payload -> {}".format(cust_payload))

        # Set startTime for duration calculation
        totalStartTime = datetime.now()

        payload_object = payload.Payload(
            payload_source=cust_payload,
            custom_settings_dir=CUST_SETTINGS_DIR,
            k8s_object=k8s_object,
            otds_object=otds_object,
            otac_object=otac_object,
            otcs_backend_object=otcs_backend_object,
            otcs_frontend_object=otcs_frontend_object,
            otcs_restart_callback=restartOTCSPods,
            otiv_object=otiv_object,
            m365_object=m365_object,
            placeholder_values=placeholder_values, # this dict includes placeholder replacements for the Ressource IDs of OTAWP and OTCS
            stop_on_error=True if LOGLEVEL == "DEBUG" else False,
        )
        # Load the payload file and initialize the payload sections:
        if not payload_object.initPayload():
            logger.error(
                "Failed to initialize payload -> {} - skipping...".format(cust_payload)
            )
            continue

        # Now process the payload in the defined ordering:
        payload_object.processPayload()

        logger.info("========== Consolidate OTDS Resources ==================")
        consolidateOTDS(otds_object)

        # Upload payload file for later review to Enterprise Workspace
        logger.info("========== Upload Payload file to Extended ECM =========")
        response = otcs_backend_object.getNodeFromNickname(CUST_TARGET_FOLDER_NICKNAME)
        target_folder_id = otcs_backend_object.getResultValue(response, "id")
        if not target_folder_id:
            target_folder_id = 2000  # use Enterprise Workspace as fallback
        # Write YAML file with upadated payload (including IDs, etc.).
        # We need to write to /tmp as initial location is read-only:
        cust_payload = "/tmp/" + os.path.basename(cust_payload)
        with open(cust_payload, "w") as f:
            data = yaml.dump(payload_object.getPayload(), f)

        # Check if the payload file has been uploaded before.
        # This can happen if we re-run the python container.
        # In this case we add a version to the existing document:
        response = otcs_backend_object.getNodeByParentAndName(
            target_folder_id, os.path.basename(cust_payload)
        )
        target_document_id = otcs_backend_object.getResultValue(response, "id")
        if target_document_id:
            response = otcs_backend_object.addDocumentVersion(
                target_document_id,
                cust_payload,
                os.path.basename(cust_payload),
                "text/plain",
                "Updated payload file after re-run of customization",
            )
        else:
            response = otcs_backend_object.uploadFileToParent(
                cust_payload,
                os.path.basename(cust_payload),
                "text/plain",
                target_folder_id,
            )

        duration = datetime.now() - totalStartTime
        logger.info(
            "========== Payload -> {} completed execution in {} ===".format(
                cust_payload, duration
            )
        )

    if OTCS_MAINTENANCE_MODE:
        # Changing the Ingress backend service to OTCS frontend service:
        logger.info(
            "Put OTCS frontend back in Production Mode by changing the Kubernetes Ingress backend service..."
        )
        k8s_object.updateIngressBackendServices(
            OTCS_K8S_INGRESS,
            "otcs",
            OTCS_HOSTNAME_FRONTEND,
            OTCS_PORT_FRONTEND,
        )
        logger.info("OTCS frontend is now back in Production Mode!")

    # Restart OTCS frontend and backend pods:
    # logger.info("Restart OTCS frontend and backend pods...")
    # restartOTCSPods(otcs_backend_object, k8s_object)
    # # give some additional time to make sure service is responsive
    # time.sleep(30)
    # logger.info("Restart OTCS frontend and backend pods has been completed.")

    # Restart AppWorksPlatform pod if it is deployed (to make settings effective):
    if OTAWP_ENABLED == "true":  # is AppWorks Platform deployed?
        logger.info("Restart OTAWP pod...")
        restartOTAWPPod(k8s_object)

    # Upload log file for later review to "Deployment" folder in "Administration" folder
    if os.path.exists(CUST_LOG_FILE):
        logger.info("========== Upload log file to Extended ECM =============")
        response = otcs_backend_object.getNodeFromNickname(CUST_TARGET_FOLDER_NICKNAME)
        target_folder_id = otcs_backend_object.getResultValue(response, "id")
        if not target_folder_id:
            target_folder_id = 2000  # use Enterprise Workspace as fallback
        # Check if the log file has been uploaded before.
        # This can happen if we re-run the python container:
        # In this case we add a version to the existing document:
        response = otcs_backend_object.getNodeByParentAndName(
            target_folder_id, os.path.basename(CUST_LOG_FILE)
        )
        target_document_id = otcs_backend_object.getResultValue(response, "id")
        if target_document_id:
            response = otcs_backend_object.addDocumentVersion(
                target_document_id,
                CUST_LOG_FILE,
                os.path.basename(CUST_LOG_FILE),
                "text/plain",
                "Updated Python Log after re-run of customization",
            )
        else:
            response = otcs_backend_object.uploadFileToParent(
                CUST_LOG_FILE,
                os.path.basename(CUST_LOG_FILE),
                "text/plain",
                target_folder_id,
            )

    totalDuration = datetime.now() - totalStartTime
    logger.info("======= Script execution completed in {} ===".format(totalDuration))


if __name__ == "__main__":
    customization_run()
