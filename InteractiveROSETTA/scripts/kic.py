import wx
import wx.grid
import wx.lib.scrolledpanel
import os
import os.path
import time
import platform
import multiprocessing
import webbrowser
from threading import Thread
from tools import *

class KICPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent, W, H):
	#if (platform.system() == "Windows"):
	wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, id=-1, pos=(10, 60), size=(340, H-330), name="ProtFixbb")
	winh = H-330
	#else:
	    #wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, id=-1, pos=(10, 60), size=(340, H-330), name="ProtMinimization")
	    #winh = H-290
	self.SetBackgroundColour("#333333")
	self.parent = parent
	
	if (platform.system() == "Windows"):
	    self.lblProt = wx.StaticText(self, -1, "Kinematic Closure", (25, 15), (270, 25), wx.ALIGN_CENTRE)
	    self.lblProt.SetFont(wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblProt = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(25, 15), size=(270, 25))
	else:
	    self.lblProt = wx.StaticText(self, -1, "Kinematic Closure", (70, 15), style=wx.ALIGN_CENTRE)
	    self.lblProt.SetFont(wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.BOLD))
	    resizeTextControlForUNIX(self.lblProt, 0, self.GetSize()[0]-20)
	self.lblProt.SetForegroundColour("#FFFFFF")
	
	if (platform.system() == "Darwin"):
	    self.HelpBtn = wx.BitmapButton(self, id=-1, bitmap=wx.Image("images/osx/HelpBtn.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(295, 10), size=(25, 25))
	else:
	    self.HelpBtn = wx.Button(self, id=-1, label="?", pos=(295, 10), size=(25, 25))
	    self.HelpBtn.SetForegroundColour("#0000FF")
	    self.HelpBtn.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	self.HelpBtn.Bind(wx.EVT_BUTTON, self.showHelp)
	self.HelpBtn.SetToolTipString("Display the help file for this window")
	
	if (platform.system() == "Windows"):
	    self.lblInst = wx.StaticText(self, -1, "Remodel existing loops or generate loops de novo", (0, 45), (320, 25), wx.ALIGN_CENTRE)
	    self.lblInst.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.NORMAL))
	elif (platform.system() == "Darwin"):
	    self.lblInst = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblInstKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(0, 45), size=(320, 25))
	else:
	    self.lblInst = wx.StaticText(self, -1, "Remodel existing loops or generate loops de novo", (5, 45), style=wx.ALIGN_CENTRE)
	    self.lblInst.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.NORMAL))
	    resizeTextControlForUNIX(self.lblInst, 0, self.GetSize()[0]-20)
	self.lblInst.SetForegroundColour("#FFFFFF")
	
	if (platform.system() == "Windows"):
	    self.lblModel = wx.StaticText(self, -1, "Model", (7, 90), (153, 20), wx.ALIGN_CENTRE)
	    self.lblModel.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblModel = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblModelKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(7, 90), size=(153, 20))
	else:
	    self.lblModel = wx.StaticText(self, -1, "Model", (7, 90), style=wx.ALIGN_CENTRE)
	    self.lblModel.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblModel, 7, 153)
	self.lblModel.SetForegroundColour("#FFFFFF")
	self.modelMenu = wx.ComboBox(self, pos=(7, 110), size=(153, 25), choices=[], style=wx.CB_READONLY)
	self.modelMenu.Bind(wx.EVT_COMBOBOX, self.modelMenuSelect)
	self.modelMenu.SetToolTipString("Model on which to perform loop modeling")
	self.selectedModel = ""
	if (platform.system() == "Windows"):
	    self.lblLoopType = wx.StaticText(self, -1, "Remodel Type", (195, 90), (100, 20), wx.ALIGN_CENTRE)
	    self.lblLoopType.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblLoopType = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblLoopType.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(195, 90), size=(100, 20))
	else:
	    self.lblLoopType = wx.StaticText(self, -1, "Remodel Type", (195, 90), style=wx.ALIGN_CENTRE)
	    self.lblLoopType.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblLoopType, 195, 100)
	self.lblLoopType.SetForegroundColour("#FFFFFF")
	if (platform.system() == "Darwin"):
	    self.btnLoopType = wx.BitmapButton(self, id=-1, bitmap=wx.Image("images/osx/btnLoopType_Refine.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(175, 110), size=(140, 25))
	else:
	    self.btnLoopType = wx.Button(self, id=-1, label="Refine", pos=(175, 110), size=(140, 25))
	    self.btnLoopType.SetForegroundColour("#000000")
	    self.btnLoopType.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	self.btnLoopType.Bind(wx.EVT_BUTTON, self.changeLoopType)
	self.loopType = "Refine"
	self.btnLoopType.SetToolTipString("Refine a pre-existing loop using the high resolution KIC remodeler only")
	
	if (platform.system() == "Windows"):
	    self.lblBegin = wx.StaticText(self, -1, "Loop Begin", (20, 140), (120, 20), wx.ALIGN_CENTRE)
	    self.lblBegin.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblBegin = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblBegin.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(20, 140), size=(120, 20))
	else:
	    self.lblBegin = wx.StaticText(self, -1, "Loop Begin", (20, 140), style=wx.ALIGN_CENTRE)
	    self.lblBegin.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblBegin, 20, 120)
	self.lblBegin.SetForegroundColour("#FFFFFF")
	self.beginMenu = wx.ComboBox(self, pos=(20, 160), size=(120, 25), choices=[], style=wx.CB_READONLY)
	self.beginMenu.Bind(wx.EVT_COMBOBOX, self.beginMenuSelect)
	self.beginMenu.SetToolTipString("Loop N-terminus")
	self.loopBegin = -1
	
	if (platform.system() == "Windows"):
	    self.lblEnd = wx.StaticText(self, -1, "Loop End", (175, 140), (120, 20), wx.ALIGN_CENTRE)
	    self.lblEnd.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblEnd = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblEnd.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(175, 140), size=(120, 20))
	else:
	    self.lblEnd = wx.StaticText(self, -1, "Loop End", (175, 140), style=wx.ALIGN_CENTRE)
	    self.lblEnd.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblEnd, 175, 120)
	self.lblEnd.SetForegroundColour("#FFFFFF")
	self.endMenu = wx.ComboBox(self, pos=(175, 160), size=(120, 25), choices=[], style=wx.CB_READONLY)
	self.endMenu.Bind(wx.EVT_COMBOBOX, self.endMenuSelect)
	self.endMenu.SetToolTipString("Loop C-terminus")
	self.loopEnd = -1
	
	if (platform.system() == "Windows"):
	    self.lblSequence = wx.StaticText(self, -1, "Loop Sequence:", (20, 198), (100, 20), wx.ALIGN_CENTRE)
	    self.lblSequence.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblSequence = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblSequence.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(20, 198), size=(100, 20))
	else:
	    self.lblSequence = wx.StaticText(self, -1, "Loop Sequence:", (20, 198), style=wx.ALIGN_CENTRE)
	    self.lblSequence.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblSequence, 20, 100)
	self.lblSequence.SetForegroundColour("#FFFFFF")
	self.txtSequence = wx.TextCtrl(self, -1, pos=(155, 195), size=(140, 25))
	self.txtSequence.SetValue("")
	self.txtSequence.SetToolTipString("Primary sequence for a de novo loop")
	self.txtSequence.Disable()
	
	if (platform.system() == "Windows"):
	    self.lblAdvanced = wx.StaticText(self, -1, "Advanced Options", (0, 230), (320, 20), wx.ALIGN_CENTRE)
	    self.lblAdvanced.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblAdvanced = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblAdvanced.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(0, 230), size=(320, 20))
	else:
	    self.lblAdvanced = wx.StaticText(self, -1, "Advanced Options", (0, 230), style=wx.ALIGN_CENTRE)
	    self.lblAdvanced.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblAdvanced, 0, 320)
	self.lblAdvanced.SetForegroundColour("#FFFFFF")
	
	if (platform.system() == "Windows"):
	    self.lblPerturb = wx.StaticText(self, -1, "KIC Type:", (10, 263), (100, 20), wx.ALIGN_CENTRE)
	    self.lblPerturb.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblPerturb = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblPerturb.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(10, 263), size=(100, 20))
	else:
	    self.lblPerturb = wx.StaticText(self, -1, "KIC Type:", (10, 263), style=wx.ALIGN_CENTRE)
	    self.lblPerturb.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblPerturb, 10, 100)
	self.lblPerturb.SetForegroundColour("#FFFFFF")
	if (platform.system() == "Darwin"):
	    self.btnPerturb = wx.BitmapButton(self, id=-1, bitmap=wx.Image("images/osx/btnPerturb_Refine.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(120, 260), size=(200, 25))
	else:
	    self.btnPerturb = wx.Button(self, id=-1, label="Perturb+Refine", pos=(120, 260), size=(200, 25))
	    self.btnPerturb.SetForegroundColour("#000000")
	    self.btnPerturb.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	self.btnPerturb.Bind(wx.EVT_BUTTON, self.changePerturbType)
	self.perturbType = "Perturb+Refine"
	self.btnPerturb.SetToolTipString("Perform KIC coarse perturbation followed by high resolution refinement")
	self.btnPerturb.Disable()
	
	if (platform.system() == "Windows"):
	    self.lblPivot = wx.StaticText(self, -1, "Pivot Residue:", (20, 293), (120, 20), wx.ALIGN_CENTRE)
	    self.lblPivot.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblPivot = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblPivot.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(20, 293), size=(120, 20))
	else:
	    self.lblPivot = wx.StaticText(self, -1, "Pivot Residue:", (20, 293), style=wx.ALIGN_CENTRE)
	    self.lblPivot.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblPivot, 20, 120)
	self.lblPivot.SetForegroundColour("#FFFFFF")
	self.menuPivot = wx.ComboBox(self, pos=(175, 290), size=(120, 25), choices=[], style=wx.CB_READONLY)
	self.menuPivot.Bind(wx.EVT_COMBOBOX, self.viewMenuSelect)
	self.menuPivot.Disable()
	self.menuPivot.SetToolTipString("Select the loop residue that will serve as the KIC pivot point")
	
	if (platform.system() == "Windows"):
	    self.lblNStruct = wx.StaticText(self, -1, "NStruct:", (20, 323), (100, 20), wx.ALIGN_CENTRE)
	    self.lblNStruct.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblNStruct = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblNStruct.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(20, 323), size=(100, 20))
	else:
	    self.lblNStruct = wx.StaticText(self, -1, "NStruct:", (20, 323), style=wx.ALIGN_CENTRE)
	    self.lblNStruct.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblNStruct, 20, 100)
	self.lblNStruct.SetForegroundColour("#FFFFFF")
	self.txtNStruct = wx.TextCtrl(self, -1, pos=(155, 320), size=(140, 25))
	self.txtNStruct.SetValue("1")
	self.txtNStruct.SetToolTipString("Number of models to generate (each KIC simulation typically takes 5-10 minutes)")
	self.txtNStruct.Disable()
	
	if (platform.system() == "Darwin"):
	    self.btnOutputDir = wx.BitmapButton(self, id=-1, bitmap=wx.Image("images/osx/btnOutputDir.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(20, 350), size=(100, 25))
	else:
	    self.btnOutputDir = wx.Button(self, id=-1, label="Output Dir", pos=(20, 350), size=(100, 25))
	    self.btnOutputDir.SetForegroundColour("#000000")
	    self.btnOutputDir.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    self.btnOutputDir.Bind(wx.EVT_BUTTON, self.setOutputDir)
	self.btnOutputDir.SetToolTipString("Set the directory to which outputted structures will be written, if NStruct > 1")
	self.btnOutputDir.Disable()
	if (platform.system() == "Windows"):
	    self.lblDir = wx.StaticText(self, -1, "", (130, 355), (190, 20), wx.ALIGN_CENTRE)
	    self.lblDir.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
	else:
	    self.lblDir = wx.StaticText(self, -1, "", (130, 355), style=wx.ALIGN_CENTRE)
	    self.lblDir.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
	    resizeTextControlForUNIX(self.lblDir, 130, 190)
	self.lblDir.SetForegroundColour("#FFFFFF")
	self.outputdir = ""
	
	if (platform.system() == "Windows"):
	    self.lblLine = wx.StaticText(self, -1, "==========================", (0, 380), (320, 20), wx.ALIGN_CENTRE)
	    self.lblLine.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
	elif (platform.system() == "Darwin"):
	    self.lblLine = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblLine.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(0, 380), size=(320, 20))
	else:
	    self.lblLine = wx.StaticText(self, -1, "==========================", (0, 380), style=wx.ALIGN_CENTRE)
	    self.lblLine.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
	    resizeTextControlForUNIX(self.lblLine, 20, 120)
	self.lblLine.SetForegroundColour("#FFFFFF")
	
	if (platform.system() == "Windows"):
	    self.lblPostKIC = wx.StaticText(self, -1, "Post-Loop Modeling", (0, 405), (320, 20), wx.ALIGN_CENTRE)
	    self.lblPostKIC.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblPostKIC = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblPostKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(0, 405), size=(320, 20))
	else:
	    self.lblPostKIC = wx.StaticText(self, -1, "Post-Loop Modeling", (0, 405), style=wx.ALIGN_CENTRE)
	    self.lblPostKIC.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.BOLD))
	    resizeTextControlForUNIX(self.lblPostKIC, 0, self.GetSize()[0]-20)
	self.lblPostKIC.SetForegroundColour("#FFFFFF")
	
	if (platform.system() == "Darwin"):
	    self.scoretypeMenu = wx.ComboBox(self, pos=(7, 435), size=(305, 25), choices=[], style=wx.CB_READONLY)
	else:
	    self.scoretypeMenu = wx.ComboBox(self, pos=(7, 435), size=(305, 25), choices=[], style=wx.CB_READONLY | wx.CB_SORT)
	self.scoretypeMenu.Bind(wx.EVT_COMBOBOX, self.scoretypeMenuSelect)
	self.scoretypeMenu.Disable() # Is only enabled after a design and before accepting it
	self.scoretypeMenu.SetToolTipString("Scoretype by which PyMOL residues will be colored")
	
	if (platform.system() == "Windows"):
	    self.lblModelView = wx.StaticText(self, -1, "View Structure:", (20, 473), (120, 20), wx.ALIGN_CENTRE)
	    self.lblModelView.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	elif (platform.system() == "Darwin"):
	    self.lblModelView = wx.StaticBitmap(self, -1, wx.Image("images/osx/lblModelView.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(20, 473), size=(120, 20))
	else:
	    self.lblModelView = wx.StaticText(self, -1, "View Structure:", (20, 473), style=wx.ALIGN_CENTRE)
	    self.lblModelView.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
	    resizeTextControlForUNIX(self.lblModelView, 20, 120)
	self.lblModelView.SetForegroundColour("#FFFFFF")
	self.viewMenu = wx.ComboBox(self, pos=(175, 470), size=(120, 25), choices=[], style=wx.CB_READONLY)
	self.viewMenu.Bind(wx.EVT_COMBOBOX, self.viewMenuSelect)
	self.viewMenu.Disable()
	self.viewMenu.SetToolTipString("Select loop positions to view in PyMOL")
	
	if (platform.system() == "Darwin"):
	    self.btnKIC = wx.BitmapButton(self, id=-1, bitmap=wx.Image("images/osx/btnKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(100, 505), size=(120, 25))
	else:
	    self.btnKIC = wx.Button(self, id=-1, label="KIC!", pos=(100, 505), size=(120, 25))
	    self.btnKIC.SetForegroundColour("#000000")
	    self.btnKIC.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.BOLD))
	self.btnKIC.Bind(wx.EVT_BUTTON, self.KICClick)
	self.btnKIC.SetToolTipString("Begin KIC simulation with selected parameters")
	self.buttonState = "KIC!"
	
	self.scrollh = self.btnKIC.GetPosition()[1] + self.btnKIC.GetSize()[1] + 5
	self.SetScrollbars(1, 1, 320, self.scrollh)
    
    def showHelp(self, event):
	# Open the help page
	webbrowser.open(self.parent.parent.scriptdir + "/help/kic.html")
    
    def setSeqWin(self, seqWin):
	self.seqWin = seqWin
	# So the sequence window knows about what model "designed_view" really is
	self.seqWin.setProtocolPanel(self)
	
    def setPyMOL(self, pymol):
	self.pymol = pymol
	self.cmd = pymol.cmd
	self.stored = pymol.stored
	
    def setSelectWin(self, selectWin):
	self.selectWin = selectWin
	self.selectWin.setProtPanel(self)
	
    def activate(self):
	# Get the list of all the models in the sequence viewer
	modelList = []
	for r in range(0, self.seqWin.SeqViewer.NumberRows):
	    model = self.seqWin.getModelForChain(r)
	    if (not(model in modelList)):
		modelList.append(model)
	# Update the combobox list if the list has changed
	if (modelList != self.modelMenu.GetItems()):
	    self.modelMenu.Clear()
	    self.modelMenu.AppendItems(modelList)
	    self.selectedModel = ""
	    if (platform.system() == "Windows"):
		self.modelMenu.SetSelection(-1)
	    else:
		self.modelMenu.SetSelection(0)
		self.modelMenuSelect(None)
	# If the user was deleting things in the sequence window, the specified begin and end positions might
	# not be valid anymore so we should erase them
	poseindx = self.seqWin.getPoseIndexForModel(self.selectedModel)
	if (poseindx >= 0):
	    naa = 0
	    for ch in self.seqWin.poses[poseindx][0]:
		for residue in ch:
		    if (residue.resname in "ALA CYS ASP GLU PHE GLY HIS ILE LYS LEU MET ASN PRO GLN ARG SER THR VAL TRP TYR "):
			naa = naa + 1
	    if (len(self.beginMenu.GetItems()) != naa-1):
		self.selectedModel = ""
		self.modelMenuSelect(None)
    
    def modelMenuSelect(self, event):
	# Update the list of positions with the new model
	if (self.selectedModel == self.modelMenu.GetStringSelection()):
	    return
	self.selectedModel = self.modelMenu.GetStringSelection()
	logInfo("Selected model " + self.selectedModel)
	# Get the location of the pose
	poseindx = self.seqWin.getPoseIndexForModel(self.selectedModel)
	# Read the positions
	pose = self.seqWin.poses[poseindx]
	positions = []
	for ch in pose[0]:
	    for residue in ch:
		if ("ALA CYS ASP GLU PHE GLY HIS ILE LYS LEU MET ASN PRO GLN ARG SER THR VAL TRP TYR ".find(residue.resname) >= 0):
		    chain = ch.id
		    if (len(chain.strip()) == 0):
			chain = "_"
		    label = chain + ":" + AA3to1(residue.resname) + str(residue.id[1])
		    positions.append(label)
	# Update the beginning and ending positions menus with the available sequence positions
	self.beginMenu.Clear()
	self.beginMenu.AppendItems(positions[0:len(positions)-1])
	if (platform.system() == "Windows"):
	    self.beginMenu.SetSelection(-1)
	    self.loopBegin = -1
	else:
	    self.beginMenu.SetSelection(0)
	    self.loopBegin = 0
	self.endMenu.Clear()
	self.endMenu.AppendItems(positions[1:])
	if (platform.system() == "Windows"):
	    self.endMenu.SetSelection(-1)
	    self.loopEnd = -1
	else:
	    self.endMenu.SetSelection(0)
	    self.loopEnd = 0
	self.txtNStruct.Enable()
    
    def changeLoopType(self, event):
	if (self.loopType == "Refine"):
	    self.loopType = "Reconstruct"
	    if (platform.system() == "Darwin"):
		self.btnLoopType.SetBitmapLabel(bitmap=wx.Image("images/osx/btnLoopType_Reconstruct.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnLoopType.SetLabel(self.loopType)
	    self.btnLoopType.SetToolTipString("Reconstruct the current loop using the wildtype sequence")
	    self.btnPerturb.Enable()
	    self.txtNStruct.Enable()
	    self.btnOutputDir.Enable()
	elif (self.loopType == "Reconstruct"):
	    self.loopType = "De Novo"
	    if (platform.system() == "Darwin"):
		self.btnLoopType.SetBitmapLabel(bitmap=wx.Image("images/osx/btnLoopType_DeNovo.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnLoopType.SetLabel(self.loopType)
	    self.btnLoopType.SetToolTipString("Construct a new loop with a new sequence")
	    self.txtSequence.Enable()
	else:
	    self.loopType = "Refine"
	    if (platform.system() == "Darwin"):
		self.btnLoopType.SetBitmapLabel(bitmap=wx.Image("images/osx/btnLoopType_Refine.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnLoopType.SetLabel(self.loopType)
	    self.btnLoopType.SetToolTipString("Refine a pre-existing loop using the high resolution KIC remodeler only")
	    self.txtSequence.Disable()
	    self.btnPerturb.Disable()
	    self.txtNStruct.Disable()
	    self.btnOutputDir.Disable()
	logInfo("Changed loop type to " + self.loopType)
	
    def changePerturbType(self, event):
	if (self.perturbType == "Perturb+Refine"):
	    self.perturbType = "Perturb Only, Fullatom"
	    if (platform.system() == "Darwin"):
		self.btnPerturb.SetBitmapLabel(bitmap=wx.Image("images/osx/btnPerturb_Fullatom.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnPerturb.SetLabel(self.perturbType)
	    self.btnPerturb.SetToolTipString("Perform only KIC coarse perturbations but convert outputted models to repacked fullatom PDBs")
	#elif (self.perturbType == "Perturb Only, Fullatom"):
	#    self.perturbType = "Perturb Only, Centroid"
	#    self.btnPerturb.SetToolTipString("Perform only KIC coarse perturbations and leave outputted PDBs in coarse centroid mode")
	else:
	    self.perturbType = "Perturb+Refine"
	    if (platform.system() == "Darwin"):
		self.btnPerturb.SetBitmapLabel(bitmap=wx.Image("images/osx/btnPerturb_Refine.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnPerturb.SetLabel(self.perturbType)
	    self.btnPerturb.SetToolTipString("Perform KIC coarse perturbation followed by high resolution refinement")
	logInfo("Changed perturbation type to " + self.perturbType)
    
    def setOutputDir(self, event):
	logInfo("Clicked Output Dir button")
	dlg = wx.DirDialog(
	    self, message="Choose a directory",
	    defaultPath=self.seqWin.cwd,
	    style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
	if (dlg.ShowModal() == wx.ID_OK):
	    path = dlg.GetPath()
	    self.outputdir = str(path)
	    # Change cwd to the last opened file
	    self.seqWin.cwd = self.outputdir
	    self.seqWin.saveWindowData(None)
	    self.lblDir.SetLabel(self.outputdir)
	    if (platform.system() != "Windows"):
		resizeTextControlForUNIX(self.lblDir, 130, 190)
	    logInfo("Set output directory as " + self.outputdir)
	else:
	    logInfo("Cancelled out of Load PDB")
    
    def populatePivots(self):
	self.menuPivot.Enable()
	# Get the location of the pose
	poseindx = self.seqWin.getPoseIndexForModel(self.selectedModel)
	# Read the positions
	pose = self.seqWin.poses[poseindx]
	positions = []
	ires = 1
	for ch in pose[0]:
	    for residue in ch:
		if (ires >= self.loopBegin and ires <= self.loopEnd):
		    if ("ALA CYS ASP GLU PHE GLY HIS ILE LYS LEU MET ASN PRO GLN ARG SER THR VAL TRP TYR ".find(residue.resname) >= 0):
			chain = ch.id
			if (len(chain.strip()) == 0):
			    chain = "_"
			label = chain + ":" + AA3to1(residue.resname) + str(residue.id[1])
			positions.append(label)
		ires = ires + 1
	self.menuPivot.Clear()
	self.menuPivot.AppendItems(positions)
	self.menuPivot.SetSelection(0)
    
    def beginMenuSelect(self, event):
	try:
	    chain = self.beginMenu.GetStringSelection()[0]
	    seqpos = self.beginMenu.GetStringSelection()[3:].strip()
	    rindx = self.seqWin.getRosettaIndex(self.selectedModel, chain, seqpos)
	    self.loopBegin = rindx
	    # If this new loop begin is further down than what is set for loop end, then it needs
	    # to be reset and the user should be notified
	    if (self.loopEnd >= 0 and self.loopEnd <= rindx):
		if (platform.system() == "Windows"):
		    self.endMenu.SetSelection(-1)
		    self.loopEnd = -1
		else:
		    self.endMenu.SetSelection(self.beginMenu.GetSelection()) # This clears the menu, SetStringSelection/SetValue doesn't seem to work
		    self.endMenuSelect(event)
		wx.MessageBox("Your selected end loop value is no longer valid.  Please choose an ending position after the one you've selected here.", "Loop End No Longer Valid", wx.OK|wx.ICON_EXCLAMATION)
	    if (self.loopBegin >= 0 and self.loopEnd >= 0 and self.loopBegin < self.loopEnd):
		# Populate the pivot menu
		self.populatePivots()
	    else:
		self.menuPivot.Disable()
	    self.focusView(self.beginMenu.GetStringSelection(), self.selectedModel)
	    logInfo("Selected " + self.beginMenu.GetStringSelection() + " as the beginning of the loop")
	except:
	    # Probably the user left the field blank, do nothing
	    pass
    
    def endMenuSelect(self, event):
	try:
	    chain = self.endMenu.GetStringSelection()[0]
	    seqpos = self.endMenu.GetStringSelection()[3:].strip()
	    rindx = self.seqWin.getRosettaIndex(self.selectedModel, chain, seqpos)
	    self.loopEnd = rindx
	    # If this new loop begin is further up than what is set for loop begin, then it needs
	    # to be reset and the user should be notified
	    if (self.loopBegin >= 0 and self.loopBegin >= rindx):
		if (platform.system() == "Windows"):
		    self.beginMenu.SetSelection(-1)
		    self.loopBegin = -1
		else:
		    self.beginMenu.SetSelection(self.endMenu.GetSelection()) # This clears the menu, SetStringSelection/SetValue doesn't seem to work
		    self.beginMenuSelect(event)
		wx.MessageBox("Your selected begin loop value is no longer valid.  Please choose a beginning position before the one you've selected here.", "Loop Begin No Longer Valid", wx.OK|wx.ICON_EXCLAMATION)
	    if (self.loopBegin >= 0 and self.loopEnd >= 0 and self.loopBegin < self.loopEnd):
		# Populate the pivot menu
		self.populatePivots()
	    else:
		self.menuPivot.Disable()
	    self.focusView(self.endMenu.GetStringSelection(), self.selectedModel)
	    logInfo("Selected " + self.endMenu.GetStringSelection() + " as the ending of the loop")
	except:
	    # Probably the user left the field blank, do nothing
	    pass
	
    def viewMenuSelect(self, event):
	try:
	    self.focusView(self.viewMenu.GetStringSelection(), self.selectedModel, "kic_view")
	    logInfo("Viewing " + self.viewMenu.GetStringSelection())
	except:
	    # Probably the user left the field blank, do nothing
	    pass
    
    def focusView(self, posID, origmodel, newmodel=None):
	model = origmodel
	loopEnd = self.loopEnd
	if (posID != "Whole Loop"):
	    chain = posID[0]
	    seqpos = posID[3:].strip()
	    # Loop end needs to be recalculated if this is a view of the de novo loop since the
	    # de novo loop may be a different size
	    if (newmodel and len(self.txtSequence.GetValue()) > 0):
		loopEnd = self.loopBegin + len(self.txtSequence.GetValue()) + 1 # For the anchor
	else:
	    i = 1
	    wholeloop_data = []
	    for ch in self.KICView[0]:
		for residue in ch:
		    if (i >= self.loopBegin and i <= loopEnd):
			chain = ch.id
			seqpos = str(residue.id[1])
			wholeloop_data.append((chain, seqpos))
		    i = i + 1
	# Find the neighborhood view
	if (newmodel):
	    firstmodel = newmodel
	else:
	    firstmodel = origmodel
	self.cmd.hide("all")
	if (chain == " " or chain == "_"):
	    self.cmd.select("viewsele", "resi " + seqpos + " and model " + firstmodel)
	else:
	    self.cmd.select("viewsele", "resi " + seqpos + " and model " + firstmodel + " and chain " + chain)
	# If the loop is validly defined, let's show the whole loop instead of individual residues
	if ((self.loopBegin >= 0 and self.loopEnd >= 0 and not(newmodel)) or posID == "Whole Loop"):	
	    for i in range(self.loopBegin, loopEnd+1):
		if (not(newmodel)):
		    (chain, seqpos) = self.seqWin.getResidueInfo(self.selectedModel, i)
		else:
		    (chain, seqpos) = wholeloop_data[i-self.loopBegin]
		if (chain == "_" or len(chain.strip()) == 0):
		    self.cmd.select("viewsele", "viewsele or (resi " + str(seqpos) + " and model " + firstmodel + ")")
		else:
		    self.cmd.select("viewsele", "viewsele or (resi " + str(seqpos) + " and chain " + chain + " and model " + firstmodel + ")")
	self.cmd.select("exviewsele", "model " + firstmodel + " within 12 of viewsele")
	self.cmd.show("cartoon", "exviewsele")
	self.cmd.hide("ribbon", "exviewsele")
	self.cmd.show("sticks", "exviewsele")
	self.cmd.set_bond("stick_radius", 0.1, "exviewsele")
	# Display energy labels for new structures
	if (newmodel):
	    relabelEnergies(self.KICView, self.residue_E, newmodel, self.scoretypeMenu.GetStringSelection(), self.cmd, seqpos)
	    self.cmd.label("not exviewsele", "")
	self.cmd.zoom("exviewsele")
	#if (chain == " " or chain == "_"):
	#    self.cmd.select("viewsele", "resi " + seqpos + " and model " + firstmodel)
	#else:
	#    self.cmd.select("viewsele", "resi " + seqpos + " and model " + firstmodel + " and chain " + chain)
	self.cmd.show("sticks", "viewsele")
	self.cmd.set_bond("stick_radius", 0.25, "viewsele")
	# Highlight this residue in PyMOL
	self.cmd.select("sele", "viewsele")
	if (newmodel):
	    # If this is after a protocol, also show the original structure in green for comparison
	    self.cmd.select("oldsele", "model " + origmodel + " and symbol c")
	    self.cmd.color("green", "oldsele")
	    self.cmd.set("cartoon_color", "green", "oldsele")
	    #if (chain == " " or chain == "_"):
		#self.cmd.select("viewsele", "resi " + seqpos + " and model " + origmodel)
	    #else:
		#self.cmd.select("viewsele", "resi " + seqpos + " and model " + origmodel + " and chain " + chain)
	    #self.cmd.select("viewsele", "model " + origmodel + " within 12 of viewsele")
	    self.cmd.select("exviewsele", "model " + origmodel + " within 12 of viewsele")
	    self.cmd.show("cartoon", "exviewsele")
	    self.cmd.hide("ribbon", "exviewsele")
	    self.cmd.show("sticks", "exviewsele")
	    self.cmd.set_bond("stick_radius", 0.1, "exviewsele")
	    self.cmd.zoom("exviewsele")
	    self.cmd.delete("oldsele")
	    #if (chain == " " or chain == "_"):
		#self.cmd.select("exviewsele", "resi " + seqpos + " and model " + origmodel)
	    #else:
		#self.cmd.select("viewsele", "resi " + seqpos + " and model " + origmodel + " and chain " + chain)
	    #self.cmd.show("sticks", "viewsele")
	    #self.cmd.set_bond("stick_radius", 0.25, "viewsele")
	self.cmd.enable("sele")
	self.cmd.delete("viewsele")
	self.cmd.select("exviewsele", "solvent")
	self.cmd.hide("everything", "exviewsele")
	self.cmd.delete("exviewsele")
	self.seqWin.selectUpdate(False)
    
    def scoretypeMenuSelect(self, event):
	# Make sure there is even a PyMOL_Mover pose loaded
	if (self.selectedModel == ""):
	    return
	logInfo("Changed scoretype view to " + self.scoretypeMenu.GetStringSelection())
	recolorEnergies(self.KICView, self.residue_E, "kic_view", self.scoretypeMenu.GetStringSelection(), self.cmd)
	self.viewMenuSelect(event) # To update all the labels
    
    def cancelKIC(self):
	logInfo("Canceled KIC operation")
	try:
	    os.remove("coarsekicinput")
	except:
	    pass
	try:
	    os.remove("coarsekicinputtemp")
	except:
	    pass
	try:
	    os.remove("repacked.pdb")
	except:
	    pass
	try:
	    os.remove("finekicinput")
	except:
	    pass
	self.tmrKIC.Stop()
	self.seqWin.cannotDelete = False
	self.scoretypeMenu.Disable()
	self.viewMenu.Disable()
	self.modelMenu.Enable()
	self.beginMenu.Enable()
	self.endMenu.Enable()
	self.btnLoopType.Enable()
	if (self.loopType == "De Novo"):
	    self.txtSequence.Enable()
	if (platform.system() == "Darwin"):
	    self.btnKIC.SetBitmapLabel(bitmap=wx.Image("images/osx/btnKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	else:
	    self.btnKIC.SetLabel("KIC!")
	self.buttonState = "KIC!"
	self.btnKIC.SetToolTipString("Perform KIC simulation with selected parameters")
	self.parent.parent.restartDaemon()
	self.parent.GoBtn.Enable()
	# Get rid of the messages
	for i in range(0, len(self.seqWin.msgQueue)):
	    if (self.seqWin.msgQueue[i].find("Performing KIC loop modeling") >= 0):
		self.seqWin.msgQueue.pop(i)
		break
	for i in range(0, len(self.seqWin.msgQueue)):
	    if (self.seqWin.msgQueue[i].find("Performing rotamer repacking") >= 0):
		self.seqWin.msgQueue.pop(i)
		break
	for i in range(0, len(self.seqWin.msgQueue)):
	    if (self.seqWin.msgQueue[i].find("Performing refined KIC loop modeling") >= 0):
		self.seqWin.msgQueue.pop(i)
		break
	if (len(self.seqWin.msgQueue) > 0):
	    self.seqWin.labelMsg.SetLabel(self.seqWin.msgQueue[len(self.seqWin.msgQueue)-1])
	else:
	    self.seqWin.labelMsg.SetLabel("")
    
    def KICClick(self, event):
	# This is also the "Finalize!" button
	if (self.buttonState == "KIC!"):
	    # First we have to make sure that the loops are defined and that the sequence is valid
	    if (self.loopBegin < 0):
		wx.MessageBox("Please select a loop beginning position.", "Loop Begin Required", wx.OK|wx.ICON_EXCLAMATION)
		return
	    elif (self.loopEnd < 0):
		wx.MessageBox("Please select a loop ending position.", "Loop End Required", wx.OK|wx.ICON_EXCLAMATION)
		return
	    elif (self.loopType == "De Novo"):
		# Make sure the sequence has only CAAs in it
		for AA in self.txtSequence.GetValue().strip().upper():
		    if (not(AA in "ACDEFGHIKLMNPQRSTVWY")):
			wx.MessageBox("The sequence you have provided is invalid.  Please only use canonical amino acids.", "Sequence Invalid", wx.OK|wx.ICON_EXCLAMATION)
			return
		if (len(self.txtSequence.GetValue().strip().upper()) == 0):
		    wx.MessageBox("You have indicated that you want to design a loop de novo but have not provided the putative sequence of the loop.  Please provide one or switch to use a pre-existing loop.", "No Sequence Indicated", wx.OK|wx.ICON_EXCLAMATION)
		    return
	    try:
		if (int(self.txtNStruct.GetValue()) <= 0):
		    raise Exception
	    except:
		wx.MessageBox("Please enter a positive value for the number of structures.", "Invalid NStruct", wx.OK|wx.ICON_EXCLAMATION)
		return
	    if (int(self.txtNStruct.GetValue()) > 1 and len(self.outputdir.strip()) == 0):
		wx.MessageBox("If you want to generate more than one structure, you need to indicate a directory to which all these structures will be outputted.", "Specify an Output Directory", wx.OK|wx.ICON_EXCLAMATION)
		return
	    self.seqWin.labelMsg.SetLabel("Performing KIC loop modeling, please be patient...")
	    self.seqWin.msgQueue.append("Performing KIC loop modeling, please be patient...")
	    self.seqWin.cannotDelete = True
	    self.parent.GoBtn.Disable()
	    self.modelMenu.Disable()
	    self.btnLoopType.Disable()
	    self.beginMenu.Disable()
	    self.endMenu.Disable()
	    self.txtSequence.Disable()
	    if (platform.system() == "Darwin"):
		self.btnKIC.SetBitmapLabel(bitmap=wx.Image("images/osx/btnKIC_Cancel.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnKIC.SetLabel("Cancel!")
	    self.buttonState = "Cancel!"
	    self.btnKIC.SetToolTipString("Cancel the KIC simulation")
	    self.stage = 1
	    #thrKIC = Thread(target=self.threadKIC, args=())
	    #thrKIC.start()
	    logInfo("Clicked the KIC button")
	    if (len(self.txtSequence.GetValue().strip())):
		logInfo("The new loop sequence is " + self.txtSequence.GetValue().strip())
	    self.tmrKIC = wx.Timer(self)
	    self.Bind(wx.EVT_TIMER, self.threadKIC, self.tmrKIC)
	    self.tmrKIC.Start(1000)
	elif (self.buttonState == "Cancel!"):
	    dlg = wx.MessageDialog(self, "Are you sure you want to cancel the KIC simulation?  All progress will be lost.", "Cancel KIC Simulation", wx.YES_NO | wx.ICON_QUESTION | wx.CENTRE)
	    result = dlg.ShowModal()
	    if (result == wx.ID_YES):
		self.cancelKIC()
	    dlg.Destroy()
	else:
	    # Finalize button, ask whether the changes will be accepted or rejected
	    dlg = wx.MessageDialog(self, "Do you want to accept the results of this loop modeling session?", "Accept/Reject Model", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION | wx.CENTRE)
	    result = dlg.ShowModal()
	    if (result == wx.ID_YES):
		logInfo("Accepted KIC model")
		accept = True
	    elif (result == wx.ID_NO):
		logInfo("Rejected KIC model")
		accept = False
	    else:
		logInfo("Cancelled Finalize operation")
		dlg.Destroy()
		return
	    dlg.Destroy()
	    self.scoretypeMenu.Disable()
	    self.viewMenu.Disable()
	    self.modelMenu.Enable()
	    self.beginMenu.Enable()
	    self.endMenu.Enable()
	    self.btnLoopType.Enable()
	    if (self.loopType == "De Novo"):
		self.txtSequence.Enable()
	    if (platform.system() == "Darwin"):
		self.btnKIC.SetBitmapLabel(bitmap=wx.Image("images/osx/btnKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	    else:
		self.btnKIC.SetLabel("KIC!")
	    self.buttonState = "KIC!"
	    self.btnKIC.SetToolTipString("Perform KIC simulation with selected parameters")
	    self.cmd.label("all", "")
	    self.seqWin.cannotDelete = False
	    if (not(accept)):
		self.cmd.remove("kic_view")
		self.cmd.delete("kic_view")
		return
	    # Get rid of the original pose, save the designed pose, and reload the structure in PyMOL
	    poseindx = -1
	    for r in range(0, len(self.seqWin.IDs)):
		if (self.seqWin.IDs[r].find(self.selectedModel) >= 0):
		    poseindx = r
		    break
	    try:
		self.cmd.remove(self.selectedModel)
		self.cmd.delete(self.selectedModel)
		self.cmd.remove("kic_view")
		self.cmd.delete("kic_view")
		self.cmd.load(self.selectedModel + "_K.pdb", self.selectedModel)
		#self.KICView.pdb_info().name(str(self.selectedModel + ".pdb"))
		self.seqWin.reloadPose(poseindx, self.selectedModel, self.selectedModel + "_K.pdb")
		defaultPyMOLView(self.cmd, self.selectedModel)
		del self.KICView
		# IMPORTANT: You have to replace the model in the sandbox with the new designed model
		os.remove(self.selectedModel + ".pdb")
		os.rename(self.selectedModel + "_K.pdb", self.selectedModel + ".pdb")
	    except:
		# Some weird error happened, do nothing instead of crashing
		print "Bug at accept button click"
		pass	
    
    def recoverFromError(self, msg=""):
	# This function tells the user what the error was and tries to revert the protocol
	# back to the pre-daemon state so the main GUI can continue to be used
	if (len(msg) == 0):
	    f = open("errreport", "r")
	    errmsg = "An error was encountered during the protocol:\n\n"
	    for aline in f:
		errmsg = errmsg + str(aline)
	    f.close()
	    os.remove("errreport")
	else:
	    errmsg = msg
	logInfo("Error Encountered")
	logInfo(errmsg)
	if (platform.system() == "Windows"):
	    sessioninfo = os.path.expanduser("~") + "\\InteractiveRosetta\\sessionlog"
	else:
	    sessioninfo = os.path.expanduser("~") + "/InteractiveRosetta/sessionlog"
	errmsg = errmsg + "\n\nIf you don't know what caused this, send the file " + sessioninfo + " to a developer along with an explanation of what you did."
	# You have to use a MessageDialog because the MessageBox doesn't always work for some reason
	dlg = wx.MessageDialog(self, errmsg, "Error Encountered", wx.OK|wx.ICON_EXCLAMATION)
	dlg.ShowModal()
	dlg.Destroy()
	self.seqWin.cannotDelete = False
	self.parent.GoBtn.Enable()
	self.modelMenu.Enable()
	self.btnLoopType.Enable()
	self.beginMenu.Enable()
	self.endMenu.Enable()
	self.txtSequence.Enable()
	self.btnKIC.Enable()
	if (platform.system() == "Darwin"):
	    self.btnKIC.SetBitmapLabel(bitmap=wx.Image("images/osx/btnKIC.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
	else:
	    self.btnKIC.SetLabel("KIC!")
	self.buttonState = "KIC!"
	# Get rid of the messages
	for i in range(0, len(self.seqWin.msgQueue)):
	    if (self.seqWin.msgQueue[i].find("Performing KIC loop modeling") >= 0):
		self.seqWin.msgQueue.pop(i)
		break
	for i in range(0, len(self.seqWin.msgQueue)):
	    if (self.seqWin.msgQueue[i].find("Performing rotamer repacking") >= 0):
		self.seqWin.msgQueue.pop(i)
		break
	for i in range(0, len(self.seqWin.msgQueue)):
	    if (self.seqWin.msgQueue[i].find("Performing refined KIC loop modeling") >= 0):
		self.seqWin.msgQueue.pop(i)
		break
	if (len(self.seqWin.msgQueue) > 0):
	    self.seqWin.labelMsg.SetLabel(self.seqWin.msgQueue[len(self.seqWin.msgQueue)-1])
	else:
	    self.seqWin.labelMsg.SetLabel("")
    
    def threadKIC(self, event):
	# Why am I doing this ridiculous timer thing for this KIC protocol?
	# Because apparently on Linux there's some kind of weird bug that manifests when you
	# attempt to run time.sleep loops looking for files to be generated
	# Pango develops a phobia of periods in strings if you do that????
	# Using this staged timer setup eliminates the error
	# What is the problem?  I don't know.  Why does this fix it?  I don't know
	# The people on StackOverflow said to do it and it fixed it -_-
	# I think it has something to do with Linux not liking things like "time.sleep"
	# and calls to wx in threads
	# Dump a file with the loop modeling parameters for the daemon to pick up
	goToSandbox()
	if (self.stage == 1):
	    self.tmrKIC.Stop()
	    self.timeoutCount = 0
	    self.nstruct = int(self.txtNStruct.GetValue())
	    f = open("coarsekicinputtemp", "w")
	    pdbfile = self.selectedModel + ".pdb"
	    # Dump the PDB from PyMOL first in case the coordinates were altered by the user
	    self.cmd.save(pdbfile.strip(), "model " + self.selectedModel)
	    fixPyMOLSave(pdbfile.strip())
	    f.write("PDBFILE\t" + pdbfile.strip() + "\n")
	    f2 = open(pdbfile, "r")
	    f.write("BEGIN PDB DATA\n")
	    for aline in f2:
		f.write(aline.strip() + "\n")
	    f.write("END PDB DATA\n")
	    f2.close()
	    f.write("REMODEL\t" + self.loopType.upper() + "\n")
	    chain = self.beginMenu.GetStringSelection()[0]
	    seqpos = self.beginMenu.GetStringSelection()[3:]
	    loopBegin = self.seqWin.getRosettaIndex(self.selectedModel, chain, seqpos)
	    f.write("LOOPBEGIN\t" + str(loopBegin) + "\n")
	    chain = self.endMenu.GetStringSelection()[0]
	    seqpos = self.endMenu.GetStringSelection()[3:]
	    loopEnd = self.seqWin.getRosettaIndex(self.selectedModel, chain, seqpos)
	    f.write("LOOPEND\t" + str(loopEnd) + "\n")
	    if (self.loopType == "De Novo"):
		f.write("SEQUENCE\t" + self.txtSequence.GetValue().strip().upper() + "\n")
	    f.write("PIVOT\t" + str(self.menuPivot.GetSelection()) + "\n")
	    f.write("NSTRUCT\t" + str(self.nstruct) + "\n")
	    f.write("PERTURB\t" + self.perturbType + "\n")
	    f.write("OUTPUTDIR\t" + self.outputdir + "\n")
	    f.close()
	    appendScorefxnParamsInfoToFile("coarsekicinputtemp", self.selectWin.weightsfile)
	    if (False): #(useServer):
		try: 
		    self.ID = sendToServer("coarsekicinput")
		    self.usingServer = True
		    logInfo("Coarse KIC input sent to server daemon with ID " + self.ID)
		    self.stage = 4 # When using server we cannot see the intermediates
		except:
		    # Something failed, default to the local daemon
		    os.rename("coarsekicinputtemp", "coarsekicinput")
		    self.usingServer = False
		    logInfo("Server daemon not available, coarse KIC input uploaded at coarsekicinput")
		    self.stage = 2
	    else:
		os.rename("coarsekicinputtemp", "coarsekicinput")
		self.usingServer = False
		logInfo("Coarse KIC input uploaded locally at coarsekicinput")
		self.stage = 2
	    if (self.perturbType == "Perturb Only, Centroid" or self.loopType == "Refine"):
		self.stage = 4
	    self.looptimecount = 0
	    self.timeout = 18000000
	    self.tmrKIC.Start(1000)
	elif (self.stage == 2):
	    # This is really annoying, here's the ugly memory problem again
	    # So first we have to do a coarse KIC job in the daemon
	    # This involves using centroid residues, so those have to be repacked in another 
	    # instance of the daemon process because the repacking step pushes the memory usage too
	    # high, so first wait for the "repackmetemp.pdb" structure to show up, kill the daemon
	    # and restart it to do the repacking step
	    if (os.path.isfile("repackmetemp_0.pdb")):
		self.tmrKIC.Stop()
		# Pop this message out of the queue
		for i in range(0, len(self.seqWin.msgQueue)):
		    if (self.seqWin.msgQueue[i].find("Performing KIC loop modeling") >= 0):
			self.seqWin.msgQueue.pop(i)
			break
		self.seqWin.labelMsg.SetLabel("Performing rotamer repacking, please be patient...")
		self.seqWin.msgQueue.append("Performing rotamer repacking, please be patient...")
		self.parent.parent.restartDaemon()
		for decoy in range(0, self.nstruct):
		    os.rename("repackmetemp_" + str(decoy) + ".pdb", "repackme_" + str(decoy) + ".pdb") # So the new daemon sees it
		logInfo("repackmetemp.pdb sent to be rotamer repacked")
		self.stage = 3
		if (self.perturbType == "Perturb Only, Fullatom"):
		    self.stage = 4
		self.tmrKIC.Start(1000)
	    elif (os.path.isfile("errreport")):
		# Something went wrong, tell the user about it (loop sequence probably too short)
		self.tmrKIC.Stop()
		self.parent.parent.restartDaemon() # Has to happen because coarse KIC is threaded
		self.recoverFromError()
	    self.looptimecount = self.looptimecount + 1
	    if (self.looptimecount > self.timeout):
		# The loop was probably too short and coarse KIC will run forever
		# Kill the daemon and tell the user about it
		self.tmrKIC.Stop()
		# First delete that input file so the new daemon doesn't pick it up right away
		try:
		    os.remove("coarsekicinput")
		except:
		    pass
		self.parent.parent.restartDaemon() # Has to happen because coarse KIC is threaded
		self.recoverFromError("ERROR: The loop sequence is too short and cannot bridge the endpoint residues!")
	elif (self.stage == 3):
	    # Now we have to wait for the output of the repacking step and restart the daemon again
	    # so we can finish up with a fine-grained KIC step
	    if (os.path.isfile("repacked_0.pdb")):
		self.tmrKIC.Stop()
		# Pop this message out of the queue
		for i in range(0, len(self.seqWin.msgQueue)):
		    if (self.seqWin.msgQueue[i].find("Performing rotamer repacking") >= 0):
			self.seqWin.msgQueue.pop(i)
			break
		self.seqWin.labelMsg.SetLabel("Performing refined KIC loop modeling, please be patient...")
		self.seqWin.msgQueue.append("Performing refined KIC loop modeling, please be patient...")
		self.parent.parent.restartDaemon()
		os.rename("finekicinputtemp", "finekicinput") # So the new daemon sees it
		logInfo("Repacked coarse structure sent to fine grained KIC")
		self.stage = 4
		self.tmrKIC.Start(1000)
	    elif (os.path.isfile("errreport")):
		# Something went wrong, tell the user about it
		self.tmrKIC.Stop()
		self.recoverFromError()
	elif (self.stage == 4):
	    if (self.usingServer):
		# See if the file has been uploaded yet and bring it here if so
		queryServerForResults("kicoutput-" + self.ID)
		queryServerForResults("coarsekicoutput-" + self.ID)
		self.timeoutCount = self.timeoutCount + 1
	    if (self.timeoutCount >= serverTimeout):
		self.tmrKIC.Stop()
		# If this is taking too long, maybe there's something wrong with the server
		# Ask the user if they want to continue waiting or use the local daemon instead
		dlg = wx.MessageDialog(self, "The server is taking a long time to respond.  Continue to wait?  Pressing No will run the calculations locally.", "Delayed Server Response", wx.YES_NO | wx.ICON_EXCLAMATION | wx.CENTRE)
		if (dlg.ShowModal() == wx.ID_YES):
		    # Reset the counter
		    self.timeoutCount = 0
		else:
		    self.usingServer = False
		    self.timeoutCount = 0
		    os.rename("coarsekicinputtemp", "coarsekicinput")
		    logInfo("Server took too long to respond so the local daemon was used")
		    self.stage = 2
		dlg.Destroy()
		self.tmrKIC.Start(1000)
	    # Read the output dumped by the child process (finally!)
	    if (os.path.isfile("repackedtemp.pdb")):
		# Flip back so the timer sees repacked.pdb and runs the local daemon
		os.rename("coarsekicinputtemp", "finekicinputtemp")
		os.rename("repackedtemp.pdb", "repacked.pdb")
		# Pop this message out of the queue
		for i in range(0, len(self.seqWin.msgQueue)):
		    if (self.seqWin.msgQueue[i].find("Performing KIC loop modeling") >= 0):
			self.seqWin.msgQueue.pop(i)
			break
		self.usingServer = False
		self.timeoutCount = 0
		self.stage = 3
	    elif (os.path.isfile("kicoutput")):
		self.tmrKIC.Stop()
		self.residue_E = []
		f = open("kicoutput", "r")
		for aline in f:
		    if (aline[0:6] == "OUTPUT"):
			pdbfile = aline.split("\t")[1].strip()
			self.KICView = self.seqWin.pdbreader.get_structure("kic_view", pdbfile)
		    elif (aline[0:9] == "LOOPBEGIN"):
			self.loopBegin = int(aline.split("\t")[1])
		    elif (aline[0:7] == "LOOPEND"):
			self.loopEnd = int(aline.split("\t")[1])
		    elif (aline[0:6] == "ENERGY"):
			if (aline.split()[1] == "total_score"):
			    # This is the scoretype line, row 0 in residue_E
			    self.residue_E.append(aline.split()[1:])
			else:
			    self.residue_E.append([])
			    indx = len(self.residue_E) - 1
			    for E in aline.split()[1:]:
				self.residue_E[indx].append(float(E))
		f.close()
		logInfo("Found KIC output at kicoutput")
		# Add the nonzero scoretypes to the energy viewing list from the current score function
		self.scoretypeMenu.Clear()
		for scoretype in self.residue_E[0]:
		    try:
			toAdd = scoretypes[str(scoretype)]
		    except:
			toAdd = str(scoretype)
		    self.scoretypeMenu.Append(toAdd)
		self.scoretypeMenu.Enable()
		# Pop this message out of the queue
		for i in range(0, len(self.seqWin.msgQueue)):
		    if (self.seqWin.msgQueue[i].find("Performing refined KIC loop modeling") >= 0):
			self.seqWin.msgQueue.pop(i)
			break
		    elif (self.seqWin.msgQueue[i].find("Performing rotamer repacking") >= 0):
			self.seqWin.msgQueue.pop(i)
			break
		    elif (self.seqWin.msgQueue[i].find("Performing KIC loop modeling") >= 0):
			self.seqWin.msgQueue.pop(i)
			break
		if (len(self.seqWin.msgQueue) > 0):
		    self.seqWin.labelMsg.SetLabel(self.seqWin.msgQueue[len(self.seqWin.msgQueue)-1])
		else:
		    self.seqWin.labelMsg.SetLabel("")
		# Add these loop residues to the view menu so the user can look at the new loop
		viewoptions = []
		i = 1
		for ch in self.KICView[0]:
		    for residue in ch:
			if (i >= self.loopBegin and i <= self.loopEnd):
			    chain = ch.id
			    seqpos = str(residue.id[1])
			    resn = AA3to1(residue.resname)
			    viewoptions.append(chain + ":" + resn + seqpos)
			i = i + 1
		viewoptions.append("Whole Loop")
		self.viewMenu.Clear()
		self.viewMenu.AppendItems(viewoptions)
		self.viewMenu.Enable()
		self.parent.GoBtn.Enable()
		self.btnKIC.Enable()
		#self.enableControls()
		#self.selectedModel = ""
		if (platform.system() == "Darwin"):
		    self.btnKIC.SetBitmapLabel(bitmap=wx.Image("images/osx/btnKIC_Finalize.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		else:
		    self.btnKIC.SetLabel("Finalize!")
		self.buttonState = "Finalize!"
		self.btnKIC.SetToolTipString("Accept or reject protocol results")
		os.remove("kicoutput")
		# Load the designed pose as the "kic_view" model so the user can look at the results
		self.cmd.load(pdbfile, "kic_view")
		self.cmd.hide("everything", "model kic_view")
		# To get the energy values in the B-factors
		recolorEnergies(self.KICView, self.residue_E, "kic_view", "Total Energy", self.cmd)
		self.seqWin.pdbwriter.set_structure(self.KICView)
		self.seqWin.pdbwriter.save(pdbfile) 
		recolorEnergies(self.KICView, self.residue_E, "kic_view", self.scoretypeMenu.GetStringSelection(), self.cmd)
	    elif (os.path.isfile("errreport")):
		# Something went wrong, tell the user about it
		self.tmrKIC.Stop()
		self.recoverFromError()