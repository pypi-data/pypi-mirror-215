import re
import pickle
import socket
import errno

"""
Command line argument processing
"""

from base64 import b64encode, b64decode
from zlib import crc32

from ..parameters import HOST, PORT_BASE
from ..core.files import getLocation

# COMMAND LINE ARGS

appPat = "^([a-zA-Z0-9_-]+)$"
appRe = re.compile(appPat)


def portIsInUse(lhost, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((lhost, port))
        result = True
    except OverflowError:
        result = None
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            result = False
        else:
            result = False

    s.close()
    return result


def getPort(portBase=PORT_BASE):
    result = None
    for port in range(portBase, portBase + 100):
        status = portIsInUse(HOST, port)
        if status is None:
            break
        if not status:
            continue
        result = port
        break

    return result


def repSlug(slug):
    info = _deSlug(slug)
    appName = info["appName"]
    checkoutApp = info["checkoutApp"]
    if checkoutApp:
        checkoutApp = f":{checkoutApp}"
    dataLoc = info["dataLoc"]
    rep = dataLoc or f"{appName}{checkoutApp}"
    args = " ".join(
        f"--{k}={v}"
        for (k, v) in sorted(info.items())
        if k not in {"appName", "checkoutApp", "dataLoc"} and v is not None
    )
    if args:
        args = f" {args}"
    return f"{rep}{args}"


def argApp(cargs):
    (appName, checkoutApp, dataLoc) = argParam(cargs)
    backend = argCollect("backend", cargs)
    checkout = argCollect("checkout", cargs)

    if (
        appName is None
        and checkoutApp is None
        and dataLoc is None
        and backend is None
        and checkout is None
    ):
        (backend, org, repo, relative) = getLocation()
        appName = f"{org}/{repo}{relative}"
        checkoutApp = "clone"
        checkout = "clone"

    locations = argCollect("locations", cargs)
    modules = argCollect("modules", cargs)
    moduleRefs = argCollect("mod", cargs)
    version = argCollect("version", cargs)
    setFile = argCollect("sets", cargs)
    return (
        appName,
        *_enSlug(
            dict(
                appName=appName,
                backend=backend,
                checkoutApp=checkoutApp,
                dataLoc=dataLoc,
                checkout=checkout,
                locations=locations,
                modules=modules,
                moduleRefs=moduleRefs,
                setFile=setFile,
                version=version,
            )
        ),
    )


def argKill(cargs):
    for arg in cargs[1:]:
        if arg == "-k":
            return True
    return False


def argShow(cargs):
    for arg in cargs[1:]:
        if arg == "-p":
            return True
    return False


def argNoweb(cargs):
    for arg in cargs[1:]:
        if arg == "-noweb":
            return True
    return False


def argCollect(prefix, cargs):
    for arg in cargs[1:]:
        if arg.startswith(f"--{prefix}="):
            return arg[len(prefix) + 3 :]
    return None


def argKernel(cargs):
    if len(cargs) != 3:
        return None
    slug = cargs[1]
    portKernel = cargs[2]
    return (_deSlug(slug), portKernel)


def argWeb(cargs):
    if len(cargs) != 4:
        return None
    slug = cargs[1]
    portKernel = cargs[2]
    portWeb = cargs[3]
    return (_deSlug(slug), portKernel, portWeb)


def argParam(cargs):
    appName = None
    checkoutApp = None

    for arg in cargs[1:]:
        if arg.startswith("-"):
            continue
        appName = arg
        break

    if appName is None:
        return (None, None, None)

    if appName.startswith("data:"):
        dataLoc = appName[5:]
        appName = None
        checkoutApp = None
    elif appName.startswith("app:"):
        dataLoc = None
        checkoutApp = None
    else:
        dataLoc = None
        parts = appName.split(":", maxsplit=1)
        if len(parts) == 1:
            parts.append("")
        (appName, checkoutApp) = parts

    return (appName, checkoutApp, dataLoc)


def _enSlug(data):
    protoSlug = b64encode(pickle.dumps(tuple(sorted(data.items()))))
    portOffset = crc32(protoSlug) % 10000
    portKernel = PORT_BASE + portOffset
    portWeb = portKernel + 10000

    return (str(protoSlug, encoding="utf8"), portKernel, portWeb)


def _deSlug(slug):
    return dict(pickle.loads(b64decode(bytes(slug, encoding="utf8"))))
