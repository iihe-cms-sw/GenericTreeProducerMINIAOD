reclusterCHSJets = False
reclusterGenJets = False
usesqlitefiles = True
iscrab = False

skims = ['', 'MCJECs', 'ZJetsResiduals', 'MCJECs', 'HFJet', 'L1Unprefirable', 'L1Study', 'L1Study_ZToMuMu', 'L1Study_ZToEE', 'L1Study_SingleMuforJME', 'L1Studies_EphemeralHLTPhysics,', 'L1Studies_EphemeralZeroBias', 'L1Study_SinglePhotonforJME', 'FourLeptons', 'skimTriggerSOS']
eras = ['DataUL2016', 'DataUL2017', 'DataUL2018', 'DataRun3', 'MCUL2016', 'MCUL2017', 'MCUL2018', 'MCRun3']
datasets = ['', 'SingleMuon', 'Muon', 'DoubleMuon', 'MuonEG', 'SingleElectron', 'SinglePhoton', 'DoubleEG', 'EGamma', 'JetHT', 'MET', 'JetMET', 'Tau', 'ZeroBias', 'HLTPhysics', 'EphemeralZeroBias', 'EphemeralHLTPhysics']

skim = ''
runera = 'MCRun3'

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')
options.register('runera', 'DataRun3', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "run era")
options.register('skim', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "skim")
options.register('dataset', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "dataset")
options.register('inputfiles', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "inputfiles")

options.inputfiles = 'file1.root', 'file2.root'
options.runera = 'DataRun3'
options.maxEvents = -1
options.parseArguments()

runera = options.runera
skim = options.skim
dataset = options.dataset 

if iscrab:
    runera = 'THERUNERA'
    skim = 'THESKIM'
    dataset = 'THEDATASET'.split('/')[1]

print('runera, skim, dataset:', runera, skim, dataset)


#Make sure the skim exists
if skim not in skims: 
    print("Undefined skim")
    exit()

#Make sure the run era exists
find_runera = False
print("runera is ", runera)
for i in eras: 
    if i in runera:
        find_runera = True
if not find_runera:
    print("Undefined era")
    exit()

#Make sure the skim exists
if dataset not in datasets:
    print("Undefined dataset")
    exit()



print("Skim is: ", skim)
print("Era is: ", runera)

ismc = False
if "MC" in runera:
    ismc = True
if not ismc:
    reclusterGenJets = False

if skim == "FourLeptons":
    reclusterCHSJets = False
    reclusterGenJets = False

if skim == "MCJECs":
   reclusterCHSJets = True
   reclusterGenJets = True


import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )  

from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask
patAlgosToolsTask = getPatAlgosToolsTask(process)

lines = []
#with open('inputfiles.txt') as f:
    #lines = f.readlines()
#    lines = ['file:'+line for line in f.readlines()]
    #print(type(lines))

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                options.inputfiles
                            )
                        )

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile) )

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.GlobalTag.globaltag="123X_mcRun3_2021_realistic_v13"

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load('Configuration.StandardSequences.Reconstruction_cff')

chsJetCollectionName = "slimmedJets"
puppiJetCollectionName = "updatedPatJetsUpdatedJECPuppi"

if reclusterCHSJets: 
    chsJetCollectionName ="selectedPatJetsCHS"
else: 
    chsJetCollectionName ="updatedPatJetsUpdatedJEC"
    

if reclusterGenJets:
    GenJetCollectionName="ak4GenJetsNoNuNEW"
else:
    GenJetCollectionName="slimmedGenJets"

EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'

rochesterCorrectionFile="RochesterCorrections/"


#Now UL data
#2016 is divided into two parts
if "DataUL2016B" in runera or "DataUL2016C" in runera or "DataUL2016D" in runera or "DataUL2016E" in runera or "DataUL2016F" in runera:
    process.GlobalTag.globaltag="106X_dataRun2_v32" #UL2016
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2016aUL.txt" 

if "DataUL2016Flate" in runera or "DataUL2016G" in runera or "DataUL2016H" in runera:
    process.GlobalTag.globaltag="106X_dataRun2_v32" #UL2016
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2016bUL.txt" 

if "DataUL2017" in runera:
    process.GlobalTag.globaltag="106X_dataRun2_v32" #UL2017      
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2017UL.txt"

if "DataUL2018" in runera:
    process.GlobalTag.globaltag="106X_dataRun2_v32" #UL2018      
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2018UL.txt"

if "DataRun3" in runera:
    process.GlobalTag.globaltag="124X_dataRun3_Prompt_v10" #Run 3
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2018UL.txt"

#Now UL MC

if "MCUL2016APV" in runera:
    process.GlobalTag.globaltag="106X_mcRun2_asymptotic_preVFP_v11" #2016
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2016aUL.txt"

if "MCUL2016nonAPV" in runera:
    process.GlobalTag.globaltag="106X_mcRun2_asymptotic_v17" #2016
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2016bUL.txt"

if "MCUL2017" in runera:
    process.GlobalTag.globaltag="106X_mc2017_realistic_v8" #UL2017
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2017UL.txt"

if "MCUL2018" in runera:
    process.GlobalTag.globaltag="106X_upgrade2018_realistic_v15" #UL2018
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2018UL.txt" #Muon POG hasn't released Rochester corrections for UL18 yet   

if "MCRun3" in runera:
    process.GlobalTag.globaltag="123X_dataRun3_Prompt_v12"
    EleVetoWP='cutBasedElectronID-Fall17-94X-V2-veto'
    EleTightWP='mvaEleID-Fall17-iso-V2-wp90'
    EleLooseWP='mvaEleID-Fall17-iso-V2-wpHZZ'
    PhotonTightWP='mvaPhoID-RunIIFall17-v2-wp80'
    rochesterCorrectionFile+="RoccoR2018UL.txt"


process.GlobalTag.globaltag="123X_dataRun3_Prompt_v12"
if "MC" in runera:
    process.GlobalTag.globaltag="123X_mcRun3_2021_realistic_v13"

print("Roch corr file: ")
print(rochesterCorrectionFile)

process.ntuplizer = cms.EDAnalyzer('Ntuplizer',
                                   METFiltersPAT = cms.InputTag("TriggerResults::PAT"),
                                   METFiltersRECO = cms.InputTag("TriggerResults::RECO"),
                                   ECALBadCalibFilterUpdate=cms.InputTag("ecalBadCalibReducedMINIAOD2019Filter"),
                                   ECALLaserCorrFilterUpdate=cms.InputTag("ecalLaserCorrFilter"),
                                   ECALDeadCellBoundaryEnergyFilterUpdate=cms.InputTag("ecalDeadCellBoundaryEnergyFilterUpdate"),
                                   BadChargedCandidateFilterUpdate=cms.InputTag("BadChargedCandidateFilterUpdate"),
                                   Vertices=cms.InputTag("offlineSlimmedPrimaryVertices"),
                                   Jets=cms.InputTag(chsJetCollectionName),
                                   JetsAK8=cms.InputTag("selectedPatJetsAK8CHS"),
                                   #JetsPuppi=cms.InputTag("updatedPatJetsUpdatedJECPuppi"),
                                   JetsPuppi=cms.InputTag(puppiJetCollectionName),
                                   JetsPuppiAK8=cms.InputTag("slimmedJetsAK8"),
                                   JetsCalo=cms.InputTag("slimmedCaloJets"),
                                   JetsPFnoCHS=cms.InputTag("selectedPatJetsPlain"),
                                   GenJets=cms.InputTag(GenJetCollectionName),
                                   GenAK8Jets=cms.InputTag("slimmedGenJetsAK8"),
                                   pileupJetIdDiscriminantUpdate = cms.InputTag('pileupJetIdUpdate:fullDiscriminant'),
                                   pileupJetIdDiscriminantUpdate2017 = cms.InputTag('pileupJetIdUpdate2017:fullDiscriminant'),
                                   pileupJetIdDiscriminantUpdate2018 = cms.InputTag('pileupJetIdUpdate2018:fullDiscriminant'),
                                   pileupJetIdVariablesUpdate = cms.InputTag('pileupJetIdUpdate'),
                                   QuarkGluonLikelihood = cms.InputTag('QGTagger:qgLikelihood'),
                                   PFCandidates=cms.InputTag("packedPFCandidates"),
                                   PuppiWeights=cms.InputTag("puppi"),
                                   PULabel = cms.InputTag("slimmedAddPileupInfo"),
                                   Triggers = cms.InputTag("TriggerResults::HLT"),
                                   l1GtSrc = cms.InputTag("gtStage2Digis"),
                                   GenParticles=cms.InputTag("prunedGenParticles"),
                                   GenInfo=cms.InputTag("generator"),
                                   LHELabel = cms.InputTag("externalLHEProducer"),
                                   LHELabelALT = cms.InputTag("source"),
                                   GenJetMatchCHS= cms.InputTag("patJetGenJetMatchUpdate"),
                                   GenJetWithNuMatchCHS= cms.InputTag("patJetGenWithNuJetMatchUpdate"),
                                   GenJetMatchPuppi= cms.InputTag("patJetGenJetMatchUpdatePuppi"),
                                   GenJetWithNuMatchPuppi= cms.InputTag("patJetGenWithNuJetMatchUpdatePuppi"),
                                   GenJetMatchCalo= cms.InputTag("patJetGenJetMatchUpdateCalo"),
                                   PFMet=cms.InputTag("slimmedMETs"),
                                   PuppiMet=cms.InputTag("slimmedMETsPuppi"),
                                   Electrons=cms.InputTag("slimmedElectrons"),
                                   Muons=cms.InputTag("slimmedMuons"),
                                   Taus=cms.InputTag("slimmedTaus"),
                                   Photons=cms.InputTag("slimmedPhotons"),
                                   JetPtCut=cms.double(2),
                                   AK8JetPtCut=cms.double(10),
                                   ElectronPtCut=cms.double(2),
                                   ElectronVetoWorkingPoint=cms.string(EleVetoWP),
                                   ElectronLooseWorkingPoint=cms.string(EleLooseWP),
                                   ElectronTightWorkingPoint=cms.string(EleTightWP),
                                   MuonPtCut=cms.double(1),
                                   TauPtCut=cms.double(1000),
                                   RochCorrFile=cms.string(rochesterCorrectionFile),
                                   PhotonPtCut=cms.double(5),
                                   PhotonTightWorkingPoint=cms.string(PhotonTightWP),
                                   PFCandPtCut=cms.double(25000),
                                   SaveTree=cms.bool(True),
                                   IsMC=cms.bool(ismc),
                                   SaveTaus=cms.bool(False),
                                   SavePUIDVariables=cms.bool(False),
                                   SaveAK8Jets=cms.bool(False),
                                   SaveCaloJets=cms.bool(True),
                                   SavenoCHSJets=cms.bool(True),
                                   DropUnmatchedJets=cms.bool(True),
                                   DropBadJets=cms.bool(False),
                                   SavePFinJets=cms.bool(False),
                                   ApplyPhotonID=cms.bool(False),
                                   Skim=cms.string(skim),
                                   RunEra=cms.string(runera),
                                   Dataset=cms.string(dataset),
                                   Debug=cms.bool(False)
                              )


if skim == "MCJECs":
    process.ntuplizer.JetPtCut=cms.double(-1)
    process.ntuplizer.AK8JetPtCut=cms.double(10)
    process.ntuplizer.SaveAK8Jets=cms.bool(True)
    process.ntuplizer.SaveCaloJets=cms.bool(True)
    process.ntuplizer.SavenoCHSJets=cms.bool(True)
    process.ntuplizer.DropUnmatchedJets=cms.bool(True)

if skim == "ZJetsResiduals" or skim == "GammaJetsResiduals":
    process.ntuplizer.JetPtCut=cms.double(-1)
    process.ntuplizer.AK8JetPtCut=cms.double(1000)
    process.ntuplizer.PhotonPtCut=cms.double(20)
    process.ntuplizer.ElectronPtCut=cms.double(10)
    process.ntuplizer.MuonPtCut=cms.double(10)
    process.ntuplizer.ApplyPhotonID=cms.bool(True)
    process.ntuplizer.SaveAK8Jets=cms.bool(False)
    process.ntuplizer.SaveCaloJets=cms.bool(False)
    process.ntuplizer.SavenoCHSJets=cms.bool(False)
    process.ntuplizer.DropUnmatchedJets=cms.bool(False)
    process.ntuplizer.DropBadJets=cms.bool(True)

if skim == "FourLeptons":
    process.ntuplizer.ElectronPtCut=cms.double(7)
    process.ntuplizer.MuonPtCut=cms.double(5)
    process.ntuplizer.JetPtCut=cms.double(25)
    process.ntuplizer.AK8JetPtCut=cms.double(1000)
    process.ntuplizer.PhotonPtCut=cms.double(2000)
    process.ntuplizer.SaveAK8Jets=cms.bool(False)
    process.ntuplizer.SaveCaloJets=cms.bool(False)
    process.ntuplizer.SavenoCHSJets=cms.bool(False)
    process.ntuplizer.DropUnmatchedJets=cms.bool(False)
    process.ntuplizer.DropBadJets=cms.bool(True)

if skim == "PhotonHFJet" or skim == "HFJet" or skim == "ZHFJet":
    process.ntuplizer.JetPtCut=cms.double(30)
    process.ntuplizer.AK8JetPtCut=cms.double(1000)
    process.ntuplizer.PhotonPtCut=cms.double(20)
    process.ntuplizer.ElectronPtCut=cms.double(10)
    process.ntuplizer.MuonPtCut=cms.double(10)
    process.ntuplizer.ApplyPhotonID=cms.bool(True)
    process.ntuplizer.SaveAK8Jets=cms.bool(False)
    process.ntuplizer.SaveCaloJets=cms.bool(False)
    process.ntuplizer.SavenoCHSJets=cms.bool(False)
    process.ntuplizer.DropUnmatchedJets=cms.bool(False)
    process.ntuplizer.DropBadJets=cms.bool(False)

if skim == "L1Unprefirable":
    process.ntuplizer.JetPtCut=cms.double(20)
    process.ntuplizer.AK8JetPtCut=cms.double(1000)
    process.ntuplizer.PhotonPtCut=cms.double(15)
    process.ntuplizer.ElectronPtCut=cms.double(10)
    process.ntuplizer.MuonPtCut=cms.double(10)
    process.ntuplizer.ApplyPhotonID=cms.bool(False)
    process.ntuplizer.SaveAK8Jets=cms.bool(False)
    process.ntuplizer.SaveCaloJets=cms.bool(False)
    process.ntuplizer.SavenoCHSJets=cms.bool(False)
    process.ntuplizer.DropUnmatchedJets=cms.bool(False)
    process.ntuplizer.DropBadJets=cms.bool(False)

if skim == "L1Study_ZToMuMu" or skim == "L1Study_ZToEE":
    process.ntuplizer.JetPtCut=cms.double(20000)
    process.ntuplizer.AK8JetPtCut=cms.double(20000)
    process.ntuplizer.PhotonPtCut=cms.double(20000)
    process.ntuplizer.ElectronPtCut=cms.double(10)
    process.ntuplizer.MuonPtCut=cms.double(3)
    process.ntuplizer.ApplyPhotonID=cms.bool(False)
    process.ntuplizer.SaveAK8Jets=cms.bool(False)
    process.ntuplizer.SaveCaloJets=cms.bool(False)
    process.ntuplizer.SavenoCHSJets=cms.bool(False)
    process.ntuplizer.DropUnmatchedJets=cms.bool(False)
    process.ntuplizer.DropBadJets=cms.bool(False)
    
if skim == "L1Study_SingleMuforJME" or skim == "L1Study_SinglePhotonforJME":
    process.ntuplizer.JetPtCut=cms.double(20)
    process.ntuplizer.AK8JetPtCut=cms.double(20000)
    process.ntuplizer.PhotonPtCut=cms.double(20)
    process.ntuplizer.ElectronPtCut=cms.double(10)
    process.ntuplizer.MuonPtCut=cms.double(10)
    process.ntuplizer.ApplyPhotonID=cms.bool(False)
    process.ntuplizer.SaveAK8Jets=cms.bool(False)
    process.ntuplizer.SaveCaloJets=cms.bool(False)
    process.ntuplizer.SavenoCHSJets=cms.bool(False)
    process.ntuplizer.DropUnmatchedJets=cms.bool(False)
    process.ntuplizer.DropBadJets=cms.bool(False)
    
#Rerunning the ecalbadcalibration filter
from RecoMET.METFilters.ecalBadCalibFilter_cfi import ecalBadCalibFilter

baddetEcallistnew2019 = cms.vuint32(
    [872439604,872422825,872420274,872423218,872423215,872416066,872435036,872439336,
     872420273,872436907,872420147,872439731,872436657,872420397,872439732,872439339,
     872439603,872422436,872439861,872437051,872437052,872420649,872421950,872437185,
     872422564,872421566,872421695,872421955,872421567,872437184,872421951,872421694,
     872437056,872437057,872437313,872438182,872438951,872439990,872439864,872439609,
     872437181,872437182,872437053,872436794,872436667,872436536,872421541,872421413,
     872421414,872421031,872423083,872421439,872423224,872421438,872420397,872421566,
     872422589,872423096,872422717,872423214,872421415,872422311,872421926,872439469,
     872438567,872436659,872439731,872438311,872438078,872438438,872439601,872437951,
     872437950,872439729,872436792,872438183,872439468,872436663,872439728,872439727,
     872437694,872437823,872438845,872438973,872439354,872438566,872439733,872436530,
     872436655,872439600,872439730]
    )

process.ecalBadCalibReducedMINIAOD2019Filter = ecalBadCalibFilter.clone(
    EcalRecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
    ecalMinEt        = cms.double(50.),
    baddetEcal    = baddetEcallistnew2019,
    taggingMode = cms.bool(True),
    debug = cms.bool(False)
    )

#Rerunning the laser correction filter
process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')
process.ecalLaserCorrFilter = cms.EDFilter(
    "EcalLaserCorrFilter",
    EBRecHitSource = cms.InputTag("reducedEgamma:reducedEBRecHits"),
    EERecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
    EBLaserMIN     = cms.double(0.3),
    EELaserMIN     = cms.double(0.3),
    EBLaserMAX     = cms.double(5.0), #this was updated wrt default
    EELaserMAX     = cms.double(100.0), #this was updated wrt default
    EBEnegyMIN     = cms.double(10.0),
    EEEnegyMIN     = cms.double(10.0),
    taggingMode    = cms.bool(True), #updated wrt default
    Debug          = cms.bool(False)
    )

#Rerunning EcalDeadCellBoundaryEnergyFilter
from RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi import EcalDeadCellBoundaryEnergyFilter
process.ecalDeadCellBoundaryEnergyFilterUpdate=EcalDeadCellBoundaryEnergyFilter.clone(
    recHitsEB = cms.InputTag("reducedEgamma:reducedEBRecHits"),
    recHitsEE = cms.InputTag("reducedEgamma:reducedEERecHits"),
    cutBoundEnergyDeadCellsEE=cms.untracked.double(10),
    taggingMode    = cms.bool(True)
    )

#Rerunning BadChargedCandidateFilter
from RecoMET.METFilters.BadChargedCandidateFilter_cfi import BadChargedCandidateFilter 
process.BadChargedCandidateFilterUpdate=BadChargedCandidateFilter.clone(
    muons = cms.InputTag("slimmedMuons"),
    PFCandidates = cms.InputTag("packedPFCandidates"),
    vtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
    taggingMode    = cms.bool(True)
)



import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())


JSONfile ='GoldenJSON_2016_2017_2018_2022.json'
#JSONfile ='Cert_Fill8456.json'
myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
#if not ismc:
#    process.source.lumisToProcess.extend(myLumis)

print( "json" )
print( JSONfile )

if "MCUL2016APV" in runera:
    JECsVersion = 'Summer19UL16APV_V7_MC'
if "MCUL2016nonAPV" in runera:
    JECsVersion = 'Summer19UL16_V7_MC'
if "MCUL2017" in runera:
    JECsVersion = 'Summer19UL17_V6_MC'
if "MCUL2018" in runera:
    JECsVersion = 'Summer19UL18_V5_MC'
if "MCRun3" in runera:
    JECsVersion = 'Summer19UL18_V5_MC'

if "DataUL2017B" in runera:
    JECsVersion = 'Summer19UL17_RunB_V6_DATA'
if "DataUL2017C" in runera:
    JECsVersion = 'Summer19UL17_RunC_V6_DATA'
if "DataUL2017D" in runera:
    JECsVersion = 'Summer19UL17_RunD_V6_DATA'
if "DataUL2017E" in runera:
    JECsVersion = 'Summer19UL17_RunE_V6_DATA'
if "DataUL2017F" in runera:
    JECsVersion = 'Summer19UL17_RunF_V6_DATA'

if "DataUL2018A" in runera:
    JECsVersion = 'Summer19UL18_RunA_V5_DATA'
if "DataUL2018B" in runera:
    JECsVersion = 'Summer19UL18_RunB_V5_DATA'
if "DataUL2018C" in runera:
    JECsVersion = 'Summer19UL18_RunC_V5_DATA'
if "DataUL2018D" in runera:
    JECsVersion = 'Summer19UL18_RunD_V5_DATA'

if "DataUL2016B" in runera:
    JECsVersion = 'Summer19UL16APV_RunBCD_V7_DATA'
if "DataUL2016C" in runera:
    JECsVersion = 'Summer19UL16APV_RunBCD_V7_DATA'
if "DataUL2016D" in runera:
    JECsVersion = 'Summer19UL16APV_RunBCD_V7_DATA'
if "DataUL2016E" in runera:
    JECsVersion = 'Summer19UL16APV_RunEF_V7_DATA'
if "DataUL2016F" in runera:
    JECsVersion = 'Summer19UL16APV_RunEF_V7_DATA'
if "DataUL2016Flate" in runera:
    JECsVersion = 'Summer19UL16_RunFGH_V7_DATA'
if "DataUL2016G" in runera:
    JECsVersion = 'Summer19UL16_RunFGH_V7_DATA'
if "DataUL2016H" in runera:
    JECsVersion = 'Summer19UL16_RunFGH_V7_DATA'
 
if "DataRun3" in runera:
    JECsVersion = 'Winter22Run3_RunA_V1_DATA'


sqlitefile = 'sqlite:jetfiles/'+JECsVersion+'.db'

TagForAK4CHSJet='JetCorrectorParametersCollection_'+JECsVersion+'_AK4PFchs'
TagForAK4PuppiJet='JetCorrectorParametersCollection_'+JECsVersion+'_AK4PFPuppi'

from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup


process.jec = cms.ESSource('PoolDBESSource',
                           CondDBSetup,
                           connect = cms.string(sqlitefile),
                           toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string(TagForAK4CHSJet),
            label  = cms.untracked.string('AK4PFchs')
            ),
        cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string(TagForAK4PuppiJet),
            label  = cms.untracked.string('AK4PFPuppi')
            ) 
        )
                           )

# Add an ESPrefer to override JEC that might be available from the global tag
if usesqlitefiles:
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')
else:
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'GlobalTag')


JERVersion = ''

if "MC2018" in runera:
    JERVersion = 'Autumn18_V7b_MC'
if "MC2017" in runera:
    JERVersion = 'Fall17_V3b_MC'
if "MC2016" in runera:
    JERVersion = 'Summer16_25nsV1b_MC'
if "MCUL2016" in runera:
    JERVersion = 'Summer16_25nsV1b_MC'

if "Data2018" in runera:
    JERVersion = 'Autumn18_V7b_DATA'
if "Data2017" in runera:
    JERVersion = 'Fall17_V3b_DATA'
if "Data2016" in runera or "DataUL2016" in runera:
    JERVersion = 'Summer16_25nsV1b_DATA'



if "MCUL2017" in runera:
    JERVersion = 'Summer19UL17_JRV3_MC'
if "DataUL2017" in runera:
    JERVersion = 'Summer19UL17_JRV3_DATA'

if "MCUL2018" in runera:
    JERVersion = 'Summer19UL18_JRV2_MC'
if "DataUL2018" in runera:
    JERVersion = 'Summer19UL18_JRV2_DATA'

if "MCRun3" in runera:
    JERVersion = 'Summer19UL18_JRV2_MC'
if "DataRun3" in runera:
    JERVersion = 'Summer19UL18_JRV2_DATA'


if "MCUL2016APV" in runera:
    JERVersion = 'Summer20UL16APV_JRV3_MC'
if "MCUL2016nonAPV" in runera:
    JERVersion = 'Summer20UL16_JRV3_MC'

if "DataUL2016B" in runera:
    JERVersion = 'Summer20UL16APV_JRV3_DATA'
if "DataUL2016C" in runera:
    JERVersion = 'Summer20UL16APV_JRV3_DATA'
if "DataUL2016D" in runera:
    JERVersion = 'Summer20UL16APV_JRV3_DATA'
if "DataUL2016E" in runera:
    JERVersion = 'Summer20UL16APV_JRV3_DATA'
if "DataUL2016F" in runera:
    JERVersion = 'Summer20UL16APV_JRV3_DATA'
if "DataUL2016Flate" in runera:
    JERVersion = 'Summer20UL16_JRV3_DATA'
if "DataUL2016G" in runera:
    JERVersion = 'Summer20UL16_JRV3_DATA'
if "DataUL2016H" in runera:
    JERVersion = 'Summer20UL16_JRV3_DATA'


sqlitefileJER='sqlite:jetfiles/'+JERVersion+'.db'


print(sqlitefileJER)
process.jer = cms.ESSource("PoolDBESSource",
                           CondDBSetup,
                           toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('JetResolutionRcd'),
            tag    = cms.string('JR_'+JERVersion+'_PtResolution_AK4PFchs'),
            label  = cms.untracked.string('AK4PFchs_pt')
            ),
        cms.PSet(
            record = cms.string('JetResolutionScaleFactorRcd'),
            tag    = cms.string('JR_'+JERVersion+'_SF_AK4PFchs'),
            label  = cms.untracked.string('AK4PFchs')
            ),
#        cms.PSet(                                                                                                                                                                                            
#            record = cms.string('JetResolutionRcd'),                                                                                                                                                         
#            tag    = cms.string('JR_'+JERVersion+'_PtResolution_AK4PFPuppi'),
#            label  = cms.untracked.string('AK4PFPuppi_pt')                                                                                                                                                   
#            ),                                                                                                                                                                                               
#        cms.PSet(                                                                                                                                                                                            
#            record = cms.string('JetResolutionScaleFactorRcd'),                                                                                                                                              
#            tag    = cms.string('JR_'+JERVersion+'_SF_AK4PFPuppi'),                                                                                                                                    
#            label  = cms.untracked.string('AK4PFPuppi')                                                                                                                                                      
#            ),                                                                                                                                                                                               
        ),
                           connect = cms.string(sqlitefileJER)
                           )

if usesqlitefiles: 
    process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')
else:
    process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'GlobalTag')


from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    labelName = 'UpdatedJEC',
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None')  
)

updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJetsPuppi'),
    labelName = 'UpdatedJEC',
    postfix = 'Puppi',
    jetCorrections = ('AK4PFPuppi', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None') 
)
process.jecSequence = cms.Sequence(process.patJetCorrFactorsUpdatedJEC * process.updatedPatJetsUpdatedJEC * process.patJetCorrFactorsUpdatedJECPuppi * process.updatedPatJetsUpdatedJECPuppi)


#recluster gen jets
## Filter out neutrinos from packed GenParticles 
#The filter on pdgid 2101, 2103, 2203 and 1103 should be harmless for standard samples. I added it because some private samples mistakenly added those unstable states as stable products. 
process.packedGenParticlesForJetsNoNuNEW = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16 && abs(pdgId) != 2101 &&abs(pdgId) != 2103 && abs(pdgId) != 2203  && abs(pdgId) != 1103 "))
process.packedGenParticlesForJetsWithNuNEW = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 2101 &&abs(pdgId) != 2103 && abs(pdgId) != 2203  && abs(pdgId) != 1103 "))
## Define GenJets 
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsNoNuNEW = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNuNEW')
process.ak4GenJetsWithNuNEW = ak4GenJets.clone(src = 'packedGenParticlesForJetsWithNuNEW')
#I didn't manage to create a new jet collection on top of MINIAOD with the matching to this updated gen jet collection   
#Work around: do the matching by hand                                                                                                                                                                                       
#Now redo the matching. The patJetGenJetMatch produces a matching between the gen jets and the reco jets. 
from PhysicsTools.PatAlgos.mcMatchLayer0.jetMatch_cfi import patJetGenJetMatch

process.patJetGenJetMatchUpdate = patJetGenJetMatch.clone(
src         = cms.InputTag(chsJetCollectionName),
matched     = cms.InputTag("ak4GenJetsNoNuNEW")
)
process.patJetGenJetMatchUpdatePuppi = patJetGenJetMatch.clone(
src         = cms.InputTag("slimmedJetsPuppi"),
matched     = cms.InputTag("ak4GenJetsNoNuNEW")
)
process.patJetGenWithNuJetMatchUpdate = patJetGenJetMatch.clone(
src         = cms.InputTag(chsJetCollectionName),
matched     = cms.InputTag("ak4GenJetsWithNuNEW")
)
process.patJetGenWithNuJetMatchUpdatePuppi = patJetGenJetMatch.clone(
src         = cms.InputTag("slimmedJetsPuppi"),
matched     = cms.InputTag("ak4GenJetsWithNuNEW")
)
process.patJetGenJetMatchUpdateCalo = patJetGenJetMatch.clone(
src         = cms.InputTag("slimmedCaloJets"),
matched     = cms.InputTag("ak4GenJetsNoNuNEW")
)



#Update MET
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

#Recompute PFMET (with updated JECs)

if skim == "MCJECs":

    runMetCorAndUncFromMiniAOD (
        process,
        isData = not ismc
    )



'''
#Rerunning PUPPI (standard approach, default tuning)
from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
makePuppiesFromMiniAOD( process, True );
#Set to false if you want to recompute PUPPI weights
process.puppiNoLep.useExistingWeights = True
process.puppi.useExistingWeights = True

#Recompute PUPPI MET (with updated JECs and possibly updated PUPPI weights)
runMetCorAndUncFromMiniAOD(process,
                           jetCollUnskimmed="updatedPatJetsUpdatedJECPuppi",
                           isData= not ismc,
                           metType="Puppi",
                           postfix="Puppi",
                           jetFlavor="AK4PFPuppi",
                           reapplyJEC = False
                           )
'''



from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection

#Rerunning PUPPi with v15 tune
'''
process.ak4PuppiJets  = ak4PFJets.clone (src = 'puppi', doAreaFastjet = True, jetPtMin = 2.)
addJetCollection(process,labelName = 'Puppi', jetSource = cms.InputTag('ak4PuppiJets'), algo = 'AK', rParam=0.4, genJetCollection=cms.InputTag(GenJetCollectionName), jetCorrections = ('AK4PFPuppi', ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual'], 'None'),pfCandidates = cms.InputTag('packedPFCandidates'),
                 pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
                 svSource = cms.InputTag('slimmedSecondaryVertices'),
                 muSource =cms.InputTag( 'slimmedMuons'),
                 elSource = cms.InputTag('slimmedElectrons'),
                 genParticles= cms.InputTag('prunedGenParticles'),
                 getJetMCFlavour=ismc
)

process.patJetsPuppi.addGenPartonMatch = cms.bool(ismc)
process.patJetsPuppi.addGenJetMatch = cms.bool(ismc)

from CommonTools.PileupAlgos.customizePuppiTune_cff import UpdatePuppiTuneV15

patAlgosToolsTask.add(process.ak4PuppiJets)
UpdatePuppiTuneV15(process,ismc)
'''

#Now doing PF jets (not CHS). Those are not in MINIAOD
process.ak4PFJetsBis  = ak4PFJets.clone (src = 'packedPFCandidates', doAreaFastjet = True, jetPtMin = 2.)
patAlgosToolsTask.add(process.ak4PFJetsBis)
addJetCollection(process,labelName = 'Plain', jetSource = cms.InputTag('ak4PFJetsBis'), algo = 'AK', rParam=0.4, genJetCollection=cms.InputTag(GenJetCollectionName), jetCorrections = ('AK4PF', ['L1FastJet','L2Relative', 'L3Absolute','L2L3Residual'], 'None'),pfCandidates = cms.InputTag('packedPFCandidates'),
                 pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
                 svSource = cms.InputTag('slimmedSecondaryVertices'),
                 muSource =cms.InputTag( 'slimmedMuons'),
                 elSource = cms.InputTag('slimmedElectrons'),
                 genParticles= cms.InputTag('prunedGenParticles'),
                 getJetMCFlavour=ismc
)
process.patJetsPlain.addGenPartonMatch = cms.bool(ismc)
process.patJetsPlain.addGenJetMatch = cms.bool(ismc)


#recluster CHS jets to go lower in pt
if reclusterCHSJets:
    process.ak4PFJetsCHSBis  = ak4PFJets.clone (src = 'pfCHS', doAreaFastjet = True, jetPtMin = 2.)
    patAlgosToolsTask.add(process.ak4PFJetsCHSBis)
    addJetCollection(process,labelName = 'CHS', jetSource = cms.InputTag('ak4PFJetsCHSBis'), algo = 'AK', rParam=0.4, genJetCollection=cms.InputTag(GenJetCollectionName), jetCorrections = ('AK4PFchs', ['L1FastJet','L2Relative', 'L3Absolute','L2L3Residual'], 'None'),pfCandidates = cms.InputTag('pfCHS'),
                     pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
                     svSource = cms.InputTag('slimmedSecondaryVertices'),
                     muSource =cms.InputTag( 'slimmedMuons'),
                     elSource = cms.InputTag('slimmedElectrons'),
                     genParticles= cms.InputTag('prunedGenParticles'),
                     getJetMCFlavour=ismc
                     )
    process.patJetsCHS.addGenPartonMatch = cms.bool(ismc)
    process.patJetsCHS.addGenJetMatch = cms.bool(ismc)

    #Now AK8 CHS
    from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJets
    process.ak8PFJetsCHSBis  = ak8PFJets.clone (src = 'pfCHS', doAreaFastjet = True, jetPtMin = 10.)
    patAlgosToolsTask.add(process.ak8PFJetsCHSBis)
    addJetCollection(process,labelName = 'AK8CHS', jetSource = cms.InputTag('ak8PFJetsCHSBis'), algo = 'AK', rParam=0.8, genJetCollection=cms.InputTag('slimmedGenJetsAK8'), jetCorrections = ('AK8PFchs', ['L1FastJet','L2Relative', 'L3Absolute','L2L3Residual'], 'None'),pfCandidates = cms.InputTag('pfCHS'),
                     pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
                     svSource = cms.InputTag('slimmedSecondaryVertices'),
                     muSource =cms.InputTag( 'slimmedMuons'),
                     elSource = cms.InputTag('slimmedElectrons'),
                     genParticles= cms.InputTag('prunedGenParticles'),
                     getJetMCFlavour=ismc
                     )
    process.patJetsAK8CHS.addGenPartonMatch = cms.bool(ismc)
    process.patJetsAK8CHS.addGenJetMatch = cms.bool(ismc)
#The produced collection is called selectedPatJetsAK8CHS 



#Recompute pile up ID
from RecoJets.JetProducers.PileupJetID_cfi import  _chsalgos_81x, _chsalgos_94x, _chsalgos_102x
process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdUpdate = process.pileupJetId.clone()
process.pileupJetIdUpdate.jets = cms.InputTag(chsJetCollectionName)
process.pileupJetIdUpdate.inputIsCorrected = True
process.pileupJetIdUpdate.applyJec = False
process.pileupJetIdUpdate.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pileupJetIdUpdate.algos = cms.VPSet(_chsalgos_81x) 


process.pileupJetIdUpdate2017 = process.pileupJetId.clone()
process.pileupJetIdUpdate2017.jets = cms.InputTag(chsJetCollectionName)
process.pileupJetIdUpdate2017.inputIsCorrected = True
process.pileupJetIdUpdate2017.applyJec = False
process.pileupJetIdUpdate2017.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pileupJetIdUpdate2017.algos = cms.VPSet(_chsalgos_94x)

process.pileupJetIdUpdate2018 = process.pileupJetId.clone()
process.pileupJetIdUpdate2018.jets = cms.InputTag(chsJetCollectionName)
process.pileupJetIdUpdate2018.inputIsCorrected = True
process.pileupJetIdUpdate2018.applyJec = False
process.pileupJetIdUpdate2018.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pileupJetIdUpdate2018.algos = cms.VPSet(_chsalgos_102x)


#Compute QGL 
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets          = cms.InputTag(chsJetCollectionName)
process.QGTagger.jetsLabel        = cms.string('QGL_AK4PFchs')   


#


'''
eraforEGMSmearing=''

if "UL2017" in runera or "UL2018" in runera:
    if "UL2017" in runera:
        eraforEGMSmearing='2017-UL'
    if "UL2018" in runera:
        eraforEGMSmearing='2018-UL'
    if "UL2016B" in runera or "UL2016C" in runera or "UL2016D" in runera or "UL2016E" in runera or "UL2016F" in runera  or "UL2016APV" in runera :
        eraforEGMSmearing='2016-UL-preVFP'
    if "UL2016Flate" in runera or "UL2016G" in runera or "UL2016H" in runera  or "UL2016nonAPV" in runera :
        eraforEGMSmearing='2016-UL-postVFP'
    from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
    setupEgammaPostRecoSeq(process,
                           runVID=False, #saves CPU time by not needlessly re-running VID, if you want the Fall17V2 IDs, set this to True or remove (default is True)
                           era=eraforEGMSmearing)    
    process.ApplyEGMScaleSmearing=cms.Path(process.egammaPostRecoSeq)


from RecoMET.METFilters.primaryVertexFilter_cfi import primaryVertexFilter
'''

#process.applyjecs =  cms.Path( process.jecSequence )
if ismc and reclusterGenJets: 
    process.reclustergenjets = cms.Path(process.packedGenParticlesForJetsNoNuNEW * process.packedGenParticlesForJetsWithNuNEW *process.ak4GenJetsNoNuNEW * process.ak4GenJetsWithNuNEW * process.patJetGenJetMatchUpdate *process.patJetGenJetMatchUpdatePuppi  * process.patJetGenWithNuJetMatchUpdate  * process.patJetGenWithNuJetMatchUpdatePuppi *process.patJetGenJetMatchUpdateCalo)


#You may want to comment out some of the following lines to speed things up
process.ApplyPatAlgos  = cms.Path(process.patAlgosToolsTask)

#process.rerunmetfilters = cms.Path( process.ecalBadCalibReducedMINIAOD2019Filter * process.ecalLaserCorrFilter * process.ecalDeadCellBoundaryEnergyFilterUpdate * process.BadChargedCandidateFilterUpdate ) 
#process.computepuid = cms.Path(process.pileupJetIdUpdate  * process.pileupJetIdUpdate2017 * process.pileupJetIdUpdate2018)
#process.computeqgl = cms.Path(process.QGTagger)

#This one obviously shouldn't be commented out
process.endpath = cms.EndPath( process.ntuplizer  )



