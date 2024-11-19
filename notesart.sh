SCRIPT_DIR="~/"
PYTHON_FILE="front_end.py"


if [[ -d $SCRIPT_DIR ]]; then
    cd "$SCRIPT_DIR" || { echo "Failed to change directory!"; exit 1; }
else
    echo "Error: Directory $SCRIPT_DIR not found!"
    exit 1
fi

if [[ -f $PYTHON_FILE ]]; then
    python3 "$PYTHON_FILE" &
else
    echo "Error: $PYTHON_FILE not found!"
    exit 1
fi

firefox &
