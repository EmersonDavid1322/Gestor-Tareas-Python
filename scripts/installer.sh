#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"

# 1. Ruta base del proyecto
BASE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

# 2. Carpeta destino
DESTINO_APP="$HOME/apps/gestor"

rm  -f "$DESTINO_APP/bot_disciplina"
rm  -f "$DESTINO_APP/GestorDisciplina"
rm  -f "$DESTINO_APP/notificador"
rm  -rf "$DESTINO_APP/assets"
echo "Elimanada la verison antigua"

mkdir -p "$DESTINO_APP"

echo "📁 Preparando carpeta: $DESTINO_APP"
echo "🚀 Iniciando compilación en: $BASE_DIR"

# 3. Limpiar compilaciones previas (ANTES de compilar)
rm -rf "$BASE_DIR/build"
rm -rf "$BASE_DIR/dist"
rm -f "$BASE_DIR"/*.spec

if python3 -c "import tkinter" &> /dev/null; then
    echo "Tkinter está instalado."
else
    echo "Tkinter NO está instalado. Instalando..."
    sudo pacman -S --noconfirm tk
fi

# 3.5. ACTIVAR EL ENTORNO VIRTUAL PARA EL SCRIPT
echo "🌐 Activando entorno virtual..."
if [ -f "$BASE_DIR/.venv/bin/activate" ]; then
    source "$BASE_DIR/.venv/bin/activate"
else
    echo "❌ No se encontró el entorno virtual en $BASE_DIR/.venv"
    echo "🔨 Creando entorno virtual e instalando dependencias..."
    
    python3 -m venv "$BASE_DIR/.venv"
    
    source "$BASE_DIR/.venv/bin/activate"
    
    if [ -f "$BASE_DIR/requirements.txt" ]; then
        pip install --upgrade pip 
        pip install -r "$BASE_DIR/requirements.txt"
        echo "✅ Entorno virtual creado y dependencias instaladas correctamente"
    else
        echo "⚠️ Advertencia: No se encontró el archivo requirements.txt en $BASE_DIR"
    fi
fi

# 4. Compilar ejecutables
echo "⚙️ Compilando bot..."
pyinstaller --noconfirm --onefile \
    --paths "$BASE_DIR/src" \
    "$BASE_DIR/discord_bot.py" \
    --name bot_disciplina

echo "⚙️ Compilando notificador..."
pyinstaller --onefile \
    --paths "$BASE_DIR/src" \
    "$BASE_DIR/notificaciones.py" \
    --name notificador \
    --collect-all plyer

echo "⚙️ Compilando interfaz..."
pyinstaller --noconfirm --onefile --windowed \
    --paths "$BASE_DIR/src" \
    "$BASE_DIR/interfaz.py" \
    --name GestorDisciplina


# 5. Copiar ejecutables
echo "📦 Copiando ejecutables..."
cp "$BASE_DIR/dist/bot_disciplina" "$DESTINO_APP/"
cp "$BASE_DIR/dist/notificador" "$DESTINO_APP/"
cp "$BASE_DIR/dist/GestorDisciplina" "$DESTINO_APP/"

# 6. Dar permisos
chmod +x "$DESTINO_APP/"*

# 7. Copiar recursos
if [ -d "$BASE_DIR/assets" ]; then
    cp -r "$BASE_DIR/assets" "$DESTINO_APP/"
    echo "📂 Carpeta de recursos copiada"
else
    echo "⚠️ No se encontró la carpeta de recursos"
fi

echo "🧹 Limpieza final..."
rm -rf "$BASE_DIR/build"
rm -rf "$BASE_DIR/dist"
rm -f "$BASE_DIR"/*.spec

echo "✅ ¡Todo listo! Ejecuta:"
echo "$DESTINO_APP/GestorDisciplina"

bash "$BASE_DIR/scripts/systemd.sh"

echo "Creando acceso directo"

RUTA_DESKTOP="$HOME/.local/share/applications/gestor_diciplina.desktop"
cat << EOF > "$RUTA_DESKTOP"
[Desktop Entry]
Type=Application
Name=Gestor Disciplina
Exec=$DESTINO_APP/GestorDisciplina
Icon=$DESTINO_APP/assets/icono.png
Categories=Development;
Terminal=false
Path=$DESTINO_APP
EOF

chmod +x "$RUTA_DESKTOP"    
update-desktop-database ~/.local/share/applications
echo "Acceso creado correctamente"