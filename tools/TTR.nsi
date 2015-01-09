############################################################################################
#      NSIS Installation Script created by NSIS Quick Setup Script Generator v1.09.18
#               Entirely Edited with NullSoft Scriptable Installation System                
#              by Vlasis K. Barkas aka Red Wine red_wine@freemail.gr Sep 2006               
############################################################################################

!define APP_NAME "Toontown World"
!define COMP_NAME "The TTW Team"
!define WEB_SITE "www.toontownworldonline.com"
!define VERSION "00.00.00.00"
!define COPYRIGHT ""
!define DESCRIPTION "Toontown World Online"
!define INSTALLER_NAME "TTWInstaller.exe"
!define MAIN_APP_EXE "Launcher.exe"
!define INSTALL_TYPE "SetShellVarContext all"
!define REG_ROOT "HKLM"
!define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

!define REG_START_MENU "Start Menu Folder"

var SM_Folder

######################################################################

VIProductVersion  "${VERSION}"
VIAddVersionKey "ProductName"  "${APP_NAME}"
VIAddVersionKey "CompanyName"  "${COMP_NAME}"
VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
VIAddVersionKey "FileVersion"  "${VERSION}"

######################################################################

Name "${APP_NAME}"
Caption "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME}"
XPStyle on
InstallDirRegKey "${REG_ROOT}" "${REG_APP_PATH}" ""
InstallDir "$PROGRAMFILES\Toontown World"

######################################################################

!include "MUI.nsh"

!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING

!define MUI_WELCOMEPAGE_TEXT "This setup will prepare your computer to run Toontown World Beta. If you still have Toontown World Alpha installed, this setup will upgrade your Alpha installation into a Beta installation. If you have Toontown World Beta installed, this setup will upgrade your launcher to the current version."
!insertmacro MUI_PAGE_WELCOME

!ifdef LICENSE_TXT
!insertmacro MUI_PAGE_LICENSE "${LICENSE_TXT}"
!endif

!insertmacro MUI_PAGE_DIRECTORY

!ifdef REG_START_MENU
!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "Toontown World"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REG_ROOT}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${UNINSTALL_PATH}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${REG_START_MENU}"
!insertmacro MUI_PAGE_STARTMENU Application $SM_Folder
!endif

!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_PAGE_FINISH

!define MUI_WELCOMEPAGE_TEXT "Setup will guide you through the uninstallation of $(^NameDA). This uninstallation process will not delete any Toontown World log files, screenshots, or settings."
!insertmacro MUI_UNPAGE_WELCOME

!insertmacro MUI_UNPAGE_CONFIRM

!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

######################################################################

Section -MainProgram
${INSTALL_TYPE}
SetOverwrite ifnewer
SetOutPath "$INSTDIR"
AccessControl::GrantOnFile "$INSTDIR" "(S-1-1-0)" "ListDirectory + GenericRead + GenericExecute + GenericWrite" 
AccessControl::EnableFileInheritance "$INSTDIR"
# Delete old alpha stuff
Delete "$INSTDIR\TTWLauncher.exe"
Delete "$INSTDIR\kickoff.bat"
Delete "$INSTDIR\rsyncbins\rsync.exe"
Delete "$INSTDIR\rsyncbins\msys-1.0.dll"
Delete "$INSTDIR\rsyncbins\msys-iconv-2.dll"
Delete "$INSTDIR\rsyncbins\msys-intl-8.dll"
Delete "$INSTDIR\rsyncbins\msys-popt-0.dll"
Delete "$INSTDIR\etc\DO NOT DELETE"
RmDir "$INSTDIR\etc"
RmDir "$INSTDIR\rsyncbins"

File "C:\Users\Jeremy\git\pylauncher\dist\Launcher.exe"
writeUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

######################################################################

Section -Icons_Reg
SetOutPath "$INSTDIR"
WriteUninstaller "$INSTDIR\uninstall.exe"

!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
CreateDirectory "$SMPROGRAMS\$SM_Folder"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
!ifdef WEB_SITE
WriteIniStr "$INSTDIR\${APP_NAME} Official Site.url" "InternetShortcut" "URL" "${WEB_SITE}"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME} Official Site.lnk" "$INSTDIR\${APP_NAME} Official Site.url"
!endif
!insertmacro MUI_STARTMENU_WRITE_END
!endif

!ifndef REG_START_MENU
CreateDirectory "$SMPROGRAMS\Toontown World"
CreateShortCut "$SMPROGRAMS\Toontown World\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
!ifdef WEB_SITE
WriteIniStr "$INSTDIR\${APP_NAME} Official Site.url" "InternetShortcut" "URL" "${WEB_SITE}"
CreateShortCut "$SMPROGRAMS\Toontown World\${APP_NAME} Official Site.lnk" "$INSTDIR\${APP_NAME} Official Site.url"
!endif
!endif

WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\uninstall.exe"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "$INSTDIR\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${VERSION}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"

!ifdef WEB_SITE
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "URLInfoAbout" "${WEB_SITE}"
!endif
SectionEnd

######################################################################

Section Uninstall
${INSTALL_TYPE}
Delete "$INSTDIR\${MAIN_APP_EXE}"
Delete "$INSTDIR\TTWEngine.exe"
Delete "$INSTDIR\TTWGame.bin"
Delete "$INSTDIR\phase_3.mf"
Delete "$INSTDIR\phase_3.5.mf"
Delete "$INSTDIR\phase_4.mf"
Delete "$INSTDIR\phase_5.mf"
Delete "$INSTDIR\phase_5.5.mf"
Delete "$INSTDIR\phase_6.mf"
Delete "$INSTDIR\phase_7.mf"
Delete "$INSTDIR\phase_8.mf"
Delete "$INSTDIR\phase_9.mf"
Delete "$INSTDIR\phase_10.mf"
Delete "$INSTDIR\phase_11.mf"
Delete "$INSTDIR\phase_12.mf"
Delete "$INSTDIR\phase_13.mf"
Delete "$INSTDIR\cg.dll"
Delete "$INSTDIR\cgGL.dll"
Delete "$INSTDIR\OpenAL32.dll"

Delete "$INSTDIR\uninstall.exe"
!ifdef WEB_SITE
Delete "$INSTDIR\${APP_NAME} Official Site.url"
!endif

RmDir "$INSTDIR"

!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_GETFOLDER "Application" $SM_Folder
Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk"
!ifdef WEB_SITE
Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME} Official Site.lnk"
!endif
Delete "$DESKTOP\${APP_NAME}.lnk"

RmDir "$SMPROGRAMS\$SM_Folder"
!endif

!ifndef REG_START_MENU
Delete "$SMPROGRAMS\Toontown World\${APP_NAME}.lnk"
!ifdef WEB_SITE
Delete "$SMPROGRAMS\Toontown World\${APP_NAME} Official Site.lnk"
!endif
Delete "$DESKTOP\${APP_NAME}.lnk"

RmDir "$SMPROGRAMS\Toontown World"
!endif

DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
SectionEnd

######################################################################
