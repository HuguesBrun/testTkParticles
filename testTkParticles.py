import FWCore.ParameterSet.Config as cms

process = cms.Process("ALZ")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.GlobalTag.globaltag = 'PRE_ST62_V8::All'

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
                                #'file:../../CMSSW_6_2_0_prod/src/MYCOPY.root'
                                '/store/relval/CMSSW_6_2_0/RelValSingleMuPt10/GEN-SIM-RECO/PRE_ST62_V8-v3/00000/FEB7D35C-5CEC-E211-80AA-003048FEB8EE.root'
                            
    )
)



process.load("SimGeneral.MixingModule.mixNoPU_cfi")

import SimGeneral.MixingModule.trackingTruthProducer_cfi
process.mergedtruthNoSimHits = process.trackingParticles.clone(
                                                            simHitCollections = cms.PSet(
                                                                                         muon = cms.VInputTag(),
                                                                                         tracker = cms.VInputTag(),
                                                                                         pixel = cms.VInputTag()
                                                                                         )
                                                            )

process.mix.digitizers.mergedtruth = process.mergedtruthNoSimHits

print process.mix.digitizers



process.out = cms.OutputModule("PoolOutputModule",
                               outputCommands = cms.untracked.vstring(
                                                                      'drop *',
                                                                      'keep *_mix_*_ALZ'),
                               fileName = cms.untracked.string('testRECOouput.root')
                               )

process.p = cms.Path(process.mix)

process.outpath = cms.EndPath(process.out)





