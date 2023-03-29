#for dataset in "Cv1" "Dv1" "Dv2" "Ev1" "Fv1" "Gv1"
for dataset in "Gv1"
do
    sh SubmitToCrab_NEW.sh /Muon/Run2022${dataset:0:1}-PromptReco-v${dataset:2:1}/MINIAOD muon_zmumu_2022"$dataset" 1 L1Study_ZToMuMu DataRun3
    sh SubmitToCrab_NEW.sh /Muon/Run2022${dataset:0:1}-PromptReco-v${dataset:2:1}/MINIAOD muon_mujet_2022$dataset 1 L1Study_SingleMuforJME DataRun3
    sh SubmitToCrab_NEW.sh /EGamma/Run2022${dataset:0:1}-PromptReco-v${dataset:2:1}/MINIAOD eg_zee_2022$dataset 1 L1Study_ZToEE DataRun3
    sh SubmitToCrab_NEW.sh /EGamma/Run2022${dataset:0:1}-PromptReco-v${dataset:2:1}/MINIAOD eg_photonjet_2022$dataset 1 L1Study_SinglePhotonforJME DataRun3

    case $dataset in
        "Cv1")
            # First half of 2022C is in a different dataset
            sh SubmitToCrab_NEW.sh /SingleMuon/Run2022C-PromptReco-v1/MINIAOD muon_zmumu_2022Cv1_begin 1 L1Study_ZToMuMu DataRun3
            sh SubmitToCrab_NEW.sh /SingleMuon/Run2022C-PromptReco-v1/MINIAOD muon_mujet_2022Cv1_begin 1 L1Study_SingleMuforJME DataRun3
            ;;
        *)
            ;;
    esac

done


