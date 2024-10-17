// let topic_ID_TOPIC = {
//     '1' : 'MAKE PUBLIC STATEMENT',
//     '2' : 'APPEAL',
//     '3' : 'EXPRESS INTENT TO COOPERATE',
//     '4' : 'CONSULT',
//     '5' : 'ENGAGE IN DIPLOMATIC COOPERATION',
//     '6' : 'ENGAGE IN MATERIAL COOPERATION',
//     '7' : 'PROVIDE AID',
//     '8' : 'YIELD',
//     '9' : 'INVESTIGATE',
//     '10' : 'DEMAND',
//     '11' : 'DISAPPROVE',
//     '12' : 'REJECT',
//     '13' : 'THREATEN',
//     '14' : 'PROTEST',
//     '15' : 'EXHIBIT FORCE POSTURE',
//     '16' : 'REDUCE RELATIONS',
//     '17' : 'COERCE',
//     '18' : 'ASSAULT',
//     '19' : 'FIGHT',
//     '20' : 'USE UNCONVENTIONAL MASS VIOLENCE'
// }

// let topic_ID_TOPIC = {
//     '1' :  'STATEMENT',
//     '2' :  'APPEAL',
//     '3' :  'COOPERATE',
//     '4' :  'CONSULT',
//     '5' :  'CO-DIPLOMACY',
//     '6' :  'CO-MATERIAL',
//     '7' :  'AID',
//     '8' :  'YIELD',
//     '9' :  'INVESTIGATE',
//     '10' : 'DEMAND',
//     '11' : 'DISAPPROVE',
//     '12' : 'REJECT',
//     '13' : 'THREATEN',
//     '14' : 'PROTEST',
//     '15' : 'FORCE',
//     '16' : 'ESTRANGED',
//     '17' : 'COERCE',
//     '18' : 'ASSAULT',
//     '19' : 'FIGHT',
//     '20' : 'VIOLENCE',
// }

let topic_ID_TOPIC = {
    '1' :  '声明',
    '2' :  '呼吁',
    '3' :  '合作',
    '4' :  '协商',
    '5' :  '共同外交',
    '6' :  '物质合作',
    '7' :  '援助',
    '8' :  '让步',
    '9' :  '调查',
    '10' : '要求',
    '11' : '反对',
    '12' : '拒绝',
    '13' : '威胁',
    '14' : '抗议',
    '15' : '强制',
    '16' : '疏远',
    '17' : '胁迫',
    '18' : '攻击',
    '19' : '冲突',
    '20' : '暴力',
}

export function getTopic(id){
    if (id in topic_ID_TOPIC) return id + "-" + topic_ID_TOPIC[id];
    else return "CONF"; // without key , waiting conform
}