Attribute VB_Name = "Snap7"
' In questo modulo sono dichiarate alcune funzioni esportate dalla dll
' Fare riferimento al manuale per la sintassi delle altre tenendo presente che :
'
'  int      (c/c++) = Integer (Delphi) = Long (VB6)
'  uint16_t (c/c++) = Word (Delphi)    = Integer (VB6)
'  unt8_t   (c/c++) = Byte (Delphi)    = Byte (VB6)
'

' Creazione / Distruzione
Public Declare Function Cli_Create Lib "Snap7.dll" () As Long
Public Declare Sub Cli_Destroy Lib "Snap7.dll" (ByRef Client As Long)

' Connessione / Disconnessione
Public Declare Function Cli_ConnectTo Lib "Snap7.dll" (ByVal Client As Long, ByVal Address As String, ByVal Rack As Long, ByVal Slot As Long) As Long
Public Declare Function Cli_SetConnectionParams Lib "Snap7.dll" (ByVal Client As Long, ByVal Address As String, ByVal LocalTSAP As Integer, ByVal RemoteTSAP As Integer) As Long
Public Declare Function Cli_Connect Lib "Snap7.dll" (ByVal Client As Long) As Long
Public Declare Function Cli_Disconnect Lib "Snap7.dll" (ByVal Client As Long) As Long

' Lettura Aree di memoria (funzione estesa)
Public Declare Function Cli_ReadArea Lib "Snap7.dll" (ByVal Client As Long, ByVal Area As Long, ByVal DBNumber As Long, ByVal Start As Long, ByVal Amount As Long, ByVal WordLen As Long, ByVal Buffer As Long) As Long
' Lettura Aree di memoria (funzioni semplificate)
Public Declare Function Cli_DBRead Lib "Snap7.dll" (ByVal Client As Long, ByVal DBNumber As Long, ByVal Start As Long, ByVal Size As Long, ByVal Buffer As Long) As Long
Public Declare Function Cli_MBRead Lib "Snap7.dll" (ByVal Client As Long, ByVal Start As Long, ByVal Sizet As Long, ByVal Buffer As Long) As Long
' ecc... per Ingressi, Uscite, Timers e Contatori

' Scrittura Aree di memoria (funzione estesa)
Public Declare Function Cli_WriteArea Lib "Snap7.dll" (ByVal Client As Long, ByVal Area As Long, ByVal DBNumber As Long, ByVal Start As Long, ByVal Amount As Long, ByVal WordLen As Long, ByVal Buffer As Long) As Long
' Scrittura Aree di memoria (funzioni semplificate)
Public Declare Function Cli_DBWrite Lib "Snap7.dll" (ByVal Client As Long, ByVal DBNumber As Long, ByVal Start As Long, ByVal Size As Long, ByVal Buffer As Long) As Long
Public Declare Function Cli_MBWrite Lib "Snap7.dll" (ByVal Client As Long, ByVal Start As Long, ByVal Sizet As Long, ByVal Buffer As Long) As Long
' ecc... per Ingressi, Uscite, Timers e Contatori


' Errori
Public Declare Function Cli_ErrorText Lib "Snap7.dll" (ByVal Error As Long, ByVal Text As String, ByVal TextLen As Long) As Long

