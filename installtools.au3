#RequireAdmin
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Change2CUI=y
#AutoIt3Wrapper_Add_Constants=n
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****

#include <MsgBoxConstants.au3>
#include <File.au3>
#include <FileConstants.au3>


$currentdir = @ScriptDir

$otpfile = $currentdir & "\" & "otp_win64_20.0.exe"
$rmqfile = $currentdir &'\'&'rabbitmq-server-3.6.10.exe'
if FileExists($otpfile) Then
	#cs
	install otp
	#ce
	Run($otpfile)
	WinWaitActive('Erlang OTP 20 Setup ','Choose Components')
	Send('!N')
	WinWaitActive('Erlang OTP 20 Setup ','Choose Install Location')
	Send('!N')
	WinWaitActive('Erlang OTP 20 Setup ','Choose Start Menu Folder')
	Send('!I')
	WinWaitActive('Erlang OTP 20 Setup ','Installation Complete')
	Send('!C')

Else
	MsgBox($MB_OK,"otp install package not exist",'otp install package not exist')
	#cs
	Exit(1)
	#ce
EndIf

if FileExists($rmqfile) Then
	#cs
	install rabbitmq
	#ce
	Run($rmqfile)
	WinWaitActive('RabbitMQ Server 3.6.10 Setup ','Choose Components')
	Send('!N')
	WinWaitActive('RabbitMQ Server 3.6.10 Setup ','Choose Install Location')
	Send('!I')
	WinWaitActive('RabbitMQ Server 3.6.10 Setup ','Installation Complete')
	Send('!N')
	WinWaitActive('RabbitMQ Server 3.6.10 Setup ','Completing the RabbitMQ Server 3.6.10 Setup Wizard')
	Send('!F')
Else
	MsgBox($MB_OK,"rabbitmq install package not exist",'rabbitmq install package not exist')
	#cs
	Exit(1)
	#ce
EndIf


;激活rabbitmq management
$rabbitbat = 'C:\Program Files\RabbitMQ Server\rabbitmq_server-3.6.10\sbin\rabbitmq-plugins.bat'
If FileExists($rabbitbat) Then
	RunWait($rabbitbat&' enable rabbitmq_management')
	RunWait('net stop RabbitMQ && net start RabbitMQ')
EndIf


;install python to local
Const $pythonbin = 'K:\tools\Python2.7.3'
Local $sDrive = "", $dir = "", $sFileName = "", $sExtension = ""
_PathSplit($pythonbin,$sDrive,$dir,$sFileName,$sExtension)
$localpythonbin = _PathMake('C:',$dir,$sFileName,$sExtension)

If FileExists($pythonbin) Then
	DirCopy($pythonbin,$localpythonbin,$FC_OVERWRITE)
	;设置环境变量
	;通过注册表来更新环境变量
	local $pathEnv = RegRead("HKEY_CURRENT_USER\Environment", "Path")
;~ 	ConsoleWrite($pathEnv)
	$localpythonscript = $localpythonbin &'\'&'Scripts'
	Local $newenvpath = $pathEnv &';'&$localpythonbin&';'&$localpythonscript&';'

	RegWrite("HKEY_CURRENT_USER\Environment", "Path",'REG_SZ',$newenvpath)
	Sleep(1000)

	EnvUpdate()
;~ 	ConsoleWrite($newenvpath)

Else
	MsgBox($MB_OK,'path K:\tools\Python2.7.3 not exist','path K:\tools\Python2.7.3 not exist')
EndIf

If FileExists('K:\tools\maya\Maya.env') Then
	ConsoleWrite(@UserName)
	Local $localmayaenv = StringReplace('C:\Users\{username}\Documents\maya\2015-x64\Maya.env','{username}',@UserName)
	FileCopy('K:\tools\maya\Maya.env',$localmayaenv,$FC_OVERWRITE)
	ConsoleWrite($localmayaenv)
EndIf

;设置工具环境变量
If FileExists('K:\tools') Then
	RegWrite("HKEY_CURRENT_USER\Environment",'ANIPIPE_TOOLS_LOC','REG_SZ','K:\tools')
	Sleep(1000)
	EnvUpdate()
EndIf








