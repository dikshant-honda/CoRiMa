#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test executing prediction and risk values
#
# Copyright (C)
# Honda Research Institute Europe GmbH
# Carl-Legien-Str. 30
# 63073 Offenbach/Main
# Germany
#
# UNPUBLISHED PROPRIETARY MATERIAL.
# ALL RIGHTS RESERVED.
#
#

import json
from copy import deepcopy
from pathlib import Path
import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import allclose

from risk_model_wrapper.run_risk_model import (
    _annotate_input_data_with_risk,
    _extract_data_points,
    _load_input_data,
    predict_collisions,
)

dictionary = {}

x1 = [-4.000019720344329, -4.000019733387448, -4.000019736599594, -4.000019739811751, -3.9982361368776536, -3.996061275969366, -3.9890564844438905, -3.984408928900666, -3.9789177263895232, -3.9669494033003008, -3.960596709917828, -3.939967591074576, -3.9229157211362513, -3.912878062893719, -3.9029741938305222, -3.893069656793929, -3.8729892687563527, -3.852907452821302, -3.843011292538729, -3.8331136932580607, -3.803110049782753, -3.7929051848950874, -3.7830019504390324, -3.762933409014334, -3.7530378885189495, -3.7329447868070145, -3.723045848696703, -3.713145131803525, -3.693037954300954, -3.6630630957303913, -3.653167021715505, -3.6429714391564416, -3.6231760618383384, -3.603073841330614, -3.582964983531982, -3.5730625991502376, -3.5529942691521312, -3.533203081840523, -3.5230052427601386, -3.513105576664214, -3.493000821650278, -3.462996902323181, -3.4531242667060824, -3.433030893267383, -3.413234452834819, -3.403033652948091, -3.3730219931685412, -3.3430540696870907, -3.333158273612361, -3.3130630142757327, -3.303162865213388, -3.293260975040285, -3.2530627988466105, -3.23328569030357, -3.213191534785492, -3.1930907834183855, -3.1831876979912312, -3.1732829115930024, -3.163078812983138, -3.133113128834959, -3.1031210569139054, -3.093220463439881, -3.073113740690042, -3.063209050245585, -3.0431323045344576, -3.023345118619924, -2.9933503020210006, -2.9732449638406866, -2.9633400427232153, -2.9432460586943523, -2.923172975070384, -2.903379041982702, -2.8832786471907124, -2.8631710356054416, -2.8532668285113902, -2.823301085389857, -2.8032082289567866, -2.783409188532845, -2.7533980527710415, -2.7333163817744115, -2.723427837235115, -2.7033364344298323, -2.6832385418622047, -2.663433601411746, -2.6433250185624684, -2.613360671643645, -2.6034645999266566, -2.5833679376701957, -2.5632643083546167, -2.54345534940439, -2.5233844825156115, -2.5032929968520232, -2.4834974785106705, -2.4534914457572503, -2.4234995112405797, -2.413315794160345, -2.3935246207213803, -2.3734271111233074, -2.353322478415453, -2.323317709390301, -2.3035486643489946, -2.283455495833607, -2.2633557909296593, -2.253453274877738, -2.2234431134482073, -2.2033767323004514, -2.1934809696463575, -2.153583964655467, -2.133475303293581, -2.123572295285982, -2.0936093670671787, -2.0735152775034953, -2.053414595565618, -2.0336068800020386, -2.0036355841351097, -1.9736448892876777, -1.9535456169856542, -1.9235343203494273, -1.8935659943847059, -1.8734741209279433, -1.8434743705944336, -1.8236659822143677, -1.7936952680951614, -1.773603000538023, -1.7436051957773475, -1.7234976895713445, -1.683627933693646, -1.663535048318466, -1.6335339093452375, -1.6035227175113884, -1.5735606936177433, -1.553766068942025, -1.523761609871213, -1.4835865984152063, -1.473689370147787, -1.433796225153832]
y1 = [2.750145768701677e-06, 2.8269651253693045e-06, 2.845883431240824e-06, 2.8648017789872105e-06, 3.073048903811444e-06, 3.0357808027199003e-06, 2.401542291521476e-06, 1.4150242228209289e-06, -7.370295741644915e-07, -2.4597003205079663e-05, -4.9607212992642215e-05, -5.500146669030254e-05, -7.178735872549868e-05, -8.410199455241576e-05, -9.616672878260196e-05, -0.00010768554658272667, -0.00012955853985726284, -0.00015362431007006217, -0.00016449374400497214, -0.00017456019010974696, -0.0002007234971828442, -0.00020847629715239682, -0.0002155866389709825, -0.0002306189267393602, -0.00023881540144734615, -0.00025347573713511697, -0.00025988257415914277, -0.00026582357993514656, -0.00027695259999941, -0.00029278740505843246, -0.0002987055268712383, -0.00030437585253899997, -0.00031416078653435356, -0.00032282259484902513, -0.00033101033725031753, -0.00033502003091533106, -0.00034449402320524424, -0.00035334471307217223, -0.0003573941264196227, -0.00036101607441856156, -0.00036807906970643355, -0.0003792217138899729, -0.0003830461292775013, -0.00039144333064696635, -0.0003983681070828274, -0.00040163503560770994, -0.00041128422607771274, -0.0004228783136046699, -0.0004267441200080186, -0.00043373099577375285, -0.00043686914603354327, -0.0004399451284904343, -0.000453935632351445, -0.00046142632868529667, -0.0004686585547828199, -0.0004751026850995838, -0.0004781829601615717, -0.0004813332497956113, -0.00048465104955647167, -0.000496438507721603, -0.0005072841954813739, -0.0005105608163273153, -0.0005170337733969539, -0.0005202994027177979, -0.0005279564513365185, -0.0005357863089892956, -0.0005460248216796512, -0.0005522750430335947, -0.000555405092874644, -0.0005628402668102706, -0.0005703899534081119, -0.0005774458240642286, -0.0005838693243606381, -0.0005901023792638443, -0.0005931981185667524, -0.0006045352406271826, -0.0006116666881325865, -0.0006177048439504418, -0.000626459260063604, -0.000633613444816714, -0.0006370617103769691, -0.0006441473959944834, -0.0006502813550624558, -0.0006560571413139674, -0.0006621830934226809, -0.000673562869308072, -0.0006771373560661469, -0.0006837659086490458, -0.0006898937652969158, -0.00069605363619233, -0.0007034054747080976, -0.0007111064315209225, -0.0007177049702372364, -0.0007265853452024957, -0.0007366927949419049, -0.0007400740013378834, -0.0007472346111909054, -0.0007534887890540603, -0.0007593868451425507, -0.0007690806939343526, -0.0007766554198211447, -0.0007837171216464761, -0.0007899631160597044, -0.000792939021545648, -0.0008023797300974741, -0.0008104565181256321, -0.0008142522693398773, -0.0008272887085830437, -0.000833423725137361, -0.000836480813981054, -0.000847831186727612, -0.0008547239984671959, -0.0008610700412274823, -0.0008672288778365716, -0.0008778275069850383, -0.0008892602274737542, -0.0008958018477926384, -0.000905192094056196, -0.0009164434309281589, -0.0009239505985219699, -0.0009335606813353987, -0.0009396608313597506, -0.0009502900611398262, -0.000958090225436964, -0.0009677087954426396, -0.0009737814166495676, -0.0009880901944968464, -0.0009952876977604734, -0.0010046246617627652, -0.0010139050159772931, -0.001025512063664532, -0.001032287247775774, -0.0010415987051666767, -0.0010554318315187656, -0.0010595744451576516, -0.001072910874306187]
x2 = [-2.5358580080612675e-06, -2.6126650356641804e-06, -2.6315803050902534e-06, -2.6504956163711873e-06, -1.420397928087291e-06, 4.26517590363531e-07, 7.310848769061958e-06, 1.2824895220689394e-05, 2.0753128969931495e-05, 5.888516674352851e-05, 9.184138818824887e-05, 0.0001317726593648585, 0.00018643088192686334, 0.0002257099060705077, 0.0002641308885619776, 0.00030041605605703317, 0.0003646471154481836, 0.0004335386867543466, 0.0004647781100320275, 0.0004937713836290279, 0.0005692872175353579, 0.0005914585796596654, 0.0006113082012639963, 0.0006495531122368235, 0.0006701945556514489, 0.0007078456557410037, 0.0007243088036692359, 0.000739539850775425, 0.0007677211335101568, 0.0008049738652142249, 0.0008188317823523778, 0.0008321166244399248, 0.0008551964505988036, 0.0008752453228189731, 0.0008928900722507512, 0.0009008454232772315, 0.0009183145527375337, 0.0009354222960043457, 0.0009433917417309405, 0.0009505901635999932, 0.0009639794143126548, 0.0009822230942458728, 0.0009883917131005894, 0.0010018156156502446, 0.001012927880160733, 0.0010180032255912256, 0.001031645564169232, 0.0010465679445548419, 0.001051580241519972, 0.0010606733210710157, 0.0010646903830810197, 0.0010685349049804646, 0.0010847851827171537, 0.0010934405445178804, 0.0011016674140608103, 0.0011089381879069496, 0.0011123894862155818, 0.0011158336084212662, 0.001119436733047572, 0.0011321869510261095, 0.0011437995873741274, 0.0011472522919005988, 0.0011539716984193802, 0.001157341031756765, 0.001165258714982976, 0.0011736077148471347, 0.0011843455396134586, 0.001190664344124549, 0.0011936654859255815, 0.001201004173034758, 0.001208462518753525, 0.0012153151243683917, 0.0012213176958830727, 0.0012272230576418322, 0.001230270600189202, 0.0012417179532066252, 0.0012491023634623169, 0.0012555073282285874, 0.0012645991940681367, 0.0012719219488733673, 0.0012755580369832838, 0.0012830141836265975, 0.0012894295386210188, 0.0012953863344013954, 0.001301627695528129, 0.0013134048817213246, 0.0013171356958581613, 0.0013239518415183655, 0.0013301858027144231, 0.00133641724721128, 0.0013438400336261952, 0.001351791132080661, 0.001358654058317006, 0.0013679705304735215, 0.0013787417146103444, 0.00138244498184044, 0.0013901674611523022, 0.0013968566054777516, 0.00140312221164981, 0.0014132961577577956, 0.0014212144039294412, 0.0014284998562668174, 0.0014349143145100192, 0.001437935865990613, 0.0014475754267111033, 0.0014559030421050275, 0.0014598370172874892, 0.001473280311978886, 0.0014795862105779463, 0.0014827611425229105, 0.0014946833700692815, 0.0015018918149310894, 0.00150837386497394, 0.0015146174203187692, 0.001525469395476375, 0.001537279777749214, 0.0015439572412519382, 0.001398662527422395, 0.0009167876818783616, 0.00036399826052789205, -0.0009898324996461436, -0.00228600908179165, -0.00487341512852786, -0.006996150701183828, -0.009979705588746363, -0.011418637895584128, -0.012662903292180623, -0.012737359081950445, -0.012782086604968882, -0.012781460812716552, -0.012828177426618346, -0.012827779973322307, -0.012878651605798657, -0.012877895501541649, -0.012877707967479156, -0.012907384441311584]
y2 = [-3.0000196940497545, -3.0000197074950457, -3.0000197108062348, -3.0000197141174376, -2.998236062797125, -2.996061142788963, -2.989056157833601, -2.9844084711102465, -2.978917110845837, -2.9669484607324006, -2.9605956051302207, -2.9399660111896457, -2.922913945339948, -2.912878719958933, -2.902976120299891, -2.893072415372401, -2.8729933132771666, -2.852928721827327, -2.843033810901388, -2.8331376902695258, -2.803137385231936, -2.792933218670659, -2.7830304107430144, -2.762971401470666, -2.753076644082904, -2.7329850965727096, -2.72308696325773, -2.713186887579393, -2.69308049411435, -2.6631079436435345, -2.6532142804396783, -2.643019200609475, -2.6232248428831713, -2.6031235013182914, -2.583015087258527, -2.5731129304005704, -2.553047484586354, -2.5332565474133535, -2.5230589547642674, -2.5131595452584463, -2.4930551810859725, -2.4630523198557697, -2.4531808032342206, -2.433087819051861, -2.4132917908737612, -2.4030911730038547, -2.3730797957648053, -2.3431138958702773, -2.3332181323619663, -2.3131230734782147, -2.303223013588661, -2.2933211896483923, -2.253124553808104, -2.2333483600327866, -2.2132543285502604, -2.193153625203572, -2.183250575306054, -2.1733458138185555, -2.1631417267088646, -2.133178285751484, -2.103186348747545, -2.0932857970602528, -2.0731791131481603, -2.0632744198941944, -2.0431995321282432, -2.0234123609250574, -1.993417682637913, -1.9733124801278334, -1.9634075731100549, -1.9433146490783673, -1.9232426112109102, -1.9034487988310262, -1.883348488073532, -1.8632408091101167, -1.8533365766615386, -1.8233726128078893, -1.803279681309911, -1.783480643741724, -1.753469594113295, -1.7333895703972075, -1.723501796365481, -1.7034104475868435, -1.6833126275324566, -1.6635077195531183, -1.643399158470979, -1.613437159785699, -1.603541141973712, -1.5834445590256327, -1.5633409582909505, -1.543532027458617, -1.523463260233682, -1.5033720519572373, -1.483576554646864, -1.4535704908638694, -1.4235800048549452, -1.4133975953334728, -1.393606476306831, -1.3735090260561782, -1.3534044374376375, -1.3234003529712566, -1.3036333476278197, -1.2835402150967652, -1.2634405790840744, -1.2535380635299442, -1.2235280766000898, -1.203464350640457, -1.1935686722289607, -1.1536717525628954, -1.133563084699535, -1.1236600917682822, -1.093699476920697, -1.0736054703606261, -1.053504874969631, -1.0336971694694872, -1.0037278592129957, -0.9737364868357444, -0.9536372537850601, -0.9237243370720423, -0.8938750801770851, -0.8739041733488362, -0.8441425252935072, -0.8245408071158178, -0.7962563176027294, -0.7788096031189643, -0.7569753196332941, -0.7463639925254452, -0.7359575216315479, -0.7351423810512193, -0.734621080284222, -0.7346291350282673, -0.7340844507138176, -0.7340895323886187, -0.7334999875359839, -0.7335097355772768, -0.7335121432559154, -0.7331744417141001]

for i in range(len(x1)):
    dictionary.update(
        {str(time.time()):
            {"data":[
                    {
                        "type":"object",
                        "position":[x1[i], y1[i], 0],
                        "velocity":[2, 2, 0],
                        "label_id": 14,
                        "label_name": "car",
                        "tracking_id": 14
                    },
                    {
                        "type":"object",
                        "position":[x2[i], y2[i], 0],
                        "velocity":[2, 2, 0],
                        "label_id": 7,
                        "label_name": "car",
                        "tracking_id": 7
                    }
                ]
            }
        }
    )

json_object = json.dumps(dictionary, indent = 4) 

with open("/home/dikshant/catkin_ws/src/CoRiMa/smart_cooperative_intersection_wrapper-main/data/Export_Honda/example1/sample.json", "w") as outfile:
    outfile.write(json_object)

for path in Path("/home/dikshant/catkin_ws/src/CoRiMa/smart_cooperative_intersection_wrapper-main/data/Export_Honda").glob("*"):
    honda_export_file_path = path.joinpath("sample.json")

    print(f"Testing: {honda_export_file_path.as_posix()}")

    input_data = _load_input_data(honda_export_file_path.as_posix())
    annotated_input_data = deepcopy(input_data)

    for timestamp, sample in input_data.items():
        if len(sample["data"]) == 0:
            continue
        data_points = _extract_data_points(sample["data"])
        predicted_collisions = predict_collisions(data_points)
        annotated_input_data[timestamp] = _annotate_input_data_with_risk(sample, predicted_collisions)

json_object_2 = json.dumps(annotated_input_data, indent = 4) 

with open("/home/dikshant/catkin_ws/src/CoRiMa/smart_cooperative_intersection_wrapper-main/data/Export_Honda/example1/processed_sample_data.json", "w") as outfile:
    outfile.write(json_object_2)