import os
import pandas as pd
import re
import glob
import shutil as sh

# User Input of name of folder (the name that you entered in 'Analysis name' under Basic Fields):
folderName = str(input('Enter the name of folder file:'))
# setting directory path to find the inputted folder:
directory = str('/Users/crystal/gsea_home/output/jan28/' + folderName)
# changing directory of script:
os.chdir(directory)

# extracting folder ID number from UserInput to find report file:
idNumber = re.findall(r'\d+\.?\d*', folderName)
idNumber = str(idNumber[1])
# reading report tsv file
reportTSV = str('gsea_report_for_KO_3d_DSS_' + idNumber + '.tsv')
originalReport = pd.read_csv(reportTSV, sep='\t')

# creating report to show gene sets that is < 0.05 in FDR q-value:
FDRReport = originalReport.copy()
# delete unnecessary columns
del FDRReport['GS<br> follow link to MSigDB']
del FDRReport['GS DETAILS']
# changing column name
FDRReport = FDRReport.rename(columns={'NAME': 'Gene Set'})
# filtering original report
FDRReport = FDRReport.loc[FDRReport['FDR q-val'] < 0.05]
# rounding all values to 6 decimal places
FDRReport['ES'] = FDRReport['ES'].round(6)
FDRReport['NES'] = FDRReport['NES'].round(6)
FDRReport['NOM p-val'] = FDRReport['NOM p-val'].round(6)
FDRReport['FDR q-val'] = FDRReport['FDR q-val'].round(6)
FDRReport['FWER q-val'] = FDRReport['FWER p-val'].round(6)
# exporting the finished file
FDRReport.to_csv(r'passFDR.csv', index=True, header=True)

# reading back report file
FDRReport = pd.read_csv('passFDR.csv')
# saving gene set column information into variable
geneSet = FDRReport['Gene Set']

# core enrichment table filter to show core enriched gene
newCoreEnrichmentList = []
for x in geneSet:
    # creating name of file
    originalCoreEnrichmentFileName = str(x + '.tsv')
    print(originalCoreEnrichmentFileName)
    # reading file by gene set
    originalCoreEnrichment = pd.read_csv(originalCoreEnrichmentFileName, sep='\t')
    filteredCoreEnrichment = originalCoreEnrichment
    # formatting numeric amount to 6 sig figs
    filteredCoreEnrichment['RANK METRIC SCORE'] = filteredCoreEnrichment['RANK METRIC SCORE'].round(6)
    filteredCoreEnrichment['RUNNING ES'] = filteredCoreEnrichment['RUNNING ES'].round(6)
    # filtering core enriched genes
    filteredCoreEnrichment = originalCoreEnrichment.loc[originalCoreEnrichment['CORE ENRICHMENT'] == 'Yes']
    # new file name:
    newCoreEnrichmentFileName = str('coreEnrichment_' + originalCoreEnrichmentFileName)
    # exporting file as csv
    filteredCoreEnrichment.to_csv(str(newCoreEnrichmentFileName), index=False, header=True)
    newCoreEnrichmentList.append(newCoreEnrichmentFileName)

    # new file name:
    newCoreEnrichmentFileName = str('Filtered_Core_Enrichment' + originalCoreEnrichmentFileName)
    # exporting file as csv
    filteredCoreEnrichment.to_csv(str(newCoreEnrichmentFileName), index=False, header=True)
    newCoreEnrichmentList.append(newCoreEnrichmentFileName)

enrichmentPlotList = []
# finding png corresponding to gene set
for x in geneSet:
    enrichmentPlot = glob.glob('enplot_' + x + '*')
    print(enrichmentPlot[0])
    enrichmentPlotList.append(enrichmentPlot[0])

# creating new folder to contain significant reports
folderDestination = directory + '_analyzed'
if os.path.exists(directory):
    try:
        # make new directory path
        os.mkdir(folderDestination)
        # confirmation that new folder has been corrected
        print(directory + '_analyzed has been created')
        # moving FDR report to new folder
        sh.copy('passFDR.csv', folderDestination)
        # moving original report to new folder
        sh.copy(reportTSV, folderDestination)
        # moving enriched gene set's enrichment plot to new folder
        for f in enrichmentPlotList:
            sh.copy(f, folderDestination)
            print(f)
        # moving enriched genes to new folder
        for z in newCoreEnrichmentList:
            sh.copy(z, folderDestination)
            print(z)
    # if there is already a folder created from a previous run, please manually change the folder name
    except OSError as error:
        print("Directory already exist")
