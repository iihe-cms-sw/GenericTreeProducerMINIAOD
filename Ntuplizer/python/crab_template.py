from CRABClient.UserUtilities import config
from time import strftime # for crabworkarea name
config = config()

config.General.requestName = 'THEREQUESTNAME'
config.General.workArea = '../crabsubmission/crabworkarea_' + strftime('%Y%b%d') # Year in decimal, month abreviation, day in decimal
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
'RochesterCorrections']
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
#config.Data.lumiMask = 'GoldenJSON_2016_2017_2018_2022.json'
config.Data.lumiMask = 'GoldenJSON_2016_2017_2018_2022_2023.json'
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
