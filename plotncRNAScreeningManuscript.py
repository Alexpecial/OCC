import pickle
import os

import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from itertools import chain, combinations, permutations
import matplotlib.font_manager as font_manager

font = font_manager.FontProperties(family='Times New Roman', size = 'x-small', style = 'italic')
plt.rcParams['mathtext.fontset'] = "stix"
plt.rcParams["font.family"] = "Times New Roman"

def main():
    restultPath = './results/data22832495_manuscript/'
    # restultPath = './results/data22832495/'

    # outPath = './figures/'
    outPath = restultPath + 'figures/'

    maxLengthOfStages = 4
    stages = getStages(maxLengthOfStages, "all")
    bestPerformers = drawFinalSamplesPerBudget(stages, restultPath, restultPath + 'finalSamplesPerBudget/')

    metrics = ['lambdas', 'cost', 'samples']
    for metric in metrics:
        # drawMetricPerBudget(metric, [(0, 3), (1, 0, 3), (0, 1, 3), (0, 1, 2, 3), (1, 0, 2, 3)], restultPath, restultPath + metric + '/')   
        drawMetricPerBudget(metric, bestPerformers, restultPath, restultPath + metric + '/', drawAll = False)   

def getStages(maxLengthOfStages, mode):
    stageOrder = list(range(maxLengthOfStages))
    allStageSetups = list(chain.from_iterable(combinations(stageOrder, r) for r in range(len(stageOrder)+1)))
    stageSetups = list()
    for i in range(len(allStageSetups)):
        stageSetup = allStageSetups[i]
        if (len(stageSetup) > 1) and (stageSetup[-1] == stageOrder[-1]):
            if mode == "all":
                # All combinations and permutations    
                if len(stageSetup) > 2:
                    allPermutations = list(permutations(stageSetup))
                    for permutation in allPermutations:
                        if (permutation[-1] == stageOrder[-1]):
                            stageSetups.append(permutation)
                else:
                    stageSetups.append(stageSetup)
                
                # # All combinations w.o. permutations  
                # stageSetups.append(stageSetup)

            elif mode == "4":
                # All permutations with four stages
                if len(stageSetup) == 4:
                    # stageSetups.append(stageSetup)
                    allPermutations = list(permutations(stageSetup))
                    for permutation in allPermutations:
                        if (permutation[-1] == stageOrder[-1]):
                            stageSetups.append(permutation)

    # # Select setups to draw
    # stageSetupsTemp = x=[[] for i in range(maxLengthOfStages)]
    # for stageSetup in stageSetups:
    #     stageSetupsTemp[len(stageSetup)-1].append(stageSetup)
    # stageSetupsToDraw = list()
    # for i in range(1, maxLengthOfStages):
    #     threshold = list()
    #     for stageSetup in stageSetupsTemp[i]:
    #         threshold.append(np.min(np.where(np.array(data["y_" + 'proposed' + '_' + ''.join(map(str, stageSetup))])>90)))
    #     for stageSetup in stageSetupsTemp[i]:
    #         if np.sort(threshold)[2] >= np.min(np.where(np.array(data["y_" + 'proposed' + '_' + ''.join(map(str, stageSetup))])>90)):
    #             stageSetupsToDraw.append(stageSetup)
    # Select all
    stageSetupsToDraw = stageSetups
    return stageSetupsToDraw

def drawFinalSamplesPerBudget(stages, restultPath, outPath):
    fontP = FontProperties()
    fontP.set_size('xx-small')

    if not os.path.isdir(outPath):
        os.mkdir(outPath)

    fileList = list()
    for root, dirs, files in os.walk(restultPath, topdown=True):
        for name in files:
            if not "minCost" in name:
                fileList.append(root + name)
        break
    
    bestSetups2Return = {}
    for fileName in fileList:
        if "DS_Store" in fileName:
            continue
        with open(fileName, 'rb') as handle:
            data = pickle.load(handle)


        # if fileName.replace(".pickle", "_0.5_minCost.pickle") != './results/data22832495/cov_0.5_minCost.pickle':
        #     continue
        with open(fileName.replace(".pickle", "_0.8_minCost.pickle"), 'rb') as handle:
            data_minCost = pickle.load(handle)

        maxDomain = []
        for stageSetup in stages:
            if len(data[''.join(map(str, stageSetup))]) > len(maxDomain):
                maxDomain = [d['x'] for d in data[''.join(map(str, stageSetup))]]

        dfList = list()
        algorithmList = []
        lStyle = {}
        lStyle1 = {}
        # pStyle = []
        # pStyle = {}
        cStyle = []
        
        dfList_minCost = list()

        # draw all
        alternativeVal = 0
        # alternativeVal = int(len(maxDomain)/28)
        if alternativeVal == 0: alternativeVal = 1
        for stageSetup in stages:
            # if len(stageSetup) != 3:
            #     continue
            for algorithm in data[''.join(map(str, stageSetup))][0]['algorithms']:
                if algorithm not in algorithmList:
                    algorithmList.append(algorithm)
                    dfList.append(pd.DataFrame(index=maxDomain[::alternativeVal]))
                    dfList_minCost.append(pd.DataFrame(columns = ['x', 'y', 'z']))
                column2Add = [d[algorithm + '_samples'][-1] for d in data[''.join(map(str, stageSetup))]] + ([NaN]*(len(maxDomain)-len([d[algorithm + '_samples'][-1] for d in data[''.join(map(str, stageSetup))]])))
                dfList[algorithmList.index(algorithm)]['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + ']$'] = column2Add[::alternativeVal]
                lStyle['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + ']$'] = getLineColor(stageSetup)
                lStyle1['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + ']$'] = getLineColor2(stageSetup)


            #     target_data_minCost = data_minCost[''.join(map(str, stageSetup))][0]
            #     element = {'x': np.sum(target_data_minCost[algorithm + '_cost']), 
            #     'y': target_data_minCost[algorithm + '_samples'][-1],
            #     'z': 'a_' + ',a_'.join(map(str, stageSetup)),
            #     'p': getStyle(stageSetup, 'point')}
            #     dfList_minCost[algorithmList.index(algorithm)] = dfList_minCost[algorithmList.index(algorithm)].append(element, ignore_index = True)
            # cStyle.append(getStyle(stageSetup, 'color'))
            # # pStyle.append(getStyle(stageSetup, 'point'))

        for i in range(len(algorithmList)):
            dfList[i].plot(figsize=(7, 6), style=lStyle, linewidth = 2, alpha=0.5) 
            for j in range(len(dfList_minCost[i])):
                plt.scatter(dfList_minCost[i]['x'][j], dfList_minCost[i]['y'][j], label=dfList_minCost[i]['z'][j], c = cStyle[j], marker = dfList_minCost[i]['p'][j], s = 150)
            plt.legend(loc='upper left', prop={'size':6}, bbox_to_anchor=(1,1), ncol=1)
            plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'])
            # plt.hlines(y=data['GT'][-1], xmin=0.0, xmax=1.0, color='b')
            plt.axhline(y = data['GT'])
            # plt.yticks(np.arange(0, 100, step=10))
            # plt.title(algorithmList[i])
            plt.xlabel('Total computational budget')
            plt.ylabel('The number of potential candidates')
            # plt.ylim(0, 20)
            # plt.ylim(0, 80)
            # plt.xlim(np.min(dfList[0].index)-1000, np.max(dfList[0].index)+1000)
            # plt.xlim(16000, 27000)
            plt.grid(True)
            plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + ".pdf")
            # # maxIndex = 0
            # # for j in range(len(dfList[i].index)):
            # #     if np.max(dfList[i].iloc[j,:]) > 90:
            # #         maxIndex = j + 4
            # #         break
            # # if maxIndex < (len(dfList[i].index)/2):
            # #     plt.xlim(0, dfList[i].index[maxIndex])
            # #     plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + "_closeup.pdf")
            # plt.xlim(0, dfList[i].index[int((len(dfList[i].index)/3))])
            # plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + "_closeup.pdf")
            plt.close()

        for i in range(len(algorithmList)):
            # dfList[i] = dfList[i].reindex(sorted(dfList[i].columns), axis=1)
            cols = dfList[i].columns.tolist()
            dfList[i] = dfList[i][[cols[0], cols[1], cols[2],
            cols[3], cols[5], cols[4], cols[7], cols[6], cols[8],
            cols[9], cols[10], cols[11], cols[12], cols[13], cols[14]
            ]]
            dfList[i].plot(figsize=(9, 3), style=lStyle, linewidth = 0.7, alpha = 0.7, markevery=5, markersize=1.8)
            dfList[i].to_excel("output.xlsx") 
            plt.legend(loc='center', bbox_to_anchor=(0.5, -0.8))
            plt.axvline(x = 26137409, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 52274818, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 78412227, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 104549636, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 130687045, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 156824454, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 182961863, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 209099272, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 235236681, ls = ':', color = 'k', linewidth = 0.8)
            # plt.axvline(x = 261374090, color = 'k', linewidth = 0.8)
            plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'], ls = '--', color = 'k', linewidth = 0.8)
            plt.axhline(y = data['GT'], ls = '--', color = 'k', linewidth = 0.8)
            # plt.yticks(np.arange(0, 100, step=10))
            plt.xlabel('Total computational budget')
            plt.ylabel('The number of potential candidates')
            # plt.tight_layout()
            # plt.ylim(0, 20)
            # plt.ylim(0, 80)
            # plt.xlim(np.min(dfList[0].index)-1000, np.max(dfList[0].index)+1000)
            # plt.xlim(16000, 27000)
            plt.grid(True)
            plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + "_man.pdf", transparent=True, bbox_inches='tight')
            plt.close()

        # Initialize the figure style
        # plt.style.use('seaborn-whitegrid')
        # multiple line plot
        for i in range(6):
            if i == 0 or i == 3:
                list2Plot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$']
                list2GrayPlot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
            elif i == 1 or i == 4:
                list2Plot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$']
                list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
            elif i == 2 or i == 5:
                list2Plot = ['$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
                list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$'] 
                        
            ax = plt.subplot(2, 3, i+1)
            if i in range(3):
                if i == 0:
                    plt.ylabel('The number of potential candidates')
                else:
                    ax.axes.yaxis.set_ticklabels([])
                if i == 1:
                    plt.xlabel('Total computational budget')
                dfList[0][list2Plot].plot(figsize=(9, 5.5), style = lStyle, linewidth=1.2, alpha=0.7, label=list2Plot, ax=ax)
                for v in list2GrayPlot:
                    plt.plot(dfList[0].index, dfList[0][v], color='grey', linewidth=0.7, alpha=0.2)
                # plt.plot(dfList[0].index, dfList[0][list2Plot], linewidth=2.4, alpha=0.5, label=list2Plot)
                legend = plt.legend(frameon = 1)
                frame = legend.get_frame()
                frame.set_color('white')
                plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'], color='k', linewidth=1)
                plt.axhline(y = data['GT'], color='k', linewidth=1)
                # Same limits for every chart
                plt.xlim(0,3*(10**8))
                plt.ylim(-100, 55000)
                # Not ticks everywhere
                # if i in range(7) :
                #     plt.tick_params(labelbottom='off')
                # if i not in [1] :
                #     plt.tick_params(labelleft='off')
                # Add title
                # plt.title(list2Plot, loc='left', fontsize=12, fontweight=0, color=palette(i))
                # plt.ylim(0, 100)
                plt.grid(True)
            else:
                if i == 3:
                    plt.ylabel('Total computational budget')
                else:
                    ax.axes.yaxis.set_ticklabels([])
                if i == 4:
                    plt.xlabel('The number of potential candidates')
                
                for v in list2Plot:
                    plt.plot(dfList[0][v], dfList[0].index, lStyle[v], linewidth=1.2, alpha=0.7)
                # dfList[0][list2Plot].plot(figsize=(9, 7), style = lStyle, linewidth=1.2, alpha=0.7, label=list2Plot, ax=ax)
                for v in list2GrayPlot:
                    plt.plot(dfList[0][v], dfList[0].index, color='grey', linewidth=0.7, alpha=0.2)
                # plt.plot(dfList[0].index, dfList[0][list2Plot], linewidth=2.4, alpha=0.5, label=list2Plot)
                legend = plt.legend(frameon = 1)
                frame = legend.get_frame()
                frame.set_color('white')
                plt.axvline(x = data['GT'], color='k', linewidth=1)
                plt.axhline(y = data['costPerStage'][-1]*data['numberOfSamples'], color='k', linewidth=1 )
                # Same limits for every chart
                
                plt.xlim(-100, 55000)
                plt.ylim(0,3*(10**8))

                plt.grid(True)
        plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + "_all.pdf", transparent=True)
        plt.close()

        for i in range(3):
            if i == 0 or i == 3:
                list2Plot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$']
                list2GrayPlot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
            elif i == 1 or i == 4:
                list2Plot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$']
                list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
            elif i == 2 or i == 5:
                list2Plot = ['$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
                list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$'] 

            ax = plt.subplot(3, 1, i+1)
            dfList[0][list2Plot].plot(figsize=(9, 5.5), style = lStyle1, linewidth=0.7, alpha=0.7, label=list2Plot, ax=ax, markevery=5, markersize=2)
            # for v in list2GrayPlot:
                # plt.plot(dfList[0][v], dfList[0].index, color='grey', linewidth=0.7, alpha=0.2)
            # plt.plot(dfList[0].index, dfList[0][list2Plot], linewidth=2.4, alpha=0.5, label=list2Plot)
            legend = plt.legend(loc=1)
            frame = legend.get_frame()
            frame.set_color('white')
            # plt.legend(loc='center', bbox_to_anchor=(0.5, -0.8))
            plt.axvline(x = 26137409, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 52274818, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 78412227, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 104549636, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 130687045, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 156824454, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 182961863, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 209099272, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = 235236681, ls = ':', color = 'k', linewidth = 0.8)
            plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'], ls = '--', color = 'k', linewidth = 0.8)
            plt.axhline(y = data['GT'], ls = '--', color = 'k', linewidth = 0.8)
            # Same limits for every chart

            # Major ticks every 20, minor ticks every 5
            major_ticks = np.arange(0, 55000, 10000)
            minor_ticks = np.arange(0, 55000, 5000)

            ax.set_yticks(major_ticks)
            # ax.set_xticks(minor_ticks, minor=True)
            # ax.set_yticks(major_ticks)
            # ax.set_yticks(minor_ticks, minor=True)
            ax.grid(which='major', alpha=0.5, linewidth = 0.7)
            plt.xlim(-10454964, data['costPerStage'][-1]*data['numberOfSamples'] + (10454964))
            plt.ylim(-2010, data['GT'] + 2010)

            # plt.ylabel('The number of potential candidates')
            # plt.xlabel('Total computational budget')
            if i in range(3):
                if i == 1:
                    plt.ylabel('The number of potential candidates')
                if i == 2:
                    plt.xlabel('Total computational budget')          

        plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + "_test.pdf", transparent=True)
        plt.close()
        
        # # draw positive samples
        # alternativeVal = 0
        # # alternativeVal = int(len(maxDomain)/28)
        # if alternativeVal == 0: alternativeVal = 1
        # for stageSetup in stages:
        #     for algorithm in data[''.join(map(str, stageSetup))][0]['algorithms']:
        #         if algorithm not in algorithmList:
        #             algorithmList.append(algorithm)
        #             dfList.append(pd.DataFrame(index=maxDomain[::alternativeVal]))
        #         column2Add = [d[algorithm + '_positiveSamples'] for d in data[''.join(map(str, stageSetup))]] + ([NaN]*(len(maxDomain)-len([d[algorithm + '_positiveSamples'] for d in data[''.join(map(str, stageSetup))]])))
        #         dfList[algorithmList.index(algorithm)]['a_' + ',a_'.join(map(str, stageSetup))] = column2Add[::alternativeVal]
        #         lStyle['a_' + ',a_'.join(map(str, stageSetup))] = getLineColor(stageSetup)

        # for i in range(len(algorithmList)):
        #     dfList[i].plot(figsize=(7, 6), style=lStyle)
        #     plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'])
        #     # plt.hlines(y=data['GT'][-1], xmin=0.0, xmax=1.0, color='b')
        #     plt.axhline(y = data['PS'])
        #     plt.title(algorithmList[i])
        #     plt.xlabel('Total computational budget')
        #     plt.ylabel('The number of positive samples passed the last stage')
        #     # plt.ylim(0, 20)
        #     # plt.ylim(0, 80)
        #     # plt.xlim(np.min(dfList[0].index)-1000, np.max(dfList[0].index)+1000)
        #     # plt.xlim(16000, 27000)
        #     plt.grid(True)
        #     # plt.yticks(np.arange(0, 100, step=10))
        #     plt.savefig(outPath + "positive_" + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + ".pdf")
        #     # # maxIndex = 0
        #     # # for j in range(len(dfList[i].index)):
        #     # #     if np.max(dfList[i].iloc[j,:]) > 90:
        #     # #         maxIndex = j + 4
        #     # #         break
        #     # # if maxIndex < (len(dfList[i].index)/2):
        #     # #     plt.xlim(0, dfList[i].index[maxIndex])
        #     # #     plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + "_closeup.pdf")
        #     # plt.xlim(0, dfList[i].index[int((len(dfList[i].index)/3))])
        #     # plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + "_closeup.pdf")
        #     plt.close()

        # # Original
        # for i in range(3):
        #     if i == 0 or i == 3:
        #         list2Plot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$']
        #         list2GrayPlot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
        #     elif i == 1 or i == 4:
        #         list2Plot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$']
        #         list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
        #     elif i == 2 or i == 5:
        #         list2Plot = ['$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
        #         list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$'] 
            
        #     ax = plt.subplot(3, 1, i+1)
        #     dfList[0][list2Plot].plot(figsize=(7.5, 6.5), style = lStyle, linewidth=0.8, alpha=0.7, label=list2Plot, ax=ax)
        #     for v in list2GrayPlot:
        #         plt.plot(dfList[0].index, dfList[0][v], color='grey', linewidth=0.3, alpha=0.2)

        #     # dfList[1][list2Plot].plot(figsize=(7.5, 6.5), linestyle = '--', style = lStyle, linewidth=0.8, alpha=0.7, label=list2Plot, ax=ax)
        #     # for v in list2GrayPlot:
        #     #     plt.plot(dfList[1].index, dfList[0][v], color='grey', linewidth=0.3, alpha=0.2)
        #     legend = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), frameon = 1, fontsize = 'small', prop=font)
        #     frame = legend.get_frame()
        #     frame.set_color('white')
        #     # plt.legend(bbox_to_anchor=(1, 1), fontsize = 'small', prop=font, loc=5, ncol=2)
        #     plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'], color='k', linewidth=0.8, ls = '--')
        #     plt.axhline(y = data['GT'], color='k', linewidth=0.8, ls = '--')
        #     # Same limits for every chart
        #     plt.xlim(0,3*(10**8))
        #     plt.ylim(-100, 55000)

        #     # plt.ylim(-100, 55000)
        #     # if i == 2:
        #     #     plt.xlabel('Total computational budget $C$')
        #     # if i == 1:
        #     #     plt.ylabel('The number of potential candidates $\mathbb{Y}$')
        #     if i == 2:
        #         plt.xlabel('Total computational budget')
        #     if i == 1:
        #         plt.ylabel('The number of potential candidates')
        #     plt.grid(True)

        # plt.tight_layout()
        # plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + "_Y.pdf", transparent=True)
        # plt.close()

        # Updated
        for i in range(3):
            if i == 0 or i == 3:
                list2Plot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$']
                list2GrayPlot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
            elif i == 1 or i == 4:
                list2Plot = ['$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$']
                list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
            elif i == 2 or i == 5:
                list2Plot = ['$[S_1,S_2,S_3,S_4]$', '$[S_1,S_3,S_2,S_4]$', '$[S_2,S_1,S_3,S_4]$', '$[S_2,S_3,S_1,S_4]$', '$[S_3,S_1,S_2,S_4]$', '$[S_3,S_2,S_1,S_4]$']
                list2GrayPlot = ['$[S_1,S_4]$', '$[S_2,S_4]$', '$[S_3,S_4]$', '$[S_1,S_2,S_4]$', '$[S_1,S_3,S_4]$', '$[S_2,S_1,S_4]$', '$[S_2,S_3,S_4]$', '$[S_3,S_1,S_4]$', '$[S_3,S_2,S_4]$'] 
            
            ax = plt.subplot(3, 2, (i*2) + 1)
            dfList[0][list2Plot].plot(figsize=(7.5, 6.5), style = lStyle1, linewidth=0.7, alpha=0.7, ax=ax, markevery=10, markersize=2, legend=None)
            for v in list2GrayPlot:
                plt.plot(dfList[0].index, dfList[0][v], color='grey', linewidth=0.3, alpha=0.2)

            # dfList[1][list2Plot].plot(figsize=(7.5, 6.5), linestyle = '--', style = lStyle, linewidth=0.8, alpha=0.7, label=list2Plot, ax=ax)
            # for v in list2GrayPlot:
            #     plt.plot(dfList[1].index, dfList[0][v], color='grey', linewidth=0.3, alpha=0.2)
            # legend = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), frameon = 1, fontsize = 'small', prop=font)
            # frame = legend.get_frame()
            # frame.set_color('white')
            # plt.legend(bbox_to_anchor=(1, 1), fontsize = 'small', prop=font, loc=5, ncol=2)
            plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'], color='k', linewidth=0.8, ls = '--')
            plt.axhline(y = data['GT'], color='k', linewidth=0.8, ls = '--')
            # Same limits for every chart
            plt.xlim(0,3*(10**8))
            plt.ylim(-100, 55000)

            # plt.ylim(-100, 55000)
            # if i == 2:
            #     plt.xlabel('Total computational budget $C$')
            # if i == 1:
            #     plt.ylabel('The number of potential candidates $\mathbb{Y}$')
            if i == 2:
                plt.xlabel('Total computational budget')
            if i == 1:
                plt.ylabel('The number of potential candidates')
            plt.grid(True)

            ax = plt.subplot(3, 2, (i*2) + 2)
            dfList[0][list2Plot].plot(figsize=(7.5, 6.5), style = lStyle1, linewidth=0.7, alpha=0.7, label=list2Plot, ax=ax, markevery=10, markersize=2)
            for v in list2GrayPlot:
                plt.plot(dfList[0].index, dfList[0][v], color='grey', linewidth=0.3, alpha=0.2)

            # dfList[1][list2Plot].plot(figsize=(7.5, 6.5), linestyle = '--', style = lStyle, linewidth=0.8, alpha=0.7, label=list2Plot, ax=ax)
            # for v in list2GrayPlot:
            #     plt.plot(dfList[1].index, dfList[0][v], color='grey', linewidth=0.3, alpha=0.2)
            legend = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), frameon = 1, fontsize = 'small', prop=font)
            frame = legend.get_frame()
            frame.set_color('white')
            # plt.legend(bbox_to_anchor=(1, 1), fontsize = 'small', prop=font, loc=5, ncol=2)
            plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'], color='k', linewidth=0.8, ls = '--')
            plt.axhline(y = data['GT'], color='k', linewidth=0.8, ls = '--')
            # Same limits for every chart

            # plt.ylim(-100, 55000)
            # if i == 2:
            #     plt.xlabel('Total computational budget $C$')
            # if i == 1:
            #     plt.ylabel('The number of potential candidates $\mathbb{Y}$')
            plt.yscale("log")
            plt.xscale("log")
            if i == 2:
                plt.xlabel('log(Total computational budget)')
            if i == 1:
                plt.ylabel('log(The number of potential candidates)')
            plt.grid(True)

        plt.tight_layout()
        plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + "_Y.pdf", transparent=True)
        plt.close()


        targetAlgorithm = 'proposedLambda'
        df = dfList[algorithmList.index(targetAlgorithm)]
        bestSetups = list()
        bestSetupsIndices = list()
        for i in range(len(df)):
            if np.max(df.iloc[i, :]) < 10:
                continue
            if np.isnan(df.iloc[i, :]).any():
                break
            bestSetups += list(df.columns[np.where(df.iloc[i, :] >= (np.max(df.iloc[i, :])-1))])
            for bestSetupIndex in list(np.where(df.iloc[i, :].astype(int) >= (int(np.max(df.iloc[i, :]))))[0]):
                bestSetupsIndices.append(bestSetupIndex)  
        bestSetups = list(set(bestSetups))
        bestSetups.sort() # sorts normally by alphabetical order
        bestSetups.sort(key=len) # sorts by descending length
        
        bestSetups = ['$[S_2,S_4]$', '$[S_1,S_2,S_4]$', '$[S_2,S_1,S_4]$']
        bestDf = df[bestSetups]
        bestDf = bestDf.add_prefix('proposed_')

        df = dfList[algorithmList.index('baseline')]
        baselineDf = df[bestSetups]
        baselineDf = baselineDf.add_prefix('baseline_')
        # bestDf = pd.concat([bestDf, baselineDf], axis=1)
        bestLineColor = {}
        bestLineStyle = {}
        for setup in bestSetups:
            bestLineColor['proposed_' + setup] = lStyle[setup]
            bestLineColor['baseline_' + setup] = lStyle[setup]
            bestLineStyle['proposed_' + setup] = 'solid'
            bestLineStyle['baseline_' + setup] = 'dotted'
        # add prefix

        # bestDf.plot(figsize=(7, 6), style =  bestLineColor, linewidth = 2, alpha=0.5)
        fig, ax = plt.subplots()
        bestDf.plot(figsize=(7, 6), style =  bestLineColor, linewidth = 2, alpha=0.5, ax=ax)
        baselineDf.plot(figsize=(7, 6), style =  bestLineColor, linewidth = 2, linestyle = 'dotted', alpha=0.5, ax=ax)
        plt.xlabel('Total computational budget')
        plt.ylabel('The number of samples passed the last stage')
        plt.axvline(x = data['costPerStage'][-1]*data['numberOfSamples'])
        plt.axhline(y = data['GT'])
        # plt.ylim(0, 100)
        plt.grid(True)
        # plt.yticks(np.arange(0, 100, step=10))
        plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + targetAlgorithm + "_best.pdf")
        plt.close()
        bestSetupsIndicesForCov = list()
        bestSetupsIndices = list(set(bestSetupsIndices))
        bestSetupsIndices.sort()
        for i in bestSetupsIndices:
            bestSetupsIndicesForCov.append(stages[i])
        bestSetups2Return[fileName] = bestSetupsIndicesForCov
    return bestSetups2Return


def getStyle(stageSetup, option='all'):
    lineOption = ''
    if stageSetup[0] == 0:
        if len(stageSetup) == 2:
            if option == 'all':
                lineOption += 'r-.'
            else:
                if option == 'color':
                    lineOption = 'r'
                else:
                    lineOption = '1'
        elif len(stageSetup) == 3:
            if option == 'point':
                if stageSetup[1] == 1:
                    lineOption += '>'
                elif stageSetup[1] == 2:
                    lineOption += '<'
            else:
                lineOption += 'g'  
                if option == 'all':
                    if stageSetup[1] == 1:
                        lineOption += ':>'
                    elif stageSetup[1] == 2:
                        lineOption += ':<'
        elif len(stageSetup) == 4:
            if option == 'point':
                if stageSetup[1] == 1:
                    lineOption += '>'
                elif stageSetup[1] == 2:
                    lineOption += '<'
            else:
                lineOption += 'b'
                if option == 'all':
                    if stageSetup[1] == 1:
                        lineOption += ':>'
                    elif stageSetup[1] == 2:
                        lineOption += ':<'

    if stageSetup[0] == 1:
        if len(stageSetup) == 2:
            if option == 'all':
                lineOption += 'r--'
            else:
                if option == 'color':
                    lineOption += 'r'
                else:
                    lineOption = '2'
        elif len(stageSetup) == 3:
            if option == 'point':
                if stageSetup[1] == 0:
                    lineOption += '^'
                elif stageSetup[1] == 2:
                    lineOption += 'v'
            else:
                lineOption += 'g'  
                if option == 'all':
                    if stageSetup[1] == 0:
                        lineOption += ':^'
                    elif stageSetup[1] == 2:
                        lineOption += ':v'
        elif len(stageSetup) == 4:
            if option == 'point':
                if stageSetup[1] == 0:
                    lineOption += '^'
                elif stageSetup[1] == 2:
                    lineOption += 'v'
            else:
                lineOption += 'b'
                if option == 'all':
                    if stageSetup[1] == 0:
                        lineOption += ':^'
                    elif stageSetup[1] == 2:
                        lineOption += ':v'
        
    if stageSetup[0] == 2:
        if len(stageSetup) == 2:
            if option == 'all':
                lineOption += 'r'
            else:
                if option == 'color':
                    lineOption = 'r'
                else:
                    lineOption = '3'
        elif len(stageSetup) == 3:
            if option == 'point':
                if stageSetup[1] == 0:
                    lineOption += '+'
                elif stageSetup[1] == 1:
                    lineOption += 'x'               
            else:
                lineOption += 'g'  
                if option == 'all':
                    if stageSetup[1] == 0:
                        lineOption += ':+'
                    elif stageSetup[1] == 1:
                        lineOption += ':x'
        elif len(stageSetup) == 4:
            if option == 'point':
                if stageSetup[1] == 0:
                    lineOption += '+'
                elif stageSetup[1] == 1:
                    lineOption += 'x'                   
            else:
                lineOption += 'b'
                if option == 'all':
                    if stageSetup[1] == 0:
                        lineOption += ':+'
                    elif stageSetup[1] == 1:
                        lineOption += ':x'   
    return lineOption 

def getLineColor(stageSetup):
    lineOption = ''
    if len(stageSetup) == 2:
        # pastel
        if "".join(map(str,stageSetup)) == '03':
            lineOption += '-or'
        elif "".join(map(str,stageSetup)) == '13':
            lineOption += '-vr'
        elif "".join(map(str,stageSetup)) == '23':
            lineOption += '-^r'

    if len(stageSetup) == 3:
        # First strong
        if "".join(map(str,stageSetup)) == '013':
            lineOption += ':og'
        elif "".join(map(str,stageSetup)) == '023':
            lineOption += ':vg'
        elif "".join(map(str,stageSetup)) == '103':
            lineOption += ':^g'
        elif "".join(map(str,stageSetup)) == '123':
            lineOption += ':>g'
        elif "".join(map(str,stageSetup)) == '203':
            lineOption += ':<g'
        elif "".join(map(str,stageSetup)) == '213':
            lineOption += ':8g'
    
    if len(stageSetup) == 4:
        if "".join(map(str,stageSetup)) == '0123':
            lineOption += '--ob'
        elif "".join(map(str,stageSetup)) == '0213':
            lineOption += '--vb'
        elif "".join(map(str,stageSetup)) == '1023':
            lineOption += '--^b'
        elif "".join(map(str,stageSetup)) == '1203':
            lineOption += '-->b'
        elif "".join(map(str,stageSetup)) == '2013':
            lineOption += '--<b'
        elif "".join(map(str,stageSetup)) == '2103':
            lineOption += '--8b'
    return lineOption  

def getLineColor2(stageSetup):
    lineOption = ''
    if len(stageSetup) == 2:
        # pastel
        if "".join(map(str,stageSetup)) == '03':
            lineOption += '-r'
        elif "".join(map(str,stageSetup)) == '13':
            lineOption += '-.^g'
        elif "".join(map(str,stageSetup)) == '23':
            lineOption += '--ob'

    if len(stageSetup) == 3:
        # First strong
        if "".join(map(str,stageSetup)) == '013':
            lineOption += '-r'
        elif "".join(map(str,stageSetup)) == '023':
            lineOption += ':r'
        elif "".join(map(str,stageSetup)) == '103':
            lineOption += '-^g'
        elif "".join(map(str,stageSetup)) == '123':
            lineOption += ':^g'
        elif "".join(map(str,stageSetup)) == '203':
            lineOption += '-ob'
        elif "".join(map(str,stageSetup)) == '213':
            lineOption += ':ob'
    
    if len(stageSetup) == 4:
        if "".join(map(str,stageSetup)) == '0123':
            lineOption += '-.r'
        elif "".join(map(str,stageSetup)) == '0213':
            lineOption += ':r'
        elif "".join(map(str,stageSetup)) == '1023':
            lineOption += '-.^g'
        elif "".join(map(str,stageSetup)) == '1203':
            lineOption += ':^g'
        elif "".join(map(str,stageSetup)) == '2013':
            lineOption += '-.ob'
        elif "".join(map(str,stageSetup)) == '2103':
            lineOption += ':ob'
    return lineOption 

def getLineColor3(stageSetup):
    lineOption = ''
    if len(stageSetup) == 2:
        # pastel
        if "".join(map(str,stageSetup)) == '03':
            lineOption += '-or'
        elif "".join(map(str,stageSetup)) == '13':
            lineOption += '-vg'
        elif "".join(map(str,stageSetup)) == '23':
            lineOption += '-^b'

    if len(stageSetup) == 3:
        # First strong
        if "".join(map(str,stageSetup)) == '013':
            lineOption += '-o'
        elif "".join(map(str,stageSetup)) == '023':
            lineOption += '-vg'
        elif "".join(map(str,stageSetup)) == '103':
            lineOption += '-^b'
        elif "".join(map(str,stageSetup)) == '123':
            lineOption += '->c'
        elif "".join(map(str,stageSetup)) == '203':
            lineOption += '-<m'
        elif "".join(map(str,stageSetup)) == '213':
            lineOption += '-8y'
    
    if len(stageSetup) == 4:
        if "".join(map(str,stageSetup)) == '0123':
            lineOption += '-or'
        elif "".join(map(str,stageSetup)) == '0213':
            lineOption += '-vg'
        elif "".join(map(str,stageSetup)) == '1023':
            lineOption += '-^b'
        elif "".join(map(str,stageSetup)) == '1203':
            lineOption += '->c'
        elif "".join(map(str,stageSetup)) == '2013':
            lineOption += '-<m'
        elif "".join(map(str,stageSetup)) == '2103':
            lineOption += '-8y'
    return lineOption 

def drawMetricPerBudget(metric, allStages, restultPath, outPath, drawAll = True):
    fontP = FontProperties()
    fontP.set_size('xx-small')

    if not os.path.isdir(outPath):
        os.mkdir(outPath)

    fileList = list()
    for root, dirs, files in os.walk(restultPath, topdown=True):
        for name in files:
            if not "minCost" in name:
                fileList.append(root + name)
        break

    for fileName in fileList:
        if "DS_Store" in fileName:
            continue
        with open(fileName, 'rb') as handle:
            data = pickle.load(handle)

        # with open(fileName.replace(".pickle", "_0.5_minCost.pickle"), 'rb') as handle:
        #     data_minCost = pickle.load(handle)

        if drawAll:
            stages = allStages[fileName]
        else:
            stage2Draw = allStages[fileName]
            checkFlag = [True]*10000
            stages = list()
            for setup in stage2Draw:
                if checkFlag[len(setup) - 1]:
                    stages.append(setup)
                    checkFlag[len(setup) - 1] = False

        maxDomain = []
        for stageSetup in stages:
            if len(data[''.join(map(str, stageSetup))]) > len(maxDomain):
                maxDomain = [d['x'] for d in data[''.join(map(str, stageSetup))]]

        dfList = list()
        algorithmList = []
        lStyle = {}
               
        dfList_minCost = list()
        cStyle = []

        alternativeVal = int(len(maxDomain)/28)
        if alternativeVal == 0: alternativeVal = 1
        for stageSetup in stages:
            for algorithm in data[''.join(map(str, stageSetup))][0]['algorithms']:
                if algorithm not in algorithmList:
                    algorithmList.append(algorithm)
                    dfList.append(pd.DataFrame(index=maxDomain[::alternativeVal]))
                    dfList_minCost.append(pd.DataFrame(columns = ['x', 'y', 'z']))
                dfs = data[''.join(map(str, stageSetup))]
                column2Add = list()
                for df in dfs:
                    if len(df) < 8:
                        column2Add.append([NaN]*len(stageSetup))
                    else:
                        if 'samples' == metric:
                            column2Add.append(df[algorithm + '_' + metric][:-1])
                        else:
                            column2Add.append(df[algorithm + '_' + metric])
                num2Add = len(maxDomain) - len(dfs)
                for i in range(num2Add):
                    column2Add.append([NaN]*len(stageSetup))
                column2Add = column2Add[::alternativeVal]
                column2Add = np.reshape(column2Add, (len(column2Add), len(stageSetup)))
                for i in range(len(stageSetup)):
                    lineOption = ''
                    dfList[algorithmList.index(algorithm)]['a_' + ',a_'.join(map(str, stageSetup)) + ":" + str(stageSetup[i])] = column2Add[:,i]
                    if len(stageSetup) == 2:
                        if stageSetup[i] == 0:
                            lineOption += '#B73A3A'
                        elif stageSetup[i] == 1:
                            lineOption += '#EC5656'
                        elif stageSetup[i] == 2:
                            lineOption += '#F28A90'
                        elif stageSetup[i] == 3:
                            # lineOption += '#F8BCBD'
                            lineOption += 'k'
                    elif len(stageSetup) == 3:
                        if stageSetup[i] == 0:
                            lineOption += '#026645'
                        elif stageSetup[i] == 1:
                            lineOption += '#0AAC00'
                        elif stageSetup[i] == 2:
                            lineOption += '#23C26F'
                        elif stageSetup[i] == 3:
                            lineOption += 'k'
                    elif len(stageSetup) == 4:
                        if stageSetup[i] == 0:
                            lineOption += '#0B31A5'
                        elif stageSetup[i] == 1:
                            lineOption += '#0050EB'
                        elif stageSetup[i] == 2:
                            lineOption += '#0078ED'
                        elif stageSetup[i] == 3:
                            lineOption += 'k'
                    lStyle['a_' + ',a_'.join(map(str, stageSetup)) + ":" + str(stageSetup[i])] = lineOption
 

            #     target_data_minCost = data_minCost[''.join(map(str, stageSetup))][0]
            #     for i in range(len(stageSetup)):
            #         element = {'x': np.sum(target_data_minCost[algorithm + '_cost']), 
            #         'y': target_data_minCost[algorithm + '_' + metric][i],
            #         'z': 'a_' + ',a_'.join(map(str, stageSetup)) + ":" + str(stageSetup[i]),
            #         'p': getStyle(stageSetup, 'point')}
            #         dfList_minCost[algorithmList.index(algorithm)] = dfList_minCost[algorithmList.index(algorithm)].append(element, ignore_index = True)
                    
            #         if algorithm == 'baseline':
            #             if stageSetup[i] == 0:
            #                 cStyle.append('r')
            #             elif stageSetup[i] == 1:
            #                 cStyle.append('g')
            #             elif stageSetup[i] == 2:
            #                 cStyle.append('b')
            #             elif stageSetup[i] == 3:
            #                 cStyle.append('k')
                    
            #         # cStyle.append(getStyle(stageSetup, 'color'))
            # # pStyle.append(getStyle(stageSetup, 'point'))

        if metric == 'lambdas':
            ylabel = 'Operator'
        elif metric == 'cost':
            ylabel = 'Computational cost consumed'
        elif metric == 'samples':
            ylabel = 'The number of samples to score'
        for i in range(len(algorithmList)):
            dfList[i].plot(figsize=(7, 6), style=lStyle, alpha=0.5)
            for j in range(len(dfList_minCost[i])):
                plt.scatter(dfList_minCost[i]['x'][j], dfList_minCost[i]['y'][j], label=dfList_minCost[i]['z'][j], c = cStyle[j], marker = dfList_minCost[i]['p'][j], s = 150)
            plt.legend(loc='upper left', prop={'size':6}, bbox_to_anchor=(1,1), ncol=1)
            # plt.title(algorithmList[i])
            plt.xlabel('Total computational budget')
            # plt.xlim(np.min(dfList[0].index)-1000, np.max(dfList[0].index)+1000)
            # plt.xlim(16000, 20000)
            plt.ylabel(ylabel)
            plt.grid(True)
            plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + algorithmList[i] + ".pdf")
            plt.close()

        stages = [[0, 3], [0, 1, 3], [0, 1, 2, 3]]
        for s_i in range(3):
            stageSetup = stages[s_i]
            maxDomain = []
            dfList = list()
            algorithmList = []
            lStyle = {}
            if len(data[''.join(map(str, stageSetup))]) > len(maxDomain):
                maxDomain = [d['x'] for d in data[''.join(map(str, stageSetup))]]

            ax = plt.subplot(3, 1, s_i + 1)
            alternativeVal = 0
            if alternativeVal == 0: alternativeVal = 1
            for algorithm in data[''.join(map(str, stageSetup))][0]['algorithms']:
                if algorithm not in algorithmList:
                    algorithmList.append(algorithm)
                    dfList.append(pd.DataFrame(index=maxDomain[::alternativeVal]))
                dfs = data[''.join(map(str, stageSetup))]
                column2Add = list()
                for df in dfs:
                    if len(df) < 8:
                        column2Add.append([NaN]*len(stageSetup))
                    else:
                        if 'samples' == metric:
                            column2Add.append(df[algorithm + '_' + metric][:-1])
                        else:
                            column2Add.append(df[algorithm + '_' + metric])
                num2Add = len(maxDomain) - len(dfs)
                for i in range(num2Add):
                    column2Add.append([NaN]*len(stageSetup))
                column2Add = column2Add[::alternativeVal]
                column2Add = np.reshape(column2Add, (len(column2Add), len(stageSetup)))
                                
                for i in range(len(stageSetup)):
                    lineOption = ''
                    if metric == 'lambdas':
                        dfList[algorithmList.index(algorithm)]['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + "]:\lambda_" + str(stageSetup[i] + 1) + '$'] = column2Add[:,i]
                    elif metric == 'cost':
                        dfList[algorithmList.index(algorithm)]['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + "]:\left|\mathbb{X}_" + str(stageSetup[i] + 1) + "\\right|\\times c_" + str(stageSetup[i] + 1) + '$'] = column2Add[:,i]
                    elif metric == 'samples':
                        dfList[algorithmList.index(algorithm)]['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + "]:\left|\mathbb{X}_" + str(stageSetup[i] + 1) + '\\right|$'] = column2Add[:,i]

                    # dfList[algorithmList.index(algorithm)]['$[S_' + ',S_'.join(map(str, stageSetup)) + "]:\lambda_" + str(stageSetup[i] + 1) + '$'] = column2Add[:,i]
                    
                    if len(stageSetup) == 2:
                        if stageSetup[i] == 0:
                            lineOption += '-or'
                        elif stageSetup[i] == 1:
                            lineOption += '-vg'
                        elif stageSetup[i] == 2:
                            lineOption += '-^b'
                        elif stageSetup[i] == 3:
                            # lineOption += '#F8BCBD'
                            lineOption += 'k'
                    elif len(stageSetup) == 3:
                        if stageSetup[i] == 0:
                            lineOption += '-or'
                        elif stageSetup[i] == 1:
                            lineOption += '-vg'
                        elif stageSetup[i] == 2:
                            lineOption += '-^b'
                        elif stageSetup[i] == 3:
                            lineOption += 'k'
                    elif len(stageSetup) == 4:
                        if stageSetup[i] == 0:
                            lineOption += '-or'
                        elif stageSetup[i] == 1:
                            lineOption += '-vg'
                        elif stageSetup[i] == 2:
                            lineOption += '-^b'
                        elif stageSetup[i] == 3:
                            lineOption += 'k'
                    if metric == 'lambdas':
                        lStyle['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + "]:\lambda_" + str(stageSetup[i] + 1) + '$'] = lineOption
                    elif metric == 'cost':
                        lStyle['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + "]:\left|\mathbb{X}_" + str(stageSetup[i] + 1) + "\\right|\\times c_" + str(stageSetup[i] + 1) + '$'] = lineOption
                    elif metric == 'samples':
                        lStyle['$[S_' + ',S_'.join(map(str, np.array(stageSetup )+1)) + "]:\left|\mathbb{X}_" + str(stageSetup[i] + 1) + '\\right|$'] = lineOption
                    
            # dfList[0].plot(figsize=(10, 8.5), style = lStyle, linewidth=0.8, alpha=0.7, label=list2Plot, ax=ax)
            dfList[0].plot(figsize=(7.5, 6.5), style = lStyle, linewidth=0.7, alpha=0.7, ax=ax, markevery=10, markersize=2)
            # ax = dfList[1].plot(figsize=(7.5, 6.5), style = lStyle, linewidth=0.8, linestyle = 'dashed', alpha=0.7, ax=ax)
            legend = ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), frameon = 1, fontsize = 'small', prop=font)
            # plt.xlim(0, 1*1000*(10**5))
            plt.xlim(0,3*(10**8))
            
            # legend = plt.legend(frameon = 1, fontsize = loc='center left', bbox_to_anchor=(1.0, 0.5)
            # legend = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), frameon = 1, fontsize = 'small', prop=font, ncol=2)
            frame = legend.get_frame()
            frame.set_color('white')
            # if s_i == 2:
            #     plt.xlabel('Total computational budget $C$')
            # if s_i == 1:
            #     if metric == 'lambdas':
            #         plt.ylabel('Screening threshold $\lambda_i$')
            #     elif metric == 'cost':
            #         plt.ylabel('Cost consumed each stage')
            #     elif metric == 'samples':
            #         plt.ylabel('The number of input samples $\left|\mathbb{X}_i\\right|$')
            if s_i == 2:
                plt.xlabel('Total computational budget')
            if s_i == 1:
                if metric == 'lambdas':
                    plt.ylabel('Screening threshold')
                elif metric == 'cost':
                    plt.ylabel('Resources used by each stage')
                elif metric == 'samples':
                    plt.ylabel('The number of input samples at each stage')
            plt.grid(True)
        plt.tight_layout()
        plt.savefig(outPath + fileName.replace(restultPath, "").replace(".pickle", "") + "_" + metric + ".pdf", transparent=True)
        plt.close()     

if __name__ == "__main__":
	main()