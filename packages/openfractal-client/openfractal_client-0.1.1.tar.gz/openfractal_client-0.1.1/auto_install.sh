ARCH=$(uname -m)
OS=$(uname)

if [[ "$OS" == "Linux" ]]; then
	PLATFORM="linux"
	if [[ "$ARCH" == "aarch64" ]]; then
		ARCH="aarch64";
	elif [[ $ARCH == "ppc64le" ]]; then
		ARCH="ppc64le";
	else
		ARCH="64";
	fi
fi

if [[ "$OS" == "Darwin" ]]; then
	PLATFORM="osx";
	if [[ "$ARCH" == "arm64" ]]; then
		ARCH="arm64";
	else
		ARCH="64"
	fi
fi

OPENFRACTAL_CLIENT_PREFIX="$HOME/.local/share/openfractal-client"

# check if it exists
# download the installer
# perform installation
# display message and instructions

bash OpenFractalClient-0.0.0-Linux-x86_64.sh -b -p ${OPENFRACTAL_CLIENT_PREFIX}

COMPUTE_MANAGER="${OPENFRACTAL_CLIENT_PREFIX}/bin/qcfractal-compute-manager"
