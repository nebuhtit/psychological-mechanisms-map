#!/usr/bin/env python3
"""Build or update the committed Russian presentation-layer translation bundle."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from claim_explanations import load_annotations


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "site" / "data" / "pmm-data.json"
OUTPUT_PATH = ROOT / "site" / "data" / "i18n-ru.json"

# Curated terminology takes precedence over generic machine translation.
OVERRIDES = {
    "Fear extinction": "Угасание страха",
    "HPA feedback": "Обратная связь ГГН-оси",
    "Multi-task working-memory battery": "Батарея заданий на рабочую память",
    "N-back performance measurement": "Результат выполнения N-back",
    "N-back task context": "Контекст задачи N-back",
    "Operation-span performance measurement": "Результат выполнения теста operation span",
    "Episodic retrieval supporting N-back performance": "Эпизодическое извлечение, поддерживающее выполнение N-back",
    "Appraisal of cardiorespiratory sensation": "Когнитивная оценка кардиореспираторных ощущений",
    "RDoC Potential Threat (Anxiety) concerns responses when harm may occur but is distant, ambiguous, or uncertain in probability.": "Конструкт RDoC «Потенциальная угроза (тревога)» описывает реакции на возможный вред, который отдалён во времени, неоднозначен или имеет неопределённую вероятность.",
    "Verbal N-back performance showed weak convergence with operation-span performance in Kane et al. 2007.": "В исследовании Kane et al. (2007) результаты вербального N-back были лишь слабо связаны с результатами теста operation span.",
    "Working-memory capacity": "Ёмкость рабочей памяти",
    "Working-memory control": "Контроль рабочей памяти",
    # Spatial-attention pilot: machine translation confuses cues, evidence,
    # latency, and decision bias, so every public scientific term is curated.
    "Spatial attention": "Пространственное внимание",
    "Spatial selective attention": "Пространственное избирательное внимание",
    "Predictive visuospatial cueing task": "Задание с предсказывающей пространственной подсказкой",
    "Spatial cue-validity manipulation": "Изменение соответствия пространственной подсказки цели",
    "Visual target response": "Ответ на зрительную цель",
    "Visual target response latency": "Время ответа на зрительную цель",
    "Visual target discrimination accuracy": "Точность различения зрительной цели",
    "Cueing-task response-latency measurement": "Измерение времени ответа в задании с подсказкой",
    "Cueing-task accuracy and signal-detection measurement": "Измерение точности и параметров обнаружения сигнала",
    "Sensory evidence enhancement at an attended location": "Усиление сенсорной информации в области внимания",
    "Spatial weighting of evidence for decision": "Изменение веса сенсорной информации при принятии решения",
    "Attention construct, visuospatial cueing task, response latency, accuracy, sensory enhancement, and decision weighting kept distinct.": "Конструкт внимания, задание с пространственной подсказкой, время ответа, точность, сенсорное усиление и изменение веса информации при принятии решения представлены раздельно.",
    "Selective prioritization of information from one or more spatial locations relative to competing locations.": "Избирательное предоставление приоритета информации из одного или нескольких участков пространства по сравнению с конкурирующими участками.",
    "Experimental task in which a spatial cue precedes a visual target and target location is more or less consistent with the cued location.": "Экспериментальное задание, в котором пространственная подсказка появляется перед зрительной целью, а положение цели соответствует или не соответствует подсказанному месту.",
    "Experimental variation of whether a cue correctly or incorrectly indicates the later target location or interval.": "Экспериментальное изменение того, правильно или неправильно подсказка указывает последующее место или интервал появления цели.",
    "Observable button press or equivalent response indicating target detection, discrimination, localization, or absence.": "Наблюдаемый ответ, например нажатие кнопки, обозначающий обнаружение, различение, определение положения или отсутствие цели.",
    "Time between target onset and a protocol-valid visual target response.": "Время от появления цели до предусмотренного протоколом ответа на неё.",
    "Probability or proportion of correct target detection, discrimination, or localization responses under a declared condition.": "Вероятность или доля правильных ответов при обнаружении, различении или определении положения цели в заданном условии.",
    "Trial-level response time and prespecified valid-minus-invalid or invalid-minus-valid latency contrast.": "Время ответа в каждой пробе и заранее заданная разность времени между условиями с правильной и неправильной подсказкой.",
    "Condition-specific accuracy plus model-based sensitivity and choice-bias estimates when the task design supports their separation.": "Точность в каждом условии, а также модельные оценки чувствительности и смещения выбора, если устройство задания позволяет разделить эти показатели.",
    "Proposed process in which allocating attention increases the quality or discriminability of sensory evidence at the attended location.": "Предполагаемый процесс, при котором направление внимания повышает качество или различимость сенсорной информации в выбранном участке пространства.",
    "Proposed process in which cue information changes the relative decision weight or criterion assigned to evidence from different locations or intervals.": "Предполагаемый процесс, при котором подсказка меняет относительный вес или критерий для сенсорной информации из разных мест или временных интервалов при выборе ответа.",
    "Attention is not identical to visual perception, target detection, response speed, or a score from one cueing task.": "Внимание не тождественно зрительному восприятию, обнаружению цели, скорости ответа или результату одного задания с подсказкой.",
    "The task operationalizes attention under a protocol; it is not the attention construct itself.": "Задание операционализирует внимание в конкретном протоколе, но не является самим конструктом внимания.",
    "A latency contrast is not a direct observation of a unique attention mechanism.": "Разность времени ответа между условиями не является прямым наблюдением единственного механизма внимания.",
    "Raw accuracy alone does not distinguish sensitivity from response bias.": "Одна только доля правильных ответов не отделяет чувствительность восприятия от смещения ответа.",
    "Sensitivity estimates are model-dependent and do not by themselves localize a neural mechanism.": "Оценки чувствительности зависят от модели и сами по себе не указывают на конкретный нейронный механизм.",
    "Decision weighting does not imply that sensory encoding is unchanged in every task.": "Изменение веса информации при принятии решения не означает, что сенсорное кодирование неизменно во всех заданиях.",
    "Decision weighting can coexist with sensory enhancement and should not be represented as its universal replacement.": "Изменение веса информации при принятии решения может сочетаться с сенсорным усилением и не должно считаться его универсальной заменой.",
    "Spatial attention is narrower than the broad RDoC Attention construct.": "Пространственное внимание является более узким понятием, чем общий конструкт Attention в RDoC.",
    "Spatial attention may improve performance in some cueing tasks by increasing perceptual sensitivity at the attended location.": "В некоторых заданиях с пространственной подсказкой внимание может улучшать результат за счёт повышения перцептивной чувствительности в указанном месте.",
    "The PMM spatial construct is narrower than broad RDoC Attention and the RDoC matrix is designed to evolve.": "Пространственный конструкт PMM уже общего конструкта Attention в RDoC; сама матрица RDoC рассчитана на дальнейшее изменение.",
    "RDoC Attention covers processes that regulate access to capacity-limited systems including awareness, higher perception, and motor action.": "Конструкт Attention в RDoC охватывает процессы, регулирующие доступ к системам с ограниченной пропускной способностью, включая осознание, сложное восприятие и двигательное действие.",
    "This is the current official RDoC construct definition, used as an external alignment rather than a complete PMM mechanism theory.": "Это действующее официальное определение конструкта RDoC. В PMM оно используется для внешнего сопоставления, а не как полная теория механизма.",
    "Research framework spanning normal-to-abnormal human functioning.": "Исследовательская рамка, охватывающая непрерывный диапазон функционирования человека от нормы до нарушений.",
    "52 paid human participants across five experiments reported by Posner, Snyder, and Davidson in 1980.": "52 участника, получавших оплату, в пяти экспериментах Posner, Snyder и Davidson (1980).",
    "13 human participants in the Johnson et al. 2020 experiment.": "13 участников в эксперименте Johnson et al. (2020).",
    "Humans performing predictive endogenous cueing tasks with multiple locations or intervals.": "Люди, выполняющие задания с эндогенными предсказывающими подсказками для нескольких мест или временных интервалов.",
    "Humans performing predictive endogenous visuospatial cueing tasks that identify sensitivity separately from choice bias.": "Люди, выполняющие зрительно-пространственные задания с эндогенными предсказывающими подсказками, в которых чувствительность оценивается отдельно от смещения выбора.",
    "Across the tested visual-signal experiments, cues indicating the likely target location reduced detection latency relative to unexpected target locations.": "В проведённых экспериментах подсказки о вероятном месте цели сокращали время её обнаружения по сравнению с появлением цели в неожиданном месте.",
    "Controlled cue-location comparisons produced faster target detection at expected locations across the reported experiments.": "В контролируемых сравнениях участники быстрее обнаруживали цель в ожидаемом месте, чем в неожиданном.",
    "Five controlled experiments showed cue-related latency benefits, but historical reporting and task-specific designs limit quantitative generalization.": "Пять контролируемых экспериментов показали преимущество по времени ответа после правильной подсказки, но старый формат отчётности и специфика заданий ограничивают количественное обобщение.",
    "The effect does not uniquely identify sensory enhancement": "Этот эффект не позволяет однозначно установить сенсорное усиление",
    "Restricted to the reported luminance and form detection tasks": "Ограничено описанными заданиями на обнаружение яркости и формы",
    "and response procedures.": "и использованными процедурами ответа.",
    "In a detection-like coarse-orientation task, valid endogenous cues improved accuracy in both simultaneous and long-SOA sequential conditions relative to invalid cues.": "В задании на грубое различение ориентации правильные эндогенные подсказки повышали точность по сравнению с неправильными как при одновременном предъявлении, так и при последовательном предъявлении с большим интервалом.",
    "Valid cues improved accuracy by similar amounts in simultaneous and sequential conditions in the tested task.": "В этом задании правильные подсказки повышали точность примерно одинаково при одновременном и последовательном предъявлении.",
    "Controlled within-participant cue-validity comparisons yielded reliable effects, but the analyzed sample was 13 and the task was deliberately narrow.": "Контролируемое сравнение правильных и неправильных подсказок у тех же участников выявило устойчивый эффект, но выборка включала только 13 человек, а задание было намеренно узким.",
    "A cueing effect on accuracy alone does not identify whether perception or decision changed.": "Само по себе влияние подсказки на точность не показывает, изменилось восприятие, принятие решения или оба процесса.",
    "and the reported simultaneous-sequential protocol.": "и описанным протоколом одновременного и последовательного предъявления.",
    "coarse orientation discrimination": "грубое различение ориентации",
    "Model-estimated perceptual sensitivity was higher at the cued location in the multialternative task.": "В многоальтернативном задании модельная оценка перцептивной чувствительности была выше в месте, указанном подсказкой.",
    "Choice-bias estimates varied with predictive cue validity independently of sensitivity estimates.": "Оценки смещения выбора менялись в зависимости от предсказывающей подсказки независимо от оценок чувствительности.",
    "Model-based separation depends on task design and model assumptions.": "Разделение показателей с помощью модели зависит от устройства задания и допущений модели.",
    "Requires a design and model that can distinguish sensitivity from criterion or choice bias; effects may depend on stimulus and task complexity.": "Требуются задание и модель, способные отделить чувствительность от критерия или смещения выбора; результат может зависеть от сложности стимулов и задания.",
    "Requires predictive cue information and a task permitting distinct evidence sources or response alternatives.": "Требуется предсказывающая подсказка и задание, в котором можно различить источники сенсорной информации или варианты ответа.",
    "A valid-cue performance benefit alone does not establish sensory enhancement.": "Само по себе улучшение результата после правильной подсказки не доказывает сенсорное усиление.",
    "Model-based signal-detection results support sensitivity enhancement in a multialternative task, while a different detection-like task challenged sensory enhancement as a universal account.": "Модельный анализ по теории обнаружения сигнала поддерживает усиление чувствительности в многоальтернативном задании, но другое задание показало, что сенсорное усиление не является универсальным объяснением эффекта подсказки.",
    "A reliable sequential cueing effect challenged sensory enhancement as the universal explanation for partially valid cueing.": "Устойчивый эффект подсказки при последовательном предъявлении поставил под сомнение сенсорное усиление как универсальное объяснение эффекта частично надёжной подсказки.",
    "Predictive spatial cues may improve performance partly by changing how evidence from cued locations or intervals is weighted during decision-making.": "Предсказывающие пространственные подсказки могут улучшать результат отчасти потому, что меняют вес сенсорной информации из указанных мест или интервалов при принятии решения.",
    "Two controlled studies used different designs to separate decision-related effects from sensory sensitivity, but both remain task- and model-dependent.": "В двух контролируемых исследованиях применялись разные способы отделить эффекты принятия решения от сенсорной чувствительности, однако оба результата зависят от задания и модели.",
    "The simultaneous-sequential dissociation supported a selective-decision account for the tested detection-like task.": "Различие между одновременным и последовательным предъявлением поддержало объяснение через избирательное принятие решения в исследованном задании.",
    "Clear displays": "Хорошо различимые стимулы",
    "Attention and the detection of signals": "Внимание и обнаружение сигналов",
    "Definitions of the RDoC Domains and Constructs — Attention": "Определения доменов и конструктов RDoC: Attention",
    "Endogenous cueing effects for detection can be accounted for by a decision model of selective attention": "Эффекты эндогенной подсказки при обнаружении можно объяснить моделью принятия решений избирательного внимания",
    "Sensory and decisional components of endogenous attention are dissociable": "Сенсорный компонент и компонент принятия решения при эндогенном внимании можно разделить",
    # Declarative-memory pilot: preserve the distinction between stored semantic
    # knowledge and semantic processing used as an experimental encoding operation.
    "Declarative memory": "Декларативная память",
    "Episodic memory": "Эпизодическая память",
    "Semantic memory": "Семантическая память",
    "Incidental word-encoding and recognition task": "Задание на непреднамеренное кодирование и узнавание слов",
    "Developmental-amnesia neuropsychological assessment": "Нейропсихологическое обследование при амнезии развития",
    "Encoding-question depth manipulation": "Изменение глубины обработки при кодировании",
    "Old-new recognition response": "Ответ «старое — новое» при узнавании",
    "Later word-recognition accuracy": "Точность последующего узнавания слов",
    "Old-new recognition-memory measurement": "Измерение узнавания по ответам «старое — новое»",
    "Episodic-semantic neuropsychological profile": "Нейропсихологический профиль эпизодической и семантической памяти",
    "Elaborative semantic encoding": "Семантическая проработка при кодировании",
    "Declarative, episodic, and semantic constructs, encoding manipulation, recognition measurement, dissociation evidence, and elaborative encoding kept distinct.": "Декларативная, эпизодическая и семантическая память, экспериментальное изменение кодирования, измерение узнавания, данные о диссоциации и семантическая проработка представлены раздельно.",
    "Acquisition, storage, consolidation, and retrieval of representations of facts and events that can support flexible use of relational information.": "Кодирование, хранение, консолидация и извлечение представлений о фактах и событиях, позволяющих гибко использовать связи между элементами.",
    "Memory for events together with spatial, temporal, or other contextual relations that locate what happened within a particular episode.": "Память о событиях вместе с пространственными, временными и другими контекстными связями, указывающими, что произошло в конкретном эпизоде.",
    "Organized knowledge of concepts, word meanings, and facts that is not tied to remembering one specific learning episode.": "Организованные знания о понятиях, значениях слов и фактах, не привязанные к воспоминанию одного конкретного эпизода обучения.",
    "Laboratory task in which participants answer questions about words without initially expecting a later old-new memory test.": "Лабораторное задание, в котором участники отвечают на вопросы о словах, первоначально не ожидая последующей проверки узнавания «старое — новое».",
    "Clinical assessment context comparing episodic remembering and acquired factual knowledge after early bilateral hippocampal pathology.": "Контекст клинического обследования, сопоставляющего память о событиях и приобретённые фактические знания после ранней двусторонней патологии гиппокампа.",
    "Experimental assignment of structural, phonemic, or meaning-based questions about each study word before a later memory test.": "Экспериментальное предъявление вопросов о внешнем виде, звучании или значении каждого изучаемого слова перед последующей проверкой памяти.",
    "Observable response indicating whether a test item was encountered during the earlier study phase.": "Наблюдаемый ответ о том, встречался ли проверяемый элемент на предыдущем этапе изучения.",
    "Correct discrimination of previously studied words from unstudied words on the later recognition test.": "Правильное различение ранее изученных и новых слов при последующей проверке узнавания.",
    "Condition-specific hits, misses, false alarms, correct rejections, or a derived discrimination measure from an old-new test.": "Число правильных узнаваний, пропусков, ложных тревог и правильных отклонений в каждом условии либо рассчитанный по ним показатель различения.",
    "A battery comparing memory for personally experienced events with language, literacy, and factual-knowledge attainment.": "Батарея методик, сопоставляющая память о лично пережитых событиях с развитием речи, грамотности и фактических знаний.",
    "Proposed process in which a new item is analyzed for meaning and related to contextual or existing knowledge, producing a more discriminable later memory representation.": "Предполагаемый процесс, при котором новый элемент анализируется по смыслу и связывается с контекстом или имеющимися знаниями, формируя более различимое представление для последующей памяти.",
    "RDoC Declarative Memory covers encoding, storage, consolidation, and retrieval of representations of facts and events.": "Конструкт Declarative Memory в RDoC охватывает кодирование, хранение, консолидацию и извлечение представлений о фактах и событиях.",
    "In the reported incidental-learning experiments, meaning-based encoding questions increased later word recognition relative to structural or phonemic questions.": "В описанных экспериментах вопросы о значении слов улучшали их последующее узнавание по сравнению с вопросами о внешнем виде или звучании.",
    "In three reported developmental-amnesia cases with early hippocampal pathology, severe episodic-memory impairment coexisted with substantially better semantic knowledge and academic attainment.": "В трёх описанных случаях амнезии развития при ранней патологии гиппокампа тяжёлое нарушение эпизодической памяти сочеталось со значительно лучше сохранёнными фактическими знаниями и учебными навыками.",
    "Meaning-based encoding may improve later episodic recognition by producing a more elaborated and distinctive representation of the studied item.": "Смысловая обработка при кодировании может улучшать последующее эпизодическое узнавание, создавая более проработанное и различимое представление изученного элемента.",
    "Controlled meaning-based encoding conditions produced better later word memory than shallower structural or sound-based conditions.": "При контролируемой смысловой обработке последующая память на слова была лучше, чем после более поверхностной обработки внешнего вида или звучания.",
    "Three developmental-amnesia cases showed much greater impairment of episodic remembering than of acquired semantic knowledge.": "В трёх случаях амнезии развития память о событиях была нарушена значительно сильнее, чем приобретённые фактические знания.",
    "Follow-up experiments supported qualitative meaning-based encoding over a simple longer-processing-time explanation.": "Дополнительные эксперименты поддержали объяснение через качественную смысловую обработку, а не просто через более длительное время обработки.",
    "Declarative Memory — NIMH RDoC": "Декларативная память в NIMH RDoC",
    "Cognitive Atlas concept — episodic memory": "Понятие Cognitive Atlas: эпизодическая память",
    "Cognitive Atlas concept — semantic memory": "Понятие Cognitive Atlas: семантическая память",
    "Depth of processing and the retention of words in episodic memory": "Глубина обработки и сохранение слов в эпизодической памяти",
    "Differential effects of early hippocampal pathology on episodic and semantic memory": "Различное влияние ранней патологии гиппокампа на эпизодическую и семантическую память",
    "A small lesion case series can demonstrate a dissociation pattern but cannot estimate a population-average causal effect.": "Небольшая серия случаев с поражением мозга может показать диссоциацию функций, но не позволяет оценить средний причинный эффект для популяции.",
    "Clinical case series with early pathology and extensive neuropsychological characterization.": "Серия клинических случаев с ранней патологией и подробным нейропсихологическим обследованием.",
    "Controlled encoding effects are consistent with elaboration and distinctiveness, but the experiments did not isolate one unique latent process.": "Контролируемые эффекты способа кодирования согласуются с проработкой и различимостью следа, но эксперименты не выделили единственный скрытый процесс.",
    "Declarative memory is broader than episodic memory and semantic memory considered separately.": "Декларативная память является более широким понятием, чем отдельно рассматриваемые эпизодическая и семантическая память.",
    "Episodic memory is not equivalent to all long-term memory or to recognition performance alone.": "Эпизодическая память не тождественна всей долговременной памяти или одному результату задания на узнавание.",
    "Humans performing incidental word-encoding tasks followed by recognition.": "Люди, выполняющие задания на непреднамеренное кодирование слов с последующей проверкой узнавания.",
    "RDoC is an evolving research framework and does not make every memory task or neural signal equivalent to the construct.": "RDoC является развивающейся исследовательской системой; отдельное задание памяти или нейронный сигнал не становятся эквивалентом конструкта.",
    "Recognition accuracy reflects both memory discrimination and response policy unless the design and analysis separate them.": "Точность узнавания зависит и от различения старых и новых элементов, и от склонности выбирать определённый ответ, если устройство задания и анализ не разделяют эти компоненты.",
    "Relative preservation does not mean completely normal semantic memory, and test batteries do not make the constructs process-identical.": "Относительная сохранность не означает полностью нормальную семантическую память, а использование одной батареи тестов не делает конструкты тождественными процессами.",
    "Semantic memory as stored knowledge is not the same object as semantic processing performed during an encoding task.": "Семантическая память как накопленное знание не является тем же объектом, что смысловая обработка во время задания на кодирование.",
    "Semantic processing, semantic memory, elaboration, distinctiveness, and retrieval match must not be collapsed into one construct.": "Смысловую обработку, семантическую память, проработку, различимость и соответствие условий кодирования и извлечения нельзя объединять в один конструкт.",
    "Superior memory after semantic questions does not uniquely identify elaboration, distinctiveness, congruity, or one neural implementation.": "Более высокая результативность после вопросов о значении не позволяет однозначно выбрать между проработкой, различимостью, смысловым соответствием и конкретной нейронной реализацией.",
    "Ten controlled experiments supported a robust within-protocol encoding effect, while historical reporting and task specificity limit quantitative generalization.": "Десять контролируемых экспериментов показали устойчивое влияние условия кодирования в этих протоколах, но старый формат отчётности и специфика заданий ограничивают количественное обобщение.",
    "The cases show a striking within-person dissociation, but the sample is three, lesion extent is not experimentally assigned, and population generalization is limited.": "Внутри каждого случая наблюдалось выраженное расхождение функций, но выборка состояла из трёх человек, объём поражения не задавался экспериментально, а обобщение на популяцию ограничено.",
    "The construct is not identical to a recognition score or to one neural structure.": "Конструкт не тождественен показателю узнавания или одной нейронной структуре.",
    "The effect establishes an encoding-condition difference but does not uniquely identify one memory mechanism or guarantee transfer to other materials and retrieval tests.": "Эффект подтверждает различие между условиями кодирования, но не выявляет единственный механизм памяти и не гарантирует перенос на другие материалы и способы извлечения.",
    "The result supports separability of measured memory functions but does not prove that the hippocampus is unnecessary for all semantic learning.": "Результат поддерживает разделимость измеренных функций памяти, но не доказывает, что гиппокамп не нужен ни для одного вида семантического научения.",
    "The task must induce meaningful analysis and later test memory for the studied items.": "Задание должно вызывать смысловой анализ, а затем проверять память на изученные элементы.",
    "This is the current official RDoC construct definition, used for alignment rather than as a complete theory of all memory systems.": "Это действующее официальное определение конструкта RDoC, используемое для сопоставления, а не как полная теория всех систем памяти.",
    "This task samples particular encoding and recognition operations; it is not declarative memory itself.": "Задание операционализирует отдельные операции кодирования и узнавания, но не является самой декларативной памятью.",
    "Three individuals with early-onset bilateral hippocampal pathology described by Vargha-Khadem and colleagues in 1997.": "Три человека с ранней двусторонней патологией гиппокампа, описанные Vargha-Khadem и коллегами в 1997 году.",
    "Undergraduate participants in ten experiments reported by Craik and Tulving in 1975.": "Студенты, участвовавшие в десяти экспериментах Craik и Tulving (1975).",
    "Words, incidental orienting questions, later recognition, and the specific structural, phonemic, and semantic comparisons reported in the source.": "Слова, ориентирующие вопросы при непреднамеренном запоминании, последующее узнавание и описанные в источнике сравнения обработки внешнего вида, звучания и значения.",
}
OVERRIDES.update({entry["en"]: entry["ru"] for entry in load_annotations().values()})


def displayed_strings(document: dict) -> set[str]:
    strings: set[str] = set()
    for family in document["families"]:
        strings.update((family["title"], family["description"]))
        for item in family["objects"]:
            strings.update((item["label"], item["definition"]))
            strings.update(item.get("boundary_notes", []))
        for claim in family["claims"]:
            strings.add(claim["statement"])
            strings.add(claim["plain_language_summary"])
            strings.add(claim["confidence"]["rationale"])
            strings.add(claim["scope"]["population"])
            strings.update(claim.get("limitations", []))
            strings.update(claim["scope"].get("boundary_conditions", []))
        for evidence in family["evidence"]:
            strings.add(evidence["summary"])
        for source in family["sources"]:
            strings.add(source["title"])
    return {value for value in strings if value}


def translate(value: str, attempts: int = 4) -> str:
    for attempt in range(attempts):
        try:
            result = subprocess.run(
                [
                    "curl", "-fsSLG", "--max-time", "30",
                    "--data-urlencode", "client=gtx",
                    "--data-urlencode", "sl=en",
                    "--data-urlencode", "tl=ru",
                    "--data-urlencode", "dt=t",
                    "--data-urlencode", f"q={value}",
                    "https://translate.googleapis.com/translate_a/single",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(result.stdout)
            translated = "".join(part[0] for part in payload[0] if part[0])
            if translated:
                return translated
        except Exception:
            if attempt == attempts - 1:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"translation failed: {value[:80]}")


def write_bundle(strings: set[str], translations: dict[str, str], status: str) -> None:
    translations.update({key: value for key, value in OVERRIDES.items() if key in strings})
    translations = {key: value.replace("\u200b", "") for key, value in translations.items()}
    payload = {
        "language": "ru",
        "canonical_language": "en",
        "translation_status": status,
        "translations": {key: translations[key] for key in sorted(strings) if key in translations},
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    document = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    strings = displayed_strings(document)
    existing = {}
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8")).get("translations", {})
    existing.update({key: value for key, value in OVERRIDES.items() if key in strings})
    missing = sorted(strings - existing.keys())
    print(f"catalog: {len(strings)} strings; translating: {len(missing)}")
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(translate, value): value for value in missing}
        for index, future in enumerate(as_completed(futures), start=1):
            source = futures[future]
            existing[source] = future.result()
            if index % 25 == 0 or index == len(missing):
                print(f"translated: {index}/{len(missing)}")
                write_bundle(strings, existing, "generation_in_progress")
    write_bundle(strings, existing, "machine_translated_pending_review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
