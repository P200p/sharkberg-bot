#!/bin/bash

echo "🛑 ปิด Edge และ VS Code ก่อนล้าง..."

# 1. ปิดโปรเซส Edge + VS Code
taskkill //F //IM msedge.exe >nul 2>&1
taskkill //F //IM Code.exe >nul 2>&1

echo "✅ ปิดโปรเซสแล้ว"

# 2. ล้าง Edge session & cache
EDGE_USER_PATH="$HOME/AppData/Local/Microsoft/Edge/User Data/Default"
rm -rf "$EDGE_USER_PATH/Cache" \
       "$EDGE_USER_PATH/Cookies" \
       "$EDGE_USER_PATH/Local Storage" \
       "$EDGE_USER_PATH/Session Storage" \
       "$EDGE_USER_PATH/Service Worker" \
       "$EDGE_USER_PATH/Web Data" \
       "$EDGE_USER_PATH/Code Cache" \
       "$EDGE_USER_PATH/Storage"

echo "🧹 ล้างแคช Edge แล้ว"

# 3. ล้าง Windsurf local session (ถ้ามี)
WINDSURF_CACHE="$HOME/.config/windsurf"
rm -rf "$WINDSURF_CACHE"

echo "🧽 ล้าง session Windsurf"

# 4. ล้าง VS Code user cache
VSCODE_USERDATA="$APPDATA/Code/User"
rm -rf "$VSCODE_USERDATA/workspaceStorage" \
       "$VSCODE_USERDATA/globalStorage"

echo "🧼 ล้างแคช VS Code เสร็จ"

echo "🎉 เสร็จแล้ว! เปิด Edge แล้วล็อกอินใหม่แบบคลีนๆ ได้เลย"
