#! /bin/bash
# TODO check for _additional, _ext flags !
# ./compareNumberNTuples.sh -x xmls_postMoriond -t /pnfs/psi.ch/cms/trivcat/store/user/ytakahas/Ntuple_80_reminiAOD/ -t /pnfs/psi.ch/cms/trivcat/store/user/ineuteli/Ntuple_80_20170303/ -s SingleElectron -s SingleMuon
#

echo
echo ">>> comparing stored root files to those listed in xml files"
BASEDIR="." #"/shome/$USER/analysis/SFrameAnalysis_Moriond/BatchSubmission"
XMLDIR="xmls_postMoriond_T2"
SITES_T3=(
    /pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring16/Ntuple_80_08022017 # data
    /pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203
    /pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170206 
    /pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170207
    #/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/Ntuple_80_reminiAOD/              # SingleMuon
    /pnfs/psi.ch/cms/trivcat/store/user/ytakahas/Ntuple_80_reminiAOD_v2/           # SingleMuon
    /pnfs/psi.ch/cms/trivcat/store/user/ytakahas/Ntuple_80_reminiAOD_v3/           # SingleMuon
    /pnfs/psi.ch/cms/trivcat/store/user/ineuteli/Ntuple_80_20170303/               # SingleElectron
)
SITES_T2=(
    #gsiftp://storage01.lcg.cscs.ch/
    /pnfs/lcg.cscs.ch/cms/trivcat/store/user/ytakahas/Ntuple_postMoriond_v5
    #/pnfs/lcg.cscs.ch/cms/trivcat/store/user/ytakahas/Ntuple_postMoriond_v3
    /pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_Moriond17
    /pnfs/lcg.cscs.ch/cms/trivcat/store/user/zucchett/Ntuple_Moriond17
)


SAMPLES=(
    
#     SingleMuon
#     SingleElectron
    
    TT_TuneCUE
    WJetsToLNu_TuneCUETP8M1_13TeV-madgraph
    W1JetsToLNu_TuneCUETP8M1_13TeV-madgraph
    W2JetsToLNu_TuneCUETP8M1_13TeV-madgraph
    W3JetsToLNu_TuneCUETP8M1_13TeV-madgraph
    W4JetsToLNu_TuneCUETP8M1_13TeV-madgraph
    DYJetsToLL_M-10to50_TuneCUETP8M1
    DY1JetsToLL_M-10to50_TuneCUETP8M1
    DY2JetsToLL_M-10to50_TuneCUETP8M1
    DY3JetsToLL_M-10to50_TuneCUETP8M1
    DYJetsToLL_M-50_TuneCUETP8M1
    DY1JetsToLL_M-50_TuneCUETP8M1
    DY2JetsToLL_M-50_TuneCUETP8M1
    DY3JetsToLL_M-50_TuneCUETP8M1
    WWTo1L1Nu2Q_13TeV_amcatnlo
    WZTo2L2Q_13TeV_amcatnlo
    WZTo3LNu_TuneCUETP8M1_13TeV-amcatnlo
    WZ_TuneCUETP8M1_13TeV-pythia8
    ZZTo2Q2Nu_13TeV_amcatnlo
    ZZTo4L_13TeV_powheg
    ZZTo4Q_13TeV_amcatnlo
    ZZTo4L_13TeV-amcatnlo
    ZZ_TuneCUETP8M1_13TeV-pythia8
    VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8
    ST_s-channel_4f_leptonDecays
    ST_t-channel_antitop_4f
    ST_t-channel_top_4f_inclusive
    ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV
    ST_tW_antitop_5f_inclusiveDecays_13TeV
    ST_tW_top_5f_NoFullyHadronicDecays_13TeV
    ST_tW_top_5f_inclusiveDecays_13TeV
        
#     DYJetsToLL_M-50_HT
#     DYJetsToLL_M-5to50_HT
#     DYJetsToLL_Pt
#     DYJetsToNuNu_PtZ
#     TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg
#     TTToSemilepton
#     TTJets_HT
#     WJetsToLNu_HT
#     WJetsToLNu_TuneCUETP8M1_13TeV-amcatnlo
#     WJetsToQQ_HT
#     ZJetsToNuNu_HT
#     
#     EWKWMinus2Jets
#     EWKWPlus2Jets
#     EWKZ2Jets_ZToLL
#     EWKWPlus2Jets_WToLNu
#     TTWJetsToLNu
#     TTZToLLNuNu
#     
#     GluGluHToTauTau_M125_13TeV_powheg
#     GluGluHToBB_M125_13TeV_amcatnlo
#     VBFHToTauTau
#     WH_HToBB_WToLNu
#     ZHToTauTau
#     ZH_HToBB_ZToLL
#     ZH_HToBB_ZToNuNu
#     ZH_HToBB_ZToQQ
#     WminusHToTauTau
#     WplusHToTauTau
#     
#     GluGluToRadionToHHTo2B2Tau_M
#     RadionTohhTohtatahbb_narrow_M
#     WprimeToWhToWhadhtata_narrow_M
#     WprimeToWhToWhadhbb_narrow_M
#     WprimeToWhToWlephbb_narrow_M
#     ZprimeToZhToZhadhbb_narrow_M
#     ZprimeToZhToZinvhbb_narrow_M
#     ZprimeToZhToZlephbb_narrow_M
#     BulkGravTohhTohtatahbb_narrow_M
)



# USER OPTIONS
# TODO: http://stackoverflow.com/a/39754944/5499028
# TODO: verbose mode: print dirs, xml files, duplicate lines
# TODO: option to add own pnfs site
SAMPLES_USER=( )
SITES_USER=( )
VERBOSITY=0
WARNING="\e[31m\e[1mWARNING!" # yellow/orange \e[93m
E="\e[0m"
while getopts b:d:x:s:p:t:u:v option; do
    case "${option}"
    in
        b) BASEDIR=${OPTARG};;
        d) XMLDIR=${OPTARG};;
        x) XMLDIR=${OPTARG};;
        s) SAMPLES_USER+=(${OPTARG});;
        p) SITES_USER+=(${OPTARG});;
        t) SITES_USER+=(${OPTARG});;
        u) SITES_USER+=(${OPTARG});;
        v) VERBOSITY=1;;
    esac
done
[[ $SAMPLES_USER ]] && SAMPLES=( ${SAMPLES_USER[@]} )

SITES_T3_USER=( )
SITES_T2_USER=( )
for site in ${SITES_USER[@]}; do
    if   echo $site | grep -q "psi.ch/cms/trivcat/store";      then SITES_T3_USER+=($site)
    elif echo $site | grep -q "lcg.cscs.ch/cms/trivcat/store"; then SITES_T2_USER+=($site)
    else echo ">>> ${WARNING} User site not recognized! $A"
    fi
done

CHECK_SITE=0
([[ $SITES_T2_USER ]] || [[ $SITES_T3_USER ]]) && SITES_T2=( ${SITES_T2_USER[@]} ) &&
                                                  SITES_T3=( ${SITES_T3_USER[@]} ) &&
                                                  CHECK_SITE=1


# LOOP over samples
cd $BASEDIR
for sample in ${SAMPLES[@]}; do
    
    
    # HEADER
    HEADER="$sample"
    BAR=`printf '#%.0s' $(seq 1 ${#HEADER})`
    echo ">>> "
    echo ">>> "
    echo ">>>     ####${BAR}####"
    echo ">>>     #   $HEADER   #"
    echo ">>>     ####${BAR}####"
    #echo ">>> "
    
    # replace * by .* wildcard to use with grep:
    sample_dotted=`echo $sample | sed 's/*/.*/'`
    
    # LOOP over PNFS sites on Tier 3
    for site in ${SITES_T3[@]}; do
        if ls $site | grep -q ^$sample_dotted; then
            echo ">>> "
            echo ">>> sample found in ${site}:"
            nFiles=0
            nFilesTot=0
            for fullsample in `ls ${site} | grep ${sample_dotted}`; do            
                nFiles=`ls ${site}/${fullsample}/*/*/* | grep .root | wc -l`
                nDirs=`ls ${site}/${fullsample}/*/* | wc -l`
                nFilesTot=$(($nFilesTot+$nFiles))
                printf ">>>  \e[1m%5s \e[0mfiles in %2s directories %s\n" "$nFiles" "$nDirs" "$fullsample"
            done
            (( $nFilesTot > $nFiles )) && printf ">>>  \e[1m%5s \e[0mfiles in total\n" "$nFilesTot"
        elif [[ $CHECK_SITE > 0 ]]; then
            echo ">>> "
            echo ">>> sample not found in ${site}"
        fi
    done
    
    
    # LOOP over PNFS sites on Tier 2
    for site in ${SITES_T2[@]}; do
        echo $site | grep -q -v "gsiftp://storage01.lcg.cscs.ch/" && site="gsiftp://storage01.lcg.cscs.ch/$site"
        if uberftp -ls $site | awk '{print $9}' | grep -q ^$sample_dotted; then
            echo ">>> "
            echo ">>> sample found in ${site}:"
            nFiles=0
            nFilesTot=0
            for fullsample in `uberftp -ls ${site} | awk '{print $9}' | grep ${sample_dotted} | xargs echo`; do
                fullsample=${fullsample:0:${#fullsample}-1} # some weird character at the end
                nFiles=`uberftp -ls ${site}/${fullsample}/*/*/* | grep .root | wc -l`
                nDirs=`uberftp -ls ${site}/${fullsample}/*/* | wc -l`
                nFilesTot=$(($nFilesTot+$nFiles))
                printf ">>>  \e[1m%5s \e[0mfiles in %2s directories of  %s\n" "$nFiles" "$nDirs" "$fullsample"
            done
            (( $nFilesTot > $nFiles )) && printf ">>>  \e[1m%5s \e[0mfiles in total\n" "$nFilesTot"
        elif [[ $CHECK_SITE > 0 ]]; then
            echo ">>> "
            echo ">>> sample not found in ${site}"
        fi
    done

    
    # CHECK XML files
    echo ">>> "
    if ls $XMLDIR | grep -q $sample_dotted; then
        echo ">>> sample found in ${XMLDIR}:"
        nFiles=`cat $XMLDIR/${sample}*.xml | grep .root | wc -l`
        nDuplicates=`cat $XMLDIR/${sample}*.xml | grep -o "${sample_dotted}.*/flatTuple_.*.root" | uniq -cd | wc -l`
        nXMLFiles=`ls $XMLDIR/${sample}*.xml | wc -l`
        
        # COUNT number of events
        NTOT=0
        NEVENTS=0
        for f in `ls ${XMLDIR}/${sample}*.xml | awk -F '/' '{print $NF}'`; do
          NEVENTS=`grep "${XMLDIR}/$f" -e 'Total number of events processed: ' | grep -Po '[0-9]*'`
          if [[ ! $NEVENTS ]]; then
            echo ">>>   ${WARNING} No number of events saved in $f!$E"
          else
            [[ $VERBOSITY > 0 ]] && echo ">>>   $NEVENTS events in $f"
            NTOT=$(($NTOT+$NEVENTS))
          fi
        done
        
        printf ">>>  \e[1m%5s \e[0mfiles in %2s xmls files (%s events)" "$nFiles" "$nXMLFiles" "$NTOT"
        (( $nDuplicates > 0 )) && printf "  ->  %s duplicate root files !!! \n" "$nDuplicates" || printf "\n"
    else
        echo ">>> sample not found in $XMLDIR"
    fi
    
    
    echo ">>> "
done


echo ">>> "
echo ">>> done"
echo
exit 0
