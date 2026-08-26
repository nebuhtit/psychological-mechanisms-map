const DATA_URL = "data/pmm-data.json";
const RU_URL = "data/i18n-ru.json";

const UI_RU = {
  "Evidence-aware knowledge map": "Карта знаний с учётом доказательств",
  "The mind as a map of": "Психика как карта",
  "testable mechanisms": "проверяемых механизмов",
  "Source data ↗": "Исходные данные ↗",
  "All": "Все",
  "Causal": "Причинные",
  "Hypotheses": "Гипотезы",
  "Contested": "Спорные",
  "How to read this map": "Как читать эту карту",
  "Open guide": "Открыть инструкцию",
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
  "mixed evidence": "смешанные данные",
  "unsupported": "не поддерживается",
  "refuted": "опровергнуто",
  "not assessed": "не оценено",
  "high": "высокая",
  "moderate": "умеренная",
  "low": "низкая",
  "very_low": "очень низкая",
  "supports": "поддерживает",
  "challenges": "оспаривает",
  "neutral": "нейтрально",
  "causal_effect": "причинный эффект",
  "causal_mechanism": "причинный механизм",
  "correlation": "корреляция",
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
};

const STATUS_LABELS = {
  supported: "supported",
  mixed: "mixed evidence",
  unsupported: "unsupported",
  refuted: "refuted",
  proposed: "proposed",
  not_assessed: "not assessed",
};

const state = { data: null, translations: {}, lang: localStorage.getItem("pmm-language") || "en", family: null, filter: "all", selectedId: null };
const svg = document.getElementById("knowledge-map");
const inspector = document.getElementById("inspector");

function t(value = "") {
  if (state.lang !== "ru") return value;
  return UI_RU[value] || state.translations[value] || value;
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
  return [...objects, ...claims];
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

  const nodes = familyRecords().filter(item => item.kind === "object" ? relevantObjects.has(item.id) : visibleClaimIds.has(item.id));
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
  return { nodes, edges };
}

function layoutNodes(nodes, width, height, compact) {
  const typeOrder = {
    Context: 0, Intervention: 1, Event: 2, Contingency: 3,
    Construct: 4, Mechanism: 5, claim: 6, State: 7,
    Behavior: 8, Outcome: 9, Measurement: 10, Observation: 11,
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
      class: `edge ${edge.type === "claim" ? "claim-edge" : ""}`,
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
    group.append(svgElement("rect", isClaim
      ? { x: "-86", y: "-38", width: "172", height: "76", rx: "12", class: "node-shape" }
      : { x: "-72", y: "-31", width: "144", height: "62", rx: node.type === "Mechanism" ? "31" : "4", class: "node-shape" }));

    const typeText = svgElement("text", { x: "0", y: "-10", "text-anchor": "middle", class: "node-type" });
    typeText.textContent = t(TYPE_LABELS[node.type] || node.type);
    group.append(typeText);
    const lines = wrapLabel(node.label, isClaim ? 20 : 22);
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
  if (record.kind === "claim") {
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

function renderInspector(record) {
  const sources = relatedSources(record);
  const evidence = evidenceFor(record);
  const definition = t(record.kind === "claim" ? record.statement : record.definition);
  const status = record.epistemic_status || record.curation_status;
  const confidence = record.confidence?.level;
  const scope = typeof record.scope === "string" ? record.scope : record.scope?.population;
  inspector.innerHTML = `
    <p class="inspector-kicker">${escapeHtml(t(TYPE_LABELS[record.type] || record.type))} · ${escapeHtml(record.id.split(":").at(-1))}</p>
    <h2>${escapeHtml(record.kind === "claim" ? wrapLabel(t(record.statement), 48).join(" ") : t(record.label))}</h2>
    <div class="status-line">
      ${status ? `<span class="status-chip">${escapeHtml(t(STATUS_LABELS[status] || status))}</span>` : ""}
      ${confidence ? `<span class="status-chip">${state.lang === "ru" ? "уверенность" : "confidence"}: ${escapeHtml(t(confidence))}</span>` : ""}
      ${record.claim_type ? `<span class="status-chip">${escapeHtml(t(record.claim_type))}</span>` : ""}
    </div>
    <p>${escapeHtml(definition)}</p>
    ${scope ? `<section class="detail-section"><h3>${t("Scope")}</h3><p>${escapeHtml(t(scope))}</p></section>` : ""}
    ${record.confidence?.rationale ? `<section class="detail-section"><h3>${t("Confidence rationale")}</h3><p>${escapeHtml(t(record.confidence.rationale))}</p></section>` : ""}
    ${evidence.length ? `<section class="detail-section"><h3>${t("Evidence")}</h3><ul class="detail-list">${evidence.map(item => `<li><strong>${escapeHtml(t(item.support_direction))}</strong> · ${escapeHtml(t(item.summary))}</li>`).join("")}</ul></section>` : ""}
    ${listSection(t("Limitations"), (record.limitations || record.boundary_notes || record.scope?.boundary_conditions)?.map(t))}
    ${sources.length ? `<section class="detail-section"><h3>${t("Sources")}</h3><div class="source-list">${sources.map(source => `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(t(source.title))}<span class="source-meta">${escapeHtml(source.year)} · ${escapeHtml(source.doi || source.pmid || "")}</span></a>`).join("")}</div></section>` : ""}
  `;
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

function renderFamilies() {
  const strip = document.getElementById("family-strip");
  strip.innerHTML = state.data.families.map((family, index) => `
    <button class="family-button ${family.id === state.family.id ? "is-active" : ""}" type="button" role="tab" aria-selected="${family.id === state.family.id}" data-family="${family.id}">
      <span class="family-number">0${index + 1}</span>
      <strong>${escapeHtml(t(family.title))}</strong>
      <span>${family.objects.length} ${state.lang === "ru" ? "объектов" : "objects"} · ${family.claims.length} ${state.lang === "ru" ? "утверждений" : "claims"}</span>
    </button>
  `).join("");
  strip.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    state.family = state.data.families.find(item => item.id === button.dataset.family);
    state.selectedId = null;
    inspector.innerHTML = `<div class="inspector-empty"><span class="empty-index">0${state.data.families.indexOf(state.family) + 1}</span><h2>${escapeHtml(t(state.family.title))}</h2><p>${t("Select an object or scientific Claim card on the map.")}</p></div>`;
    renderFamilies();
    renderFamilyDescription();
    renderMap();
  }));
}

function renderFamilyDescription() {
  document.getElementById("family-description").textContent = t(state.family.description);
}

function setLanguage(language) {
  state.lang = language;
  localStorage.setItem("pmm-language", language);
  document.getElementById("language-toggle").textContent = language === "ru" ? "EN" : "RU";
  translateStaticDom();
  renderFamilies();
  renderFamilyDescription();
  renderMap();
  if (state.selectedId) renderInspector(recordById(state.selectedId));
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
    renderMap();
    document.getElementById("language-toggle").addEventListener("click", () => setLanguage(state.lang === "ru" ? "en" : "ru"));
    setLanguage(state.lang);

    document.querySelectorAll(".filter-button").forEach(button => button.addEventListener("click", () => {
      state.filter = button.dataset.filter;
      state.selectedId = null;
      document.querySelectorAll(".filter-button").forEach(item => item.classList.toggle("is-active", item === button));
      renderMap();
    }));
    new ResizeObserver(() => renderMap()).observe(svg);
  } catch (error) {
    inspector.innerHTML = `<div class="inspector-empty"><span class="empty-index">!</span><h2>${t("Data failed to load")}</h2><p>${t("Open the site through a local server or GitHub Pages.")} ${escapeHtml(error.message)}</p></div>`;
  }
}

init();
