#let _type-labels = (
  venue: "Площадка",
  community: "Сообщество",
  website: "Сайт",
  channel: "Канал",
  shop: "Магазин",
  maker: "Мастерская",
  event: "Мероприятие",
  person: "Человек",
  resource: "Ресурс",
)

#let _status-labels = (
  active: "Действует",
  inactive: "Не действует",
  uncertain: "Статус не подтверждён",
  archived: "Архив",
)

#let _tag-labels = (
  socialization: "Социализация",
  education: "Обучение",
  equipment: "Снаряжение",
  venues: "Площадки",
  events: "Мероприятия",
  dating: "Знакомства",
  community: "Сообщество",
  literature: "Литература",
  safety: "Безопасность",
  shopping: "Покупки",
)

#let _label(value, labels) = {
  if type(value) == str and value in labels {
    labels.at(value)
  } else {
    value
  }
}

#let _meta-line(items) = {
  let visible = items.filter(item => item != none and item != "")
  if visible.len() > 0 {
    text(size: 0.65em, fill: luma(50%))[
      #visible.join([ · ])
    ]
  }
}

#let note(body) = [
  #text(style: "italic")[/**Комментарий*. */#body]
]

#let resource(
  name,
  body,
  id: none,
  type: none,
  tags: (),
  location: none,
  status: none,
  url: none,
  last_checked: none,
) = {
  let type-label = _label(type, _type-labels)
  let status-label = _label(status, _status-labels)
  let tag-labels = tags.map(tag => _label(tag, _tag-labels))

  let metadata = (
    type-label,
    location,
    status-label,
    if last_checked != none {
      "проверено " + last_checked.display("[day].[month].[year]")
    } else {
      none
    },
    ..tag-labels,
  ).filter(item => item != none and item != "")

  [
    #block(sticky: true, below: 0.45em)[
      *#name*#text(size: 0.65em, weight: "regular")[#if metadata.len() > 0 [
        · #metadata.join(" · ")
      ]#if url != none [
        · #link(url)[сайт]
      ]]
    ]
    #body
  ]
}
