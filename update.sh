#!/bin/bash

# 1. Detectar la ruta donde está guardado este script
# Esto hace que funcione en tu PC o en cualquier otra sin cambiar rutas
BASE_DIR=$(dirname "$(readlink -f "$0")")

# 2. Definir dónde quieres que se guarde el ejecutable final
# Si quieres que siga yendo a tu carpeta de apps, puedes usar $HOME
# $HOME equivale automáticamente a /home/tu_usuario
DESTINO_APP="$HOME/apps/gestor"

mkdir -p "$DESTINO_APP"
echo "📁 Preparando carpeta: $DESTINO_APP"

echo "🚀 Iniciando actualización en: $BASE_DIR"

echo "🚀 Iniciando actualización en: $BASE_DIR"

# 3. Ejecutar PyInstaller
# Usamos --distpath para enviarlo directo a la carpeta de apps
pyinstaller --noconfirm --onefile --windowed \
    --name "GestorDisciplina" \
    --distpath "$DESTINO_APP" \
    "$BASE_DIR/interfaz.py"

echo "✅ ¡Compilación completada!"

# 4. Copiar la carpeta de sonidos (noti) usando rutas relativas
# Así no importa si tu proyecto está en Documentos o en el Escritorio
if [ -d "$BASE_DIR/noti" ]; then
    cp -r "$BASE_DIR/noti" "$DESTINO_APP/"
    echo "📂 Carpeta de sonidos actualizada en $DESTINO_APP"
else
    echo "⚠️ Advertencia: No se encontró la carpeta 'noti' en $BASE_DIR"
fi

# 5. Limpieza de archivos temporales
rm -rf "$BASE_DIR/build"
rm -rf "$BASE_DIR/dist"
rm "$BASE_DIR"/*.spec

echo "🧹 Limpieza completada. Proyecto impecable."
