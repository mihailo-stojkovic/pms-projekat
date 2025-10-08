# PMS Domaci

## Aplikacija

Sam UI je dizajniran u Qt Designer 5.11.1, a nakon toga je export-ovan kao Python klasa. U originalnoj klasi je jedino promenjen jedan widget koji je služio kao placeholder za grafik widget.

Aplikacija se sastoji iz X glavnih delova:
1. MachineStateManager
2. MainWindow
3. SerialComProvider



### MachineStateManager
Mozak operacije celokupnog projekta. Preko njega se vrši komunikacija, sinhronizacija i nešto za sve ostale delove programa. 