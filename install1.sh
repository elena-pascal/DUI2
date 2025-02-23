mkdir dui_install
cd dui_install
INI_DIR_PATH=$(pwd)
printf "========================================\n"
printf "#           DOWNLOADING DUI2            #\n"
printf "========================================\n\n"
curl -L -O https://github.com/ccp4/DUI2/archive/refs/heads/master.zip
printf "========================================\n"
printf "#       DUI2 DOWNLOADED (as .zip)      #\n"
printf "========================================\n\n"
unzip master.zip
mv DUI2-master DUI2
rm master.zip
printf "========================================\n"
printf "  using CURL intead of GIT  \n "
printf "  Done   \n"
printf "========================================\n\n"
printf "Setting up launchers ...\n"
mkdir dui_cmd_tools
cd dui_cmd_tools
CMD_TOOLS_PATH=$(pwd)
CLIENT_EXE_CMD="dials.python $INI_DIR_PATH/DUI2/src/only_client.py \$@"
echo $CLIENT_EXE_CMD > dui_client
chmod +x dui_client
SERVER_EXE_CMD="dials.python $INI_DIR_PATH/DUI2/src/only_server.py \$@"
echo $SERVER_EXE_CMD > dui_server
chmod +x dui_server
ALL_LOCAL_CMD="dials.python $INI_DIR_PATH/DUI2/src/all_local.py \$@"
echo $ALL_LOCAL_CMD > dui_all_local
chmod +x dui_all_local
printf " ... Done\n\n"
printf "========================================\n"
printf "#               DUI2 READY             #\n"
printf "========================================\n\n"
printf " commands abailable: \n\n"
printf "   dui_all_local,  dui_server,  dui_client\n\n"
printf " To set enviromet to run DUI2 (including Dials) type:\n\n"
printf "   export PATH=$CMD_TOOLS_PATH:\$PATH  \n\n"
printf " or add it to your init bash shell\n\n"
cd $INI_DIR_PATH
cd ..


