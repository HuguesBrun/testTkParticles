import FWCore.ParameterSet.Config as cms

process = cms.Process("ALZ")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.GlobalTag.globaltag = 'START53_V14::All'

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
                                #'file:../../CMSSW_6_2_0_prod/src/MYCOPY.root'
                                '/store/relval/CMSSW_5_3_6-START53_V14/RelValSingleMuPt1000/GEN-SIM-RECO/v2/00000/7C1AEF1C-FF29-E211-BA60-003048678B20.root'
                            
    )
)



process.load("SimGeneral.MixingModule.mixNoPU_cfi")
process.load("SimGeneral.TrackingAnalysis.trackingParticlesNoSimHits_cfi")
process.out = cms.OutputModule("PoolOutputModule",
                               outputCommands = cms.untracked.vstring(
                                                                      'drop *',
                                                                      'keep *_*_*_ALZ'),
                               fileName = cms.untracked.string('testRECOouput.root')
                               )

process.p = cms.Path(process.mix*process.mergedtruthNoSimHits)

process.outpath = cms.EndPath(process.out)





