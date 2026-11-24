#import "@preview/glossarium:0.5.10": gls

#let entries = (
  (
    key: "bdsm",
    short: "БДСМ",
    long: "Bondage & Discipline, Domination & Submission, Sadism & Masochism",
    styles: ("short-long",),
    description: [
      Психосексуальная субкультура, основанная на эротическом
      обмене властью и иных формах сексуальных отношений,
      затрагивающих ролевые игры в господство и подчинение
      @BDSM2026.
    ],
    group: "Основы",
  ),
  (
    key: "tema",
    short: "Тема",
    description: [
      Маскирующее название БДСМ, закрепившееся
      в русскоязычном сообществе.
    ],
    group: "Основы",
  ),
  (
    key: "vanilla",
    short: "ваниль",
    description: [
      Обозначение обычного, традиционного, не относящегося
      к БДСМ и другим кинк-практикам.
    ],
    group: "Основы",
  ),
  (
    key: "fetish",
    short: "фети\u{0301}ш",
    long: "фр. fétiche от порт. feitiço – амулет, волшебство",
    description: [
      Предмет, становящийся объектом поклонения, фетишизма
      @Fetishizm2026. В сексуальности -- источник влечения,
      связанный с неодушевлёнными предметами, материалами,
      частями тела или действиями с ними @SeksualnyyFetishizm2026.
    ],
    group: "Основы",
  ),
  (
    key: "kink",
    short: "кинк",
    long: "англ. kink – изгиб, странность, заскок, причуда",
    description: [
      Использование нетрадиционных сексуальных практик,
      концепций или фантазий @KinkSeksualnost2026.
    ],
    group: "Основы",
  ),
  (
    key: "top",
    short: "верх",
    description: [
      Участник, занимающий доминирующую или активную
      позицию во взаимодействии.
    ],
    group: "Роли",
  ),
  (
    key: "bottom",
    short: "низ",
    description: [
      Участник, занимающий подчинённую или принимающую
      позицию во взаимодействии.
    ],
    group: "Роли",
  ),
  (
    key: "switch",
    short: "свитч",
    description: [
      Участник, способный занимать как верхнюю,
      так и нижнюю роль.
    ],
    group: "Роли",
  ),
  (
    key: "scene",
    short: "экшн",
    long: "сцена, англ. scene",
    styles: ("short-long",),
    plural: "экшны",
    description: [
      Ограниченный во времени эпизод взаимодействия
      участников БДСМ.
    ],
    group: "Взаимодействие",
  ),
  (
    key: "limits",
    short: "лимиты",
    long: "табу",
    styles: ("short-long",),
    description: [
      Границы допустимого взаимодействия, вытекающие
      из согласия сторон и возможности отказать.
      Различают жёсткие и мягкие лимиты.
    ],
    group: "Взаимодействие",
  ),
  (
    key: "safeword",
    short: "стоп-слово",
    long: "стоп-сигнал",
    styles: ("short-long",),
    plural: "стоп-слова",
    description: [
      Заранее оговорённый сигнал, означающий немедленное
      прекращение или корректировку сцены.
    ],
    group: "Взаимодействие",
  ),
  (
    key: "aftercare",
    short: "афтеркейр",
    long: "англ. aftercare",
    styles: ("short-long",),
    description: [
      Уход и забота об участнике непосредственно
      после завершения экшна.
    ],
    group: "Взаимодействие",
  ),
  (
    key: "drop",
    short: "дроп",
    description: [
      Откат физического или эмоционального состояния
      после экшна. Может возникать как у нижнего,
      так и у верхнего участника.
    ],
    group: "Взаимодействие",
  ),
  (
    key: "tpe",
    short: "TPE",
    long: "Total Power Exchange",
    styles: ("short-long",),
    description: [
      Тотальный обмен властью.
    ],
    group: "Взаимодействие",
  ),
  // Безопасность
  (
    key: "ssc",
    short: "БДР",
    long: "Safe, Sane, Consensual",
    styles: ("short-long",),
    description: [
      Принцип «Безопасность, Добровольность, Разумность».
      Предполагает минимизацию рисков, осознанность
      участников и добровольность взаимодействия
      @SafeSaneConsensual2025.
    ],
    group: "Безопасность",
  ),
  (
    key: "rack",
    short: "RACK",
    long: "Risk-Aware Consensual Kink",
    styles: ("short-long",),
    description: [
      Парадигма осознанного согласия на рискованные
      практики, при которой участники понимают
      и принимают связанные с ними риски
      @RiskawareConsensualKink2026.
    ],
    group: "Безопасность",
  ),
  (
    key: "reage",
    short: "принцип Реаж",
    description: [
      Каждая сторона имеет право односторонне и моментально
      прекратить происходящее. Формулировка автора справочника;
      общепринятым термином не является.
    ],
    group: "Безопасность",
  ),
)

// Определение в тексте главы: заголовок и описание из entries.
// gls(..., display:) учитывает использование и ставит обратную ссылку,
// поэтому определение в главе 1 попадает в бэклинки глоссария.
#let def(key) = {
  let e = entries.find(x => x.key == key)
  let s = str(e.short)
  let s = s.replace(regex("^."), m => upper(m.text))
  let l = e.at("long", default: none)
  let title = if l != none [*#s* (#l)] else [*#s*]
  par[#gls(key, display: title) -- #e.description]
}

#let glossary-title(entry) = {
  let bold = strong.with(delta: 200)

  if entry.long != none and entry.short != none {
    bold[#entry.short -- #entry.long]
  } else if entry.long != none {
    bold[#entry.long]
  } else {
    bold[#entry.short]
  }
}