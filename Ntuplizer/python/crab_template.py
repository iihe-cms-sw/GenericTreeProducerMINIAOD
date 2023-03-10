from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'THEREQUESTNAME'
config.General.workArea = 'crabworkarea_14feb2023_Run3data'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'

config.JobType.psetName = 'theconfig.py'
config.JobType.outputFiles = ['output.root']

#To specify run time and memory
#config.JobType.maxJobRuntimeMin = 1000
#config.JobType.maxMemoryMB = 2500
config.JobType.inputFiles = [
'jetfiles',
'*.json',
'RochesterCorrections',
'UnprefireableEventList']
config.Data.inputDataset = 'THEDATASET'

config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
#Next two lines if you want to manually tell crab how many files to run per job
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = NJOBS
config.Data.allowNonValidInputDataset = True 


#config.Data.publication = True
config.Data.publication = False
config.Data.outputDatasetTag = 'CAMPAIGN_RUNERA_THESKIM'
config.Data.partialDataset = True

#Lumi mask to be applied
config.Data.lumiMask = 'GoldenJSON_2016_2017_2018_2022.json'
#If you want to store the output file on a EOS group folder: 
#config.Data.outLFNDirBase = '/store/group/dpg_trigger/comm_trigger/L1Trigger/lathomas/Run3Commissioning'
#config.Site.storageSite = 'T2_CH_CERN'

config.Site.storageSite = 'T2_BE_IIHE'
#config.Site.blacklist = ['T2_US_Vanderbilt','T1_IT_CNAF']
#config.Site.whitelist = ['T1_US_FNAL']
#config.Site.ignoreGlobalBlacklist = True
config.section_("Debug")
config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
config.User.voGroup = 'becms'
