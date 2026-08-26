const DATA_URL = "data/pmm-data.json?v=0.15.0";
const RU_URL = "data/i18n-ru.json?v=0.15.0";

const UI_RU = {
  "Evidence-aware knowledge map": "Карта знаний с учётом доказательств",
  "The mind as a map of": "Психика как карта",
  "testable mechanisms": "проверяемых механизмов",
  "Source data ↗": "Исходные данные ↗",
  "Choose a way to explore PMM": "Выберите способ изучения PMM",
  "01 · Practical foundations": "01 · Практическая база",
  "Foundational Models": "Базовые модели",
  "02 · Familiar navigation": "02 · Знакомая навигация",
  "General Psychology": "Общая психология",
  "03 · Scientific core": "03 · Научное ядро",
  "Mechanisms & Evidence": "Механизмы и доказательства",
  "04 · Terminology alignment": "04 · Сопоставление терминов",
  "Scientific Systems": "Научные системы",
  "All": "Все",
  "Causal": "Причинные",
  "Hypotheses": "Гипотезы",
  "Contested": "Спорные",
  "How to read this map": "Как читать эту карту",
  "Open guide": "Открыть инструкцию",
  "Explore all mechanisms": "Все механизмы",
  "Compare processes across every evidence pack": "Сравните процессы из всех пакетов доказательств",
  "Cross-family index": "Межтематический индекс",
  "One inventory, without false unification.": "Единый каталог без ложного объединения.",
  "Each card is a Mechanism record from one evidence pack. Counts show traceability to modeled Claims, Evidence records, and Sources. They are not truth scores, effect sizes, or scientific rankings.": "Каждая карточка — запись механизма из одного пакета доказательств. Числа показывают прослеживаемость до утверждений, записей доказательств и источников. Это не оценки истинности, размеры эффектов и не научный рейтинг.",
  "Find a mechanism": "Найти механизм",
  "Similar labels do not establish that mechanisms are identical or causally connected. Cross-family bridges require separate scientific review.": "Похожие названия не доказывают, что механизмы тождественны или причинно связаны. Межтематические мосты требуют отдельной научной проверки.",
  "mechanisms": "механизмов",
  "linked claims": "связанных утверждений",
  "evidence records": "записей доказательств",
  "sources": "источников",
  "Open in map": "Открыть на карте",
  "No mechanisms match this search.": "По этому запросу механизмы не найдены.",
  "learning": "обучение",
  "cognitive": "когнитивный",
  "integrative": "интегративный",
  "physiological": "физиологический",
  "computational": "вычислительный",
  "social": "социальный",
  "Reading rule": "Правило чтения",
  "Follow the records, not the visual distance.": "Следуйте данным записей, а не визуальному расстоянию.",
  "PMM is an evidence-aware knowledge map. Nearby nodes help navigation only; they do not show a stronger effect, a causal direction, or a scientific consensus.": "PMM — карта знаний с учётом доказательств. Близость узлов помогает только навигации и не означает более сильный эффект, причинное направление или научный консенсус.",
  "Shapes": "Формы",
  "Object card": "Карточка объекта",
  "A construct, mechanism, state, behavior, intervention, measurement, context, event, outcome, contingency, or observation.": "Конструкт, механизм, состояние, поведение, вмешательство, измерение, контекст, событие, исход, зависимость или наблюдение.",
  "Mechanism pill": "Капсула механизма",
  "A proposed or established process with specified roles and conditions. It is not automatically proven by appearing on the map.": "Предлагаемый или установленный процесс с заданными ролями и условиями. Само присутствие на карте не доказывает его.",
  "Claim card": "Карточка утверждения",
  "A scoped scientific assertion. Open it to see its status, confidence, evidence, limitations, and sources.": "Научное утверждение с заданными границами. Откройте его, чтобы увидеть статус, уверенность, доказательства, ограничения и источники.",
  "Research question": "Исследовательский вопрос",
  "A faint dashed card marks an important gap suggested by mapped limitations. It is a question, not a finding or evidence rating.": "Бледная пунктирная карточка отмечает важный пробел, следующий из ограничений карты. Это вопрос, а не результат исследования и не оценка доказанности.",
  "Claim colours": "Цвета утверждений",
  "Green: supported": "Зелёный: поддерживается",
  "The mapped evidence supports the stated claim within its declared scope.": "Собранные доказательства поддерживают утверждение в заявленных границах.",
  "Amber: mixed or unsupported": "Янтарный: смешанные или недостаточные данные",
  "Results disagree, are null, or do not currently support the claim.": "Результаты расходятся, являются нулевыми или пока не поддерживают утверждение.",
  "Blue: proposed": "Синий: предложено",
  "A falsifiable mechanism or causal hypothesis, not an established result.": "Фальсифицируемая гипотеза о механизме или причинности, а не установленный результат.",
  "Lines and interaction": "Линии и взаимодействие",
  "Solid line": "Сплошная линия",
  "A structural or operational relation, such as “measured by” or “occurs in context.”": "Структурная или операциональная связь, например «измеряется с помощью» или «происходит в контексте».",
  "Dashed arrow": "Пунктирная стрелка",
  "Connects an object to a Claim. The Claim, not the arrow, carries the empirical or causal interpretation.": "Соединяет объект с утверждением. Эмпирическую или причинную интерпретацию несёт утверждение, а не стрелка.",
  "Select a node": "Выберите узел",
  "The right panel reveals the full record. Use filters to show causal claims, hypotheses, or contested results.": "Справа откроется полная запись. Фильтры показывают причинные утверждения, гипотезы и спорные результаты.",
  "supported": "поддерживается",
  "mixed": "смешанные данные",
  "proposed": "предложено",
  "Select a map node": "Выберите узел карты",
  "Its definition, scientific status, limitations, evidence, and sources will appear here.": "Здесь появятся определение, научный статус, ограничения, доказательства и источники.",
  "PMM is not a diagnostic tool. The map distinguishes observations, measurements, hypotheses, and causal inferences.": "PMM не является диагностическим инструментом. Карта различает наблюдения, измерения, гипотезы и причинные выводы.",
  "Scope": "Границы",
  "Confidence rationale": "Обоснование уверенности",
  "Evidence": "Доказательства",
  "Limitations": "Ограничения",
  "Sources": "Источники",
  "Select an object or scientific Claim card on the map.": "Выберите на карте объект или карточку научного утверждения.",
  "Data failed to load": "Не удалось загрузить данные",
  "Open the site through a local server or GitHub Pages.": "Откройте сайт через локальный сервер или GitHub Pages.",
  "Select a node. Click empty space or press Escape to show the full map. Solid lines are structural relations; dashed arrows pass through scientific Claim cards. Faint dotted links lead to open research questions.": "Выберите узел. Нажмите на пустое место или клавишу Escape, чтобы снова показать всю карту. Сплошные линии обозначают структурные связи; пунктирные стрелки проходят через карточки научных утверждений. Бледные точечные линии ведут к открытым исследовательским вопросам.",
  "Construct": "Конструкт",
  "Mechanism": "Механизм",
  "State": "Состояние",
  "Behavior": "Поведение",
  "Intervention": "Вмешательство",
  "Measurement": "Измерение",
  "Context": "Контекст",
  "Event": "Событие",
  "Outcome": "Исход",
  "Contingency": "Зависимость",
  "Observation": "Наблюдение",
  "Claim": "Утверждение",
  "Open question": "Открытый вопрос",
  "open question": "открытый вопрос",
  "mixed evidence": "смешанные данные",
  "unsupported": "не поддерживается",
  "refuted": "опровергнуто",
  "not assessed": "не оценено",
  "accepted": "принято",
  "provisional": "предварительно",
  "draft": "черновик",
  "deprecated": "устарело",
  "high": "высокая",
  "moderate": "умеренная",
  "low": "низкая",
  "very_low": "очень низкая",
  "supports": "поддерживает",
  "challenges": "оспаривает",
  "neutral": "нейтрально",
  "causal_effect": "причинный эффект",
  "causal_hypothesis": "причинная гипотеза",
  "mechanism_hypothesis": "гипотеза механизма",
  "association": "связь без доказанной причинности",
  "definition": "определение",
  "prediction": "предсказание",
  "mediation": "медиация",
  "moderation": "модерация",
};

const TYPE_LABELS = {
  Construct: "Construct",
  Mechanism: "Mechanism",
  State: "State",
  Behavior: "Behavior",
  Intervention: "Intervention",
  Measurement: "Measurement",
  Context: "Context",
  Event: "Event",
  Outcome: "Outcome",
  Contingency: "Contingency",
  Observation: "Observation",
  claim: "Claim",
  research_question: "Open question",
};

const STATUS_LABELS = {
  supported: "supported",
  mixed: "mixed evidence",
  unsupported: "unsupported",
  refuted: "refuted",
  proposed: "proposed",
  not_assessed: "not assessed",
};

const state = {
  data: null,
  translations: {},
  lang: localStorage.getItem("pmm-language") || "en",
  perspective: localStorage.getItem("pmm-perspective") || "models",
  family: null,
  filter: "all",
  selectedId: null,
  mechanismQuery: "",
};
const svg = document.getElementById("knowledge-map");
const inspector = document.getElementById("inspector");

function t(value = "") {
  if (state.lang !== "ru") return value;
  return UI_RU[value] || state.translations[value] || value;
}

function localText(value = "") {
  if (!value || typeof value === "string") return t(value || "");
  return value[state.lang] || value.en || "";
}

function translateStaticDom() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll("[data-en]").forEach(element => {
    element.textContent = state.lang === "ru" ? t(element.dataset.en) : element.dataset.en;
  });
}

function prepareStaticDom() {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const node of nodes) {
    const value = node.textContent.trim();
    if (!value || node.parentElement?.closest("script, style")) continue;
    const wrapper = document.createElement("span");
    wrapper.dataset.en = value;
    wrapper.textContent = value;
    node.replaceWith(wrapper);
  }
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function wrapLabel(label, max = 23) {
  const words = label.split(/\s+/);
  const lines = [];
  let line = "";
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > max && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines.slice(0, 3);
}

function isHypothesis(claim) {
  return claim.claim_type === "mechanism_hypothesis" || claim.claim_type === "causal_hypothesis";
}

function claimVisible(claim) {
  if (state.filter === "all") return true;
  if (state.filter === "hypothesis") return isHypothesis(claim);
  if (state.filter === "contested") return ["mixed", "unsupported", "refuted"].includes(claim.epistemic_status);
  return claim.claim_type === state.filter;
}

function familyRecords() {
  const objects = state.family.objects.map(item => ({ ...item, kind: "object", label: t(item.label) }));
  const claims = state.family.claims.map(item => ({ ...item, kind: "claim", type: "claim", label: t(item.statement) }));
  const questions = (state.family.research_questions || []).map(item => ({
    ...item,
    kind: "question",
    type: "research_question",
    label: localText(item.question),
  }));
  return [...objects, ...claims, ...questions];
}

function linkedObjectIds(claim) {
  return [claim.exposure_id, claim.mechanism_id, claim.mediator_id, claim.moderator_id, claim.outcome_id].filter(Boolean);
}

function graphModel() {
  const visibleClaims = state.family.claims.filter(claimVisible);
  const visibleClaimIds = new Set(visibleClaims.map(item => item.id));
  const objectIds = new Set(state.family.objects.map(item => item.id));
  const relevantObjects = state.filter === "all"
    ? objectIds
    : new Set(visibleClaims.flatMap(linkedObjectIds));

  const nodes = familyRecords().filter(item => {
    if (item.kind === "object") return relevantObjects.has(item.id);
    if (item.kind === "claim") return visibleClaimIds.has(item.id);
    return state.filter === "all";
  });
  const nodeIds = new Set(nodes.map(item => item.id));
  const edges = [];

  for (const relation of state.family.relations) {
    if (nodeIds.has(relation.subject_id) && nodeIds.has(relation.object_id)) {
      edges.push({ source: relation.subject_id, target: relation.object_id, type: "relation", label: relation.predicate });
    }
  }

  for (const claim of visibleClaims) {
    for (const sourceId of [claim.exposure_id, claim.mechanism_id, claim.mediator_id, claim.moderator_id].filter(Boolean)) {
      if (nodeIds.has(sourceId)) edges.push({ source: sourceId, target: claim.id, type: "claim", label: claim.claim_type });
    }
    if (claim.outcome_id && nodeIds.has(claim.outcome_id)) {
      edges.push({ source: claim.id, target: claim.outcome_id, type: "claim", label: claim.claim_type });
    }
  }
  for (const question of state.family.research_questions || []) {
    const anchorId = question.about_ids[0];
    if (nodeIds.has(anchorId) && nodeIds.has(question.id)) {
      edges.push({ source: anchorId, target: question.id, type: "question", label: "open question" });
    }
  }
  return { nodes, edges };
}

function layoutNodes(nodes, width, height, compact) {
  const typeOrder = {
    Context: 0, Intervention: 1, Event: 2, Contingency: 3,
    Construct: 4, Mechanism: 5, claim: 6, State: 7,
    Behavior: 8, Outcome: 9, Measurement: 10, Observation: 11,
    research_question: 12,
  };
  const columnCount = compact ? 3 : 5;
  const ordered = [...nodes].sort((first, second) => {
    const firstOrder = typeOrder[first.type || "claim"] ?? 12;
    const secondOrder = typeOrder[second.type || "claim"] ?? 12;
    return firstOrder - secondOrder || first.label.localeCompare(second.label);
  });
  const positions = new Map();
  ordered.forEach((node, index) => {
    const column = index % columnCount;
    const row = Math.floor(index / columnCount);
    positions.set(node.id, {
      x: ((column + 0.5) / columnCount) * width,
      y: 86 + row * 108,
    });
  });
  return positions;
}

function svgElement(name, attributes = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
  return element;
}

function renderMap() {
  const { nodes, edges } = graphModel();
  const width = Math.max(svg.clientWidth, 620);
  const countsByType = new Map();
  for (const node of nodes) {
    const key = node.type || "claim";
    countsByType.set(key, (countsByType.get(key) || 0) + 1);
  }
  const largestColumn = Math.max(...countsByType.values(), 1);
  const compact = window.innerWidth < 900;
  const gridColumns = compact ? 3 : 5;
  const gridRows = Math.ceil(nodes.length / gridColumns);
  const height = Math.max(
    610,
    150 + (largestColumn - 1) * 92,
    160 + gridRows * 108,
  );
  svg.style.height = `${height}px`;
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.replaceChildren();

  const defs = svgElement("defs");
  const marker = svgElement("marker", { id: "arrow", viewBox: "0 0 10 10", refX: "8", refY: "5", markerWidth: "5", markerHeight: "5", orient: "auto-start-reverse" });
  marker.append(svgElement("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: "rgba(23,33,29,.58)" }));
  defs.append(marker);
  svg.append(defs);

  const positions = layoutNodes(nodes, width, height, compact);
  const edgesGroup = svgElement("g", { "aria-hidden": "true" });
  for (const edge of edges) {
    const source = positions.get(edge.source);
    const target = positions.get(edge.target);
    if (!source || !target) continue;
    const dx = target.x - source.x;
    const curve = Math.max(30, Math.abs(dx) * 0.44);
    const path = svgElement("path", {
      d: `M ${source.x} ${source.y} C ${source.x + Math.sign(dx || 1) * curve} ${source.y}, ${target.x - Math.sign(dx || 1) * curve} ${target.y}, ${target.x} ${target.y}`,
      class: `edge ${edge.type === "claim" ? "claim-edge" : edge.type === "question" ? "question-edge" : ""}`,
      "data-source": edge.source,
      "data-target": edge.target,
      "marker-end": edge.type === "claim" ? "url(#arrow)" : "",
    });
    edgesGroup.append(path);
  }
  svg.append(edgesGroup);

  const nodesGroup = svgElement("g");
  for (const node of nodes) {
    const position = positions.get(node.id);
    const group = svgElement("g", {
      class: `node ${node.kind} type-${node.type} status-${node.epistemic_status || "neutral"}`,
      transform: `translate(${position.x} ${position.y})`,
      tabindex: "0",
      role: "button",
      "aria-label": `${t(TYPE_LABELS[node.type] || node.type)}: ${node.label}`,
      "data-id": node.id,
    });
    const isClaim = node.kind === "claim";
    const isQuestion = node.kind === "question";
    const shape = isClaim
      ? { x: "-86", y: "-38", width: "172", height: "76", rx: "12", class: "node-shape" }
      : isQuestion
        ? { x: "-76", y: "-28", width: "152", height: "56", rx: "7", class: "node-shape" }
        : { x: "-72", y: "-31", width: "144", height: "62", rx: node.type === "Mechanism" ? "31" : "4", class: "node-shape" };
    group.append(svgElement("rect", shape));

    const typeText = svgElement("text", { x: "0", y: "-10", "text-anchor": "middle", class: "node-type" });
    typeText.textContent = t(TYPE_LABELS[node.type] || node.type);
    group.append(typeText);
    const lines = wrapLabel(node.label, isClaim ? 20 : isQuestion ? 23 : 22);
    lines.forEach((line, index) => {
      const text = svgElement("text", { x: "0", y: `${4 + index * 12}`, "text-anchor": "middle" });
      text.textContent = line.length > 26 ? `${line.slice(0, 24)}…` : line;
      group.append(text);
    });
    group.addEventListener("click", () => selectNode(node.id));
    group.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectNode(node.id);
      }
    });
    nodesGroup.append(group);
  }
  svg.append(nodesGroup);
  document.getElementById("visible-count").textContent = state.lang === "ru" ? `${nodes.length} узлов · ${edges.length} связей` : `${nodes.length} nodes · ${edges.length} edges`;
  if (state.selectedId) emphasizeSelection(state.selectedId);
}

function recordById(id) {
  return familyRecords().find(item => item.id === id);
}

function relatedSources(record) {
  const evidenceById = new Map(state.family.evidence.map(item => [item.id, item]));
  const sourceIds = new Set();
  if (record.kind === "question") {
    for (const sourceId of record.source_ids || []) sourceIds.add(sourceId);
  } else if (record.kind === "claim") {
    for (const evidenceId of record.evidence_ids || []) {
      const evidence = evidenceById.get(evidenceId);
      if (evidence?.source_id) sourceIds.add(evidence.source_id);
    }
    for (const sourceId of record.source_ids || []) sourceIds.add(sourceId);
  } else {
    for (const claim of state.family.claims) {
      if (linkedObjectIds(claim).includes(record.id)) {
        for (const evidenceId of claim.evidence_ids || []) {
          const evidence = evidenceById.get(evidenceId);
          if (evidence?.source_id) sourceIds.add(evidence.source_id);
        }
      }
    }
  }
  return state.family.sources.filter(item => sourceIds.has(item.id));
}

function evidenceFor(record) {
  if (record.kind !== "claim") return [];
  const ids = new Set(record.evidence_ids || []);
  return state.family.evidence.filter(item => ids.has(item.id));
}

function listSection(title, items) {
  if (!items?.length) return "";
  return `<section class="detail-section"><h3>${escapeHtml(title)}</h3><ul class="detail-list">${items.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>`;
}

function ui(english, russian) {
  return state.lang === "ru" ? russian : english;
}

function statusExplanation(record) {
  if (record.kind !== "claim") {
    return record.curation_status === "provisional"
      ? ui("Working definition: useful for the map, but its boundaries may still change. This is not an evidence rating.", "Рабочее определение: оно уже используется на карте, но его границы ещё могут измениться. Это не оценка доказанности.")
      : ui("Curated ontology object. Its status describes the definition, not whether every related scientific claim is proven.", "Проверенный объект онтологии. Его статус относится к качеству определения, а не к доказанности всех связанных утверждений.");
  }
  const explanations = {
    supported: ui("The linked evidence supports this statement within the stated population and conditions.", "Связанные исследования поддерживают это утверждение в указанной выборке и условиях."),
    mixed: ui("Studies or analyses disagree. The statement should not be treated as settled.", "Исследования или анализы расходятся. Утверждение нельзя считать установленным."),
    unsupported: ui("The mapped evidence currently does not support this statement.", "Собранные данные сейчас не поддерживают это утверждение."),
    refuted: ui("The mapped evidence contradicts this statement within its tested scope.", "Собранные данные противоречат утверждению в проверенных границах."),
    proposed: ui("This is a testable hypothesis, not an established result.", "Это проверяемая гипотеза, а не установленный результат."),
    not_assessed: ui("The statement is represented, but its evidence has not yet been assessed.", "Утверждение представлено, но его доказательства ещё не оценены."),
  };
  return explanations[record.epistemic_status] || "";
}

function inferenceExplanation(claim) {
  const explanations = {
    causal_effect: ui("Causal claim: the study changed one factor and tested whether another changed as a consequence.", "Причинное утверждение: исследование изменяло один фактор и проверяло, изменился ли другой вследствие этого."),
    causal_hypothesis: ui("Causal hypothesis: a possible cause-and-effect path proposed for future testing.", "Причинная гипотеза: возможная цепочка причины и следствия, которую ещё нужно проверить."),
    association: ui("Association only: the elements vary together, but this does not show that one causes the other.", "Только связь: элементы изменяются совместно, но это не доказывает, что один вызывает другой."),
    prediction: ui("Prediction: one element forecasts another in data not used for fitting; prediction is not causation.", "Предсказание: один элемент прогнозирует другой на данных, не использованных для подгонки; прогноз не равен причинности."),
    mediation: claim.mediation_inference === "causal"
      ? ui("Causal mediation: the evidence aims to identify an intervening causal pathway.", "Причинная медиация: данные направлены на выявление промежуточного причинного пути.")
      : ui("Statistical mediation: the middle element explains part of an association statistically, not necessarily causally.", "Статистическая медиация: промежуточный элемент статистически объясняет часть связи, но не обязательно является причиной."),
    moderation: ui("Moderation: the strength or direction of a relationship differs depending on another condition.", "Модерация: сила или направление связи различается в зависимости от другого условия."),
    mechanism_hypothesis: ui("Mechanism hypothesis: a proposed process that could produce the outcome; it remains falsifiable.", "Гипотеза механизма: предполагаемый процесс, который может приводить к результату; его ещё можно опровергнуть."),
    definition: ui("Definition: this claim states how a concept is delimited, not an observed cause-and-effect result.", "Определение: утверждение задаёт границы понятия, а не описывает наблюдавшийся причинный эффект."),
  };
  return explanations[claim.claim_type] || "";
}

function roleFor(claim, id) {
  if (claim.exposure_id === id) {
    if (claim.claim_type === "causal_effect") return ui("tested cause", "проверяемая причина");
    if (claim.claim_type === "prediction") return ui("predictor", "предиктор");
    if (claim.claim_type === "association") return ui("associated factor", "связанный фактор");
    return ui("starting factor", "исходный фактор");
  }
  if (claim.mechanism_id === id) return ui("proposed process", "предполагаемый процесс");
  if (claim.mediator_id === id) return ui("intermediate link", "промежуточное звено");
  if (claim.moderator_id === id) return ui("condition changing the relationship", "условие, изменяющее связь");
  if (claim.outcome_id === id) {
    if (claim.claim_type === "causal_effect") return ui("tested consequence", "проверяемое следствие");
    if (claim.claim_type === "prediction") return ui("predicted result", "прогнозируемый результат");
    if (claim.claim_type === "association") return ui("associated result", "связанный результат");
    return ui("result", "результат");
  }
  if (claim.defined_object_id === id) return ui("defined concept", "определяемое понятие");
  return ui("related element", "связанный элемент");
}

function nodeLink(id, role) {
  const record = recordById(id);
  if (!record) return "";
  const label = record.kind === "claim" ? record.statement : record.label;
  return `<button class="inspector-node-link" type="button" data-select-id="${escapeHtml(id)}"><small>${escapeHtml(role)}</small>${escapeHtml(t(label))}</button>`;
}

function relationConnector(kind, label) {
  const symbols = { association: "↔", moderation: "↔", default: "→" };
  return `<span class="relation-connector relation-${escapeHtml(kind)}"><i aria-hidden="true">${symbols[kind] || symbols.default}</i><small>${escapeHtml(label)}</small></span>`;
}

function claimDiagram(claim) {
  if (claim.claim_type === "definition" && claim.defined_object_id) {
    return `<div class="claim-diagram kind-definition">${nodeLink(claim.defined_object_id, ui("defined concept", "определяемое понятие"))}</div>`;
  }

  const exposure = claim.exposure_id ? nodeLink(claim.exposure_id, roleFor(claim, claim.exposure_id)) : "";
  const outcome = claim.outcome_id ? nodeLink(claim.outcome_id, roleFor(claim, claim.outcome_id)) : "";
  if (!exposure && !outcome) return "";

  let main = "";
  if (claim.claim_type === "mediation" && claim.mediator_id) {
    const label = claim.mediation_inference === "causal" ? ui("causally through", "причинно через") : ui("statistically through", "статистически через");
    main = `${exposure}${relationConnector("mediation", label)}${nodeLink(claim.mediator_id, roleFor(claim, claim.mediator_id))}${relationConnector("mediation", label)}${outcome}`;
  } else if (claim.claim_type === "mechanism_hypothesis" && claim.mechanism_id) {
    main = `${exposure}${relationConnector("hypothesis", ui("may act through", "может действовать через"))}${nodeLink(claim.mechanism_id, roleFor(claim, claim.mechanism_id))}${relationConnector("hypothesis", ui("may contribute to", "может способствовать"))}${outcome}`;
  } else {
    const connectors = {
      causal_effect: ["causal", ui("causes in this study", "вызывает в этом исследовании")],
      causal_hypothesis: ["hypothesis", ui("may cause", "может вызывать")],
      association: ["association", ui("associated; no causal direction", "связаны; причинное направление не установлено")],
      prediction: ["prediction", ui("predicts; does not prove cause", "предсказывает; не доказывает причину")],
      moderation: ["moderation", ui("relationship changes", "связь изменяется")],
    };
    const [kind, label] = connectors[claim.claim_type] || ["neutral", ui("relates to", "связано с")];
    main = `${exposure}${relationConnector(kind, label)}${outcome}`;
  }

  const moderator = claim.moderator_id
    ? `<div class="moderator-branch"><span>${ui("This condition changes the strength or direction of the relationship", "Это условие изменяет силу или направление связи")}</span>${nodeLink(claim.moderator_id, roleFor(claim, claim.moderator_id))}</div>`
    : "";
  return `<div class="claim-diagram kind-${escapeHtml(claim.claim_type)}"><div class="diagram-main">${main}</div>${moderator}</div>`;
}

function relatedClaims(record) {
  if (record.kind === "claim") return [];
  return state.family.claims.filter(claim => linkedObjectIds(claim).includes(record.id) || claim.defined_object_id === record.id);
}

function renderConnections(record) {
  if (record.kind === "claim") {
    const diagram = claimDiagram(record);
    return diagram ? `<section class="explain-section"><h3>${ui("How the elements connect", "Как связаны элементы")}</h3><p class="inference-note">${escapeHtml(inferenceExplanation(record))}</p>${diagram}</section>` : "";
  }
  const claims = relatedClaims(record);
  if (!claims.length) return `<section class="explain-section"><h3>${ui("Connections", "Связи")}</h3><p>${ui("No empirical claim currently links this object to another map element.", "Пока нет эмпирического утверждения, связывающего этот объект с другим элементом карты.")}</p></section>`;
  return `<section class="explain-section"><h3>${ui("How it affects or relates to other elements", "Как влияет или связано с другими элементами")}</h3><div class="connection-list">${claims.map(claim => `
    <button class="connection-card" type="button" data-select-id="${escapeHtml(claim.id)}">
      <span class="connection-top"><strong>${escapeHtml(t(claim.claim_type))}</strong><span>${escapeHtml(t(STATUS_LABELS[claim.epistemic_status] || claim.epistemic_status))}</span></span>
      <span class="connection-role">${escapeHtml(roleFor(claim, record.id))}</span>
      <span>${escapeHtml(t(claim.statement))}</span>
      <small>${escapeHtml(inferenceExplanation(claim))}</small>
    </button>`).join("")}</div></section>`;
}

function bindInspectorLinks() {
  inspector.querySelectorAll("[data-select-id]").forEach(button => {
    button.addEventListener("click", () => selectNode(button.dataset.selectId));
  });
}

function actionabilityLabel(value) {
  const labels = {
    direct_within_tested_scope: ["Direct only in tested conditions", "Прямо подтверждено только в проверенных условиях"],
    transfer_uncertain: ["Promising transfer; not directly established", "Перенос выглядит возможным, но прямо не доказан"],
    interpretation_only: ["Interpretation or candidate action", "Интерпретация или кандидатное действие"],
  };
  const [en, ru] = labels[value] || [value, value];
  return ui(en, ru);
}

function practicalFor(record) {
  const applications = state.family.practical_implications || [];
  if (record.kind !== "claim") return [];
  return applications.filter(item => item.claim_ids.includes(record.id));
}

function renderPracticalImplications(applications, compact = false) {
  if (!applications.length) return "";
  return `<section class="practical-section ${compact ? "is-compact" : ""}">
    <div class="practical-heading">
      <div><span class="section-eyebrow">${ui("From evidence to possible use", "От данных к возможному применению")}</span><h3>${ui("What can be done with this?", "Что с этим можно делать?")}</h3></div>
      <span>${ui("Not automatic advice", "Не автоматический совет")}</span>
    </div>
    <p class="practical-rule">${ui(
      "Applications are curated separately from scientific claims. A plausible use is not presented as proven transfer.",
      "Применение курируется отдельно от научных утверждений. Правдоподобная польза не выдаётся за доказанный перенос."
    )}</p>
    <div class="practical-list">${applications.map(item => `
      <article class="practical-card action-${escapeHtml(item.actionability)}">
        <div class="practical-card-top"><strong>${escapeHtml(localText(item.title))}</strong><span>${escapeHtml(actionabilityLabel(item.actionability))} · ${escapeHtml(t(item.confidence))}</span></div>
        <p class="practical-question">${escapeHtml(localText(item.practical_question))}</p>
        <dl>
          <div><dt>${ui("Possible action", "Возможное действие")}</dt><dd>${escapeHtml(localText(item.action))}</dd></div>
          <div><dt>${ui("Expected change", "Ожидаемое изменение")}</dt><dd>${escapeHtml(localText(item.expected_change))}</dd></div>
          ${compact ? "" : `<div><dt>${ui("Why this follows from the evidence", "Почему это следует из данных")}</dt><dd>${escapeHtml(localText(item.evidence_basis))}</dd></div>`}
          <div><dt>${ui("What is not established", "Что не доказано")}</dt><dd>${escapeHtml(localText(item.not_established))}</dd></div>
          ${item.safety_note ? `<div class="practical-safety"><dt>${ui("Safety boundary", "Граница безопасности")}</dt><dd>${escapeHtml(localText(item.safety_note))}</dd></div>` : ""}
        </dl>
      </article>`).join("")}</div>
  </section>`;
}

function renderClaimPractical(record) {
  const applications = practicalFor(record);
  if (applications.length) return renderPracticalImplications(applications);
  const guidance = {
    definition: [
      ui("Use the definition to choose the right object and measurement, and to avoid mixing a construct with a task, score, state, or mechanism.", "Используйте определение для выбора правильного объекта и измерения и не смешивайте конструкт с заданием, баллом, состоянием или механизмом."),
      ui("Clearer interpretation and fewer category errors.", "Более ясная интерпретация и меньше ошибок классификации."),
      ui("A definition alone does not show that changing the object will improve an outcome.", "Одно определение не показывает, что изменение объекта улучшит результат."),
    ],
    association: [
      ui("Use the relationship to form a question, select additional measurements, or identify a group-level pattern; do not choose an intervention from the direction of association alone.", "Используйте связь для постановки вопроса, выбора дополнительных измерений или выявления групповой закономерности; не выбирайте вмешательство только по направлению связи."),
      ui("Better hypothesis generation and fewer false causal conclusions.", "Более точные гипотезы и меньше ложных причинных выводов."),
      ui("It is not established that changing either associated element will change the other.", "Не доказано, что изменение одного связанного элемента изменит другой."),
    ],
    prediction: [
      ui("Use the predictor only in populations and conditions where it was validated, and monitor errors on new data.", "Используйте предиктор только в тех группах и условиях, где он проверен, и контролируйте ошибки на новых данных."),
      ui("More disciplined forecasting within the validated scope.", "Более дисциплинированное прогнозирование в проверенных границах."),
      ui("Prediction does not identify a cause or justify changing the predictor as an intervention.", "Прогноз не выявляет причину и не оправдывает изменение предиктора как вмешательство."),
    ],
    causal_effect: [
      ui("If the tested manipulation is practical and safe, use the claim to estimate only the stated consequence under similar conditions, then verify transfer in the new setting.", "Если проверенное воздействие практично и безопасно, ожидайте только указанное следствие в сходных условиях и отдельно проверяйте перенос в новую ситуацию."),
      ui("A bounded expectation about what may change after a specific action.", "Ограниченное ожидание того, что может измениться после конкретного действия."),
      ui("The effect is not automatically a treatment, a durable benefit, or a result for every person and context.", "Эффект не становится автоматически лечением, долговременной пользой или результатом для каждого человека и контекста."),
    ],
    mediation: [
      ui("Use the intermediate variable to plan measurement; target it only when the mediation claim is causally identified and intervention evidence exists.", "Используйте промежуточную переменную для планирования измерений; воздействуйте на неё только при причинно установленной медиации и наличии данных вмешательства."),
      ui("A more explicit test of a possible pathway.", "Более явная проверка возможного пути воздействия."),
      ui("Statistical mediation does not prove that changing the mediator will change the outcome.", "Статистическая медиация не доказывает, что изменение посредника изменит результат."),
    ],
    moderation: [
      ui("Check the modifying condition before applying an average relationship to a person or setting.", "Проверяйте изменяющее условие, прежде чем переносить среднюю связь на человека или ситуацию."),
      ui("Better matching of expectations to context.", "Лучшее соответствие ожиданий конкретному контексту."),
      ui("A statistical interaction does not by itself identify why the effect differs or how to change it.", "Статистическое взаимодействие само по себе не объясняет причину различия и способ воздействия."),
    ],
    mechanism_hypothesis: [
      ui("Use the proposed process to design a discriminating test against alternatives, not as an established intervention target.", "Используйте предполагаемый процесс для проверки против альтернатив, а не как уже установленную цель вмешательства."),
      ui("A testable mechanism question and clearer competing explanations.", "Проверяемый вопрос о механизме и более ясные конкурирующие объяснения."),
      ui("It is not established that the process is necessary, sufficient, unique, or practically modifiable.", "Не доказано, что процесс необходим, достаточен, уникален или практически изменяем."),
    ],
    causal_hypothesis: [
      ui("Use the proposed causal direction to design a controlled test before acting on it.", "Используйте предполагаемое причинное направление для контролируемой проверки до практического применения."),
      ui("A falsifiable intervention question.", "Опровержимый вопрос о вмешательстве."),
      ui("The proposed direction is not yet an established effect.", "Предполагаемое направление ещё не является установленным эффектом."),
    ],
  };
  const [action, expected, notEstablished] = guidance[record.claim_type] || guidance.association;
  return `<section class="practical-section practical-fallback">
    <div class="practical-heading"><div><span class="section-eyebrow">${ui("Practical meaning of this claim", "Практический смысл этого утверждения")}</span><h3>${ui("How can this be used safely?", "Как это можно использовать без завышения?")}</h3></div><span>${ui("Inference rule", "Правило вывода")}</span></div>
    <p class="practical-rule">${ui("No claim-specific application has been independently established yet. The guidance below follows from the inference type.", "Отдельное применение именно этого утверждения пока не установлено. Ниже показано безопасное правило, следующее из типа научного вывода.")}</p>
    <article class="practical-card action-interpretation_only"><dl>
      <div><dt>${ui("Possible use", "Возможное применение")}</dt><dd>${escapeHtml(action)}</dd></div>
      <div><dt>${ui("Expected benefit", "Ожидаемая польза")}</dt><dd>${escapeHtml(expected)}</dd></div>
      <div><dt>${ui("What is not established", "Что не доказано")}</dt><dd>${escapeHtml(notEstablished)}</dd></div>
    </dl></article>
  </section>`;
}

function renderInspector(record) {
  if (record.kind === "question") {
    renderResearchQuestionInspector(record);
    return;
  }
  const sources = relatedSources(record);
  const evidence = evidenceFor(record);
  const definition = t(record.kind === "claim" ? record.statement : record.definition);
  const heading = record.kind === "claim" ? t(record.statement) : t(record.label);
  const status = record.epistemic_status || record.curation_status;
  const confidence = record.confidence?.level;
  const scope = typeof record.scope === "string" ? record.scope : record.scope?.population;
  inspector.innerHTML = `
    <p class="inspector-kicker">${escapeHtml(t(TYPE_LABELS[record.type] || record.type))} · ${escapeHtml(record.id.split(":").at(-1))}</p>
    <h2 class="${record.kind === "claim" ? "claim-heading" : ""}">${escapeHtml(heading)}</h2>
    <section class="meaning-card">
      <span class="section-eyebrow">${record.kind === "claim" ? ui("What is being claimed", "Что утверждается") : ui("What this means", "Что это значит")}</span>
      <p>${escapeHtml(definition)}</p>
    </section>
    ${record.kind === "claim" ? `<section class="plain-language-card">
      <span class="section-eyebrow">${ui("Source-checked plain explanation", "Проверенное по источникам объяснение")}</span>
      <p>${escapeHtml(t(record.plain_language_summary))}</p>
      <small>${ui("Editorial explanation of the linked evidence; it is not an additional scientific claim.", "Редакторское объяснение связанных данных; это не дополнительное научное утверждение.")}</small>
    </section>` : ""}
    <div class="evidence-summary status-${escapeHtml(status || "neutral")}">
      <div><span class="section-eyebrow">${record.kind === "claim" ? ui("Degree of evidence", "Степень доказанности") : ui("Definition status", "Статус определения")}</span><strong>${escapeHtml(t(STATUS_LABELS[status] || status))}</strong></div>
      ${confidence ? `<div><span class="section-eyebrow">${ui("Confidence", "Уверенность")}</span><strong>${escapeHtml(t(confidence))}</strong></div>` : ""}
      <p>${escapeHtml(statusExplanation(record))}</p>
    </div>
    ${renderConnections(record)}
    ${record.kind === "claim" ? renderClaimPractical(record) : ""}
    ${scope ? `<section class="detail-section"><h3>${t("Scope")}</h3><p>${escapeHtml(t(scope))}</p></section>` : ""}
    ${record.confidence?.rationale ? `<section class="detail-section"><h3>${t("Confidence rationale")}</h3><p>${escapeHtml(t(record.confidence.rationale))}</p></section>` : ""}
    ${evidence.length ? `<section class="detail-section"><h3>${t("Evidence")}</h3><ul class="detail-list">${evidence.map(item => `<li><strong>${escapeHtml(t(item.support_direction))}</strong> · ${escapeHtml(t(item.summary))}</li>`).join("")}</ul></section>` : ""}
    ${listSection(t("Limitations"), (record.limitations || record.boundary_notes || record.scope?.boundary_conditions)?.map(t))}
    ${sources.length ? `<section class="detail-section"><h3>${t("Sources")}</h3><div class="source-list">${sources.map(source => `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(t(source.title))}<span class="source-meta">${escapeHtml(source.year)} · ${escapeHtml(source.doi || source.pmid || "")}</span></a>`).join("")}</div></section>` : ""}
  `;
  bindInspectorLinks();
}

function renderResearchQuestionInspector(record) {
  const sources = relatedSources(record);
  inspector.innerHTML = `
    <p class="inspector-kicker">${ui("Open research question", "Открытый исследовательский вопрос")} · ${escapeHtml(record.id.split(":").at(-1))}</p>
    <h2 class="question-heading">${escapeHtml(localText(record.question))}</h2>
    <section class="research-question-note">
      <span class="section-eyebrow">${ui("How to read this card", "Как читать эту карточку")}</span>
      <p>${ui("This is a mapped knowledge gap, not a scientific finding, hypothesis score, or claim that no research exists.", "Это отмеченный пробел в знаниях, а не научный результат, оценка гипотезы или утверждение, что исследований вообще нет.")}</p>
    </section>
    <section class="detail-section">
      <h3>${ui("Why it remains open", "Почему вопрос остаётся открытым")}</h3>
      <p>${escapeHtml(localText(record.why_open))}</p>
    </section>
    <section class="detail-section">
      <h3>${ui("What evidence would help", "Какие данные помогли бы")}</h3>
      <p>${escapeHtml(localText(record.what_would_help))}</p>
    </section>
    <section class="detail-section">
      <h3>${ui("Related map elements", "Связанные элементы карты")}</h3>
      <div class="connection-list">${record.about_ids.map(id => nodeLink(id, ui("question concerns", "вопрос относится к"))).join("")}</div>
    </section>
    ${sources.length ? `<section class="detail-section"><h3>${t("Sources")}</h3><div class="source-list">${sources.map(source => `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(t(source.title))}<span class="source-meta">${escapeHtml(source.year)} · ${escapeHtml(source.doi || source.pmid || "")}</span></a>`).join("")}</div></section>` : ""}
  `;
  bindInspectorLinks();
}

function emphasizeSelection(id) {
  const connected = new Set([id]);
  svg.querySelectorAll(".edge").forEach(edge => {
    const active = edge.dataset.source === id || edge.dataset.target === id;
    edge.classList.toggle("is-dimmed", !active);
    if (active) {
      connected.add(edge.dataset.source);
      connected.add(edge.dataset.target);
    }
  });
  svg.querySelectorAll(".node").forEach(node => {
    node.classList.toggle("is-selected", node.dataset.id === id);
    node.classList.toggle("is-dimmed", !connected.has(node.dataset.id));
  });
}

function selectNode(id) {
  const record = recordById(id);
  if (!record) return;
  state.selectedId = id;
  emphasizeSelection(id);
  renderInspector(record);
  if (window.innerWidth < 900) inspector.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderEmptyInspector() {
  const familyNumber = String(state.data.families.indexOf(state.family) + 1).padStart(2, "0");
  const sources = state.family.sources || [];
  const applications = state.family.practical_implications || [];
  const sourceLinks = sources.map(source => {
    const metadata = [source.year, source.doi || source.pmid].filter(Boolean).join(" · ") || ui("Open source", "Открыть источник");
    return `
      <a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">
        ${escapeHtml(t(source.title))}
        <span class="source-meta">${escapeHtml(metadata)}</span>
      </a>
    `;
  }).join("");

  inspector.innerHTML = `
    <div class="inspector-empty family-overview">
      <span class="empty-index">${familyNumber}</span>
      <h2>${escapeHtml(t(state.family.title))}</h2>
      <section class="family-overview-card">
        <span class="section-eyebrow">${ui("What this section studies", "Что изучает этот раздел")}</span>
        <p>${escapeHtml(t(state.family.description))}</p>
      </section>
      <div class="family-stats" aria-label="${ui("Section contents", "Состав раздела")}">
        <div><strong>${state.family.objects.length}</strong><span>${ui("objects", "объектов")}</span></div>
        <div><strong>${state.family.claims.length}</strong><span>${ui("claims", "утверждений")}</span></div>
        <div><strong>${state.family.evidence.length}</strong><span>${ui("evidence records", "записей доказательств")}</span></div>
        <div class="question-stat"><strong>${state.family.research_questions?.length || 0}</strong><span>${ui("open questions", "открытых вопросов")}</span></div>
        <div class="application-stat"><strong>${applications.length}</strong><span>${ui("practical interpretations", "практических интерпретаций")}</span></div>
        <div><strong>${sources.length}</strong><span>${ui("sources", "источников")}</span></div>
      </div>
      ${renderPracticalImplications(applications, true)}
      <section class="detail-section family-sources">
        <h3>${ui("Sources included in this section", "Источники этого раздела")}</h3>
        <p class="family-source-note">${ui(
          "There is no single defining source. This is a curated evidence pack assembled from the publications below, not a diagnosis or an exhaustive systematic review.",
          "У раздела нет одного определяющего источника. Это отобранный пакет доказательств из публикаций ниже, а не диагноз и не исчерпывающий систематический обзор."
        )}</p>
        <div class="source-list">${sourceLinks}</div>
      </section>
      <p class="family-select-hint">${ui(
        "Select a map element to see its plain-language meaning, evidence status, causal role, limitations, and linked sources.",
        "Выберите элемент карты, чтобы увидеть простое объяснение, степень доказанности, причинную роль, ограничения и связанные источники."
      )}</p>
    </div>
  `;
}

function clearSelection() {
  if (!state.selectedId) return;
  state.selectedId = null;
  svg.querySelectorAll(".is-selected, .is-dimmed").forEach(element => {
    element.classList.remove("is-selected", "is-dimmed");
  });
  renderEmptyInspector();
}

function renderFamilies() {
  const strip = document.getElementById("family-strip");
  strip.innerHTML = state.data.families.map((family, index) => `
    <button class="family-button ${family.id === state.family.id ? "is-active" : ""}" type="button" role="tab" aria-selected="${family.id === state.family.id}" data-family="${family.id}">
      <span class="family-number">${String(index + 1).padStart(2, "0")}</span>
      <strong>${escapeHtml(t(family.title))}</strong>
      <span>${family.objects.length} ${state.lang === "ru" ? "объектов" : "objects"} · ${family.claims.length} ${state.lang === "ru" ? "утверждений" : "claims"}</span>
    </button>
  `).join("");
  strip.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    state.family = state.data.families.find(item => item.id === button.dataset.family);
    state.selectedId = null;
    renderEmptyInspector();
    renderFamilies();
    renderFamilyDescription();
    renderMap();
  }));
}

function renderFamilyDescription() {
  document.getElementById("family-description").textContent = t(state.family.description);
}

function mechanismStatusSummary(mechanism) {
  const entries = Object.entries(mechanism.claim_status_counts);
  if (!entries.length) return ui("No linked scientific claims", "Нет связанных научных утверждений");
  return entries
    .map(([status, count]) => `${count} ${t(STATUS_LABELS[status] || status)}`)
    .join(" · ");
}

function renderMechanismCatalog() {
  const query = state.mechanismQuery.trim().toLocaleLowerCase(state.lang === "ru" ? "ru" : "en");
  const mechanisms = state.data.mechanism_index.filter(mechanism => {
    const searchable = [
      t(mechanism.label),
      t(mechanism.definition),
      t(mechanism.family_title),
      t(mechanism.mechanism_kind),
    ].join(" ").toLocaleLowerCase(state.lang === "ru" ? "ru" : "en");
    return !query || searchable.includes(query);
  });
  document.getElementById("mechanism-count").textContent = `${state.data.mechanism_index.length} ${ui("mechanisms", "механизмов")}`;
  const search = document.getElementById("mechanism-search");
  search.placeholder = ui("Search by mechanism, family, or kind", "Поиск по механизму, теме или виду");
  search.value = state.mechanismQuery;
  const grid = document.getElementById("mechanism-grid");
  grid.innerHTML = mechanisms.length ? mechanisms.map(mechanism => `
    <article class="mechanism-card">
      <p>${escapeHtml(t(mechanism.family_title))}</p>
      <h3>${escapeHtml(t(mechanism.label))}</h3>
      <span class="mechanism-kind">${escapeHtml(t(mechanism.mechanism_kind))}</span>
      <p class="mechanism-definition">${escapeHtml(t(mechanism.definition))}</p>
      <div class="mechanism-metrics">
        <span><strong>${mechanism.claim_ids.length}</strong>${ui("linked claims", "связанных утверждений")}</span>
        <span><strong>${mechanism.evidence_count}</strong>${ui("evidence records", "записей доказательств")}</span>
        <span><strong>${mechanism.source_count}</strong>${ui("sources", "источников")}</span>
      </div>
      <p class="mechanism-status">${escapeHtml(mechanismStatusSummary(mechanism))}</p>
      <button type="button" data-open-mechanism="${escapeHtml(mechanism.id)}" data-family-id="${escapeHtml(mechanism.family_id)}">${ui("Open in map", "Открыть на карте")}</button>
    </article>
  `).join("") : `<p class="catalog-empty">${ui("No mechanisms match this search.", "По этому запросу механизмы не найдены.")}</p>`;

  grid.querySelectorAll("[data-open-mechanism]").forEach(button => {
    button.addEventListener("click", () => {
      state.family = state.data.families.find(family => family.id === button.dataset.familyId);
      state.filter = "all";
      document.querySelectorAll(".filter-button").forEach(item => item.classList.toggle("is-active", item.dataset.filter === "all"));
      renderFamilies();
      renderFamilyDescription();
      renderMap();
      selectNode(button.dataset.openMechanism);
      document.getElementById("mechanism-catalog").open = false;
      document.querySelector(".map-layout").scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

function navigationSource(sourceId) {
  return state.data.navigation_views.sources.find(source => source.id === sourceId);
}

function canonicalRecord(familyId, canonicalId) {
  const family = state.data.families.find(item => item.id === familyId);
  if (!family) return null;
  const record = [...family.objects, ...family.claims].find(item => item.id === canonicalId);
  return record ? { family, record } : null;
}

function coverageLabel(coverage) {
  const labels = {
    partial: ["Partially modeled", "Частично смоделировано"],
    planned: ["Not modeled yet", "Пока не смоделировано"],
    complete: ["Modeled", "Смоделировано"],
  };
  const [en, ru] = labels[coverage] || [coverage, coverage];
  return ui(en, ru);
}

function membershipRole(role) {
  const labels = {
    construct_example: ["Construct", "Конструкт"],
    task_context_example: ["Task context, not the construct", "Контекст задания, не сам конструкт"],
    measurement_example: ["Measurement, not the ability itself", "Измерение, не сама способность"],
    mechanism_example: ["Proposed mechanism", "Предложенный механизм"],
    state_example: ["Momentary state", "Текущее состояние"],
    regulation_mechanism_example: ["Regulation mechanism", "Механизм регуляции"],
    intervention_example: ["Experimental intervention", "Экспериментальное воздействие"],
    appraisal_mechanism_example: ["Appraisal mechanism", "Механизм оценки"],
    behavior_example: ["Observable response", "Наблюдаемый ответ"],
    mapped_record: ["Mapped canonical record", "Сопоставленная каноническая запись"],
  };
  const [en, ru] = labels[role] || [role, role];
  return ui(en, ru);
}

function nodeKindLabel(kind) {
  const labels = {
    topic: ["Topic", "Тема"],
    taxonomy: ["Taxonomy", "Классификация"],
    domain: ["Domain", "Раздел"],
  };
  const [en, ru] = labels[kind] || [kind.replaceAll("_", " "), kind.replaceAll("_", " ")];
  return ui(en, ru);
}

function systemKindLabel(kind) {
  const labels = {
    research_framework: ["Research framework", "Исследовательская система"],
    collaborative_knowledge_base: ["Collaborative knowledge base", "Совместная база знаний"],
    trait_taxonomy: ["Trait taxonomy", "Классификация черт"],
    developmental_individual_differences_framework: ["Developmental framework", "Модель индивидуального развития"],
    psychopathology_taxonomy: ["Psychopathology taxonomy", "Классификация психопатологии"],
  };
  const [en, ru] = labels[kind] || [kind.replaceAll("_", " "), kind.replaceAll("_", " ")];
  return ui(en, ru);
}

function modelKindLabel(kind) {
  const labels = {
    developmental_social_theory: ["Developmental-social theory", "Теория социального развития"],
    therapeutic_formulation: ["Therapeutic formulation", "Терапевтическая формулировка"],
    learning_framework: ["Learning framework", "Модель научения"],
    affective_framework: ["Emotion framework", "Модель эмоций"],
    motivational_framework: ["Motivational framework", "Мотивационная модель"],
    control_framework: ["Control framework", "Модель контроля"],
    developmental_framework: ["Developmental framework", "Модель развития"],
    individual_differences_framework: ["Individual-differences framework", "Модель индивидуальных различий"],
    adaptation_framework: ["Adaptation framework", "Модель адаптации"],
  };
  const [en, ru] = labels[kind] || [kind.replaceAll("_", " "), kind.replaceAll("_", " ")];
  return ui(en, ru);
}

function renderViewSources(sourceIds = []) {
  return sourceIds.map(sourceId => navigationSource(sourceId)).filter(Boolean).map(source => `
    <a class="view-source" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">
      ${escapeHtml(source.title)} <span>↗</span>
    </a>
  `).join("");
}

function renderMemberships(memberships = []) {
  if (!memberships.length) {
    return `<p class="coverage-gap">${ui(
      "No canonical PMM records have been curated for this area yet. The gap is visible by design.",
      "Для этой области пока не отобраны канонические записи PMM. Пробел показан намеренно."
    )}</p>`;
  }
  return `<div class="view-memberships">${memberships.map(membership => {
    const resolved = canonicalRecord(membership.family_id, membership.canonical_id);
    if (!resolved) return "";
    const { family, record } = resolved;
    return `
      <button class="canonical-link" type="button" data-family-id="${escapeHtml(family.id)}" data-canonical-id="${escapeHtml(record.id)}">
        <span class="canonical-role">${escapeHtml(membershipRole(membership.role || "mapped_record"))}</span>
        <strong>${escapeHtml(t(record.label || record.statement))}</strong>
        <small>${escapeHtml(t(TYPE_LABELS[record.type] || record.type))} · ${escapeHtml(t(family.title))}</small>
        <i>${ui("Open evidence record", "Открыть запись с доказательствами")} →</i>
      </button>
    `;
  }).join("")}</div>`;
}

function bindCanonicalLinks(container) {
  container.querySelectorAll("[data-canonical-id]").forEach(button => {
    button.addEventListener("click", () => openCanonicalRecord(button.dataset.familyId, button.dataset.canonicalId));
  });
}

function renderFoundationalModels() {
  const view = state.data.navigation_views.foundational_models;
  const container = document.getElementById("foundational-models-view");
  container.innerHTML = `
    <header class="view-hero models-hero">
      <div>
        <p class="view-kicker">${ui("Process-based entry · not a school ranking", "Процессный вход · не рейтинг школ")}</p>
        <h2>${escapeHtml(localText(view.title))}</h2>
        <p class="view-subtitle">${escapeHtml(localText(view.subtitle))}</p>
      </div>
      <aside class="method-note pbt-note">
        <strong>${ui("PBT architecture rule", "Архитектурное правило PBT")}</strong>
        <p>${escapeHtml(localText(view.process_based_note))}</p>
        <div class="pbt-sources">${renderViewSources(view.source_ids)}</div>
      </aside>
    </header>
    <ol class="pbt-workflow" aria-label="${ui("Process-based workflow", "Процессный рабочий цикл")}">
      ${view.workflow.map((step, index) => `<li><span>${String(index + 1).padStart(2, "0")}</span><strong>${escapeHtml(localText(step))}</strong></li>`).join("")}
    </ol>
    <div class="model-grid">
      ${view.models.map((model, index) => `
        <article class="model-card coverage-${model.coverage}">
          <header>
            <span class="model-index">${String(index + 1).padStart(2, "0")}</span>
            <div><p>${escapeHtml(modelKindLabel(model.model_kind))}</p><h3>${escapeHtml(localText(model.label))}</h3></div>
            <span class="coverage-chip">${coverageLabel(model.coverage)}</span>
          </header>
          <p class="model-summary">${escapeHtml(localText(model.plain_summary))}</p>
          <section class="human-chain">
            <strong>${ui("Plain process chain", "Понятная цепочка процесса")}</strong>
            <ol>${model.chain.map((step, stepIndex) => `<li><span>${stepIndex + 1}</span><p>${escapeHtml(localText(step))}</p></li>`).join("")}</ol>
          </section>
          <section class="leverage-box"><strong>${ui("Where change can be tested", "Где можно проверить изменение")}</strong><p>${escapeHtml(localText(model.practical_focus))}</p></section>
          <div class="model-evidence-grid">
            <section><strong>${ui("Empirically established", "Эмпирически установлено")}</strong><p>${escapeHtml(localText(model.established))}</p></section>
            <section class="proposed"><strong>${ui("Proposed or unresolved", "Предложено или не решено")}</strong><p>${escapeHtml(localText(model.proposed))}</p></section>
            <section><strong>${ui("How it is measured", "Как это измеряют")}</strong><p>${escapeHtml(localText(model.measurements))}</p></section>
            <section class="limit"><strong>${ui("Do not overread", "Что нельзя заключать")}</strong><p>${escapeHtml(localText(model.limitation))}</p></section>
          </div>
          ${renderMemberships(model.mapped_memberships)}
          <details class="view-sources"><summary>${ui("Sources for this model", "Источники модели")}</summary>${renderViewSources(model.source_ids)}</details>
        </article>
      `).join("")}
    </div>
    <p class="scope-footer">${ui(
      "Model names make the map readable. Canonical records, scoped claims, and repeated outcome checks carry the scientific weight.",
      "Названия моделей делают карту понятной. Научную нагрузку несут канонические записи, ограниченные утверждения и повторные проверки результатов."
    )}</p>
  `;
  bindCanonicalLinks(container);
}

function renderGeneralPsychology() {
  const view = state.data.navigation_views.general_psychology;
  const coverageTopics = view.nodes.filter(node => ["topic", "taxonomy"].includes(node.kind));
  const partialTopicCount = coverageTopics.filter(node => node.coverage === "partial").length;
  const plannedTopicCount = coverageTopics.filter(node => node.coverage === "planned").length;
  const byParent = new Map();
  for (const node of view.nodes) {
    const key = node.parent_id || "root";
    byParent.set(key, [...(byParent.get(key) || []), node]);
  }
  const domains = byParent.get(view.root_id) || [];
  const container = document.getElementById("general-psychology-view");
  container.innerHTML = `
    <header class="view-hero">
      <div>
        <p class="view-kicker">${ui("Educational navigation · pilot v0.1", "Учебная навигация · пилот v0.1")}</p>
        <h2>${escapeHtml(localText(view.title))}</h2>
        <p class="view-subtitle">${escapeHtml(localText(view.subtitle))}</p>
      </div>
      <aside class="method-note">
        <strong>${ui("Important distinction", "Важное различие")}</strong>
        <p>${escapeHtml(localText(view.methodological_note))}</p>
      </aside>
    </header>
    <div class="view-legend">
      <span><i class="coverage-dot partial"></i>${coverageLabel("partial")}</span>
      <span><i class="coverage-dot planned"></i>${coverageLabel("planned")}</span>
      <span><strong>${partialTopicCount}</strong> ${ui("areas with evidence", "областей с данными")}</span>
      <span><strong>${plannedTopicCount}</strong> ${ui("explicit gaps", "явных пробелов")}</span>
      <p>${ui(
        "A category is a navigation facet. Colored record cards below are the canonical scientific objects.",
        "Категория — это способ навигации. Цветные карточки ниже — канонические научные объекты."
      )}</p>
    </div>
    <div class="domain-grid">
      ${domains.map((domain, index) => {
        const topics = byParent.get(domain.id) || [];
        return `
          <article class="domain-card coverage-${domain.coverage}">
            <header>
              <span class="domain-index">${String(index + 1).padStart(2, "0")}</span>
              <div>
                <p>${ui("Area of psychology", "Раздел психологии")}</p>
                <h3>${escapeHtml(localText(domain.label))}</h3>
              </div>
              <span class="coverage-chip">${coverageLabel(domain.coverage)}</span>
            </header>
            <p class="domain-description">${escapeHtml(localText(domain.description))}</p>
            <div class="topic-list">
              ${topics.map(topic => `
                <section class="topic-card coverage-${topic.coverage}">
                  <div class="topic-heading">
                    <div>
                      <span>${escapeHtml(nodeKindLabel(topic.kind))}</span>
                      <h4>${escapeHtml(localText(topic.label))}</h4>
                    </div>
                    <span class="coverage-chip">${coverageLabel(topic.coverage)}</span>
                  </div>
                  <p>${escapeHtml(localText(topic.description))}</p>
                  ${topic.ontological_note ? `<p class="ontology-note"><strong>${ui("How PMM treats it:", "Как это трактует PMM:")}</strong> ${escapeHtml(localText(topic.ontological_note))}</p>` : ""}
                  ${renderMemberships(topic.memberships || [])}
                  <details class="view-sources"><summary>${ui("Definitions and alignment sources", "Источники определений и сопоставлений")}</summary>${renderViewSources(topic.source_ids)}</details>
                </section>
              `).join("")}
            </div>
          </article>
        `;
      }).join("")}
    </div>
    <p class="scope-footer">${ui(
      "The main-area scaffold is now visible, but partial means only that at least one evidence pack exists. It does not mean that the area is complete or scientifically settled.",
      "Каркас основных областей теперь виден полностью, но статус «частично» означает лишь наличие хотя бы одного пакета доказательств. Он не означает, что область заполнена полностью или научно закрыта."
    )}</p>
  `;
  bindCanonicalLinks(container);
}

function renderScientificSystems() {
  const view = state.data.navigation_views.scientific_systems;
  const container = document.getElementById("scientific-systems-view");
  container.innerHTML = `
    <header class="view-hero systems-hero">
      <div>
        <p class="view-kicker">${ui("Crosswalk, not a merger", "Сопоставление, а не слияние")}</p>
        <h2>${escapeHtml(localText(view.title))}</h2>
        <p class="view-subtitle">${escapeHtml(localText(view.subtitle))}</p>
      </div>
      <aside class="method-note">
        <strong>${ui("Reading rule", "Правило чтения")}</strong>
        <p>${ui(
          "A mapped record means that PMM documents a qualified correspondence. It does not mean the systems define the term identically.",
          "Связанная запись означает, что PMM документирует ограниченное соответствие. Это не означает, что системы определяют термин одинаково."
        )}</p>
      </aside>
    </header>
    <div class="systems-grid">
      ${view.systems.map((system, index) => `
        <article class="system-card coverage-${system.coverage}">
          <header>
            <span>${String(index + 1).padStart(2, "0")}</span>
            <div><p>${escapeHtml(systemKindLabel(system.system_kind))}</p><h3>${escapeHtml(localText(system.label))}</h3></div>
            <span class="coverage-chip">${coverageLabel(system.coverage)}</span>
          </header>
          <section><strong>${ui("What it is", "Что это")}</strong><p>${escapeHtml(localText(system.scope))}</p></section>
          <section class="system-limit"><strong>${ui("Do not use it as", "Чем это не является")}</strong><p>${escapeHtml(localText(system.limitation))}</p></section>
          ${renderMemberships((system.mapped_memberships || []).map(item => ({ ...item, role: "mapped_record" })))}
          <div class="system-sources">${renderViewSources(system.source_ids)}</div>
        </article>
      `).join("")}
    </div>
  `;
  bindCanonicalLinks(container);
}

function setPerspective(perspective, persist = true) {
  const allowed = new Set(["models", "general", "mechanisms", "systems"]);
  state.perspective = allowed.has(perspective) ? perspective : "models";
  if (persist) localStorage.setItem("pmm-perspective", state.perspective);
  document.querySelectorAll("[data-perspective-panel]").forEach(panel => {
    panel.hidden = panel.dataset.perspectivePanel !== state.perspective;
  });
  document.querySelectorAll("[data-perspective]").forEach(button => {
    const active = button.dataset.perspective === state.perspective;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  if (state.perspective === "mechanisms") requestAnimationFrame(() => renderMap());
}

function openCanonicalRecord(familyId, canonicalId) {
  state.family = state.data.families.find(family => family.id === familyId);
  state.filter = "all";
  state.selectedId = null;
  document.querySelectorAll(".filter-button").forEach(item => item.classList.toggle("is-active", item.dataset.filter === "all"));
  renderFamilies();
  renderFamilyDescription();
  setPerspective("mechanisms");
  requestAnimationFrame(() => {
    renderMap();
    selectNode(canonicalId);
    document.querySelector(".map-layout").scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function setLanguage(language) {
  state.lang = language;
  localStorage.setItem("pmm-language", language);
  document.getElementById("language-toggle").textContent = language === "ru" ? "EN" : "RU";
  translateStaticDom();
  renderFamilies();
  renderFamilyDescription();
  renderMechanismCatalog();
  renderFoundationalModels();
  renderGeneralPsychology();
  renderScientificSystems();
  renderMap();
  if (state.selectedId) renderInspector(recordById(state.selectedId));
  else renderEmptyInspector();
}

async function init() {
  try {
    prepareStaticDom();
    const [response, translationResponse] = await Promise.all([fetch(DATA_URL), fetch(RU_URL)]);
    if (!response.ok || !translationResponse.ok) throw new Error(`HTTP ${response.status}/${translationResponse.status}`);
    state.data = await response.json();
    state.translations = (await translationResponse.json()).translations;
    state.family = state.data.families[0];
    document.getElementById("build-version").textContent = `Schema ${state.data.pmm_version} · Interface ${state.data.interface_version}`;
    renderFamilies();
    renderFamilyDescription();
    renderMechanismCatalog();
    renderFoundationalModels();
    renderGeneralPsychology();
    renderScientificSystems();
    renderMap();
    document.getElementById("language-toggle").addEventListener("click", () => setLanguage(state.lang === "ru" ? "en" : "ru"));
    document.getElementById("mechanism-search").addEventListener("input", event => {
      state.mechanismQuery = event.target.value;
      renderMechanismCatalog();
      document.getElementById("mechanism-search").focus();
    });
    document.querySelectorAll("[data-perspective]").forEach(button => {
      button.addEventListener("click", () => setPerspective(button.dataset.perspective));
    });
    svg.addEventListener("click", event => {
      if (!event.target.closest(".node")) clearSelection();
    });
    svg.addEventListener("keydown", event => {
      if (event.key === "Escape") clearSelection();
    });
    setLanguage(state.lang);
    setPerspective(state.perspective, false);

    document.querySelectorAll(".filter-button").forEach(button => button.addEventListener("click", () => {
      state.filter = button.dataset.filter;
      state.selectedId = null;
      document.querySelectorAll(".filter-button").forEach(item => item.classList.toggle("is-active", item === button));
      renderMap();
      renderEmptyInspector();
    }));
    new ResizeObserver(() => renderMap()).observe(svg);
  } catch (error) {
    inspector.innerHTML = `<div class="inspector-empty"><span class="empty-index">!</span><h2>${t("Data failed to load")}</h2><p>${t("Open the site through a local server or GitHub Pages.")} ${escapeHtml(error.message)}</p></div>`;
  }
}

init();
