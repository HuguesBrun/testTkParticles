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

process.load("SimMuon.MCTruth.MuonAssociatorByHitsESProducer_NoSimHits_cfi") 

process.classByHitsTM = cms.EDProducer("MuonMCClassifier",
     muons = cms.InputTag("muons"),
     muonPreselection = cms.string("isTrackerMuon"),  #
     #muonPreselection = cms.string("muonID('TrackerMuonArbitrated')"), # You might want this
     trackType = cms.string("segments"),  # or 'inner','outer','global'
     trackingParticles = cms.InputTag("mix"),         
     associatorLabel   = cms.string("muonAssociatorByHits_NoSimHits"),
     decayRho  = cms.double(200), # to classifiy differently decay muons included in ppMuX
     decayAbsZ = cms.double(400), # and decay muons that could not be in ppMuX
     linkToGenParticles = cms.bool(True),          # produce also a collection of GenParticles for secondary muons
     genParticles = cms.InputTag("genParticles"),  # and associations to primary and secondaries
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

process.mix.digitizers = cms.PSet( mergedtruth = process.mergedtruthNoSimHits )
process.mix.mixObjects = cms.PSet()
del process.simCastorDigis
del process.simEcalUnsuppressedDigis
del process.simHcalUnsuppressedDigis
del process.simSiPixelDigis
del process.simSiStripDigis



process.out = cms.OutputModule("PoolOutputModule",
                               outputCommands = cms.untracked.vstring(
                                                                      'drop *',
                                                                      'keep *_classByHitsTM_*_ALZ',
                                                                      'keep *_mix_*_ALZ'),
                               fileName = cms.untracked.string('testRECOouput.root')
                               )

#process.p = cms.Path(process.mix)
process.p = cms.Path(process.mix*process.classByHitsTM)

process.outpath = cms.EndPath(process.out)





