; Inno Setup script for the YanaNotes Windows installer.
; 1. Build the app first:  pyinstaller build/yananotes.spec
; 2. Then compile this with Inno Setup (iscc build/installer.iss).
; Produces YanaNotes-Setup.exe.

#define AppName "YanaNotes"
#define AppVersion "0.1.0"
#define AppPublisher "Yanakan"
#define AppExe "YanaNotes.exe"

[Setup]
AppId={{B8F4E2A1-9C3D-4E7F-A1B2-YANANOTES0001}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputBaseFilename=YanaNotes-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#AppExe}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
; Pack the whole one-folder PyInstaller build.
Source: "..\dist\YanaNotes\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
