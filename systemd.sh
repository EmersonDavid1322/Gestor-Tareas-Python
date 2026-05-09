#!/bin/bash

APP_DIR="$HOME/apps/gestor"
SYSTEMD_DIR="/etc/systemd/system"
CURRENT_USER=$(whoami)

USER_SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$USER_SYSTEMD_DIR"

echo "🔧 Configurando servicios systemd..."

# =========================
# BOT
# =========================

if [ ! -f "$APP_DIR/bot_disciplina" ]; then
    echo "❌ bot_disciplina no encontrado"
    exit 1
fi

sudo bash -c "cat > $SYSTEMD_DIR/bot_disciplina.service" <<EOF
[Unit]
Description=Bot Disciplina
After=network.target

[Service]
ExecStart=$APP_DIR/bot_disciplina
WorkingDirectory=$APP_DIR
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
User=$CURRENT_USER

[Install]
WantedBy=multi-user.target
EOF

# =========================
# NOTIFICADOR
# =========================

if [ ! -f "$APP_DIR/notificador" ]; then
    echo "❌ notificador no encontrado"
    exit 1
fi

tee "$USER_SYSTEMD_DIR/notificador.service" > /dev/null <<EOF
[Unit]
Description=Notificador Disciplina
After=default.target

[Service]
ExecStart=$APP_DIR/notificador
WorkingDirectory=$APP_DIR
Restart=always
RestartSec=5
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/$(id -u)

[Install]
WantedBy=default.target
EOF

# =========================
# RECARGAR SYSTEMD
# =========================

sudo systemctl daemon-reload

sudo systemctl enable bot_disciplina.service
systemctl --user enable notificador
systemctl --user start notificador

sudo systemctl restart bot_disciplina.service
systemctl --user restart notificador

DESTINO_APP="$HOME/apps/gestor"
sudo chcon -t bin_t "$DESTINO_APP/bot_disciplina"
sudo chcon -t bin_t "$DESTINO_APP/notificador"

echo ""
echo "📊 Estado BOT:"
sudo systemctl status bot_disciplina.service --no-pager

echo ""
echo "📊 Estado NOTIFICADOR:"
systemctl --user status notificador --no-pager