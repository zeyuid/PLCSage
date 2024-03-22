VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   6330
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   10020
   LinkTopic       =   "Form1"
   ScaleHeight     =   6330
   ScaleWidth      =   10020
   StartUpPosition =   3  'Windows Default
   Begin VB.TextBox Text1 
      Height          =   2295
      Left            =   480
      MultiLine       =   -1  'True
      TabIndex        =   7
      Top             =   2400
      Width           =   8535
   End
   Begin VB.CommandButton Command4 
      Caption         =   "DBRead"
      Height          =   495
      Left            =   480
      TabIndex        =   6
      Top             =   1560
      Width           =   1935
   End
   Begin VB.Frame Frame1 
      Caption         =   "Connessione - Usare uno dei due pulsanti"
      Height          =   855
      Left            =   240
      TabIndex        =   3
      Top             =   240
      Width           =   4455
      Begin VB.CommandButton Command2 
         Caption         =   "SetConnectionParams"
         Height          =   495
         Left            =   2280
         TabIndex        =   5
         Top             =   240
         Width           =   1935
      End
      Begin VB.CommandButton Command1 
         Caption         =   "ConnectTo"
         Height          =   495
         Left            =   240
         TabIndex        =   4
         Top             =   240
         Width           =   1935
      End
   End
   Begin VB.CommandButton Command3 
      Caption         =   "Disconnect"
      Enabled         =   0   'False
      Height          =   495
      Left            =   4800
      TabIndex        =   2
      Top             =   480
      Width           =   1935
   End
   Begin VB.Label Label2 
      Caption         =   "Result"
      Height          =   255
      Left            =   360
      TabIndex        =   1
      Top             =   5160
      Width           =   855
   End
   Begin VB.Label Label1 
      Height          =   255
      Left            =   360
      TabIndex        =   0
      Top             =   5520
      Width           =   9375
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
' Variabile Handle del Client
Dim Client As Long
Dim Buffer(1024) As Byte

Private Sub ShowResult(Error As Long)
  ' Questa funzione trasforma il codice di errore in una stringa descrittiva (in inglese)
  ' E' utile dato che ci sono moltissimi codici di errore
  Dim StrError As String * 1024
  
  Result = Cli_ErrorText(Error, StrError, 1023)
  Label1.Caption = StrError
End Sub

Private Sub Command1_Click()
' Questa funzione permette di connettersi usando Rack e Slot
' Viene usata per tutti i sistemi S7300/400/1200/1500/WinAC, Drive SINAMICS ecc..
  Dim Result As Long
  Result = Cli_ConnectTo(Client, "192.168.0.71" + Chr$(0), 0, 2)
  ShowResult (Result)
  ' Disabilitiamo i pulsanti di connessione e abilitiamo quello di disconnessione
  If Result = 0 Then
    Command1.Enabled = False
    Command2.Enabled = False
    Command3.Enabled = True
  End If
End Sub

Private Sub Command2_Click()
' Questa funzione permette di connettersi usando TSAP (locale e remoto) invece di Rack e Slot
' Viene usata per il LOGO e S7 200
  Dim Result As Long
  Result = Cli_SetConnectionParams(Client, "192.168.0.71" + Chr$(0), &H101, &H102)
  ' Il primo Result è sempre 0, la funzione setta solo i parametri interni
  Result = Cli_Connect(Client)
  ' Questo Result invece ci interessa, è quello della connessione vera e propria
  ShowResult (Result)
  ' Disabilitiamo i pulsanti di connessione e abilitiamo quello di disconnessione
  If Result = 0 Then
    Command1.Enabled = False
    Command2.Enabled = False
    Command3.Enabled = True
  End If
End Sub

Private Sub Command3_Click()
  ' Questa funzione disconnette il Client ma non distrugge l'oggetto, esso può essere connesso ad
  ' un'altro PLC se voluto
  Result = Cli_Disconnect(Client)
  ' Disabilitiamo il pulsanti di disconnessione e abilitiamo quelli di connessione
  If Result = 0 Then
    Command1.Enabled = True
    Command2.Enabled = True
    Command3.Enabled = False
  End If

End Sub

Private Sub Command4_Click()
  Dim i As Integer
  ' Legge 16 bytes da DB1 a partire da offset 0 e li mette nel buffer
  ' La scrittura non l'ho implementata per motivi di sicurezza, magari premete il
  ' pulsante e siete collegati ad un PLC di produzione.
  ' I parametri della scrittura sono esattamente gli stessi
  Result = Cli_DBRead(Client, 1, 0, 16, VarPtr(Buffer(0)))
  ShowResult (Result)
  Text1.Text = ""
  For i = 0 To 15
    Text1.Text = Text1.Text + Hex$(Buffer(i)) + " "
  Next
End Sub

Private Sub Form_Load()
' Creazione del Client
' La variabile Client la passeremo ad ogni funzione, *non dobbiamo mai modificarla a mano*
    Client = Cli_Create()
End Sub

Private Sub Form_Unload(Cancel As Integer)
' Distruzione del Client
' La disconnessione avviene automaticamente
    Cli_Destroy (Client)
End Sub

