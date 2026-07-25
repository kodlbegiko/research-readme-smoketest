# JOSS issue 121 sampling frame

## Static frame

The official JOSS issue 121 order contained 39 papers. Thirty-eight GitHub source repositories met the preregistered eligibility rules. One GitLab repository was excluded under the predeclared non-GitHub rule. There was no replacement sampling. The detector and reference evaluation used all 38 eligible GitHub repositories.

## Dynamic frame

Ten cases were locked only after prediction and reference labels were committed. Selection was feasibility-aware and stratified across strict-ready agreements/disagreements, hard findings, ecosystems, CLI/library paths, external documentation, and resource requirements. Selection was not outcome-aware.

| Case | Repository | Predicted strict-ready | Reference strict-ready | Final dynamic status |
|---|---|---:|---:|---|
| D01-himap | `GroupiSP/himap` | false | true | SUCCESS |
| D02-hlafreq | `BarinthusBio/HLAfreq` | false | true | SUCCESS |
| D03-woodtapper | `artefactory/woodtapper` | true | true | FAILURE_DEPENDENCY_COMPATIBILITY |
| D04-multimodars | `yungselm/multimoda-rs` | true | true | SUCCESS |
| D05-cowfootr | `juanmarcosmoreno-arch/cowfootR` | false | true | SUCCESS |
| D06-kigali | `SchmidtDSE/kigali-sim` | true | true | SUCCESS_WITH_FRICTION |
| D07-gapflow | `hannes-holey/GaPFlow` | false | true | SUCCESS |
| D08-sklearn-migrator | `anvaldes/sklearn-migrator` | false | true | SUCCESS |
| D09-boost-geometry | `boostorg/geometry` | false | false | SUCCESS_WITH_FRICTION |
| D10-ecodive | `cmmr/ecodive` | false | true | UNTESTABLE_HERE |

## Limits

The ten cases are an adjudicated validation sample. Percentages describe only this sample. They do not estimate the prevalence of README defects or first-use success across JOSS, GitHub, or research software generally.
