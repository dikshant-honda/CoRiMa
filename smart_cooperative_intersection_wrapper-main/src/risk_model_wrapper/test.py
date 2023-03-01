#!/usr/bin/env python3

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

x1 = np.array([-0.9000146578820524, -0.89991759442514, -0.8998057780082596, -0.8994599093641423, -0.8989922527385608, -0.8989922527385608, -0.8981588679258112, -0.8970703414338622, -0.8949146276514374, -0.8938611986957126, -0.8928390446328108, -0.8918571650360159, -0.890904565501907, -0.8899843242018943, -0.8890946662054702, -0.8882221103255477, -0.8873778082687547, -0.8865542583911289, -0.8857529525043863, -0.884965173249616, -0.8834655372794189, -0.8827445135700045, -0.8820455438990475, -0.8813676255458529, -0.8807098852451236, -0.8800711941535921, -0.8794505973567343, -0.878847224587346, -0.8782604869382488, -0.8776900609200412, -0.8771358920480254, -0.8760752795010334, -0.8755691818459073, -0.8750783805126131, -0.8746016912126384, -0.8741382584691687, -0.8736931926115877, -0.8732557459316731, -0.8728312332131825, -0.8724192585469429, -0.8720196748145219, -0.8716317974744905, -0.870889111984962, -0.8705331280447979, -0.870187792012735, -0.8698525493737013, -0.8695270723835326, -0.8692110665107132, -0.868904247673323, -0.8686063436189688, -0.8683170947342237, -0.8680419700574844, -0.8677690706037193, -0.8675035693160534, -0.8672462010016111, -0.8669956496874457, -0.8665191613215202, -0.8662914696465852, -0.8660705856462472, -0.8658562025957458, -0.8656478695613935, -0.8654456090723154, -0.865249301246233, -0.8648738824081277, -0.8646938410825655, -0.8643565471707458, -0.8643565471707458, -0.8641945417345194, -0.8640354751813224, -0.8638768943581052, -0.8635749187295358, -0.8634307352183241, -0.8632903978067195, -0.8631534607054183, -0.8630198943652497, -0.8628899161325175, -0.8627639301065554, -0.8625229367337345, -0.8624086621625517, -0.862297844069584, -0.8621902641473896, -0.8621902641473896, -0.8620858115403474, -0.8619839794027069, -0.8618854926834163, -0.8616966694976115, -0.8616062962485364, -0.861518259790972, -0.8614320278284618, -0.8612692431071742, -0.8611900011314008, -0.8610320930716149, -0.8609555573888222, -0.860881283205843, -0.860809164582695, -0.8607391314529217, -0.8606711227694589, -0.8606050818798278, -0.8605414538515974, -0.8604776635323299, -0.8604142988854098, -0.8603544374102522, -0.8602941272805621, -0.8602354672034709, -0.8601785365957244, -0.8601233034272623, -0.8600693567029151, -0.8600170381523398, -0.8599662922571931, -0.8599169144985251, -0.8598690468957622, -0.8598228930480233, -0.8597771311466533, -0.8597317719639768, -0.8596868916702664, -0.8595971724556408, -0.8595541225000614, -0.85951233982826, -0.8594717656674906, -0.8594323593664561, -0.859394085857125, -0.8593569135912518, -0.8593208147105247, -0.8592486179749548, -0.8592139934534611, -0.8591794075625868, -0.8591794075625868, -0.8591122791684219, -0.8590801619039324, -0.859048993591624, -0.8590183807489621, -0.8589886480278905, -0.85895953899156, -0.8588996551656843, -0.8588712880775126, -0.8588428384561984, -0.8587861637096242, -0.8587583147189064, -0.8587049987956231, -0.858630709088152, -0.8585847029065007, -0.8585411068192035, -0.8584982828608669, -0.8584566279558231, -0.8584173458104922, -0.858379786897262, -0.8583220235703344, -0.8582841560718096, -0.8582647892235318, -0.8582269715618455, -0.8581737383507443, -0.8581408029712373, -0.8581097497146203, -0.8580798156227749, -0.8580501175725778, -0.8580212250848882, -0.8579939112932646, -0.857966066348503, -0.8579404500949172, -0.8579162477804899, -0.8578934601044326, -0.8578720100988242, -0.857842914955278, -0.8578253266967567, -0.8578088056867956, -0.8577924323962913, -0.8577756298949708, -0.857759585418678, -0.8577278371651794, -0.8577129058966416, -0.8576693270550276, -0.8575328827879586])
y1 = np.array([-10.000371048802709, -9.990311541621391, -9.977386085318559, -9.957668430380728, -9.933401403138115, -9.933401403138115, -9.90530054934845, -9.87181718417792, -9.801849436612748, -9.766871298228565, -9.731892515707193, -9.696916931295355, -9.661951405530147, -9.627000361933877, -9.592058682717454, -9.557113371898884, -9.522150347441574, -9.487181062771677, -9.452244301866358, -9.417269160192456, -9.347313605184084, -9.312315176751726, -9.277315887267607, -9.242317103882865, -9.207319509884064, -9.172323427160947, -9.137328683934985, -9.102334716965327, -9.067340692411944, -9.032345720906076, -8.99734926541588, -8.927362554849138, -8.89237354152504, -8.85738441748673, -8.82239479023447, -8.787408694744574, -8.752443441275702, -8.717453561851228, -8.682463786211326, -8.64747364390945, -8.61248334734272, -8.577493066115256, -8.507524237557103, -8.472533349474284, -8.437542305119091, -8.402551131917429, -8.367559853920033, -8.332568488386437, -8.297577046731423, -8.262585536477552, -8.227593963248976, -8.19259870099023, -8.157599666934688, -8.122599340297848, -8.087597106653522, -8.052598319505048, -7.982614594230011, -7.947622591026999, -7.912630534408326, -7.877638959535174, -7.842647000597661, -7.807654717641738, -7.772662360222291, -7.702677836254788, -7.66769868460132, -7.597668208274674, -7.597668208274674, -7.562643181151418, -7.52762709098046, -7.492620526552549, -7.422612130275814, -7.387610650178999, -7.3526104886499, -7.317610870581896, -7.2826108803144045, -7.247609685897833, -7.212606713266033, -7.142609248741857, -7.107616734586067, -7.072624167346795, -7.037631574710266, -7.037631574710266, -7.002638974527783, -6.967647845155626, -6.93265745836095, -6.862672390212143, -6.827681575065543, -6.792700254038338, -6.757689796516012, -6.687646536047089, -6.652620645250035, -6.582617924739604, -6.5476252678723705, -6.51263262008428, -6.4776399829844795, -6.442647355157585, -6.407654732384151, -6.372662106439755, -6.3376705099702875, -6.30269630814634, -6.267683278732378, -6.232658894188264, -6.197666711434857, -6.162673990202959, -6.127681266000575, -6.092688548812354, -6.057699564851901, -6.022707016049262, -5.987714502461842, -5.952725430756247, -5.917735666940726, -5.882720899420122, -5.84770166328557, -5.8126783425797575, -5.777652493481041, -5.707657198443022, -5.672664469443751, -5.637671752056848, -5.602679048697162, -5.5676863586860135, -5.532693678564726, -5.497701000900757, -5.462708312842573, -5.392694565760031, -5.357668578064843, -5.322664502963477, -5.322664502963477, -5.25267900129572, -5.217686257400221, -5.182693526914562, -5.14770463841337, -5.112712306433328, -5.0777234717830275, -5.007726342241179, -4.972707609336497, -4.937684699185443, -4.867656850849682, -4.832664096213003, -4.762678604382823, -4.657700467620483, -4.587715071832315, -4.517683984336244, -4.447646095327519, -4.377660576560989, -4.307675083471818, -4.237693777648943, -4.132709921137928, -4.062669310909783, -4.027643856569385, -3.9576475860406597, -3.8526693369434377, -3.782683906675994, -3.712698498890606, -3.6426721028164244, -3.572626496456184, -3.5026409656359796, -3.432655467090458, -3.362676126039755, -3.292690937062433, -3.2227056182146745, -3.152720098634931, -3.0827344589684853, -2.977757616692702, -2.907772225337795, -2.8377868490666187, -2.7677733591899147, -2.6977218235161495, -2.6277360619445482, -2.487771187684945, -2.4177860052064672, -2.3477993804503634, -2.2777915847261543])
x2 = np.array([8.998496727553738, 8.998480964394199, 8.998477023534265, 8.995986697520864, 8.98784711189737, 8.98784711189737, 8.97423452250259, 8.95546474704392, 8.930218057760221, 8.901797989992858, 8.871799660222338, 8.841817100658888, 8.811840851150844, 8.781881848409604, 8.751894188793267, 8.721909663315186, 8.69192776155896, 8.661945426934615, 8.631962675099958, 8.601979564575435, 8.542015238258651, 8.512031088262066, 8.482049647858533, 8.452068440644025, 8.422079337441538, 8.392094331044547, 8.362121967936902, 8.332145004514299, 8.302157361668693, 8.272180497010671, 8.242203191101154, 8.182247085683407, 8.152271844718616, 8.122297350301752, 8.092318824963835, 8.062345555703121, 8.032368065774902, 8.002367334396476, 7.972364912876132, 7.942360725012755, 7.91235500623785, 7.882360170624586, 7.82237787121734, 7.792386542923614, 7.762395122503522, 7.732403621938461, 7.702412050044222, 7.672420413632208, 7.64242871824675, 7.612436968094021, 7.582445165023082, 7.552453306626389, 7.522462954437216, 7.492448116996781, 7.462441788890778, 7.432449754075421, 7.372468437081773, 7.342462252316039, 7.312457682272587, 7.282454721615318, 7.252453160291192, 7.222452562710624, 7.192452316927972, 7.132450243513852, 7.102447282774535, 7.042436493479766, 7.042436493479766, 7.012439654320606, 6.982447315238087, 6.952454907547671, 6.892469963652569, 6.86247745462972, 6.832484931467614, 6.802492399662952, 6.772499862289363, 6.742507321077738, 6.712514775580042, 6.652529651404338, 6.622537053736637, 6.592547062028279, 6.5625220258538075, 6.5625220258538075, 6.532522761068122, 6.502530132497867, 6.472537475565605, 6.412552118669518, 6.382559432748922, 6.352566791883406, 6.322574239046322, 6.262588940134309, 6.2325962689540235, 6.172578462237515, 6.142555114225724, 6.112529159719052, 6.0825016701903545, 6.052489609207033, 6.022496951152091, 5.992504274134933, 5.9625115917159, 5.932518909013576, 5.902526229113309, 5.872533553530904, 5.842540881865472, 5.812555243114316, 5.782551844805995, 5.752535275587428, 5.722514834619756, 5.692490912873072, 5.662464703612775, 5.63247067824088, 5.602477958035466, 5.5724852212705365, 5.542492477468506, 5.5124997329951375, 5.4825069922606735, 5.422521532267059, 5.392528813951337, 5.362536099129314, 5.332541320721316, 5.302523691640898, 5.2725017400215, 5.242476338751956, 5.212448884341699, 5.152454835333795, 5.122462110659391, 5.092469381082748, 5.092469381082748, 5.0324839282122715, 5.002493805700953, 4.972501245925997, 4.942508674068364, 4.912516081102373, 4.882523455924897, 4.822538077307784, 4.792545324881057, 4.762552540632709, 4.702565661264258, 4.67256463915228, 4.612560101224344, 4.522558597789305, 4.462554036252165, 4.402543188912586, 4.342557856806578, 4.282572466248371, 4.222587002028998, 4.162601532965008, 4.072625884906441, 4.012640670338382, 3.982648012124304, 3.9226625671095676, 3.832684180235309, 3.77268087171472, 3.7126780826498385, 3.65267737034776, 3.5926737147000485, 3.5326639156418027, 3.472673529914118, 3.41268816393312, 3.352702706888123, 3.2927172371825177, 3.2327340821489097, 3.1727489207418307, 3.0827709771658873, 3.0227854787605306, 2.962799868994074, 2.9028012599637036, 2.8485491073561318, 2.8319433782770536, 2.831474683185253, 2.8322951015492785, 2.8429355973911346, 2.855517490246677])
y2 = np.array([-0.9004343159856443, -0.9004385570334464, -0.9004396173395574, -0.9004470170008901, -0.9004582794300078, -0.9004582794300078, -0.900582448791796, -0.9008712458856494, -0.9015200217255404, -0.9021411847594536, -0.9029197752390375, -0.9037007106482575, -0.904468525439975, -0.9052112029973121, -0.9059341768661914, -0.9066406226457153, -0.9073266420626973, -0.9079924595137011, -0.9086390768586684, -0.9092670867695769, -0.9104695148763153, -0.9110443816450277, -0.9116029514394064, -0.9121450760725681, -0.9126669897697303, -0.9131793091372643, -0.9136764616950207, -0.9141603048993552, -0.9146295909023157, -0.9150870891680747, -0.9155298776250704, -0.9163793108933672, -0.916785910135515, -0.9171806034693593, -0.9175685692741968, -0.9179357400597355, -0.918301342478594, -0.9186586576623457, -0.9190057325045058, -0.9193432438783264, -0.9196717366443709, -0.9199893332378248, -0.9205996512154394, -0.9208911416454026, -0.9211741078243266, -0.9214488338099895, -0.9217155621511044, -0.9219745242078111, -0.9222259420982352, -0.9224700306205021, -0.9227069994990199, -0.9229370725523094, -0.9231603806339503, -0.9233656400103372, -0.923571455536822, -0.9237764334039182, -0.9241715150779694, -0.9243624593877453, -0.9245470070581976, -0.9247262892470329, -0.924900319266595, -0.9250689485625453, -0.9252322791245459, -0.9255439963733507, -0.9256932194668882, -0.9259805129782019, -0.9259805129782019, -0.926117289390784, -0.9262513351377093, -0.9263814932759488, -0.9266302220215139, -0.9267491057884159, -0.9268644278126674, -0.9269763739340852, -0.9270850556458107, -0.9271905662270853, -0.9272929961655092, -0.927488974747126, -0.9275826176492372, -0.9276746543123777, -0.9277575265813253, -0.9277575265813253, -0.9278426023502833, -0.9279257956510336, -0.9280065593812308, -0.9281610334223377, -0.9282348078088906, -0.9283064090693698, -0.9283759282436871, -0.9285090057073282, -0.9285725899364689, -0.928689452883211, -0.9287442550046839, -0.9287979367927209, -0.9288501547273972, -0.9289026902000901, -0.9289553657957944, -0.9290064814277225, -0.9290561053200964, -0.9291042801209155, -0.9291510471702791, -0.9291964463561005, -0.929240516707665, -0.9292826892213892, -0.9293182993072214, -0.9293541668606636, -0.9293886789643431, -0.9294217995297868, -0.9294535844041846, -0.9294875064556264, -0.9295200858739358, -0.9295516732013759, -0.9295823329640925, -0.9296120709308958, -0.9296409117851583, -0.9296960030753488, -0.9297223037297904, -0.9297478058443148, -0.9297722319212359, -0.9297942772412159, -0.929815997806564, -0.9298371434375551, -0.9298575819762268, -0.9298995108999113, -0.9299195987365124, -0.9299390802893412, -0.9299390802893412, -0.9299763384356573, -0.9299923730302326, -0.9300093923197073, -0.9300258806656829, -0.9300418834628841, -0.9300574176209891, -0.9300870903033706, -0.9301012653479189, -0.9301150219403752, -0.9301431878320353, -0.9301615428653135, -0.9301884858997327, -0.9302228608728561, -0.9302430470917926, -0.9302640172346534, -0.9302831312975882, -0.9303027493837981, -0.9303212047491413, -0.9303385640026879, -0.9303603060041762, -0.9303746701874107, -0.9303815315322232, -0.9303946346007645, -0.9304128260473604, -0.930433184645775, -0.9304467603296176, -0.9304577692167846, -0.9304671723458481, -0.9304775787454377, -0.9304873513568156, -0.9304981135473003, -0.9305082291005201, -0.9305177344667259, -0.9305246415967909, -0.9305324892151909, -0.9305433807044945, -0.9305500940265112, -0.9305563949962466, -0.9305707477948969, -0.9310418029768491, -0.9303758363192863, -0.9304372302863841, -0.9303027855263849, -0.9285889662836538, -0.9267285057429936])
# x3 = np.array([-9.998512780170573, -9.998497020262745, -9.998493080215841, -9.995989967648145, -9.987490968274875, -9.987490968274875, -9.973409921098868, -9.954172414951689, -9.929126795407107, -9.898233746143173, -9.863399724854519, -9.82841139465685, -9.793443134975355, -9.758460582121414, -9.72348245847003, -9.688503291270118, -9.65354639889965, -9.61858848986391, -9.583623819732715, -9.548635139739996, -9.478657298250594, -9.443668210731463, -9.408680560588811, -9.373699902874012, -9.33870988411622, -9.303719663161003, -9.268729263416192, -9.233738707369362, -9.198748014229432, -9.163756064417642, -9.128756213990354, -9.058759996782602, -9.023761773556062, -8.988762303164773, -8.95376103428524, -8.918757754887109, -8.883766643925783, -8.848775188174583, -8.813783609952264, -8.778791937102254, -8.743800706804576, -8.708808973038112, -8.638824743218692, -8.603832581413451, -8.568840416385846, -8.533849989622574, -8.498879133109076, -8.463874579994375, -8.428849747653919, -8.393857768968907, -8.358865584189092, -8.323873348348146, -8.28888107586809, -8.253888777566488, -8.21889645985098, -8.183904126941226, -8.113920945355773, -8.078916920326954, -8.043898833701412, -8.008875924356493, -7.9738767670335555, -7.938884331877951, -7.903892033280336, -7.833907861057008, -7.79891527265236, -7.72892999714166, -7.72892999714166, -7.693937454855609, -7.658953872588928, -7.623949448305243, -7.553907538379964, -7.518881682488701, -7.4838554017072, -7.448861124028827, -7.413868554113192, -7.378875976542296, -7.343883397757144, -7.273898246133641, -7.238905669433632, -7.2039130803838605, -7.168931084746221, -7.168931084746221, -7.133912163557188, -7.098888096872223, -7.063896003975729, -6.993910679506944, -6.958921415114576, -6.92392903175534, -6.888936375605334, -6.818951211732947, -6.783966103626676, -6.713985011320947, -6.6789923112987495, -6.643999571080519, -6.609006800657715, -6.574014011783559, -6.539021247090858, -6.504029823514745, -6.469037117071585, -6.434044418616438, -6.399051729888097, -6.364059048605606, -6.329066366247095, -6.294083367637636, -6.259087703693637, -6.224062110963095, -6.189055299056626, -6.154062606148831, -6.119069892228724, -6.08407717123996, -6.049084452227539, -6.014095547489063, -5.979103125059762, -5.944110820875184, -5.90912529740364, -5.839110041346448, -5.804087640193288, -5.769062035097412, -5.734047599979562, -5.699054902482408, -5.664062189273375, -5.629069473234913, -5.594076761636296, -5.524091365286146, -5.489098679693861, -5.454105993651677, -5.454105993651677, -5.384106877767252, -5.349081859671904, -5.314065676214966, -5.279072985142946, -5.244080264377545, -5.2090875352206325, -5.139105729628179, -5.104113419904348, -5.069121183881629, -4.999138833128441, -4.964121386947432, -4.894074184782596, -4.7890739201689545, -4.7190884698207505, -4.6491030524510215, -4.579117665281699, -4.5090997800091435, -4.439050472323383, -4.369065543436219, -4.2640873594037725, -4.194106375760572, -4.159120707228217, -4.089109052262877, -3.984045236980554, -3.9140598011708465, -3.844074340097126, -3.774088911231564, -3.704103516168922, -3.6340891559564987, -3.5640383393786133, -3.4940488009981565, -3.424063340763646, -3.354081708591148, -3.2841020651780557, -3.2140954946997233, -3.1090285559368005, -3.0390432111547243, -2.9690577457889784, -2.899072310968969, -2.8290869123149323, -2.759076959010932, -2.6284048518074217, -2.6128896409034765, -2.611510710710469, -2.6118238447197744])
# y3 = np.array([0.9004324077700668, 0.9004366732703207, 0.9004377396897205, 0.9004540050000416, 0.9004502303496964, 0.9004502303496964, 0.9004132211073521, 0.9003237926132373, 0.8998356230378514, 0.8991785810098193, 0.8985486679147807, 0.8979222607527462, 0.897305031466211, 0.8967044893571586, 0.8961232657433255, 0.8955539771536604, 0.8950061869860826, 0.8944730766567834, 0.8939538928735552, 0.8934418481336189, 0.8924630483131857, 0.8919952378166275, 0.8915408925875439, 0.8911000241147241, 0.8906708176424148, 0.8902540626665284, 0.8898494553294916, 0.8894566367068808, 0.8890752532495706, 0.8887099380727561, 0.8883538806242576, 0.8876665158050648, 0.8873369449402596, 0.8870168410490912, 0.886706169240954, 0.8864051233245193, 0.886111646895652, 0.885828022832242, 0.8855529086028942, 0.8852860512700111, 0.8850272428444741, 0.8847758067255047, 0.884295039623847, 0.8840655152839926, 0.88384277862164, 0.8836265611771499, 0.8834157884248223, 0.8832154527722778, 0.8830222668379868, 0.8828246534679512, 0.882633329598085, 0.8824475737862026, 0.8822673615410965, 0.8820924082106442, 0.8819226797620832, 0.8817580344250002, 0.8814431311089209, 0.8812967325372859, 0.8811549354084244, 0.8810157144498049, 0.8808749071214224, 0.880736925486292, 0.8806030416993677, 0.8803464343152294, 0.8802236489479258, 0.8799890450265158, 0.8799890450265158, 0.8798770334622354, 0.8797679824945561, 0.8796619993289785, 0.8794624066462328, 0.8793655299604433, 0.8792706997871194, 0.8791736683275573, 0.8790794812346798, 0.8789880210262941, 0.8788992123006816, 0.8787292458659405, 0.8786480102503891, 0.8785691437105951, 0.878491970781706, 0.878491970781706, 0.8784180718424164, 0.878345951698568, 0.8782730071141104, 0.8781332596076944, 0.878066242833748, 0.878001181252931, 0.8779379066510012, 0.8778169344521892, 0.8777587724709615, 0.8776456407319576, 0.8775915532475723, 0.8775390656834454, 0.8774881092402068, 0.8774386348127624, 0.8773905873968373, 0.8773449007090053, 0.8773000720495453, 0.8772565652023365, 0.8772143161810492, 0.8771732880397396, 0.8771334815762368, 0.8770945747166081, 0.8770545855987139, 0.8770167402892273, 0.876978935037812, 0.8769415364937967, 0.8769052247425803, 0.8768699652681192, 0.8768357255604584, 0.8768021216840803, 0.8767695242187046, 0.8767378558990029, 0.8767066492747322, 0.8766427674598593, 0.876612486061347, 0.876582330264468, 0.8765524899847638, 0.8765225822529397, 0.8764935563937433, 0.8764653688098709, 0.8764380152355998, 0.8763856728305591, 0.8763606575558309, 0.8763363860683177, 0.8763363860683177, 0.8762874503857974, 0.8762639431817851, 0.8762401454720359, 0.8762168268828866, 0.876194151009469, 0.8761721286757441, 0.8761297857619071, 0.8761093183500274, 0.8760893921613095, 0.8760471343077505, 0.8760269529312736, 0.8759862902338871, 0.8759258081548421, 0.8758882207143549, 0.8758528319059826, 0.8758194698109621, 0.8757880965822776, 0.8757571225251791, 0.8757270959764899, 0.8756850990977516, 0.8756584090962959, 0.8756451508611122, 0.8756148337147329, 0.8755706782158517, 0.8755418263219109, 0.8755146249436394, 0.8754889707432602, 0.8754647719142414, 0.8754418112700675, 0.8754192503123739, 0.8753966784917425, 0.8753756009991611, 0.8753554713608593, 0.8753354586415457, 0.8753113863222451, 0.8752756265275279, 0.8752520492760428, 0.8752298564362597, 0.8752089195592145, 0.8751891625135717, 0.8751702911712707, 0.8751360129791274, 0.8751344398052296, 0.8751339912310493, 0.8751342359534691])

for i in range(len(x1)):
    dictionary.update(
        {str(time.time()):
            {"data":[
                    {
                        "type":"object",
                        "position":[x1[i], y1[i], 0],
                        "velocity":[0, 0.7, 0],
                        "label_id": 14,
                        "label_name": "pedestrian",
                        "tracking_id": 14
                    },
                    {
                        "type":"object",
                        "position":[x2[i], y2[i], 0],
                        "velocity":[0.6, 0, 0],
                        "label_id": 7,
                        "label_name": "car",
                        "tracking_id": 7
                    },
                    # {
                    #     "type":"object",
                    #     "position":[x3[i], y3[i], 0],
                    #     "velocity":[0.7, 0, 0],
                    #     "label_id": 0,
                    #     "label_name": "car",
                    #     "tracking_id": 0
                    # }
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