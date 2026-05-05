#!/bin/bash

# 1. Ruta base del proyecto
BASE_DIR=$(dirname "$(readlink -f "$0")")

# 2. Carpeta destino
DESTINO_APP="$HOME/apps/gestor"

mkdir -p "$DESTINO_APP"

echo "📁 Preparando carpeta: $DESTINO_APP"
echo "🚀 Iniciando compilación en: $BASE_DIR"

# 3. Limpiar compilaciones previas (ANTES de compilar)
rm -rf "$BASE_DIR/build"
rm -rf "$BASE_DIR/dist"
rm -f "$BASE_DIR"/*.spec

# 4. Compilar ejecutables
echo "⚙️ Compilando bot..."
pyinstaller --noconfirm --onefile "$BASE_DIR/discord_bot.py" --name bot_disciplina

echo "⚙️ Compilando notificador..."
pyinstaller --noconfirm --onefile "$BASE_DIR/notificaciones.py" --name notificador

echo "⚙️ Compilando interfaz..."
pyinstaller --noconfirm --onefile --windowed "$BASE_DIR/interfaz.py" --name GestorDisciplina

# 5. Copiar ejecutables
echo "📦 Copiando ejecutables..."
cp "$BASE_DIR/dist/bot_disciplina" "$DESTINO_APP/"
cp "$BASE_DIR/dist/notificador" "$DESTINO_APP/"
cp "$BASE_DIR/dist/GestorDisciplina" "$DESTINO_APP/"

# 6. Dar permisos
chmod +x "$DESTINO_APP/"*

# 7. Copiar recursos (sonidos)
if [ -d "$BASE_DIR/noti" ]; then
    cp -r "$BASE_DIR/noti" "$DESTINO_APP/"
    echo "📂 Carpeta de sonidos copiada"
else
    echo "⚠️ No se encontró la carpeta 'noti'"
fi

echo "🧹 Limpieza final..."
rm -rf "$BASE_DIR/build"
rm -rf "$BASE_DIR/dist"
rm -f "$BASE_DIR"/*.spec

echo "✅ ¡Todo listo! Ejecuta:"
echo "$DESTINO_APP/GestorDisciplina"