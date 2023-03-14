# Instructions
```
cmsrel CMSSW_12_4_8
cd CMSSW_12_4_8/src
cmsenv
git cms-addpkg RecoMET/METFilters
git clone https://github.com/iihe-cms-sw/MacrosNtuples.git 
scram b -j4
```
To run the code: 
```
cmsRun GenericTreeProducerMINIAOD/Ntuplizer/python/ntuplizer.py --inputfiles=file_input.root --outputfile=file_output.root --runera=RUNERA --dataset=DATASET --skim=SKIM
```
You can check the available run era/dataset/skim here:
https://github.com/iihe-cms-sw/GenericTreeProducerMINIAOD/blob/main/Ntuplizer/python/ntuplizer.py#L6-L8


To get the EGM scaling/smearing correction (enabled by default), the following is also needed, as instructed in:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018
```
git cms-addpkg RecoEgamma/EgammaTools  ### essentially just checkout the package from CMSSW
git clone https://github.com/cms-egamma/EgammaPostRecoTools.git
mv EgammaPostRecoTools/python/EgammaPostRecoTools.py RecoEgamma/EgammaTools/python/.
git clone -b ULSSfiles_correctScaleSysMC https://github.com/jainshilpi/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data/
git cms-addpkg EgammaAnalysis/ElectronTools
scram b -j 4
```

You can make test with a local input file currently on lxplus: 
```
'file:/afs/cern.ch/work/l/lathomas/public/qcdht1000to1500_1.root'
```

For that file, please set
```
runEra=MCUL2017
```

One can send jobs through crabs by using the SubmitToCrab.sh. For example:
```
sh SubmitToCrab_NEW.sh /SingleMuon/Run2022C-PromptReco-v1/MINIAOD  singlemu_4l_2022c 2 FourLeptons  DataRun3 
```
Arguments are (in that order):
 
- dataset name
- local folder for crab
- files per job
- skim name
- run era (for reapplying JECs etc)
