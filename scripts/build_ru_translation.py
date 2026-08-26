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
OVERRIDES.update({
    "A cross-system review supports normalization as a widely useful candidate neural computation, not as one uniquely established circuit.": "Обзор разных нейронных систем поддерживает нормализацию как широко применимую кандидатную нейронную операцию, но не как единственную установленную схему нейронной цепи.",
    "A normalization model accounted for a broader set of cat visual-cortex response properties than an unnormalized linear-energy model.": "Модель с нормализацией объяснила больше свойств ответов зрительной коры кошки, чем линейно-энергетическая модель без нормализации.",
    "A specified normalization pool and model must predict contrast-response or threshold data beyond simpler alternatives.": "Нужно заранее указать пул нормализации и модель, а затем показать, что они предсказывают ответы на контраст или пороги лучше более простых альтернатив.",
    "A threshold is conditional on the task, psychometric criterion, stimulus, observer, and viewing conditions.": "Порог зависит от задания, психометрического критерия, стимула, наблюдателя и условий просмотра.",
    "A visual stimulus, a detection response, a psychophysical score, and a neural model are not the visual-perception construct itself.": "Зрительный стимул, ответ об обнаружении, психофизический показатель и нейронная модель не являются самим конструктом зрительного восприятия.",
    "Application of Fourier analysis to the visibility of gratings": "Применение анализа Фурье к видимости решёток",
    "Candidate neural computation in which a neuron's stimulus-driven response is divided by a factor that includes pooled activity from other neurons, regulating response gain and saturation.": "Предполагаемая нейронная операция, при которой вызванный стимулом ответ нейрона делится на величину, учитывающую суммарную активность других нейронов; это регулирует усиление и насыщение ответа.",
    "Capacity to detect luminance variation in a visual pattern as a function of the pattern's spatial frequency under specified viewing conditions.": "Способность обнаруживать изменения яркости в зрительном изображении в зависимости от его пространственной частоты при заданных условиях просмотра.",
    "Cognitive Atlas concept — visual perception": "Понятие Cognitive Atlas: зрительное восприятие",
    "Cognitive Atlas task — contrast detection task": "Задание Cognitive Atlas: обнаружение контраста",
    "Contrast definition, threshold criterion, spatial frequency, stimulus, and viewing conditions must be stated.": "Необходимо указать способ расчёта контраста, критерий порога, пространственную частоту, стимул и условия просмотра.",
    "Contrast detection threshold": "Порог обнаружения контраста",
    "Contrast sensitivity function": "Функция контрастной чувствительности",
    "Controlled changes to spatial frequency and waveform changed the contrast required for human observers to detect gratings.": "Контролируемое изменение пространственной частоты и формы сигнала меняло контраст, необходимый людям для обнаружения решётки.",
    "Detection threshold depends on the stimulus, display, adaptation, task rule, and response criterion.": "Порог обнаружения зависит от стимула, экрана, адаптации, правил задания и критерия ответа.",
    "Different stimuli, threshold procedures, response alternatives, and viewing conditions can yield different profiles.": "Разные стимулы, способы определения порога, варианты ответа и условия просмотра могут давать разные профили.",
    "Divisive normalization is a computational description with multiple possible biological implementations.": "Дивизивная нормализация является вычислительным описанием, которое может иметь несколько биологических реализаций.",
    "Divisive normalization may shape visual response gain and thereby contribute to contrast-dependent neural and behavioral sensitivity.": "Дивизивная нормализация может регулировать усиление зрительного ответа и тем самым вносить вклад в зависимость нейронной и поведенческой чувствительности от контраста.",
    "Divisive visual normalization": "Дивизивная нормализация зрительных ответов",
    "Evidence that the model explains cat visual-cortex responses does not by itself establish that it causes human contrast thresholds.": "То, что модель объясняет ответы зрительной коры кошки, само по себе не доказывает, что она причинно определяет контрастные пороги человека.",
    "Experimental variation of the spacing and luminance contrast of a periodic visual pattern across trials or conditions.": "Экспериментальное изменение частоты чередования и яркостного контраста периодического зрительного изображения между пробами или условиями.",
    "Grating detection response": "Ответ об обнаружении решётки",
    "Grating spatial-frequency and contrast manipulation": "Изменение пространственной частоты и контраста решётки",
    "Human observers tested in the Campbell and Robson 1968 grating experiments.": "Люди, участвовавшие в экспериментах Campbell и Robson 1968 года с решётками.",
    "In contrast psychophysics, sensitivity is the reciprocal of the contrast threshold, and a contrast sensitivity function records that quantity across spatial frequencies.": "В психофизике контраста чувствительность равна величине, обратной контрастному порогу, а функция контрастной чувствительности показывает эту величину для разных пространственных частот.",
    "In the Campbell and Robson experiments, controlled changes in grating spatial frequency and waveform produced systematic differences in contrast-detection thresholds.": "В экспериментах Campbell и Robson контролируемое изменение пространственной частоты и формы решётки приводило к закономерным различиям порогов обнаружения контраста.",
    "Lowest protocol-defined target contrast that supports a prespecified level of reliable detection at a given spatial frequency.": "Минимальный контраст цели, при котором по правилам протокола достигается заранее заданная надёжность обнаружения на конкретной пространственной частоте.",
    "Measuring contrast sensitivity": "Измерение контрастной чувствительности",
    "Model fit is not proof of a unique causal circuit, and nonhuman cortical physiology is indirect evidence for human contrast-detection behavior.": "Соответствие модели данным не доказывает существование единственной причинной нейронной цепи, а физиология коры животных является лишь косвенным свидетельством для поведения человека при обнаружении контраста.",
    "Normalization as a canonical neural computation": "Нормализация как каноническая нейронная операция",
    "Normalization of cell responses in cat striate cortex": "Нормализация ответов клеток стриарной коры кошки",
    "Observable report indicating whether or where the protocol-defined grating was detected.": "Наблюдаемый ответ о том, была ли и где именно обнаружена заданная протоколом решётка.",
    "Observers completing protocol-defined contrast detection or identification tasks.": "Наблюдатели, выполняющие заданные протоколом задания на обнаружение или распознавание контраста.",
    "Perception — NIMH RDoC": "Восприятие в NIMH RDoC",
    "Periodic gratings, the reported spatial-frequency range, waveform comparisons, adaptation, luminance, viewing geometry, and threshold procedure.": "Периодические решётки, описанный диапазон пространственных частот, сравнение форм сигнала, адаптация, яркость, геометрия просмотра и способ определения порога.",
    "Processes that compute over visual sensory data to construct and transform representations of the external environment and use them to acquire information, predict, and guide action.": "Процессы, которые обрабатывают зрительные сенсорные данные, создают и преобразуют представления о внешней среде и используют их для получения информации, прогнозирования и управления действием.",
    "Psychophysical measurement that expresses sensitivity, the reciprocal of contrast threshold, across spatial frequencies.": "Психофизическое измерение чувствительности, равной величине, обратной контрастному порогу, для разных пространственных частот.",
    "Psychophysical task in which an observer reports the presence or location of a luminance grating while contrast and spatial frequency are controlled.": "Психофизическое задание, в котором наблюдатель сообщает о наличии или расположении яркостной решётки при контролируемых контрасте и пространственной частоте.",
    "RDoC defines Perception as processes that compute over sensory data to construct and transform representations of the external environment, acquire information, make predictions, and guide action.": "RDoC определяет восприятие как процессы обработки сенсорных данных, которые создают и преобразуют представления о внешней среде, получают информацию, формируют прогнозы и направляют действие.",
    "Reciprocal threshold is an operational measurement and does not identify a unique sensory or neural mechanism.": "Величина, обратная порогу, является операциональным измерением и не выявляет единственный сенсорный или нейронный механизм.",
    "Sine-wave grating detection task": "Задание на обнаружение синусоидальной решётки",
    "Spatial contrast sensitivity": "Пространственная контрастная чувствительность",
    "Spatial contrast sensitivity is one restricted aspect of visual functioning, not a complete model of visual perception.": "Пространственная контрастная чувствительность отражает лишь один узкий аспект зрительной функции, а не полную модель зрительного восприятия.",
    "The capacity is operationalized by threshold measurements; it is not identical to one observed threshold or fitted curve.": "Эта способность операционализируется через измерение порогов, но не тождественна одному наблюдаемому порогу или аппроксимированной кривой.",
    "The contrast sensitivity function is a measurement profile, not visual perception as a whole.": "Функция контрастной чувствительности является профилем измерения, а не зрительным восприятием в целом.",
    "The experiment identifies effects of stimulus properties on task thresholds, not a unique neural channel, normalization process, or complete account of visual perception.": "Эксперимент выявляет влияние свойств стимула на пороги в задании, но не устанавливает единственный нейронный канал, процесс нормализации или полное объяснение зрительного восприятия.",
    "The measurement definition is explicit in a peer-reviewed methods review and is standard for grating contrast psychophysics.": "Определение измерения явно дано в рецензируемом методическом обзоре и является стандартным для психофизики контраста решёток.",
    "The model explains a broad set of visual-cortex response properties and is supported by physiological literature, but the cited evidence does not uniquely identify its biological implementation or directly establish the human psychophysical pathway.": "Модель объясняет широкий набор свойств ответов зрительной коры и поддерживается физиологическими исследованиями, но приведённые данные не выявляют единственную биологическую реализацию и напрямую не устанавливают психофизический путь у человека.",
    "The source reports repeated controlled psychophysical comparisons across frequencies and waveforms, but it is a historical study with limited modern reporting and protocol-specific generalizability.": "Источник описывает повторные контролируемые психофизические сравнения разных частот и форм сигнала, но это историческое исследование с ограниченной по современным стандартам отчётностью и узкой обобщаемостью протокола.",
    "The visual-perception matrix lists many paradigms and units of analysis; no single paradigm or signal is equivalent to the construct.": "Матрица зрительного восприятия включает множество парадигм и уровней анализа; ни одна отдельная парадигма или сигнал не эквивалентны конструкту.",
    "This is the current official RDoC parent-construct definition; it is used for terminology alignment rather than as a complete theory of vision.": "Это действующее официальное определение родительского конструкта RDoC; оно используется для согласования терминов, а не как полная теория зрения.",
    "This task operationalizes a narrow detection problem; it is not visual perception itself.": "Это задание операционализирует узкую задачу обнаружения, но не является самим зрительным восприятием.",
    "Visual Perception — NIMH RDoC": "Зрительное восприятие в NIMH RDoC",
    "Visual perception": "Зрительное восприятие",
    "Visual perception is broader than detecting one grating or estimating one contrast threshold.": "Зрительное восприятие шире, чем обнаружение одной решётки или оценка одного контрастного порога.",
    "Visual perception, contrast sensitivity, grating manipulation, detection response, threshold measurement, and divisive normalization kept distinct.": "Зрительное восприятие, контрастная чувствительность, изменение решётки, ответ об обнаружении, измерение порога и дивизивная нормализация представлены раздельно.",
    "Visual systems studied with contrast-varying stimuli, including cat visual cortex and human psychophysics.": "Зрительные системы, исследованные с помощью стимулов разного контраста, включая зрительную кору кошки и психофизику человека.",
})

OVERRIDES.update({
    "A diffusion model account of the lexical decision task": "Объяснение задания лексического решения с помощью диффузионной модели",
    "A diffusion model provided a joint quantitative account of lexical-decision choices and response-time distributions across several manipulations.": "Диффузионная модель совместно описала выбор ответов и распределения времени реакции в нескольких вариантах задания лексического решения.",
    "A faster response is not a direct observation of comprehension, lexical access, or spreading activation.": "Более быстрый ответ не является прямым наблюдением понимания, лексического доступа или распространения активации.",
    "A lexical-decision response can also depend on orthography, semantics, decision criteria, motor execution, and task strategy.": "Ответ в задании лексического решения может также зависеть от написания, значения, критерия решения, моторного выполнения и стратегии.",
    "A semantic-priming effect does not uniquely identify spreading activation, a localist network, or an automatic process.": "Эффект семантического прайминга не позволяет однозначно установить распространение активации, локальную сетевую модель или автоматический процесс.",
    "Access to stored lexical information sufficient to distinguish a familiar written word form from a nonword and make task-relevant information available.": "Доступ к хранящейся информации о словах, достаточный для различения знакомого письменного слова и неслова и использования нужной для задания информации.",
    "Accuracy and response-latency distributions summarized separately for prime relation, timing, visibility, target lexical status, and other prespecified conditions.": "Точность и распределения времени ответа, рассчитанные отдельно для смысловой связи, времени и видимости прайма, статуса цели как слова или неслова и других заранее заданных условий.",
    "Adequate fit does not prove that the fitted decomposition is the only psychologically valid account.": "Хорошее соответствие модели данным не доказывает, что это единственное психологически верное разложение процесса.",
    "Automatic semantic preactivation": "Автоматическая семантическая предактивация",
    "Automatic spreading activation, distributed feature overlap, and other early processes are not distinguished by the observed latency contrast alone.": "По одной разнице времени ответа нельзя различить автоматическое распространение активации, перекрытие распределённых признаков и другие ранние процессы.",
    "Broad comprehension, visual lexical access, semantic priming, word decisions, latency, model parameters, and competing automatic and strategic processes kept distinct.": "Широкое понимание языка, зрительный лексический доступ, семантический прайминг, решения о словах, время ответа, параметры модели и конкурирующие автоматические и стратегические процессы представлены раздельно.",
    "Capacity to derive communicative meaning from linguistic or other conventional symbolic signals, including spoken, written, or signed forms.": "Способность извлекать смысл сообщения из языковых или других условных символических сигналов, включая устную, письменную и жестовую формы.",
    "Cognitive Atlas concept — language comprehension": "Понятие Cognitive Atlas: понимание языка",
    "Cognitive Atlas concept — lexical access": "Понятие Cognitive Atlas: лексический доступ",
    "Cognitive Atlas task — lexical decision task": "Задание Cognitive Atlas: лексическое решение",
    "Comprehension is not identical to language production, a lexical-decision response, or response time.": "Понимание не тождественно порождению речи, ответу в задании лексического решения или времени ответа.",
    "Condition-specific lexical-decision performance": "Показатели лексического решения по условиям",
    "Drift rate and nondecision time are model-dependent parameters, not direct observations of lexical access or unique biological mechanisms.": "Скорость накопления информации и время вне решения — зависящие от модели параметры, а не прямые наблюдения лексического доступа или конкретных биологических механизмов.",
    "Elapsed time from protocol-defined target onset to the participant's word or nonword response, usually analyzed for correct trials.": "Время от заданного протоколом появления цели до ответа участника «слово» или «не слово», обычно анализируемое для правильных ответов.",
    "Expectancy before target identification and retrospective matching after lexical access are related but distinguishable candidate processes grouped here only for this pilot comparison.": "Ожидание до распознавания цели и ретроспективное сопоставление после лексического доступа — связанные, но различимые предполагаемые процессы; здесь они объединены только для пилотного сравнения.",
    "Experimental task in which a prime precedes a target letter string and the participant classifies the target as a word or nonword while prime-target relation and timing can be varied.": "Экспериментальное задание, где перед целевой последовательностью букв показывают прайм, после чего участник определяет, является ли цель словом; смысловую связь и временной интервал можно изменять.",
    "Experimental variation of the semantic relation between prime and target and the interval or visibility conditions under which the prime can influence target processing.": "Экспериментальное изменение смысловой связи прайма с целью, а также интервала и видимости, при которых прайм может влиять на обработку цели.",
    "Facilitation in recognizing pairs of words — evidence of a dependence between retrieval operations": "Ускорение распознавания пар слов: свидетельство зависимости между операциями извлечения",
    "Foundational controlled experiments show robust within-protocol priming contrasts, but protocol variants and task-dependent processes constrain generalization.": "Классические контролируемые эксперименты показывают устойчивые различия прайминга внутри протоколов, но различия методик и зависимость от задания ограничивают обобщение.",
    "Grouping expectancy and retrospective matching is provisional; future packs should represent and test them separately.": "Объединение ожидания и ретроспективного сопоставления является предварительным; далее их нужно представлять и проверять отдельно.",
    "Human participants completing lexical-decision experiments varying word frequency, list composition, and nonword type.": "Люди, выполнявшие задания лексического решения с изменением частоты слов, состава списка и типа неслов.",
    "Human participants in the Meyer and Schvaneveldt and Neely laboratory word-classification experiments.": "Участники лабораторных экспериментов Meyer и Schvaneveldt, а также Neely по классификации слов.",
    "Humans completing semantic-priming tasks with brief or short-interval primes.": "Люди, выполняющие задания семантического прайминга с кратко показанными праймами или коротким интервалом.",
    "Humans completing visible-prime semantic-priming tasks, especially at longer prime-target intervals or high relatedness proportions.": "Люди, выполняющие задания семантического прайминга с видимым праймом, особенно при длинных интервалах или высокой доле связанных пар.",
    "Humans receiving conventional linguistic or symbolic communication.": "Люди, воспринимающие общепринятые языковые или символические сообщения.",
    "In Ratcliff, Gomez, and McKoon's lexical-decision experiments, a diffusion model jointly accounted for accuracy and correct and error response-time distributions using separable evidence-accumulation and decision components.": "В экспериментах Ratcliff, Gomez и McKoon диффузионная модель совместно описывала точность и распределения времени правильных и ошибочных ответов, разделяя накопление информации и компоненты решения.",
    "In controlled semantic-priming protocols, changing a preceding prime from unrelated or neutral to semantically related changed target word-classification latency under the tested timing and task conditions.": "В контролируемых протоколах семантического прайминга замена несвязанного или нейтрального прайма на связанный по смыслу изменяла время классификации целевого слова при проверенных временных параметрах и условиях задания.",
    "Language comprehension": "Понимание языка",
    "Language comprehension includes deriving communicative meaning from signals such as speech, written text, or sign, while isolated written-word recognition is only one narrow component.": "Понимание языка включает извлечение смысла из речи, письменного текста или жестового языка, а распознавание отдельного письменного слова является лишь узкой частью этой способности.",
    "Latency interpretation depends on accuracy, exclusions, response deadline, device, and distributional analysis.": "Интерпретация времени ответа зависит от точности, правил исключения проб, ограничения времени, устройства ввода и анализа распределения.",
    "Lexical-decision diffusion profile": "Диффузионный профиль лексического решения",
    "Lexical-decision response latency": "Время ответа в задании лексического решения",
    "Manipulated prime relation changed target response latency and duration influenced the pattern of facilitation and inhibition.": "Изменение связи прайма с целью меняло время ответа, а длительность влияла на соотношение ускорения и замедления.",
    "Mean correct-trial response time can hide speed-accuracy tradeoffs and distributional differences.": "Среднее время правильных ответов может скрывать компромисс между скоростью и точностью и различия в форме распределения.",
    "Meyer and Schvaneveldt used simultaneous word pairs, whereas later semantic-priming protocols often use a sequential prime and target.": "Meyer и Schvaneveldt показывали пары слов одновременно, тогда как в более поздних протоколах прайм и цель обычно предъявляют последовательно.",
    "Model fit is not a causal intervention on evidence accumulation and does not validate the diffusion profile as a unique measure of lexical access.": "Соответствие модели данным не является причинным вмешательством в накопление информации и не подтверждает диффузионный профиль как единственное измерение лексического доступа.",
    "Model-based estimates separating evidence accumulation, response threshold, starting bias, and nondecision time from lexical-decision choices and response-time distributions.": "Модельные оценки, разделяющие накопление информации, порог ответа, начальное смещение и время вне решения по ответам и распределениям времени реакции.",
    "Naming and semantic-categorization tasks can produce different priming patterns because they require different decisions.": "Задания на называние и семантическую категоризацию могут давать другой рисунок прайминга, потому что требуют других решений.",
    "Observable response classifying a target letter string as an existing word or a nonword under the task instructions.": "Наблюдаемый ответ, классифицирующий целевую последовательность букв как существующее слово или неслово по инструкции задания.",
    "Prime visibility, stimulus-onset asynchrony, relatedness proportion, target properties, and task demands are measured or controlled.": "Видимость прайма, интервал между началом стимулов, доля связанных пар, свойства цели и требования задания измеряются или контролируются.",
    "Prime-target relatedness and timing manipulation": "Изменение смысловой связи и времени между праймом и целью",
    "Proposed rapid process by which processing a prime makes related target information more available before the target decision without requiring deliberate prediction.": "Предполагаемый быстрый процесс, при котором обработка прайма делает связанную информацию о цели доступнее до решения без намеренного прогнозирования.",
    "Proposed task-sensitive process in which participants predict likely targets or use the detected prime-target relation to influence a decision after target information becomes available.": "Предполагаемый зависящий от задания процесс, при котором участники ожидают вероятные цели или используют замеченную связь прайма с целью после появления информации о цели.",
    "Rapid automatic preactivation of related target information may contribute to semantic priming, especially when timing and task conditions constrain deliberate strategies.": "Быстрая автоматическая предактивация связанной информации о цели может вносить вклад в семантический прайминг, особенно когда время и задание ограничивают осознанные стратегии.",
    "Semantic priming and retrieval from lexical memory — evidence for facilitatory and inhibitory processes": "Семантический прайминг и извлечение из лексической памяти: данные об ускоряющих и тормозящих процессах",
    "Semantic-priming lexical-decision task": "Задание лексического решения с семантическим праймингом",
    "Semantically related word pairs produced faster correct classifications than unrelated pairs in two foundational experiments.": "В двух классических экспериментах смыслово связанные пары слов классифицировались правильно быстрее, чем несвязанные.",
    "Short-latency and limited-awareness findings are compatible with automatic contribution, but prime identification, task requirements, and alternative distributed or post-lexical processes prevent unique identification.": "Результаты при коротких интервалах и ограниченном осознании согласуются с автоматическим вкладом, но распознавание прайма, требования задания и альтернативные процессы не позволяют установить его однозначно.",
    "Strategic expectancy or post-lexical matching": "Стратегическое ожидание или постлексическое сопоставление",
    "Strategic expectancy or retrospective prime-target matching may contribute to semantic priming when timing, prime visibility, list structure, and the required response make the relation useful.": "Стратегическое ожидание или ретроспективное сопоставление прайма и цели может вносить вклад в прайминг, когда время, видимость, структура списка и требуемый ответ позволяют использовать эту связь.",
    "The causal effect is on response latency in these tasks, not direct proof of one lexical or semantic mechanism.": "Причинный эффект относится ко времени ответа в этих заданиях, а не является прямым доказательством одного лексического или семантического механизма.",
    "The definition does not establish that lexical decision measures broad comprehension or specify a unique mechanism.": "Определение не доказывает, что лексическое решение измеряет широкое понимание языка, и не задаёт единственный механизм.",
    "The influence of prime characteristics in semantic priming": "Влияние характеристик прайма на семантический прайминг",
    "The lexical-decision datasets and diffusion-model specification reported by Ratcliff, Gomez, and McKoon.": "Наборы данных лексического решения и спецификация диффузионной модели, описанные Ratcliff, Gomez и McKoon.",
    "The model explained multiple experimental manipulations and distributional outcomes, but parameter interpretation remains conditional on model specification and comparison.": "Модель объяснила несколько экспериментальных изменений и распределения результатов, но смысл параметров зависит от спецификации и сравнения моделей.",
    "The protocol allows conscious prime processing or makes prime-target relation informative for the required decision.": "Протокол позволяет осознанно обработать прайм или делает связь прайма с целью полезной для требуемого решения.",
    "The reported visual word materials, prime-target relations, timing conditions, instructions, and speeded classification procedures.": "Описанные письменные слова, связи прайма с целью, временные условия, инструкции и процедуры быстрой классификации.",
    "The review concludes that both automatic and strategic processes can contribute and that a priming effect alone does not identify one mechanism.": "Обзор заключает, что вклад могут вносить и автоматические, и стратегические процессы, а один эффект прайминга не выявляет единственный механизм.",
    "The scope follows common usage and the linked Cognitive Atlas entry, but that collaborative record is marked Unreviewed and does not settle a complete language ontology.": "Объём понятия соответствует общему употреблению и записи Cognitive Atlas, но эта совместно редактируемая запись не проверена и не задаёт полную онтологию языка.",
    "The task is not language comprehension itself and does not isolate one stage of word recognition.": "Задание не является самим пониманием языка и не выделяет одну стадию распознавания слова.",
    "This broad construct includes more than recognizing isolated written words; sentence, discourse, pragmatic, and sign-language comprehension are not modeled in this pilot.": "Этот широкий конструкт включает больше, чем распознавание отдельных письменных слов; понимание предложений, дискурса, прагматики и жестового языка в пилоте не моделируется.",
    "This restricted construct concerns written word forms and does not assume that lexical access is one indivisible stage.": "Этот узкий конструкт относится к письменным формам слов и не предполагает, что лексический доступ является одной неделимой стадией.",
    "Timing changed the priming pattern in a way compatible with a slower strategic contribution in addition to rapid facilitation.": "Временные параметры меняли рисунок прайминга так, что наряду с быстрым облегчением возможен более медленный стратегический вклад.",
    "Timing-dependent facilitation and inhibition plus task-sensitive review evidence support strategic contribution, but expectancy and post-lexical matching are not always separately identified.": "Зависящие от времени ускорение и торможение и данные обзора поддерживают стратегический вклад, но ожидание и постлексическое сопоставление не всегда разделены.",
    "Visual lexical access": "Зрительный лексический доступ",
    "Word-nonword classification response": "Ответ о том, является ли цель словом",
    "Experimental task in which two letter strings are presented together and the participant rapidly classifies whether both are words or whether their lexical status is the same.": "Экспериментальное задание, в котором две последовательности букв показывают одновременно, а участник быстро определяет, являются ли обе словами или совпадает ли их лексический статус.",
    "Faster paired classification does not reveal which member was recognized first or identify one retrieval mechanism.": "Более быстрая классификация пары не показывает, какой элемент был распознан первым, и не выявляет единственный механизм извлечения.",
    "Simultaneous paired-word classification task": "Задание на одновременную классификацию пары слов",
    "This historical paired procedure is not interchangeable with a sequential prime-target lexical-decision task.": "Эта историческая процедура с одновременной парой не взаимозаменяема с последовательным заданием, где прайм показывают перед целью.",
})

OVERRIDES.update({entry["en"]: entry["ru"] for entry in load_annotations().values()})

OVERRIDES.update({
    "993 participants represented in 22 syllogistic confidence-rating studies reanalyzed by Trippas and colleagues.": "993 участника из 22 исследований силлогистических суждений с оценкой уверенности, повторно проанализированных Trippas и коллегами.",
    "A hierarchical meta-analysis separated response criterion from validity discrimination and found no unconditional believability effect on discriminability.": "Иерархический метаанализ отделил критерий ответа от способности различать валидность и не выявил общего безусловного влияния правдоподобия на эту способность.",
    "Acceptance rates, rejection rates, accuracy, response time, confidence, or verbal protocols summarized separately by validity and believability condition.": "Доли принятия и отклонения выводов, точность, время ответа, уверенность или словесные отчёты, рассчитанные отдельно для условий разной валидности и правдоподобия.",
    "Accuracy depends on the selected normative logic, argument interpretation, item content, and response procedure.": "Точность зависит от выбранной нормативной логики, понимания аргумента, содержания задания и процедуры ответа.",
    "Aggregating heterogeneous people or items can distort receiver-operating-characteristic interpretations.": "Объединение неоднородных участников или заданий может исказить интерпретацию ROC-кривых.",
    "Behavioral interference and autonomic evidence support concurrent conflict in some tasks, but recent experiments show that experimenter-defined logical conflict can mismatch participants' subjective representations.": "Поведенческое взаимное влияние и показатели автономной нервной системы поддерживают одновременный конфликт в некоторых заданиях, но новые эксперименты показывают, что заданный исследователем логический конфликт может не совпадать с субъективным представлением участника.",
    "Belief-based and logic-based evaluations may sometimes proceed in parallel and generate response conflict when they favor different judgments.": "Оценка на основе житейской правдоподобности и оценка логической структуры иногда могут идти параллельно и создавать конфликт ответа, если подсказывают разные решения.",
    "Characterizing belief bias in syllogistic reasoning — a hierarchical Bayesian meta-analysis of ROC data": "Характеристика влияния убеждений на силлогистическое рассуждение: иерархический байесовский метаанализ ROC-данных",
    "Cognitive Atlas concept — deductive reasoning": "Понятие Cognitive Atlas: дедуктивное рассуждение",
    "Cognitive Atlas task — deductive reasoning task": "Задание Cognitive Atlas: дедуктивное рассуждение",
    "Condition-specific syllogism judgments": "Показатели силлогистических суждений по условиям",
    "Conflict detection with invalid inferences — all heuristics, no logic": "Обнаружение конфликта при невалидных выводах: конкуренция эвристик без логики",
    "Conflict effects do not establish two discrete mental systems, and the same response pattern can arise from different representations or strategies.": "Эффекты конфликта не доказывают существование двух отдельных психических систем, а одинаковый рисунок ответов может возникать из-за разных представлений или стратегий.",
    "Construction or evaluation of arguments in which a conclusion is assessed as following necessarily from stated premises or hypotheses.": "Построение или оценка аргументов, при которой проверяется, должен ли вывод следовать из заданных посылок или гипотез.",
    "Deductive construct, syllogism task, validity and believability, judgments, performance, signal detection, and parallel evaluation kept distinct.": "Конструкт дедуктивного рассуждения, задание с силлогизмами, валидность и правдоподобие, ответы, результат, анализ обнаружения сигнала и гипотеза параллельной оценки представлены раздельно.",
    "Deductive reasoning": "Дедуктивное рассуждение",
    "Deductive reasoning constructs or evaluates arguments intended to show that a conclusion necessarily follows from premises or hypotheses.": "Дедуктивное рассуждение строит или оценивает аргументы, призванные показать, что вывод с необходимостью следует из посылок или гипотез.",
    "Deductive reasoning is broader than performance on one syllogism task and narrower than thinking or intelligence in general.": "Дедуктивное рассуждение шире результата одного задания с силлогизмами, но уже мышления или интеллекта в целом.",
    "Discriminability and criterion are model-dependent estimates, not direct observations of reasoning mechanisms.": "Способность различать валидность и критерий ответа являются зависящими от модели оценками, а не прямыми наблюдениями механизмов рассуждения.",
    "Experimental crossing of whether a conclusion is logically entailed by its premises and whether it is believable from prior world knowledge.": "Экспериментальное сочетание двух признаков: следует ли вывод логически из посылок и кажется ли он правдоподобным с учётом знаний о мире.",
    "Experimental task in which a participant decides whether a conclusion follows from stated premises while logical validity and conclusion believability can agree or conflict.": "Экспериментальное задание, в котором участник решает, следует ли вывод из заданных посылок, а логическая валидность и житейская правдоподобность вывода могут совпадать или конфликтовать.",
    "Experimenter-defined logical conflict does not guarantee that every participant represents or experiences the same conflict.": "Заданный исследователем логический конфликт не гарантирует, что каждый участник понимает или переживает его одинаково.",
    "Feeling we're biased — autonomic arousal and reasoning conflict": "Чувство собственной предвзятости: автономное возбуждение и конфликт при рассуждении",
    "Greater skin conductance during belief-logic conflict was consistent with implicit conflict sensitivity even when final judgments were biased.": "Повышенная кожная проводимость при конфликте правдоподобия и логики согласуется с неявной чувствительностью к конфликту даже тогда, когда итоговый ответ зависел от убеждений.",
    "Human participants in three syllogistic-reasoning experiments reported by Evans, Barston, and Pollard in 1983.": "Участники трёх экспериментов по силлогистическому рассуждению, опубликованных Evans, Barston и Pollard в 1983 году.",
    "Humans constructing or evaluating deductive arguments.": "Люди, строящие или оценивающие дедуктивные аргументы.",
    "Humans evaluating syllogistic arguments in which conclusion believability and experimenter-defined validity agree or conflict.": "Люди, оценивающие силлогизмы, в которых правдоподобие вывода и заданная исследователем валидность совпадают или конфликтуют.",
    "In a hierarchical signal-detection meta-analysis of 22 confidence-rating studies, conclusion believability did not unconditionally reduce discrimination between valid and invalid syllogisms.": "В иерархическом метаанализе обнаружения сигнала по 22 исследованиям с оценкой уверенности правдоподобие вывода не снижало безусловно способность различать валидные и невалидные силлогизмы.",
    "In the Evans, Barston, and Pollard experiments, manipulated conclusion believability changed syllogism endorsement, with a larger belief bias for invalid than valid arguments.": "В экспериментах Evans, Barston и Pollard изменение правдоподобия вывода влияло на принятие силлогизма, причём влияние убеждений было сильнее для невалидных аргументов, чем для валидных.",
    "Logical validity is a property of an argument; it is not a mental state, observed response, or mechanism.": "Логическая валидность является свойством аргумента, а не психическим состоянием, наблюдаемым ответом или механизмом.",
    "Model-based separation of sensitivity to argument validity from response criteria using endorsement and confidence distributions for valid and invalid syllogisms.": "Модельное разделение чувствительности к валидности аргумента и критериев ответа по распределениям принятия и уверенности для валидных и невалидных силлогизмов.",
    "Observable acceptance or rejection of a conclusion as following logically from the presented premises.": "Наблюдаемое принятие или отклонение вывода как логически следующего из предъявленных посылок.",
    "On the conflict between logic and belief in syllogistic reasoning": "О конфликте логики и убеждений в силлогистическом рассуждении",
    "Parallel belief-logic evaluation": "Параллельная оценка правдоподобия и логики",
    "Parallel evaluation is a process hypothesis, not another name for a validity-by-believability interaction.": "Параллельная оценка является гипотезой о процессе, а не другим названием взаимодействия валидности и правдоподобия.",
    "Participants must represent both content-based and structural cues; objective and subjective conflict cannot be assumed equivalent.": "Участники должны учитывать и содержание, и структуру аргумента; объективный и субъективный конфликт нельзя заранее считать одинаковыми.",
    "Proposed process in which content-based plausibility and argument-structure information are evaluated concurrently and can support compatible or competing responses.": "Предполагаемый процесс, при котором правдоподобие содержания и структура аргумента оцениваются одновременно и могут поддерживать совпадающие или конкурирующие ответы.",
    "Protocol-scored agreement between a participant's validity judgment and the formal validity classification of the argument.": "Рассчитанное по протоколу совпадение ответа участника о валидности с формальной классификацией аргумента.",
    "Raw acceptance or accuracy does not by itself separate validity discrimination from a tendency to accept believable conclusions.": "Обычная доля принятия или точность сама по себе не отделяет способность различать валидность от склонности принимать правдоподобные выводы.",
    "Slower responses, lower confidence, skin conductance, or mutual interference are indirect and non-unique indicators of conflict.": "Более медленные ответы, меньшая уверенность, кожная проводимость и взаимное влияние являются косвенными и неспецифичными признаками конфликта.",
    "Studies with confidence-rating or compatible response data included in the hierarchical signal-detection corpus.": "Исследования с оценками уверенности или совместимыми данными ответов, включённые в корпус иерархического анализа обнаружения сигнала.",
    "Syllogism validity judgment": "Суждение о валидности силлогизма",
    "Syllogism validity-believability manipulation": "Изменение валидности и правдоподобия силлогизма",
    "Syllogistic judgment performance": "Результативность силлогистических суждений",
    "Syllogistic signal-detection profile": "Профиль обнаружения сигнала в силлогистических суждениях",
    "Syllogistic validity-judgment task": "Задание на оценку валидности силлогизмов",
    "The analysis included 993 participants and modeled participant and item heterogeneity, but conclusions depend on the signal-detection specification and available confidence-rating studies.": "Анализ охватил 993 участника и учитывал различия между людьми и заданиями, но выводы зависят от выбранной модели обнаружения сигнала и доступных исследований с оценкой уверенности.",
    "The definition does not establish that one task validly measures all forms of deduction or that formal correctness identifies one psychological mechanism.": "Определение не доказывает, что одно задание валидно измеряет все формы дедукции или что формально правильный ответ выявляет один психологический механизм.",
    "The definition matches standard usage and the linked Cognitive Atlas concept, but that collaborative record is marked Unreviewed.": "Определение соответствует общепринятому употреблению и связанному понятию Cognitive Atlas, однако эта коллективно созданная запись помечена как непроверенная.",
    "The effect concerns endorsement in these tasks and does not prove that participants ignored logic or identify a unique cognitive process.": "Эффект относится к принятию выводов в этих заданиях и не доказывает, что участники игнорировали логику, а также не выявляет единственный когнитивный процесс.",
    "The reported categorical syllogisms, believable and unbelievable conclusions, logical-validity classifications, instructions, and response procedures.": "Описанные категориальные силлогизмы, правдоподобные и неправдоподобные выводы, классификация логической валидности, инструкции и процедуры ответа.",
    "The task samples a restricted form of deductive evaluation; it is not deductive reasoning itself.": "Задание проверяет только ограниченную форму дедуктивной оценки и не является самим дедуктивным рассуждением.",
    "This result does not mean that believability never changes judgments; it distinguishes unconditional validity discrimination from response bias and conditional effects.": "Этот результат не означает, что правдоподобие никогда не меняет ответы; он отделяет общую способность различать валидность от смещения ответа и условных эффектов.",
    "Three controlled experiments reproduced the validity-by-believability pattern with several response-bias controls, but the historical samples and task materials limit generalization.": "Три контролируемых эксперимента воспроизвели совместный эффект валидности и правдоподобия с несколькими проверками смещения ответа, но старые выборки и материалы заданий ограничивают обобщение.",
    "Three experiments found that both logical validity and conclusion believability influenced syllogism judgments, with stronger belief bias on invalid arguments.": "Три эксперимента показали, что на суждения о силлогизмах влияли и логическая валидность, и правдоподобие вывода, причём влияние убеждений было сильнее для невалидных аргументов.",
    "Two experiments found complexity-dependent mutual interference between logical and belief judgments, supporting but not proving parallel evaluation.": "Два эксперимента обнаружили зависящее от сложности взаимное влияние логических суждений и оценки правдоподобия, что поддерживает, но не доказывает параллельную обработку.",
    "Two recent experiments showed that objective logical conflict can mismatch subjective conflict and challenged a universal logic-versus-heuristic interpretation.": "Два новых эксперимента показали, что объективный логический конфликт может не совпадать с субъективным, и поставили под сомнение универсальное объяснение через конфликт логики и эвристики.",
    "When fast logic meets slow belief — evidence for a parallel-processing model of belief bias": "Когда быстрая логика встречает медленные убеждения: данные в пользу модели параллельной обработки влияния убеждений",
})


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
