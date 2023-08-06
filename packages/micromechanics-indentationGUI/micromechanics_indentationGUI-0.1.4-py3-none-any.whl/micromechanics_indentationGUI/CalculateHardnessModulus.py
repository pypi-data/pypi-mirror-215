""" Graphical user interface to calculate hardness and young's modulus """
import numpy as np
from PySide6.QtCore import Qt # pylint: disable=no-name-in-module
from PySide6.QtWidgets import QTableWidgetItem # pylint: disable=no-name-in-module
from micromechanics import indentation
from .CorrectThermalDrift import correctThermalDrift
from .WaitingUpgrade_of_micromechanics import IndentationXXX

def Calculate_Hardness_Modulus(self):
  """ Graphical user interface to calculate hardness and young's modulus """
  #set Progress Bar
  progressBar = self.ui.progressBar_tabHE
  progressBar.setValue(0)
  #Reading Inputs
  fileName = f"{self.ui.lineEdit_path_tabHE.text()}"
  Poisson = self.ui.doubleSpinBox_Poisson_tabHE.value()
  E_Tip = self.ui.doubleSpinBox_E_Tip_tabHE.value()
  Poisson_Tip = self.ui.doubleSpinBox_Poisson_Tip_tabHE.value()
  unloaPMax = self.ui.doubleSpinBox_Start_Pmax_tabHE.value()
  unloaPMin = self.ui.doubleSpinBox_End_Pmax_tabHE.value()
  relForceRateNoise = self.ui.doubleSpinBox_relForceRateNoise_tabHE.value()
  max_size_fluctuation = self.ui.spinBox_max_size_fluctuation_tabHE.value()
  UsingRate2findSurface = self.ui.checkBox_UsingRate2findSurface_tabHE.isChecked()
  Rate2findSurface = self.ui.doubleSpinBox_Rate2findSurface_tabHE.value()
  DataFilterSize = self.ui.spinBox_DataFilterSize_tabHE.value()
  min_hc4mean = self.ui.doubleSpinBox_minhc4mean_tabHE.value()
  max_hc4mean = self.ui.doubleSpinBox_maxhc4mean_tabHE.value()
  if DataFilterSize%2==0:
    DataFilterSize+=1
  TAF_terms = []
  for j in range(9):
    lineEdit = eval(f"self.ui.lineEdit_TAF{j+1}_tabHE") # pylint: disable=eval-used
    TAF_terms.append(float(lineEdit.text()))
  TAF_terms.append('iso')
  FrameCompliance=float(self.ui.lineEdit_FrameCompliance_tabHE.text())
  #define the Tip
  Tip = indentation.Tip(compliance= FrameCompliance, shape=TAF_terms)
  #define Inputs (Model, Output, Surface)
  Model = {
              'nuTip':      Poisson_Tip,
              'modulusTip': E_Tip,      # GPa from Oliver,Pharr Method paper
              'unloadPMax':unloaPMax,        # upper end of fitting domain of unloading stiffness: Vendor-specific change
              'unloadPMin':unloaPMin,         # lower end of fitting domain of unloading stiffness: Vendor-specific change
              'relForceRateNoise':relForceRateNoise, # threshold of dp/dt use to identify start of loading: Vendor-specific change
              'maxSizeFluctuations': max_size_fluctuation # maximum size of small fluctuations that are removed in identifyLoadHoldUnload
              }
  def guiProgressBar(value, location):
    if location=='convert':
      value = value/2
      progressBar.setValue(value)
  Output = {
              'progressBar': guiProgressBar,   # function to use for plotting progress bar
              }
  Surface = {}
  if UsingRate2findSurface:
    Surface = {
                "abs(dp/dh)":Rate2findSurface, "median filter":DataFilterSize
                }
  #Reading Inputs
  self.i_tabHE = IndentationXXX(fileName=fileName, tip=Tip, nuMat= Poisson, surface=Surface, model=Model, output=Output)
  i = self.i_tabHE
  #show Test method
  Method=i.method.value
  self.ui.comboBox_method_tabHE.setCurrentIndex(Method-1)
  #plot load-depth of test 1
  i.output['ax'] = self.static_ax_load_depth_tab_inclusive_frame_stiffness_tabHE
  i.output['ax'][0].cla()
  i.output['ax'][1].cla()
  i.output['ax'][0].set_title(f"{i.testName}")
  if self.ui.checkBox_UsingDriftUnloading_tabHE.isChecked():
    correctThermalDrift(indentation=i, reFindSurface=True) #calibrate the thermal drift using the collection during the unloading
  if i.method in (indentation.definitions.Method.ISO, indentation.definitions.Method.MULTI):
    i.stiffnessFromUnloading(i.p, i.h, plot=True)
  elif i.method== indentation.definitions.Method.CSM:
    i.output['ax'][0].scatter(i.h, i.p, s=1)
    i.output['ax'][0].axhline(0, linestyle='-.', color='tab:orange', label='zero Load or Depth') #!!!!!!
    i.output['ax'][0].axvline(0, linestyle='-.', color='tab:orange') #!!!!!!
    i.output['ax'][0].legend()
    i.output['ax'][0].set_ylabel(r'force [$\mathrm{mN}$]')
    i.output['ax'][1].set_ylabel(r"$\frac{P_{cal}-P_{mea}}{P_{mea}}x100$ [%]")
    i.output['ax'][1].set_xlabel(r'depth [$\mathrm{\mu m}$]')
  self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabHE.figure.set_tight_layout(True)
  i.output['ax'] = [None, None]
  self.static_canvas_load_depth_tab_inclusive_frame_stiffness_tabHE.draw()
  #changing i.allTestList to calculate using the checked tests
  OriginalAlltest = list(self.i_tabHE.allTestList)
  for k, theTest in enumerate(OriginalAlltest):
    try:
      IsCheck = self.ui.tableWidget_tabHE.item(k,0).checkState()
    except:
      pass
    else:
      if IsCheck==Qt.Unchecked:
        self.i_tabHE.allTestList.remove(theTest)
  self.i_tabHE.restartFile()
  #calculate Hardnss and Modulus for all Tests
  hc_collect=[]
  Pmax_collect=[]
  H_collect=[]
  Hmean_collect=[]
  H4mean_collect=[]
  Hstd_collect=[]
  E_collect=[]
  Emean_collect=[]
  E4mean_collect=[]
  Estd_collect=[]
  Notlist=[]
  testName_collect=[]
  test_number_collect=[]
  ax_H_hc = self.static_ax_H_hc_tabHE
  ax_E_hc = self.static_ax_E_hc_tabHE
  ax_H_hc.cla()
  ax_E_hc.cla()
  while True:
    i.analyse()
    progressBar_Value=int((2*len(i.allTestList)-len(i.testList))/(2*len(i.allTestList))*100)
    progressBar.setValue(progressBar_Value)
    if i.testName not in Notlist:
      Pmax_collect.append(i.Ac*i.hardness)
      hc_collect.append(i.hc)
      H_collect.append(i.hardness)
      E_collect.append(i.modulus)
      marker4mean= np.where((i.hc>=min_hc4mean) & (i.hc<=max_hc4mean))
      Hmean_collect.append(np.mean(i.hardness[marker4mean]))
      H4mean_collect.append(i.hardness[marker4mean])
      Emean_collect.append(np.mean(i.modulus[marker4mean]))
      E4mean_collect.append(i.modulus[marker4mean])
      if len(i.hardness[marker4mean]) > 1:
        Hstd_collect.append(np.std(i.hardness[marker4mean], ddof=1))
        Estd_collect.append(np.std(i.modulus[marker4mean], ddof=1))
      elif len(i.hardness[marker4mean]) == 1:
        Hstd_collect.append(0)
        Estd_collect.append(0)
      testName_collect.append(i.testName)
      test_number_collect.append(int(i.testName[4:]))
      #plotting hardness and young's modulus
      ax_H_hc.plot(i.hc,i.hardness,'.-', linewidth=1)
      ax_E_hc.plot(i.hc,i.modulus,'.-', linewidth=1)
      if not i.testList:
        break
    i.nextTest()
    if self.ui.checkBox_UsingDriftUnloading_tabHE.isChecked():
      correctThermalDrift(indentation=i, reFindSurface=True) #calibrate the thermal drift using the collection during the unloading
  ax_H_hc.axvline(min_hc4mean,color='gray',linestyle='dashed', label='min./max. hc for calculating mean values')
  ax_E_hc.axvline(min_hc4mean,color='gray',linestyle='dashed', label='min./max. hc for calculating mean values')
  if np.max(hc_collect[0])*1.1 > max_hc4mean:
    ax_H_hc.axvline(max_hc4mean,color='gray',linestyle='dashed')
    ax_E_hc.axvline(max_hc4mean,color='gray',linestyle='dashed')
  ax_H_hc.set_ylim(np.mean(Hmean_collect)-np.mean(Hmean_collect)*0.3,np.mean(Hmean_collect)+np.mean(Hmean_collect)*0.3)
  ax_E_hc.set_ylim(np.mean(Emean_collect)-np.mean(Emean_collect)*0.3,np.mean(Emean_collect)+np.mean(Emean_collect)*0.3)
  ax_H_hc.legend()
  ax_E_hc.legend()
  #prepare for export
  self.tabHE_hc_collect=hc_collect
  self.tabHE_Pmax_collect=Pmax_collect
  self.tabHE_H_collect=H_collect
  self.tabHE_E_collect=E_collect
  self.tabHE_testName_collect=testName_collect
  #listing Test
  self.ui.tableWidget_tabHE.setRowCount(len(OriginalAlltest))
  for k, theTest in enumerate(OriginalAlltest):
    qtablewidgetitem=QTableWidgetItem(theTest)
    if theTest in self.i_tabHE.allTestList:
      qtablewidgetitem.setCheckState(Qt.Checked)
    else:
      qtablewidgetitem.setCheckState(Qt.Unchecked)
    self.ui.tableWidget_tabHE.setItem(k,0,qtablewidgetitem)
    if f"{theTest}" in i.output['successTest']:
      self.ui.tableWidget_tabHE.setItem(k,1,QTableWidgetItem("Yes"))
    else:
      self.ui.tableWidget_tabHE.setItem(k,1,QTableWidgetItem("No"))
  #plotting hardness-Indent's Nummber and young's modulus-Indent's Nummber
  ax_H_Index = self.static_ax_H_Index_tabHE
  ax_E_Index = self.static_ax_E_Index_tabHE
  ax_H_Index.cla()
  ax_E_Index.cla()
  H4mean_collect=np.hstack(H4mean_collect)
  E4mean_collect=np.hstack(E4mean_collect)
  ax_H_Index.errorbar(test_number_collect,Hmean_collect,yerr=Hstd_collect,marker='s', markersize=10, capsize=10, capthick=5,elinewidth=2, color='black',alpha=0.7,linestyle='')
  ax_H_Index.axhline(np.mean(H4mean_collect), color = 'tab:orange', label = f"average Hardenss: {np.mean(H4mean_collect)} GPa")
  ax_H_Index.axhline(np.mean(H4mean_collect)+np.std(H4mean_collect,ddof=1), color = 'tab:orange', linestyle='dashed', label = f"standard Deviation: +- {np.std(H4mean_collect,ddof=1)} GPa")
  ax_H_Index.axhline(np.mean(H4mean_collect)-np.std(H4mean_collect,ddof=1), color = 'tab:orange', linestyle='dashed')
  ax_E_Index.errorbar(test_number_collect,Emean_collect,yerr=Estd_collect,marker='s', markersize=10, capsize=10, capthick=5,elinewidth=2, color='black',alpha=0.7,linestyle='')
  ax_E_Index.axhline(np.mean(E4mean_collect), color = 'tab:orange', label = f"average Young's Modulus: {np.mean(E4mean_collect)} GPa")
  ax_E_Index.axhline(np.mean(E4mean_collect)+np.std(E4mean_collect,ddof=1), color = 'tab:orange', linestyle='dashed', label = f"standard Deviation: +- {np.std(E4mean_collect,ddof=1)} GPa")
  ax_E_Index.axhline(np.mean(E4mean_collect)-np.std(E4mean_collect,ddof=1), color = 'tab:orange', linestyle='dashed')
  ax_H_hc.set_xlabel('Contact depth [µm]')
  ax_H_hc.set_ylabel('Hardness [GPa]')
  ax_H_Index.set_xlabel('Indents\'s Nummber')
  ax_H_Index.set_ylabel('Hardness [GPa]')
  ax_E_hc.set_xlabel('Contact depth [µm]')
  ax_E_hc.set_ylabel('Young\'s Modulus [GPa]')
  ax_E_Index.set_xlabel('Indents\'s Nummber')
  ax_E_Index.set_ylabel('Young\'s Modulus [GPa]')
  ax_H_Index.legend()
  ax_E_Index.legend()
  self.static_canvas_H_hc_tabHE.figure.set_tight_layout(True)
  self.static_canvas_E_hc_tabHE.figure.set_tight_layout(True)
  self.static_canvas_H_Index_tabHE.figure.set_tight_layout(True)
  self.static_canvas_E_Index_tabHE.figure.set_tight_layout(True)
  self.set_aspectRatio(ax=ax_H_hc)
  self.set_aspectRatio(ax=ax_E_hc)
  self.set_aspectRatio(ax=ax_H_Index)
  self.set_aspectRatio(ax=ax_E_Index)
  self.static_canvas_H_hc_tabHE.draw()
  self.static_canvas_E_hc_tabHE.draw()
  self.static_canvas_H_Index_tabHE.draw()
  self.static_canvas_E_Index_tabHE.draw()
