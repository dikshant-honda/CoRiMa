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

x1 = np.array([-0.5, -0.5002281522086193, -0.5002295843999113, -0.5002314953665513, -0.500235681839131, -0.5002510700237066, -0.5002777401773031, -0.5003143968491403, -0.5003295512425942, -0.5004108661888768, -0.5004542843227393, -0.5005082540616579, -0.5007058970320863, -0.5009567688489791, -0.5011291293874073, -0.501343091228792, -0.5016117636100976, -0.5028329183723099, -0.5034807347670252, -0.5051780809571819, -0.5082062195394617, -0.510139978924963, -0.5109855767007265, -0.5117802535481341, -0.5125052402872736, -0.5143595819667051, -0.5153441979277122, -0.5165326135166299, -0.5168515738821803, -0.5174044945886085, -0.5176454777801954, -0.5178759491616987, -0.5182799633595094, -0.5187567564008679, -0.518901796831672, -0.519149944718469, -0.5193467341766694, -0.5195147747374579, -0.5195960056552694, -0.5197322008814693, -0.5198389027363712, -0.5199517648585945, -0.5200419550055722, -0.5201083316590976, -0.5201444323876476, -0.5202526667461329, -0.5203006416108343, -0.5203570659100458, -0.5204273169710146, -0.5204572716877038, -0.5204808566372537, -0.5205014904611738, -0.5205446815877511, -0.5205715481716172, -0.5205869748324132, -0.5205996681688444, -0.5206347786068464, -0.5206465121996339, -0.5206671359320805, -0.5206771159008327, -0.5206857450778942, -0.5206958827922329, -0.5206980108740029, -0.5207068582797236, -0.52071008281104, -0.5207096882316253, -0.5207114266911055, -0.5207101122554186, -0.5207042375115777, -0.5206997069056779, -0.5206956988778233, -0.5206818955068976, -0.5206666854494607, -0.5206585850712687, -0.5206240978180051, -0.5206113907273509, -0.5205896489708755, -0.520560349434429, -0.5205442799469405, -0.5205071256242556, -0.520490834169791, -0.5204708740109468, -0.5204364926563031, -0.5204220808455334, -0.5204027964680065, -0.5203832935195982, -0.5203342470297019, -0.520323856173884, -0.5202987197376052, -0.5202672553096558, -0.5202371356442463, -0.520191357899291, -0.5201798675121195, -0.5201592400072708, -0.5201139349679902, -0.5200904534204912, -0.5200662418525267, -0.5200209938809157, -0.5200007114859165, -0.5199735808974572, -0.5199426176829187, -0.5199122450066492, -0.5198983752867322, -0.519856888544078, -0.5198476804582877, -0.519806133200253, -0.5197761228126804, -0.5197561080573921, -0.5197275429803557, -0.5196866616635526, -0.5196620262815502, -0.5196474898314547, -0.5195956934893194, -0.5195687494690656, -0.5195540544626354, -0.5195187302331516, -0.5195062216825871, -0.519460868102645, -0.5194297246359415, -0.5194163308932881, -0.5193629337750554, -0.5193389009621922, -0.519324656199453, -0.5192844833913011, -0.5192599763637267, -0.5192294016268124, -0.5192130097941137, -0.5191801075328661, -0.5191325261508959, -0.5190991704747507, -0.5190847842183176, -0.5190519716704268, -0.5190301119208472, -0.5189738383355732, -0.5189504878878788, -0.5189405234017076, -0.5189130335466234, -0.5188630515049971, -0.518836041140278, -0.5188038421080267, -0.518784275021372, -0.5187418304594095, -0.5187126532964512, -0.5186911922950238, -0.5186616339188087, -0.5186202638560302, -0.5186084566669242, -0.5185624435369853, -0.5185372533850643, -0.518498550767347, -0.5184674447348765, -0.5184486287670148, -0.5184079315276832, -0.5183908887339634, -0.5183607572376623, -0.5183153967898559, -0.5182939177277431, -0.5182675423760611, -0.5182219176895833, -0.5182002396157157, -0.5181548664198173, -0.5181301979720995, -0.5180900384855649, -0.5180562280707717, -0.5180352542886221, -0.5180216593155145, -0.5179600651982635, -0.5179360888001815, -0.5178872493559357, -0.5178624531666973, -0.5178191597326495, -0.5177765634571928, -0.5177517588645807, -0.5177217041873998, -0.517685159847717, -0.5176417536834954, -0.5176143681979994, -0.5175906391680078, -0.5175759464436372, -0.5175204530744673, -0.5174927025826797, -0.5174463313533895, -0.5174251906215479, -0.5173960519939201, -0.5173416998464464, -0.51731295933254, -0.5172798021875479, -0.5172465234837023, -0.5172167956753431, -0.5171634157276127, -0.517148938134009, -0.5171021367112669, -0.5170499955231872, -0.5170062836230331, -0.516978875727961, -0.5169462365591723, -0.516891842187876, -0.5168432140346089, -0.5167964095295342, -0.5167811825738445, -0.5167302620882757, -0.5167011209437967, -0.5166706878477458, -0.5166196147601291, -0.5166035343974504, -0.516552182099824, -0.516502952842591, -0.5164674497039697, -0.5164362560961476, -0.5163960140118533, -0.5163505899890788, -0.5163085861007165, -0.516265247707855, -0.5162483490960849, -0.5161941573927263, -0.5161620107480558, -0.5161215215548896, -0.5160745111357496, -0.5160453593959332, -0.5160028485734351, -0.5158732643746535, -0.5153652177237863, -0.5153097170338897, -0.515169275709338, -0.5146851864816201, -0.5136256527744172, -0.5133225798121529, -0.5132441333641085, -0.5134154925153033, -0.513455122436317, -0.5134718923102131, -0.5134844714567041, -0.5134845284104824, -0.513514233139519, -0.5135316905990422, -0.513563150962097, -0.5135769701919132, -0.5135966452943856, -0.5136107731610521])
y1 = np.array([-10.0, -10.000044613033007, -10.000044845300287, -9.999606935090526, -9.998261877387819, -9.993063583165323, -9.984438370208105, -9.973107016055444, -9.960833007884297, -9.947440117996056, -9.939888666247644, -9.931236975629979, -9.902175888075675, -9.88135850284934, -9.869479425278294, -9.85712143575145, -9.844168101379795, -9.803418200015454, -9.788329246406411, -9.756981245241542, -9.708082758160781, -9.674553931539728, -9.658015510831207, -9.64099833195001, -9.624515253143786, -9.574474997092592, -9.54090978868918, -9.490923216369687, -9.47439989107171, -9.440843399411746, -9.424353328722143, -9.407863311851697, -9.374353923593647, -9.324315546641516, -9.307826812605251, -9.274326757191288, -9.240780936293868, -9.207801058814935, -9.190813369146818, -9.157797138751011, -9.124270646017333, -9.090806014404775, -9.05779749030223, -9.024263494553201, -9.007785934941419, -8.957802449697265, -8.924264962942734, -8.890803756940723, -8.840791800275895, -8.807786998094205, -8.7908081931751, -8.774320647454156, -8.724283948123102, -8.690813744372639, -8.674327857336696, -8.657830750637592, -8.590815884154441, -8.574334316915316, -8.524312161489812, -8.490815826869024, -8.474339338881139, -8.440843988166945, -8.407806589775609, -8.374341927058444, -8.357854245432733, -8.307816595692774, -8.274342707499924, -8.240857792699883, -8.207824383578627, -8.15785761101777, -8.140862167926448, -8.107833089993951, -8.057859330303943, -8.040866668753333, -7.990822862247728, -7.957861566878499, -7.924369017670899, -7.89083248169545, -7.85786604148542, -7.807865149927769, -7.790843866074483, -7.757870128793536, -7.707877793444489, -7.6908568678710685, -7.657870608476061, -7.624395757658093, -7.557867605818576, -7.540894014939185, -7.507898505594174, -7.474361242662387, -7.424409865943469, -7.374372885407902, -7.357867631064232, -7.324416372854479, -7.274384907589995, -7.240906963624997, -7.207927016467007, -7.157881184011722, -7.124428665204069, -7.090929856887713, -7.0578927940237355, -7.0079441782498435, -6.990940967307155, -6.940905262309816, -6.924438954784477, -6.874437286286768, -6.8409075633048255, -6.807957286261073, -6.774449632437841, -6.724444693891467, -6.6909699816443045, -6.674462251826284, -6.607969403670763, -6.574474251051837, -6.557957012943474, -6.507974690120601, -6.4909865052008255, -6.440948841710819, -6.390993309827608, -6.374494610494057, -6.307983871805194, -6.274503965513813, -6.257994779009419, -6.207982704689657, -6.174512583016301, -6.140987359471276, -6.1244686614946025, -6.074520891496382, -6.024480899438702, -5.974528762820197, -5.958028639722855, -5.92449396743184, -5.891022560961315, -5.824506997102896, -5.791024502873899, -5.774542077495202, -5.741039757569249, -5.674547858494453, -5.641051575909137, -5.608014374095179, -5.574552806828414, -5.524547386608114, -5.491022898175181, -5.458071770875657, -5.424560519263274, -5.374563030192158, -5.358078088868488, -5.308052860743953, -5.274563076825368, -5.224585769546738, -5.191047928837633, -5.158089600577861, -5.108080422140981, -5.0910596961047725, -5.041107755491901, -4.99107182255404, -4.958100888717397, -4.924617442303896, -4.874571085494803, -4.841122055840098, -4.791099206620472, -4.758102467286635, -4.7081311185849835, -4.674593481012932, -4.641133029293529, -4.6246443394063, -4.558102090232045, -4.524652303248144, -4.4746195675539795, -4.441145068800434, -4.3911543922357925, -4.34114660550501, -4.308174817306521, -4.2746491679251974, -4.224673415668273, -4.174663048168013, -4.1411453896263115, -4.108191576061406, -4.091190867643168, -4.024685440187501, -3.991201245382661, -3.941155025705193, -3.9082057089594824, -3.8747027968296863, -3.8082115125273206, -3.774714896303383, -3.7411771144514065, -3.6912285296772582, -3.658210886140314, -3.591236199536992, -3.574736943801952, -3.5246916059527313, -3.45823698644769, -3.4082290222046807, -3.3747566142666066, -3.341230326485061, -3.2747661225664273, -3.2247254222982225, -3.1582739109679374, -3.1412593296509224, -3.0747821042496963, -3.041272721676645, -3.00823785232186, -2.941285596213413, -2.9247655931205, -2.858303312020274, -2.808260131298878, -2.758312287238858, -2.7247941460944234, -2.6748076803593297, -2.62480832570545, -2.574813742909776, -2.5248219105200627, -2.508301228575354, -2.4413417377261624, -2.4083156114337854, -2.3583409833361064, -2.3083299486248645, -2.2748133725753092, -2.224859479925125, -2.1784329712127746, -2.123724300918525, -2.112116890413564, -2.080407828671892, -2.0526272855278744, -2.020870985588093, -2.0091044075645326, -2.0008394975816053, -1.9935317602197458, -1.9928522249406466, -1.992586701702129, -1.992412970268501, -1.9924385763819612, -1.9919645731366813, -1.9916786843773653, -1.9911581788868429, -1.9909440801763385, -1.9906145420694392, -1.9903864020528828])
x2 = np.array([9.0, 9.000043344311344, 9.000043572508545, 8.999605644871997, 8.998260533426441, 8.993062037889954, 8.9844364971811, 8.973104716343611, 8.960830302781826, 8.947436660252578, 8.939884728730465, 8.931232417231664, 8.902168587614197, 8.881348129620836, 8.869466702023548, 8.85710533929715, 8.84414693682847, 8.803370753586657, 8.788266993756189, 8.756773462122917, 8.707565551272639, 8.674029226824336, 8.65748989368663, 8.640472259256363, 8.62399276682784, 8.573968068150887, 8.540413135418298, 8.490436931818381, 8.47392020786775, 8.440367151085134, 8.423880435963513, 8.407392710505817, 8.373886643495068, 8.323844507995172, 8.307359051812739, 8.273862873900564, 8.240317878358812, 8.207335917101158, 8.19034925821284, 8.157334057914808, 8.123800207881427, 8.09033801300439, 8.057331147790237, 8.023792948439835, 8.00731438790654, 7.957332474743518, 7.923792376039744, 7.890329367278144, 7.840318571374337, 7.807307450651106, 7.790328492095586, 7.77384191240245, 7.7238045097929104, 7.690329621961652, 7.673844889341862, 7.657348229206659, 7.590332633414959, 7.573849493771216, 7.5238276964466095, 7.490333809753965, 7.473853408831412, 7.440358522867605, 7.4073201026048725, 7.3738556314786745, 7.357368459237479, 7.307330039127984, 7.273857364356847, 7.240374432578295, 7.207340069950768, 7.157374008120261, 7.1403794893493115, 7.10734929617757, 7.0573736203159285, 7.040382406918949, 6.990336790560592, 6.957370894671351, 6.9238795644012, 6.890341175202105, 6.857370016700465, 6.807369941412965, 6.790347488901824, 6.75737115746209, 6.707378112281839, 6.6903563250617735, 6.657371273451015, 6.623895182229314, 6.557368115569717, 6.540393255490281, 6.507398315371611, 6.473860243434692, 6.423910156212426, 6.37387250034648, 6.357365657306053, 6.3239171090439745, 6.273885419318287, 6.24040940548149, 6.207431077765816, 6.157384694808173, 6.123933951955996, 6.090436034364903, 6.057398120874041, 6.007452119264716, 5.990449355864389, 5.940411306320598, 5.923948421508985, 5.873948871097297, 5.840416979030962, 5.807470538526476, 5.773963611215748, 5.723959968041891, 5.690485080957312, 5.673977779162993, 5.607486283480175, 5.573991623512002, 5.557474469135464, 5.507493898752364, 5.49050664948999, 5.4404686450330155, 5.390516387676658, 5.374018129900913, 5.307508061379784, 5.274029550330653, 5.257520719197891, 5.207510468486705, 5.174040913337531, 5.140516080252032, 5.123996789746841, 5.07405185215154, 5.024011246776864, 4.974061272882819, 4.957561545350222, 4.924026072082395, 4.890556612225303, 4.824042632672521, 4.790562149849066, 4.77408019615484, 4.740578904869942, 4.674088702467903, 4.640593358542693, 4.607555505674069, 4.574096371363042, 4.524092457311801, 4.490565637685528, 4.457618623271747, 4.424108151982792, 4.374112086315838, 4.357628565712538, 4.307603843615673, 4.274116282905107, 4.22413902457326, 4.1906006136014575, 4.157646012799398, 4.10763778133701, 4.090616184396281, 4.04066841335069, 3.9906323629695697, 3.957663831260579, 3.9241823456737226, 3.8741355498187344, 3.840690098947701, 3.7906681978268333, 3.757673505624368, 3.707704250573109, 3.6741660001739653, 3.640708433729365, 3.6242204883474054, 3.5576772411943094, 3.5242314488566344, 3.4741985318296864, 3.4407251200442492, 3.390736452785016, 3.3407306297252726, 3.3077585717448823, 3.2742333477388503, 3.224258951277323, 3.174249621353214, 3.1407301881236913, 3.1077795062990567, 3.090779383829077, 3.024274583271098, 2.990792142004004, 2.940745101776323, 2.9077982067598995, 2.874296400495742, 2.8078061625534545, 2.774310324943884, 2.740772008276804, 2.690826056427955, 2.6578090994146635, 2.590835874125756, 2.574337028100401, 2.524290623820586, 2.4578392475068633, 2.407832339357833, 2.374361157107752, 2.3408353080942725, 2.2743723204283075, 2.224330887409067, 2.15788307619647, 2.140868760981294, 2.0743931352471425, 2.040884654966408, 2.007849072265143, 1.9409008258400506, 1.9243805520704147, 1.8579207361281354, 1.8078774814355116, 1.7579318572420701, 1.7244145094276764, 1.674427942749165, 1.6244309047597958, 1.574435555905378, 1.5244456030503137, 1.5079245371533878, 1.4409664222083856, 1.407940596482958, 1.357967395186682, 1.3079572381505948, 1.274439367140284, 1.2244870522643299, 1.1744433196299808, 1.1079892460492076, 1.0909668299475292, 1.0410081803565936, 0.9909848316642482, 0.9245249660643122, 0.8910010489400801, 0.8579921070162125, 0.7910173828542015, 0.7579931109634044, 0.7080459739462166, 0.6745106543691421, 0.6410385947219841, 0.5745268004574805, 0.5245627933940367, 0.47454328118162586, 0.4410449377049033, 0.39107681885425094, 0.3580389194094515])
y2 = np.array([-0.5, -0.5002239791064298, -0.5002254116134804, -0.5002269597719519, -0.5002299767584726, -0.5002406126707013, -0.5002585239109139, -0.5002817914285881, -0.5002801983352742, -0.500338652955218, -0.5003670387002915, -0.5004015451169296, -0.5005143720955285, -0.5006759657598185, -0.500783484756729, -0.5009164336104756, -0.5010823417718683, -0.5018429814360013, -0.502262114165487, -0.5034247820327052, -0.5056013360990305, -0.5069769651611324, -0.507575978800422, -0.5081362816162777, -0.5086562005178681, -0.510002281924751, -0.510738670704597, -0.5116754515375624, -0.5119358360132573, -0.5123989330991404, -0.5126035725425184, -0.5128040588112305, -0.513156542085561, -0.5135779802635985, -0.5137111123642216, -0.5139409221806107, -0.5141304633120078, -0.5142956175919884, -0.5143768154745567, -0.5145155327797484, -0.5146216768625169, -0.5147361984633848, -0.5148292323306132, -0.5149003792193662, -0.5149379008957486, -0.5150557222058174, -0.5151101684292781, -0.5151719687531351, -0.5152535536090019, -0.5152889927899094, -0.5153174768075225, -0.5153417103635807, -0.5153977790926043, -0.5154303364050746, -0.5154500277782427, -0.5154669077180913, -0.5155166957290498, -0.5155339696903182, -0.5155697910357789, -0.5155857712250094, -0.5156009269180858, -0.5156224343697311, -0.5156335998776412, -0.5156517285102621, -0.5156607098170402, -0.5156763879169015, -0.515688011922723, -0.5157008769623975, -0.5157060681865012, -0.515717732221661, -0.515721069213317, -0.5157233454976504, -0.5157282168278544, -0.5157294617556066, -0.5157265847007746, -0.5157272025163272, -0.5157237878332612, -0.5157146413961491, -0.5157095890454777, -0.5156927017544771, -0.5156814121498526, -0.5156667166255661, -0.5156392494297624, -0.5156258490604319, -0.5156047149154748, -0.5155835935268993, -0.5155315532159511, -0.51551949506531, -0.51549196048234, -0.5154587511707388, -0.5154220424506972, -0.5153732725434488, -0.5153587302020614, -0.5153327165538842, -0.5152820361027319, -0.5152533949015203, -0.515221665781118, -0.5151679006722266, -0.5151407309078709, -0.5151071853086753, -0.5150700735083789, -0.515027652653991, -0.5150105545787929, -0.5149595429796235, -0.5149458748747006, -0.5148950862482436, -0.5148588082100596, -0.5148311104589554, -0.5147962888100696, -0.5147461646648955, -0.5147129490068191, -0.5146956486652093, -0.5146306614370043, -0.5145961952679086, -0.5145783781713918, -0.514530566120147, -0.5145136630014129, -0.5144592799137138, -0.5144144323097704, -0.514397611229593, -0.5143318859521533, -0.5142988913700884, -0.5142817996729374, -0.5142319804360551, -0.5141987169033256, -0.5141629065938706, -0.5141428786113919, -0.5140975072329761, -0.5140401678092419, -0.5139921142096866, -0.5139739648495272, -0.5139345144764308, -0.5139028375716685, -0.513827235210229, -0.5137941489565556, -0.5137769394161941, -0.51373981387217, -0.5136702936809626, -0.5136337778038048, -0.5135938335087809, -0.5135632457906039, -0.5135077584391745, -0.5134696697042889, -0.5134377602703472, -0.513400123295456, -0.5133470255524671, -0.5133291606253578, -0.5132720578553821, -0.5132383538028715, -0.5131840523381731, -0.5131429878024478, -0.5131124202818523, -0.5130555581292131, -0.5130334446995368, -0.5129821701304147, -0.5129215205182864, -0.5128879757482658, -0.5128482869216533, -0.5127868493328963, -0.5127528924964575, -0.5126931242284756, -0.5126580390107032, -0.5126017983768243, -0.512560351478688, -0.5125280577112828, -0.5125095920171842, -0.512432500385404, -0.5123991259985305, -0.5123401975445603, -0.5123060563925699, -0.5122479416873417, -0.5121937649961849, -0.5121590309864152, -0.512122661858425, -0.5120732320798435, -0.5120207872626383, -0.5119857177974882, -0.5119535913479261, -0.5119357872537755, -0.5118682461486401, -0.5118329300074186, -0.5117768414049858, -0.5117463901425228, -0.5117101134476474, -0.511640837519029, -0.511605085398912, -0.5115658412688654, -0.5115187350175936, -0.5114835192719003, -0.5114146715919151, -0.511397065785525, -0.511340203667182, -0.5112717898429697, -0.5112180754988958, -0.5111817490411976, -0.5111442769847899, -0.511073922809326, -0.5110151344888854, -0.5109453903506018, -0.5109260096451812, -0.5108527516298985, -0.5108147026973042, -0.5107745279256609, -0.5107031333480198, -0.5106833925800025, -0.5106091770705847, -0.510546836997685, -0.5104929067814707, -0.5104536163839105, -0.5103974859488409, -0.5103406506067594, -0.5102876702428635, -0.5102341041049168, -0.5102152292157204, -0.5101459247532398, -0.5101098243386193, -0.5100577425240572, -0.5100022694834904, -0.5099643979799697, -0.5099104533048368, -0.5098520293980752, -0.5097823770901195, -0.5097620068975692, -0.5097092881087477, -0.5096533136178714, -0.5095841542343346, -0.5095479604085495, -0.509512446518587, -0.5094401743043206, -0.5094020097538045, -0.509349542261988, -0.509310257850244, -0.5092752654809545, -0.5092001878813525, -0.5091472746096315, -0.5090913037444555, -0.5090546902074314, -0.5089990063224595, -0.5089591096055295])
for i in range(len(x1)):
    dictionary.update(
        {str(time.time()):
            {"data":[
                    {
                        "type":"object",
                        "position":[x1[i], y1[i], 0],
                        "velocity":[0, 0.5, 0],
                        "label_id": 14,
                        "label_name": "car",
                        "tracking_id": 14
                    },
                    {
                        "type":"object",
                        "position":[x2[i], y2[i], 0],
                        "velocity":[0.5, 0, 0],
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