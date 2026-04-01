from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import List, Dict

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pptx import Presentation
from pptx.util import Inches as PptInches, Pt as PptPt

ROOT = Path('/Users/kerriannlark/Documents/Playground/LSAT-WRITING-OS')
OUTPUT = ROOT / 'output'
OUTPUT.mkdir(parents=True, exist_ok=True)

MODEL_PATH = OUTPUT / 'lsat_argumentative_curriculum_model.json'
GUIDE_PATH = OUTPUT / 'LSAT_Argumentative_Writing_Companion_Guide.docx'
DECK_PATH = OUTPUT / 'LSAT_Learning_Module_Companion_Deck.pptx'
OVERVIEW_PATH = OUTPUT / 'lsat_argumentative_curriculum_overview.md'
REFERENCE_LIBRARY_PATH = OUTPUT / 'reference_library_registry.json'
MODULE_RESOURCE_MAP_PATH = OUTPUT / 'module_resource_map.json'
WEAKNESS_RESOURCE_MAP_PATH = OUTPUT / 'weakness_resource_map.json'
GENERATED_ON = str(date.today())

modules: List[Dict] = [
    {
        'lesson_id': 'module-0',
        'title': 'Orientation + Official Mechanics',
        'goal': 'Understand what LSAT Argumentative Writing asks for and how timing modes should be labeled.',
        'core_concept': 'Strong LSAT writing rewards clear judgment, organized reasoning, perspective integration, and clean prose under time pressure.',
        'drill_type': 'Format check + workflow rehearsal',
        'timing_mode': 'Official 15/35; extended training default 23/53; accommodation simulation labeled separately',
        'source_grounding': 'Blueprint synthesis + official LSAC timing clarification',
        'input_template': 'Key question | perspective count | prewrite tasks | writing tasks | timing mode selected',
        'success_standard': 'User can explain the task, distinguish official timing from training timing, and describe what to do in prewriting versus drafting.',
        'coach_mapping': 'timing confusion -> Orientation + Official Mechanics',
        'checkpoint_output': 'One-sentence workflow plan for prewriting and essay drafting',
        'formula': 'Task = answer key question + compare perspectives + justify judgment',
        'example': 'Official mode = 15-minute prewrite + 35-minute essay. Extended training can remain 23/53, but it must never be labeled standard LSAT timing.',
        'drill_prompt': 'In 2 minutes, explain what happens in prewriting, what happens in the essay window, and what law schools are evaluating.',
        'strong_writer_note': 'Strong writers choose a lane early and protect time for actual drafting instead of spending the whole session planning.'
    },
    {
        'lesson_id': 'module-1',
        'title': 'Prompt Deconstruction + Scope Box',
        'goal': 'Narrow the prompt before drafting so the essay stays inside the actual evaluative task.',
        'core_concept': 'A scope box turns a broad topic into a controlled argumentative lane.',
        'drill_type': 'Ask-type detection + scope construction',
        'timing_mode': '6-minute microdrill or first 5 minutes of prewriting',
        'source_grounding': 'Learning module docs + writing notes + blueprint scope-box synthesis',
        'input_template': 'Topic subset | population/context | timeframe/condition | analytical lens | comparison rule',
        'success_standard': 'User fills all 5 parts of the scope box and identifies what falls outside the essay.',
        'coach_mapping': 'scope drift / vague framing -> Prompt Deconstruction + Scope Box',
        'checkpoint_output': 'Completed scope box + 2 exclusions',
        'formula': 'Topic subset | population/context | timeframe/condition | analytical lens | comparison rule',
        'example': 'Whether colleges should emphasize career preparation | undergraduate students in changing labor markets | long-term student development | adaptability + intellectual growth | favor the model that preserves opportunity and judgment',
        'drill_prompt': 'Underline the operative verbs in the question, then build a full 5-part scope box and list two tempting but irrelevant ideas to exclude.',
        'strong_writer_note': 'Strong writers define what “best” means before they start choosing evidence.'
    },
    {
        'lesson_id': 'module-2',
        'title': 'Perspective Extraction + Stakeholder Lattice',
        'goal': 'Map the perspectives into usable argumentative material instead of summarizing them in source order.',
        'core_concept': 'Each perspective should be read for claim, assumption, strength, weakness, value lens, and thesis use.',
        'drill_type': 'Perspective audit + topic-by-topic conversion',
        'timing_mode': '8-minute drill',
        'source_grounding': 'Study guide + practice essay notes + blueprint perspective synthesis',
        'input_template': 'Perspective | core claim | assumption | strength | weakness | value lens | thesis use',
        'success_standard': 'User can convert a source-order summary into topic-by-topic synthesis.',
        'coach_mapping': 'source-by-source summary -> Perspective Extraction + Stakeholder Lattice',
        'checkpoint_output': 'Completed perspective grid + one topic-by-topic synthesis paragraph',
        'formula': 'Perspective -> what it wants -> what it assumes -> where it helps or hurts your thesis',
        'example': 'Perspective 1 values market readiness; its strength is employability, but its weakness is over-reliance on narrow training staying relevant.',
        'drill_prompt': 'Audit all perspectives, then sort them by themes such as adaptability, civic growth, fairness, or independence rather than keeping them in source order.',
        'strong_writer_note': 'Strong writers use perspectives as evidence, not as a checklist of quotes to mention one by one.'
    },
    {
        'lesson_id': 'module-3',
        'title': 'Mechanism Lab',
        'goal': 'Build the habit of explaining how a claimed benefit or harm actually happens.',
        'core_concept': 'Mechanism = what the condition gives, allows, prevents, preserves, or changes that then produces the result.',
        'drill_type': '3-step mechanism builder + causal chain drill',
        'timing_mode': '10-minute drill or first body paragraph planning block',
        'source_grounding': 'Diagnostics + learning modules + verb-bank synthesis',
        'input_template': 'Claim -> what it gives -> what that allows/prevents -> resulting outcome',
        'success_standard': 'User can explain the causal chain without vague filler verbs.',
        'coach_mapping': 'weak mechanism -> Mechanism Lab',
        'checkpoint_output': 'Three mechanism chains + one sentence using a precise causal verb',
        'formula': 'Because X gives Y, it enables/prevents Z, which leads to the result claimed.',
        'example': 'Broader education exposes students to competing ideas, which strengthens judgment, which makes them more adaptable when their first professional framework stops working.',
        'drill_prompt': 'Take one claim from your outline and build the full causal chain. Then rewrite it with stronger mechanism verbs such as enables, preserves, reduces, or prevents.',
        'strong_writer_note': 'Strong writers do not say a policy is “better” and stop. They show what it changes and why that change matters.'
    },
    {
        'lesson_id': 'module-4',
        'title': 'Evidence → Inference → Why It Matters',
        'goal': 'Push beyond summary into meaning and consequence.',
        'core_concept': 'Evidence is only useful if the draft explains what it proves and why the proof matters for the judgment standard.',
        'drill_type': 'Inference ladder + weak/strong comparison',
        'timing_mode': '8-minute drill',
        'source_grounding': 'Diagnostic notes + study guide + blueprint inference chain',
        'input_template': 'Evidence | inference | why it matters | standard connection',
        'success_standard': 'User can write “This matters because…” lines that tie evidence to the thesis standard.',
        'coach_mapping': 'shallow inference -> Evidence → Inference → Why It Matters',
        'checkpoint_output': 'Two evidence ladders and one revised paragraph sentence',
        'formula': 'Evidence suggests X. This matters because Y, which supports the claim that Z is stronger.',
        'example': 'Perspective 2’s emphasis on reflection suggests college develops judgment. This matters because graduates face ambiguous problems that technical skill alone cannot solve.',
        'drill_prompt': 'Write one evidence sentence, one inference sentence, and one “why it matters” sentence for the same idea without repeating the same wording.',
        'strong_writer_note': 'Strong writers convert prompt material into argumentative meaning instead of paraphrasing it twice.'
    },
    {
        'lesson_id': 'module-5',
        'title': 'Thesis + Standard + Introduction',
        'goal': 'Create a thesis that clearly states the side, the standard, the narrowed scope, and the basis for comparison.',
        'core_concept': 'A good thesis is evaluative, comparative, scoped, and often slightly qualified.',
        'drill_type': 'Thesis lab + intro builder',
        'timing_mode': '10-minute drill',
        'source_grounding': 'Writing notes + practice essay + blueprint thesis system',
        'input_template': 'Competing concern | side | standard | scope | mechanism | optional qualification',
        'success_standard': 'User writes a thesis with a real comparative standard and a controlled introduction that does not wander into summary.',
        'coach_mapping': 'vague thesis/metric -> Thesis + Standard + Introduction',
        'checkpoint_output': 'Final thesis + 3-sentence introduction plan',
        'formula': 'Although [competing concern], [position] is stronger for [scope] because [mechanism], especially when judged by [standard/comparison rule].',
        'example': 'Although career readiness matters, colleges best serve students when they balance professional preparation with intellectual growth because that combination produces both immediate opportunity and long-term adaptability.',
        'drill_prompt': 'Draft a thesis that names the strongest opposing concern, your side, the judging standard, and one sentence of mechanism.',
        'strong_writer_note': 'Strong writers treat the thesis as a control panel for the whole essay, not just a slogan at the end of the intro.'
    },
    {
        'lesson_id': 'module-6',
        'title': 'Counterargument + Limitation Studio',
        'goal': 'Train fair counterargument treatment and precise narrowing instead of shallow rebuttal.',
        'core_concept': 'A counterargument becomes powerful when it is steelmanned, then limited by a real condition.',
        'drill_type': 'Objection extraction + limitation rewrite',
        'timing_mode': '10-minute drill or counter-paragraph planning block',
        'source_grounding': 'Learning module docs + diagnostic notes + blueprint counter studio',
        'input_template': 'Strongest objection | hidden assumption | limiting condition | rebuttal | comparative return',
        'success_standard': 'User can write a counter paragraph that acknowledges force, narrows it, and returns to the comparison.',
        'coach_mapping': 'weak counter + limitation -> Counterargument + Limitation Studio',
        'checkpoint_output': 'One completed counter paragraph plan',
        'formula': 'Critics argue X. That objection matters because Y. Yet it is strongest only when Z; under the actual condition, the original position remains stronger because…',
        'example': 'A career-first model is appealing when students face urgent economic pressure, but it weakens when narrow training becomes outdated faster than broader reasoning can adapt.',
        'drill_prompt': 'Write the strongest version of the objection. Then name the condition that limits it and add one return sentence that re-establishes your standard.',
        'strong_writer_note': 'Strong writers do not swat away the counterargument. They narrow it with a believable condition.'
    },
    {
        'lesson_id': 'module-7',
        'title': 'Paragraph Skeleton Mastery',
        'goal': 'Make every body paragraph follow a complete argumentative chain.',
        'core_concept': 'Claim, mechanism, evidence, inference, counterpoint, limitation, comparative close.',
        'drill_type': 'Paragraph build + Paragraph 2 expansion drill',
        'timing_mode': '12-minute drill',
        'source_grounding': 'Learning module drill chain + diagnostic emphasis on weak Paragraph 2',
        'input_template': 'Claim | mechanism | evidence | inference | counterpoint | limitation | comparative close',
        'success_standard': 'User can produce one full paragraph skeleton and especially expand Paragraph 2 instead of leaving it thin.',
        'coach_mapping': 'underdeveloped body paragraph -> Paragraph Skeleton Mastery',
        'checkpoint_output': 'One complete paragraph + one expanded Paragraph 2 plan',
        'formula': 'Sentence 1 claim -> sentence 2 mechanism -> sentence 3 evidence -> sentence 4 inference -> sentence 5 counter -> sentence 6 limitation -> sentence 7 comparative close',
        'example': 'Paragraph 2 should add a second dimension, not repeat Paragraph 1 with new wording.',
        'drill_prompt': 'Build Body Paragraph 2 on a second stakeholder, second value, or second dimension of the standard so the essay broadens rather than repeats itself.',
        'strong_writer_note': 'Strong writers know the second paragraph often decides whether the essay feels mature or repetitive.'
    },
    {
        'lesson_id': 'module-8',
        'title': 'Outline + Essay Architecture',
        'goal': 'Turn the paragraph system into a full 4-5 paragraph essay plan.',
        'core_concept': 'A full essay should feel sequenced: intro, reason 1, reason 2, counter/limitation, conclusion.',
        'drill_type': 'Outline builder + architecture check',
        'timing_mode': '10-minute prewrite drill',
        'source_grounding': 'Study guide + practice essay structure + blueprint architecture',
        'input_template': 'Intro lane | body 1 role | body 2 role | counter role | conclusion role',
        'success_standard': 'User can produce a full outline where each paragraph has a distinct job.',
        'coach_mapping': 'weak comparative close / essay structure drift -> Outline + Essay Architecture',
        'checkpoint_output': 'Complete outline with paragraph jobs and key transitions',
        'formula': 'Intro = scoped issue + tension + thesis; Body 1 = primary reason; Body 2 = second dimension; Counter = objection + limit; Conclusion = comparative judgment',
        'example': 'If Body 1 proves immediate opportunity and Body 2 proves long-term adaptability, the counter paragraph can concede economic pressure while limiting narrow specialization.',
        'drill_prompt': 'Write one sentence for the job of each paragraph before drafting the essay itself.',
        'strong_writer_note': 'Strong writers give every paragraph a different burden of proof.'
    },
    {
        'lesson_id': 'module-9',
        'title': 'Timed Performance System',
        'goal': 'Convert the reasoning system into repeatable timed performance.',
        'core_concept': 'Timed training should save notes, output, weaknesses, and next-step drills so each rep compounds.',
        'drill_type': 'Official simulation + extended training + microdrills',
        'timing_mode': 'Official 15/35, extended 23/53, microdrills 6/8/10/12/15',
        'source_grounding': 'Blueprint timing system + study guide workflow',
        'input_template': 'Timing mode | prewrite notes | word count | paragraph count | weakness bucket | next drill',
        'success_standard': 'User completes reps without losing the counter paragraph or conclusion and records which weakness showed up.',
        'coach_mapping': 'execution breakdown / missing counter / weak close -> Timed Performance System',
        'checkpoint_output': 'Timed rep log + next drill recommendation',
        'formula': 'Rep -> diagnose -> assign weakness bucket -> run targeted drill -> repeat',
        'example': 'After a timed rep, classify the weakest area as mechanism, inference, scope, counter, comparison, or sentence clarity and assign one drill before the next essay.',
        'drill_prompt': 'Run one full timed rep and log: timing mode, whether the counter paragraph was completed, total word count, and the single biggest weakness to address next.',
        'strong_writer_note': 'Strong writers do not just write more essays; they convert each rep into a specific next drill.'
    }
]

slides: List[Dict] = [
    {
        'title': 'What the modern LSAT writing task is',
        'concept': 'Answer the key question, compare perspectives, and justify the better judgment in clean prose.',
        'formula': 'Key question + standard + side + reasoning chain = strong LSAT essay',
        'example': 'A strong essay does not list all four perspectives. It uses the most relevant ones to prove a controlled judgment.',
        'drill': 'In one minute, explain what makes the task argumentative rather than merely descriptive.',
        'strong_note': 'Strong writers choose a standard early and make every paragraph answer that standard.'
    },
    {
        'title': 'Official vs extended timing',
        'concept': 'Official LSAT timing is 15/35. Extended 23/53 belongs to training or accommodation simulation only.',
        'formula': 'Official = 15 prewrite / 35 write | Extended training = 23 / 53 | Microdrills = 6-15 minutes',
        'example': 'Use extended timing for skills work, but always label it clearly so the student knows it is not the standard LSAT format.',
        'drill': 'Write down what you will do in the first 5 minutes of prewriting and the first 5 minutes of drafting.',
        'strong_note': 'Strong writers protect drafting time; they do not spend the whole session planning.'
    },
    {
        'title': 'The core reasoning chain',
        'concept': 'Every strong paragraph follows the same logic chain.',
        'formula': 'Claim -> Mechanism -> Evidence -> Inference -> Counter -> Limitation -> Comparative close',
        'example': 'If career preparation helps students, explain how it does so, what evidence supports it, and why that matters more than the competing concern.',
        'drill': 'Label each sentence of a model paragraph by function.',
        'strong_note': 'Strong writers know what each sentence is doing before they worry about sounding impressive.'
    },
    {
        'title': 'Scope box system',
        'concept': 'A scope box narrows the prompt into a usable lane.',
        'formula': 'Topic subset | population/context | timeframe/condition | analytical lens | comparison rule',
        'example': 'Undergraduate education | students in changing labor markets | long-term development | adaptability + judgment | favor the model that protects both opportunity and growth',
        'drill': 'Build a full scope box and then list two ideas that fall outside it.',
        'strong_note': 'Strong writers use the scope box to exclude tempting but irrelevant points.'
    },
    {
        'title': 'Perspective audit system',
        'concept': 'Treat each perspective as a value lens and argumentative tool.',
        'formula': 'Core claim + assumption + strength + weakness + value lens + thesis use',
        'example': 'A perspective may help your thesis on adaptability but hurt it on fairness. Track both.',
        'drill': 'Convert a source-order summary into a topic-by-topic map.',
        'strong_note': 'Strong writers sort perspectives by issue, not by the order they appeared in the prompt.'
    },
    {
        'title': 'Mechanism lab',
        'concept': 'Mechanism explains how the result happens.',
        'formula': 'Because X gives/allows/prevents Y, it leads to Z',
        'example': 'Exposure to competing ideas strengthens judgment, which makes graduates more adaptable when circumstances change.',
        'drill': 'Build a 3-step causal chain for one claim from your outline.',
        'strong_note': 'Strong writers replace vague verbs like “helps” with causal verbs that show what changes.'
    },
    {
        'title': 'Inference lab',
        'concept': 'Evidence matters only if the draft explains what it proves and why that proof matters.',
        'formula': 'Evidence suggests X. This matters because Y. Therefore Z is stronger.',
        'example': 'Perspective 2 suggests reflection strengthens judgment. This matters because ambiguous problems cannot be solved by technical skill alone.',
        'drill': 'Write one evidence sentence, one inference sentence, and one why-it-matters sentence for the same idea.',
        'strong_note': 'Strong writers do not paraphrase the same evidence twice and call it analysis.'
    },
    {
        'title': 'Thesis + intro system',
        'concept': 'A thesis should concede the competing concern, take a side, name the standard, and state the mechanism.',
        'formula': 'Although [competing concern], [position] is stronger because [mechanism], especially when judged by [standard].',
        'example': 'Although career readiness matters, a balanced college model is stronger because it produces both immediate opportunity and long-term adaptability.',
        'drill': 'Draft a thesis that includes one hedge or qualification.',
        'strong_note': 'Strong writers use the introduction to narrow the debate, not to summarize every perspective.'
    },
    {
        'title': 'Counter + limitation system',
        'concept': 'A powerful counter paragraph acknowledges force and then narrows it with a real condition.',
        'formula': 'Critics argue X because Y. That matters, but it is strongest only when Z. Under the actual condition, the original position remains stronger because…',
        'example': 'A career-first model helps under urgent economic pressure, but it weakens when narrow specialization becomes obsolete.',
        'drill': 'Write the strongest objection first. Then write the condition that limits it.',
        'strong_note': 'Strong writers do not avoid the best objection. They control it.'
    },
    {
        'title': 'Paragraph skeleton',
        'concept': 'Every body paragraph needs a full argumentative skeleton.',
        'formula': 'Claim | Mechanism | Evidence | Inference | Counterpoint | Limitation | Comparative conclusion',
        'example': 'Paragraph 2 should prove a second dimension of the standard instead of repeating Paragraph 1.',
        'drill': 'Run a Paragraph 2 Expansion Drill on your weakest essay.',
        'strong_note': 'Strong writers know their second paragraph often determines whether the essay feels mature.'
    },
    {
        'title': '5-paragraph essay architecture',
        'concept': 'Each paragraph should carry a distinct burden of proof.',
        'formula': 'Intro -> Body 1 -> Body 2 -> Counter/Limitation -> Conclusion',
        'example': 'Body 1 can prove immediate opportunity; Body 2 can prove long-term adaptability; Counter can concede economic pressure but limit narrow training.',
        'drill': 'Write one sentence describing the job of each paragraph before drafting.',
        'strong_note': 'Strong writers avoid paragraphs that all do the same thing with different wording.'
    },
    {
        'title': 'Timed workflow',
        'concept': 'Timed reps should preserve diagnosis, not just output.',
        'formula': 'Rep -> diagnose weakness -> assign next drill -> repeat',
        'example': 'After the essay, log whether the counter paragraph was completed and which single weakness hurt the score most.',
        'drill': 'Run one microdrill and one full rep, then compare what breaks down under pressure.',
        'strong_note': 'Strong writers use timed reps to gather data, not just to feel busy.'
    },
    {
        'title': 'Diagnostic weakness map',
        'concept': 'The same weakness categories should appear in coaching, revision, and tracker data.',
        'formula': 'Mechanism | Inference | Scope | Thesis | Counter | Limitation | Comparative close | Sentence clarity',
        'example': 'If the essay summarizes perspectives but never interprets them, the weakness is inference depth, not merely evidence use.',
        'drill': 'Tag one old draft with every weakness category you can find.',
        'strong_note': 'Strong writers diagnose specific failures instead of calling an essay “bad” in general.'
    },
    {
        'title': 'Daily drill loop',
        'concept': 'Skill gains come from short focused reps, not only full essays.',
        'formula': 'Scope box -> perspective audit -> mechanism -> inference -> paragraph build',
        'example': 'A 45-minute block can still move the needle if it targets one weakness category fully.',
        'drill': 'Build a one-day drill stack around your weakest category.',
        'strong_note': 'Strong writers practice subskills separately so the full essay feels lighter.'
    },
    {
        'title': 'Weekly improvement loop',
        'concept': 'Each week should include full reps, diagnosis, and targeted repair.',
        'formula': '2 timed reps + 3 drill blocks + 1 revision session + 1 tracker review',
        'example': 'If two essays in a row break down on mechanism, the next week should bias toward causal chain drills before another full rep.',
        'drill': 'Map your next 7 days: which two full reps and which three drills will you run?',
        'strong_note': 'Strong writers treat improvement like a system, not a mood.'
    }
]

chapters: List[Dict] = [
    {
        'title': 'Official Mechanics',
        'overview': 'Keep one truth clear: the standard LSAT format is 15 minutes of prewriting and 35 minutes of essay writing. Training can still foreground 23/53 if that is useful for extended practice, but the app, guide, and deck should label it as training or accommodation simulation rather than standard timing.',
        'formula': 'Official mode: 15 / 35 | Extended training: 23 / 53 | Microdrills: 6, 8, 10, 12, 15',
        'worked_example': 'A student can use a 23-minute prewrite to practice deeper reasoning, but when simulating the real test they should rehearse 15 minutes of planning and 35 minutes of drafting.',
        'drill_instructions': [
            'Write down the first five moves you make in official prewriting.',
            'List what must be on the scratch paper before you start the essay.',
            'Explain why extended timing is still useful without confusing it with the official standard.'
        ],
        'mistakes': [
            ('Treating 23/53 as standard LSAT timing', 'Relabel the mode immediately as extended training or accommodation simulation.'),
            ('Overplanning and underdrafting', 'Use a visible checkpoint: thesis, body map, counter condition, then start drafting.'),
        ]
    },
    {
        'title': 'Scope and Prompt Reading',
        'overview': 'Prompt reading should move from issue recognition to scope control. Ask-type detection, operative-verb detection, and exclusion testing prevent the essay from drifting into generic opinion writing.',
        'formula': 'Topic subset | population/context | timeframe/condition | analytical lens | comparison rule',
        'worked_example': 'Prompt: Should colleges emphasize career preparation? Scope box: role of undergraduate education | students in changing labor markets | long-term student development | adaptability + intellectual growth | favor the model that preserves both opportunity and judgment.',
        'drill_instructions': [
            'Underline the task verbs.',
            'Capture the real constraint or operating condition.',
            'Name two ideas that are outside the scope and should not appear in the essay.'
        ],
        'mistakes': [
            ('Broad topic statement', 'Rewrite the issue as a smaller subset that can actually be evaluated.'),
            ('No comparison rule', 'Add a sentence defining what makes one side stronger than the other.'),
        ]
    },
    {
        'title': 'Perspective Synthesis',
        'overview': 'Perspective work should generate argumentative leverage, not summary. The goal is to map values, assumptions, strengths, weaknesses, and how each perspective interacts with your thesis.',
        'formula': 'Perspective -> claim -> assumption -> strength -> weakness -> value lens -> thesis use',
        'worked_example': 'A workforce perspective may support your essay on employability while still being vulnerable on long-term adaptability or civic judgment.',
        'drill_instructions': [
            'Complete a perspective grid for all perspectives in the prompt.',
            'Sort the perspectives by theme instead of source order.',
            'Write one paragraph that synthesizes two perspectives under the same topic heading.'
        ],
        'mistakes': [
            ('Source-order summary', 'Re-sort by issue or value lens.'),
            ('Name-dropping perspectives without analysis', 'Add one line that says what the perspective proves and why that matters.'),
        ]
    },
    {
        'title': 'Mechanism',
        'overview': 'Mechanism is the largest recurring weakness in the diagnostic documents. Students often assert that something is better without explaining what it changes and why that change produces the claimed result.',
        'formula': 'Because X gives/allows/prevents Y, it leads to Z',
        'worked_example': 'Reflective education exposes students to competing ideas, which strengthens judgment, which helps them adapt when technical routines no longer fit new problems.',
        'drill_instructions': [
            'Write a claim.',
            'Name what that condition gives, allows, reduces, or preserves.',
            'Finish the causal chain with the result that matters for the thesis.'
        ],
        'mistakes': [
            ('Using vague verbs like helps or improves', 'Swap in causal verbs such as enables, preserves, reduces, prevents, or accelerates.'),
            ('Skipping the middle step', 'Add the missing link between the condition and the final outcome.'),
        ]
    },
    {
        'title': 'Inference',
        'overview': 'Evidence becomes analysis only when the writer explains what it proves and why that proof matters. Students should practice the ladder from evidence to inference to consequence.',
        'formula': 'Evidence suggests X. This matters because Y. Therefore Z is stronger.',
        'worked_example': 'Perspective 2 values reflection. This suggests college builds independent judgment. That matters because unfamiliar professional and civic problems require judgment, not just technical fluency.',
        'drill_instructions': [
            'Write one evidence sentence from the prompt.',
            'Translate it into an inference sentence.',
            'Add a why-it-matters sentence tied to your judging standard.'
        ],
        'mistakes': [
            ('Repeating the same evidence in different words', 'Force yourself to add “This matters because…” and name the consequence.'),
            ('Inference disconnected from the thesis', 'Tie the inference back to the standard such as adaptability, fairness, or intellectual independence.'),
        ]
    },
    {
        'title': 'Thesis / Standard / Introduction',
        'overview': 'The thesis is the control point for the essay. It should name the best opposing concern, the position taken, the standard, and the mechanism that makes the position stronger.',
        'formula': 'Although [competing concern], [position] is stronger because [mechanism], especially when judged by [standard].',
        'worked_example': 'Although career readiness matters, colleges best serve students when they balance professional preparation with intellectual growth because that combination produces both immediate opportunity and long-term adaptability.',
        'drill_instructions': [
            'Write the strongest opposing concern first.',
            'State your side in evaluative language.',
            'Add the comparison standard and one mechanism clause.'
        ],
        'mistakes': [
            ('Generic thesis with no metric', 'Add what “best serves students” means in this essay.'),
            ('Overlong introduction', 'Limit the intro to scoped issue, tension, and thesis.'),
        ]
    },
    {
        'title': 'Counter + Limitation',
        'overview': 'The counter paragraph shows maturity when the writer gives the objection real force and then narrows it under a condition. This prevents the essay from sounding brittle or one-sided.',
        'formula': 'Objection matters because Y, but it is strongest only when Z. Under the actual condition, the original position remains stronger because…',
        'worked_example': 'A career-first model matters when students face urgent financial pressure, but it weakens when narrow specialization becomes obsolete before broader judgment can be replaced.',
        'drill_instructions': [
            'Write the strongest version of the objection.',
            'Identify the hidden assumption behind it.',
            'Name the condition that limits it and write a comparative return sentence.'
        ],
        'mistakes': [
            ('Dismissive rebuttal', 'Acknowledge what makes the objection persuasive first.'),
            ('No limitation condition', 'Add “This is strongest only when…” and finish the condition.'),
        ]
    },
    {
        'title': 'Paragraph and Outline Architecture',
        'overview': 'Paragraph design and full-essay architecture should be explicit. The second body paragraph deserves special attention because it often collapses into repetition or rushed summary.',
        'formula': 'Intro | Body 1 | Body 2 | Counter/Limitation | Conclusion',
        'worked_example': 'Body 1 can prove immediate opportunity. Body 2 can prove long-term adaptability or intellectual independence. The counter paragraph can handle the strongest economic objection.',
        'drill_instructions': [
            'Write the job of each paragraph in one sentence.',
            'Run a Paragraph 2 Expansion Drill.',
            'Add the comparative conclusion line for each body paragraph.'
        ],
        'mistakes': [
            ('Paragraph 2 repeats Paragraph 1', 'Force Paragraph 2 to prove a second stakeholder, second value, or second dimension of the same standard.'),
            ('Weak conclusion', 'Make the conclusion weigh the positions explicitly instead of merely restating the thesis.'),
        ]
    },
    {
        'title': 'Timed Performance',
        'overview': 'Timed writing should generate data: what broke down, what held, and what drill should come next. The app and guide should help the student turn every rep into a diagnosis.',
        'formula': 'Rep -> diagnose weakness -> targeted drill -> next rep',
        'worked_example': 'If a timed essay loses the counter paragraph twice in a row, the next session should include a 10-minute counter/limitation drill before another full rep.',
        'drill_instructions': [
            'Run one official simulation and one extended training rep.',
            'Record word count, paragraph count, whether the counter paragraph was completed, and the biggest weakness category.',
            'Assign the next drill before you close the session.'
        ],
        'mistakes': [
            ('Treating timed reps as isolated events', 'Track weakness patterns over multiple reps.'),
            ('Trying to fix everything at once', 'Choose the single highest-leverage weakness for the next session.'),
        ]
    },
    {
        'title': 'Self-Diagnosis and Revision Loops',
        'overview': 'Revision should be driven by recurring weakness categories rather than vague dissatisfaction. The same buckets should appear in the app, deck, and written guide.',
        'formula': 'Thesis clarity | scope control | perspective integration | mechanism depth | inference depth | counter precision | limitation quality | comparative judgment | paragraph completeness | sentence clarity',
        'worked_example': 'An essay that mentions the perspectives but never explains what they prove should be tagged for inference depth, not just evidence use.',
        'drill_instructions': [
            'Tag one completed essay with every weakness category you can find.',
            'Choose one paragraph to revise for mechanism and one for inference.',
            'Write the next drill assignment at the top of the page before ending the session.'
        ],
        'mistakes': [
            ('Global self-criticism with no diagnosis', 'Replace “This essay is bad” with one or two specific failure categories.'),
            ('Revision without a goal', 'Name the exact category being repaired before rewriting.'),
        ]
    },
]

sprint_days = [
    {
        'day': 'Day 1',
        'focus': 'Official mechanics, prompt deconstruction, perspective reading, mechanism basics, one full paragraph',
        'must_outputs': ['Scope box', 'Thesis direction', 'Perspective grid', 'One complete body paragraph']
    },
    {
        'day': 'Day 2',
        'focus': 'Thesis, standard, intro, counter/limitation, paragraph skeleton, full outline',
        'must_outputs': ['Final thesis', 'Introduction plan', 'Counter paragraph plan', 'Full outline']
    },
    {
        'day': 'Day 3',
        'focus': 'Timed reps, diagnosis, revision, capstone essay',
        'must_outputs': ['Official or extended timed rep', 'Weakness diagnosis', 'Targeted revision', 'Best model essay']
    },
]

reference_library = [
    {
        'id': 'companion-guide',
        'title': 'Companion Guide',
        'group': 'Companion Outputs',
        'source_type': 'DOCX guide',
        'role': 'Full written manual aligned to the app sequence',
        'best_use': 'Read before a drill block or before rewriting a weak essay.',
        'related_modules': ['module-0', 'module-1', 'module-3', 'module-4', 'module-5', 'module-6', 'module-7', 'module-8', 'module-9'],
        'weakness_categories': ['mechanism depth', 'inference depth', 'thesis clarity', 'counter precision', 'comparative judgment'],
        'summary': 'A structured written guide with formulas, drill instructions, and common mistake -> fix tables.',
        'href': './output/LSAT_Argumentative_Writing_Companion_Guide.docx',
        'public_safe': True,
        'local_only': False
    },
    {
        'id': 'companion-deck',
        'title': 'Learning Module Companion Deck',
        'group': 'Companion Outputs',
        'source_type': 'PPTX deck',
        'role': 'Slide-based review and teaching companion',
        'best_use': 'Skim before practice or use as a recap after a drill block.',
        'related_modules': ['module-0', 'module-1', 'module-2', 'module-3', 'module-4', 'module-5', 'module-6', 'module-7', 'module-8', 'module-9'],
        'weakness_categories': ['scope control', 'mechanism depth', 'inference depth', 'counter precision', 'paragraph completeness'],
        'summary': 'A concise slide deck with one concept, one formula, one example, one drill prompt, and one strong-writer note per topic.',
        'href': './output/LSAT_Learning_Module_Companion_Deck.pptx',
        'public_safe': True,
        'local_only': False
    },
    {
        'id': 'curriculum-overview',
        'title': 'Curriculum Overview',
        'group': 'Companion Outputs',
        'source_type': 'Markdown overview',
        'role': 'Quick reference map of the whole system',
        'best_use': 'Use to orient yourself before a study session.',
        'related_modules': ['module-0', 'module-9'],
        'weakness_categories': ['scope control', 'paragraph completeness'],
        'summary': 'A compact map of the module order, sprint outputs, and timing rules.',
        'href': './output/lsat_argumentative_curriculum_overview.md',
        'public_safe': True,
        'local_only': False
    },
    {
        'id': 'curriculum-model',
        'title': 'Curriculum Model JSON',
        'group': 'Companion Outputs',
        'source_type': 'JSON model',
        'role': 'Structured curriculum registry',
        'best_use': 'Use for implementation review, QA, or future automation.',
        'related_modules': ['module-0', 'module-9'],
        'weakness_categories': ['sentence clarity'],
        'summary': 'The structured curriculum dataset that mirrors the deck, guide, and lesson order.',
        'href': './output/lsat_argumentative_curriculum_model.json',
        'public_safe': True,
        'local_only': False
    },
    {
        'id': 'module-docx',
        'title': 'Original Learning Module DOCX',
        'group': 'Learning Module Files',
        'source_type': 'DOCX source',
        'role': 'Private local source document',
        'best_use': 'Read when expanding lesson explanations or checking the original drill sequencing.',
        'related_modules': ['module-0', 'module-3', 'module-4', 'module-7'],
        'weakness_categories': ['mechanism depth', 'inference depth', 'paragraph completeness'],
        'summary': 'Original learning-module writeup used to shape drill sequence, chunking, and explanation flow.',
        'companion_id': 'companion-guide',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'module-pptx',
        'title': 'Original Learning Module PPTX',
        'group': 'Learning Module Files',
        'source_type': 'PPTX source',
        'role': 'Private local slide source',
        'best_use': 'Use for slide framing, lesson summaries, and visual study recaps.',
        'related_modules': ['module-0', 'module-3', 'module-4', 'module-7'],
        'weakness_categories': ['mechanism depth', 'inference depth', 'paragraph completeness'],
        'summary': 'Original deck source used to strengthen slide-level explanation and quick review structure.',
        'companion_id': 'companion-deck',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'argumentative-notes',
        'title': 'Argumentative Notes from Sources',
        'group': 'Argumentative Writing Notes',
        'source_type': 'DOCX notes',
        'role': 'Private notes synthesis',
        'best_use': 'Read before mechanism, thesis, or counter drills to gather phrasing and logic patterns.',
        'related_modules': ['module-3', 'module-4', 'module-5', 'module-6'],
        'weakness_categories': ['mechanism depth', 'inference depth', 'thesis clarity', 'counter precision'],
        'summary': 'Aggregated argumentative notes used to shape drills, sentence stems, and revision targets.',
        'companion_id': 'companion-guide',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'study-guide-source',
        'title': 'LSAT Argumentative Writing Study Guide',
        'group': 'Study Guides',
        'source_type': 'DOCX guide',
        'role': 'Private workflow guide',
        'best_use': 'Read before official-mode or timed practice sessions.',
        'related_modules': ['module-0', 'module-1', 'module-8', 'module-9'],
        'weakness_categories': ['scope control', 'paragraph completeness', 'comparative judgment'],
        'summary': 'Original guide that informed timing, prewriting structure, scratch-paper use, and full-essay flow.',
        'companion_id': 'companion-guide',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'practice-essay-source',
        'title': 'LSAT Practice Argumentative Essay',
        'group': 'Practice Essay / Examples',
        'source_type': 'DOCX example',
        'role': 'Private example essay source',
        'best_use': 'Use while reviewing paragraph architecture and revision decisions.',
        'related_modules': ['module-5', 'module-7', 'module-8'],
        'weakness_categories': ['thesis clarity', 'paragraph completeness', 'comparative judgment'],
        'summary': 'Practice essay source used to reinforce outline sequencing and paragraph-role clarity.',
        'companion_id': 'companion-guide',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'writing-notes-source',
        'title': 'LSAT Argumentative Writing Notes',
        'group': 'Argumentative Writing Notes',
        'source_type': 'DOCX notes',
        'role': 'Private notes source',
        'best_use': 'Use for scope, thesis, and counterargument review before drilling.',
        'related_modules': ['module-1', 'module-5', 'module-6'],
        'weakness_categories': ['scope control', 'thesis clarity', 'counter precision', 'limitation quality'],
        'summary': 'Source notes that shaped the scope-box system, thesis formulas, and counter/limitation studio.',
        'companion_id': 'companion-guide',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'document2-source',
        'title': 'Document2',
        'group': 'Study Guides',
        'source_type': 'DOCX notes',
        'role': 'Private diagnostic/refinement source',
        'best_use': 'Use when diagnosing repeated weakness patterns and planning the next drill block.',
        'related_modules': ['module-4', 'module-6', 'module-9'],
        'weakness_categories': ['inference depth', 'counter precision', 'sentence clarity'],
        'summary': 'Supplemental notes source used to reinforce revision patterns and coaching language.',
        'companion_id': 'curriculum-overview',
        'public_safe': False,
        'local_only': True
    },
    {
        'id': 'document6-source',
        'title': 'Document (6)',
        'group': 'Study Guides',
        'source_type': 'DOCX notes',
        'role': 'Private diagnostic/refinement source',
        'best_use': 'Use while reviewing fallback examples and revision logic.',
        'related_modules': ['module-2', 'module-4', 'module-9'],
        'weakness_categories': ['perspective integration', 'inference depth', 'sentence clarity'],
        'summary': 'Supplemental notes that help with perspective synthesis, evidence meaning, and controlled revisions.',
        'companion_id': 'curriculum-overview',
        'public_safe': False,
        'local_only': True
    },
]

study_paths = [
    {
        'id': 'path-mechanism',
        'title': 'Mechanism Path',
        'summary': 'Read the mechanism explanation first, then run a causal-chain drill before writing.',
        'lesson_id': 'module-3',
        'resource_ids': ['companion-guide', 'argumentative-notes', 'module-docx']
    },
    {
        'id': 'path-inference',
        'title': 'Inference Path',
        'summary': 'Use the inference ladder to move from evidence to meaning to consequence.',
        'lesson_id': 'module-4',
        'resource_ids': ['companion-guide', 'writing-notes-source', 'document6-source']
    },
    {
        'id': 'path-counter',
        'title': 'Counter + Limitation Path',
        'summary': 'Read how to steelman the objection, limit it, and return to comparison before timed rewriting.',
        'lesson_id': 'module-6',
        'resource_ids': ['companion-guide', 'writing-notes-source', 'document2-source']
    },
    {
        'id': 'path-thesis',
        'title': 'Thesis + Scope Path',
        'summary': 'Use the scope box and thesis formulas together before drafting any intro.',
        'lesson_id': 'module-5',
        'resource_ids': ['companion-deck', 'study-guide-source', 'writing-notes-source']
    },
    {
        'id': 'path-timed',
        'title': 'Timed Performance Path',
        'summary': 'Review the timing rules, run a rep, then diagnose the single biggest weakness category.',
        'lesson_id': 'module-9',
        'resource_ids': ['curriculum-overview', 'study-guide-source', 'document2-source']
    },
]

module_resource_map = {
    'module-0': ['curriculum-overview', 'companion-guide', 'module-docx', 'module-pptx'],
    'module-1': ['companion-guide', 'companion-deck', 'study-guide-source', 'writing-notes-source'],
    'module-2': ['companion-guide', 'module-pptx', 'document6-source'],
    'module-3': ['companion-guide', 'companion-deck', 'argumentative-notes', 'module-docx'],
    'module-4': ['companion-guide', 'argumentative-notes', 'document6-source'],
    'module-5': ['companion-guide', 'companion-deck', 'writing-notes-source', 'practice-essay-source'],
    'module-6': ['companion-guide', 'writing-notes-source', 'document2-source'],
    'module-7': ['companion-guide', 'practice-essay-source', 'module-pptx'],
    'module-8': ['companion-guide', 'study-guide-source', 'practice-essay-source'],
    'module-9': ['curriculum-overview', 'curriculum-model', 'study-guide-source', 'document2-source'],
}

weakness_resource_map = {
    'thesis clarity': {'lesson_id': 'module-5', 'resource_ids': ['companion-guide', 'writing-notes-source']},
    'scope control': {'lesson_id': 'module-1', 'resource_ids': ['companion-deck', 'study-guide-source']},
    'perspective integration': {'lesson_id': 'module-2', 'resource_ids': ['companion-guide', 'document6-source']},
    'mechanism depth': {'lesson_id': 'module-3', 'resource_ids': ['companion-guide', 'argumentative-notes', 'module-docx']},
    'inference depth': {'lesson_id': 'module-4', 'resource_ids': ['companion-guide', 'document6-source']},
    'counter precision': {'lesson_id': 'module-6', 'resource_ids': ['companion-guide', 'writing-notes-source']},
    'limitation quality': {'lesson_id': 'module-6', 'resource_ids': ['companion-guide', 'document2-source']},
    'comparative judgment': {'lesson_id': 'module-8', 'resource_ids': ['companion-guide', 'practice-essay-source']},
    'paragraph completeness': {'lesson_id': 'module-7', 'resource_ids': ['companion-guide', 'module-pptx']},
    'sentence clarity': {'lesson_id': 'module-9', 'resource_ids': ['curriculum-overview', 'document2-source']},
}

payload = {
    'metadata': {
        'title': 'LSAT Argumentative Writing Curriculum Model',
        'official_timing': {'prewrite_minutes': 15, 'writing_minutes': 35},
        'extended_training_default': {'prewrite_minutes': 23, 'writing_minutes': 53},
        'generated_on': GENERATED_ON,
        'source_of_truth': str(OUTPUT / 'lsat_argumentative_curriculum_blueprint.md'),
    },
    'modules': modules,
    'slides': slides,
    'chapters': chapters,
    'sprint_days': sprint_days,
    'resources': reference_library,
    'study_paths': study_paths,
    'module_resource_map': module_resource_map,
    'weakness_resource_map': weakness_resource_map,
}


def set_doc_margins(section):
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)


def add_bullet(doc: Document, text: str, level: int = 0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.25 * level)
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p


def shade_cell(cell, fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)


def build_guide():
    doc = Document()
    for section in doc.sections:
        set_doc_margins(section)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('LSAT Argumentative Writing Companion Guide')
    run.bold = True
    run.font.size = Pt(20)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run('Original curriculum guide synthesized from local learning-module documents and official LSAC timing guidance.').italic = True

    doc.add_paragraph('START HERE: Use this guide with the app. Keep official timing (15/35) visible as the authoritative baseline. Use extended 23/53 only as labeled training or accommodation simulation.')

    doc.add_heading('Three-Day Sprint Map', level=1)
    for day in sprint_days:
        doc.add_heading(f"{day['day']} — {day['focus']}", level=2)
        for output in day['must_outputs']:
            add_bullet(doc, output)

    for chapter in chapters:
        doc.add_page_break()
        doc.add_heading(chapter['title'], level=1)
        doc.add_paragraph(chapter['overview'])

        doc.add_paragraph().add_run(f"Formula: {chapter['formula']}").bold = True
        doc.add_paragraph().add_run(f"Worked example: {chapter['worked_example']}")

        doc.add_heading('Drill Instructions', level=2)
        for item in chapter['drill_instructions']:
            add_bullet(doc, item)

        doc.add_heading('Common Mistake → Fix', level=2)
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Common mistake'
        hdr[1].text = 'Fix'
        shade_cell(hdr[0], 'D9EAF7')
        shade_cell(hdr[1], 'D9EAF7')
        for mistake, fix in chapter['mistakes']:
            row = table.add_row().cells
            row[0].text = mistake
            row[1].text = fix

        doc.add_heading('Timed Variant', level=2)
        doc.add_paragraph('Run this chapter as a microdrill first, then attach it to a full essay rep. Log the weakness category that shows up when time pressure returns.')

        doc.add_heading('Checkpoint', level=2)
        doc.add_paragraph('Before moving on, save one output from this chapter into the tracker: either a completed drill, a thesis, a paragraph skeleton, or a timed-rep diagnosis.')

    doc.add_page_break()
    doc.add_heading('Weekly Improvement Loop', level=1)
    loop_items = [
        '2 full essay reps (one official-timing simulation, one extended training rep)',
        '3 targeted drill blocks focused on the highest-frequency weakness bucket',
        '1 revision session that rewrites at least one paragraph for mechanism or inference',
        '1 tracker review that assigns the next week’s first drill',
    ]
    for item in loop_items:
        add_bullet(doc, item)

    doc.save(GUIDE_PATH)


def add_slide_title_content(prs: Presentation, title_text: str):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title_text
    title_tf = slide.shapes.title.text_frame
    title_tf.paragraphs[0].font.size = PptPt(26)
    body = slide.placeholders[1].text_frame
    body.clear()
    body.word_wrap = True
    return slide, body


def add_bullet_paragraph(tf, text, level=0):
    p = tf.add_paragraph()
    p.text = text
    p.level = level
    p.font.size = PptPt(18 if level == 0 else 15)
    return p


def build_deck():
    prs = Presentation()
    prs.slide_width = PptInches(13.333)
    prs.slide_height = PptInches(7.5)

    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = 'LSAT Argumentative Writing Learning Module'
    title_slide.placeholders[1].text = 'Companion deck aligned to the app curriculum, drill system, and official timing rules.'

    for slide_data in slides:
        slide, body = add_slide_title_content(prs, slide_data['title'])
        first = body.paragraphs[0]
        first.text = f"Concept: {slide_data['concept']}"
        first.font.size = PptPt(18)
        add_bullet_paragraph(body, f"Formula: {slide_data['formula']}")
        add_bullet_paragraph(body, f"Example: {slide_data['example']}")
        add_bullet_paragraph(body, f"Drill prompt: {slide_data['drill']}")
        add_bullet_paragraph(body, f"What strong writers do: {slide_data['strong_note']}")

    prs.save(DECK_PATH)


def build_overview():
    lines = [
        '# LSAT Argumentative Writing Companion Asset Overview',
        '',
        'Generated assets:',
        f'- `{MODEL_PATH.name}`',
        f'- `{GUIDE_PATH.name}`',
        f'- `{DECK_PATH.name}`',
        f'- `{REFERENCE_LIBRARY_PATH.name}`',
        f'- `{MODULE_RESOURCE_MAP_PATH.name}`',
        f'- `{WEAKNESS_RESOURCE_MAP_PATH.name}`',
        '',
        '## Official timing rule',
        '- Official LSAT: **15 minutes prewriting + 35 minutes writing**',
        '- Extended training default: **23 / 53** (training or accommodation simulation only)',
        '',
        '## Module order',
    ]
    for module in modules:
        lines.append(f"- **{module['title']}** — {module['goal']}")
    lines += ['', '## Three-day sprint', '']
    for day in sprint_days:
        lines.append(f"### {day['day']}")
        lines.append(f"Focus: {day['focus']}")
        for output in day['must_outputs']:
            lines.append(f"- {output}")
        lines.append('')
    lines += ['## Study library groups', '']
    for group in sorted({item['group'] for item in reference_library}):
        lines.append(f"- **{group}**")
    lines += ['', '## Read-first study paths', '']
    for path in study_paths:
        lines.append(f"- **{path['title']}** — {path['summary']}")
    OVERVIEW_PATH.write_text('\n'.join(lines))


def build_reference_registry():
    registry = {
        'metadata': {
            'title': 'LSAT Writing Reference Library Registry',
            'generated_on': GENERATED_ON,
            'official_timing': {'prewrite_minutes': 15, 'writing_minutes': 35},
            'extended_training_default': {'prewrite_minutes': 23, 'writing_minutes': 53},
            'hybrid_mode': 'public app stays synthesized; local/mac app unlocks private reference library cards'
        },
        'resources': reference_library,
        'study_paths': study_paths
    }
    REFERENCE_LIBRARY_PATH.write_text(json.dumps(registry, indent=2))


def build_resource_maps():
    module_payload = {
        'metadata': {
            'generated_on': GENERATED_ON,
            'description': 'Maps curriculum modules to recommended resources.'
        },
        'module_resource_map': module_resource_map
    }
    weakness_payload = {
        'metadata': {
            'generated_on': GENERATED_ON,
            'description': 'Maps weakness categories to the strongest lesson/resource pair.'
        },
        'weakness_resource_map': weakness_resource_map
    }
    MODULE_RESOURCE_MAP_PATH.write_text(json.dumps(module_payload, indent=2))
    WEAKNESS_RESOURCE_MAP_PATH.write_text(json.dumps(weakness_payload, indent=2))


MODEL_PATH.write_text(json.dumps(payload, indent=2))
build_guide()
build_deck()
build_overview()
build_reference_registry()
build_resource_maps()
print(f'Wrote {MODEL_PATH}')
print(f'Wrote {GUIDE_PATH}')
print(f'Wrote {DECK_PATH}')
print(f'Wrote {OVERVIEW_PATH}')
print(f'Wrote {REFERENCE_LIBRARY_PATH}')
print(f'Wrote {MODULE_RESOURCE_MAP_PATH}')
print(f'Wrote {WEAKNESS_RESOURCE_MAP_PATH}')
