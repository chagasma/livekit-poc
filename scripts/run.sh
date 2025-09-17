set -e

case "$1" in
  -dev)
    echo "dev running..."
    ;;
  -tests)
    echo "tests running..."
    ;;
  *)
    echo "Uso: $0 [-dev | -tests]"
    exit 1
    ;;
esac
