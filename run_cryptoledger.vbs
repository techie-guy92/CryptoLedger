Set fso = CreateObject("Scripting.FileSystemObject")
Set logFile = fso.OpenTextFile("C:\Users\Administrator\Downloads\IT\Projects\Django_Projects\CryptoLedger\logs\vbs_trace.txt", 8, True)
logFile.WriteLine "[" & Now & "] VBS triggered"
logFile.Close

WScript.Sleep 10000 ' 10 seconds before launching batch

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\Users\Administrator\Downloads\IT\Projects\Django_Projects\CryptoLedger\start_cryptoledger.bat" & chr(34), 0