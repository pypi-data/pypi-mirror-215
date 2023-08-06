#!/usr/bin/env bash

# IMPORTANT: Currently the installer construction does not include the opfc library.
# Ideally we would install it via `pip` but it does not seem possible.
# See https://github.com/conda/constructor/issues/515

set -e

ARCH=$(uname -m)
OS=$(uname)

if [[ "$OS" == "Linux" ]]; then
  PLATFORM="linux"
  if [[ "$ARCH" == "aarch64" ]]; then
    ARCH="aarch64"
  elif [[ $ARCH == "ppc64le" ]]; then
    ARCH="ppc64le"
  else
    ARCH="64"
  fi
fi

if [[ "$OS" == "Darwin" ]]; then
  PLATFORM="osx"
  if [[ "$ARCH" == "arm64" ]]; then
    ARCH="arm64"
  else
    ARCH="64"
  fi
fi

echo "***** Building for platform: ${PLATFORM} and ARCH: ${ARCH} *****"

if [[ -z "${OPENFRACTAL_CLIENT_CONSTRUCTOR_VERSION}" ]]; then
  echo "OPENFRACTAL_CLIENT_CONSTRUCTOR_VERSION is not set"
  exit 1
fi

export INSTALLERS_DIR="./build/"
export CONDA_SOLVER="libmamba"

echo "***** Construct the installer *****"

mkdir -p ${INSTALLERS_DIR}
constructor . --output-dir ${INSTALLERS_DIR}

if [[ "$(uname)" == MINGW* ]]; then
  EXT="exe"
else
  EXT="sh"
fi

echo "***** Rename installer file *****"
INSTALLER_PATH=$(find ${INSTALLERS_DIR} -name "OpenFractalClient*.${EXT}" | head -n 1)
NEW_INSTALLER_PATH="${INSTALLERS_DIR}/OpenFractalClient-${OPENFRACTAL_CLIENT_CONSTRUCTOR_VERSION}-${PLATFORM}-${ARCH}.${EXT}"
mv ${INSTALLER_PATH} "${NEW_INSTALLER_PATH}"

echo "***** Generate sha256sum file *****"
HASH_PATH="${NEW_INSTALLER_PATH}.sha256"
sha256sum "${NEW_INSTALLER_PATH}" >"${HASH_PATH}"

echo "***** Copy files to latest *****"
LATEST_INSTALLER_PATH="${INSTALLERS_DIR}/OpenFractalClient-${PLATFORM}-${ARCH}.${EXT}"
LATEST_HASH_PATH="${LATEST_INSTALLER_PATH}.sha256"
cp "${NEW_INSTALLER_PATH}" "${LATEST_INSTALLER_PATH}"
cp "${HASH_PATH}" "${LATEST_HASH_PATH}"

echo "***** DONE *****"
