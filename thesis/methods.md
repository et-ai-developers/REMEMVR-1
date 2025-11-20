1	INTRODUCTION
 
2	METHOD
This chapter gives an overview of the final methodology used for data collection. The rationale and process behind designing and refining this method can be found in Chapter 3. The placement of this chapter prior to the explanation of design rationale is intended to give the reader a general understanding of the task as a whole before undertaking a more granular exploration of the decision-making process that resulted in the methodology presented in this chapter. Furthermore, due to the complexity of the data analysis pipeline, I have included the statistical methodology and rationale as its own chapter (Chapter 4).
2.1	PARTICIPANTS
One hundred healthy adults aged 20–70 years participated in this study. Participants were stratified into ten 5-year age bands (20–24, 25–29, ..., 65–70), with ten individuals recruited per group. Recruitment was conducted via multiple sources, including The University of Queensland’s psychology research participation pool, Facebook advertisements, physical flyers posted in local community spaces, and word of mouth. (See Appendix X for examples of advertising materials)
Eligibility screening was conducted via the study website prior to enrolment (https://rememvr.com.au). Participants confirmed that they (1) belonged to an available age group, (2) had no current or previously diagnosed cognitive or neurological impairments, (3) had no significant uncorrected visual or auditory impairments, (4) had not previously experienced discomfort while using virtual reality technology, and (5) were physically capable of ascending stairs to access the virtual reality testing laboratory. Participants were compensated $100 AUD upon full completion of the study via direct bank transfer, with prorated payments offered for participants who withdrew prior to the completion of their participation.
A total of five participants withdrew or were excluded. Two participants withdrew voluntarily due to external personal circumstances unrelated to the experiment. Three participants were excluded after answering "I don’t know" for the majority of text-based responses and reporting no confidence for almost all test items for one or more follow up recall tasks. These results were determined to be the result of insufficient effort in recalling test answers rather actual poor episodic memory ability due to the significantly shorter time taken to complete tests compared to other participants and were therefore removed. These participant removals were performed during data collection and were replaced with new participants to maintain a full cohort of ten participants per age group.
The final sample included both Australian and international participants. All participants demonstrated sufficient English fluency and cultural familiarity to the virtual environments such that they could complete all tasks without confounding performance due to any cultural or language barriers.
The study received ethical approval from The University of Queensland Human Research Ethics Committee (ethics reference: 2022/HE001298). Informed consent was obtained prior to participation. Participants were debriefed following study completion. Copies of the participant information sheet, consent forms, and ethics application can be found in appendices X, X, and X respectively.
2.2	APPARATUS AND MATERIALS
2.2.1	Virtual Reality Hardware and Environment
All aspects of the VR task were designed, developed, and built entirely by myself with no third-party technical support. The VR app was built using Unity software (Unity version 2021.2.17f1) running on a Lenovo ThinkPad P14s with a Windows 11 operating system. The VR experience was delivered using an Oculus Quest Pro headset (firmware version 50837850062000150, software build 64.0) and used custom software to integrate Oculus’ native hand tracking functionality into the application. This allowed participants to interact with the virtual environment using their own hands, thus eliminating the need for handheld controllers. This reduced technological demands for participants, particularly for those unfamiliar with VR or with a general apprehension towards learning unfamiliar technology.
The VR task was performed in an 8×5 metre open space dedicated to VR experiments at the Queensland Brain Institute. Virtual movement was mapped 1:1 to real-world walking and head movements to prevent VR sickness associated with artificial locomotion methods (e.g., teleportation or joystick control). The physical space was unobstructed, and padded flooring was installed to reduce the risk of injury due to participants losing their balance. Oculus’ boundary detection system was activated to provide visual warnings if participants approached room edges; however, the VR scenes were designed to fit well within these physical boundaries, preventing any collisions. A supervising experimenter was present throughout all VR sessions, and no participants reported nausea, disorientation, or discomfort during VR use.
2.2.2	REMEMVR Stimulus Design
The REMEMVR task involved participant encoding of four virtual household environments (bathroom, kitchen, bedroom, and living room), chosen for their cross-cultural familiarity and ease of construction within resource constraints. Room layouts followed strict design rules to ensure equal memorability across rooms. Each room was designed such that it contained the following:
-	One unique wall and floor texture per room
-	A door and one or two windows (with unique exterior weather/environmental conditions)
-	Four large furniture or fixture items positioned in each corner of the room
-	A large, static, incongruent "bizarre" object (e.g., fire axe, car tyre)
-	Two wall-mounted pictures (one landscape, one portrait), generated via AI for standardisation
-	A visible clock indicating time of day
-	An adjacent ‘no-context’ room connected by an open doorway
Each room contained six interactable items: two congruent, two incongruent, and two semantically neutral (“common”) objects. Congruent items were items one would associate with that room (Toothbrushes in the bathroom). Incongruent items were items one would not expect to find in that room (A battery drill in the living room). Common items were items one would not associate with a particular room, but their presence would not be unexpected (A mobile phone in the bedroom). A full list of items can be found in Appendix X.
Object placement followed a fixed structure to balance memory load across rooms but also counterbalanced between rooms to prevent the emergence of any memorable patterns. Some items were initially located in a separate "no-context" room (3×3 metres), which contained four numbered pillars as placement locations. Item movements also followed counterbalanced placement rules to ensure equal exposure across object categories and spatial transitions while minimising semantic overlap between items and identifiable patterns of movement between rooms.
All stimulus programming, object modelling, counterbalancing, and scripting were developed entirely by myself. No third-party technical support was involved in any phase of the experiment’s design, construction, or execution. All software is available for download at the study’s GitHub repository (https://github.com/rememvr).
2.2.3	Cognitive Testing Materials
In addition to the virtual REMEMVR encoding and recall task, participants completed a battery of neuropsychological testing during their first laboratory visit. All cognitive tests were administered on paper following standard protocols and scoring rubrics:
-	Rey Auditory Verbal Learning Test (RAVLT): Trials 1–8 with immediate and delayed free recall, interference list, and recognition components (Appendix X).
-	Brief Visuospatial Memory Test – Revised (BVMT-R): Trials 1–4, including delayed recall and recognition (Appendix X).
-	National Adult Reading Test (NART): Single-session reading of irregularly spelled words (Appendix X).
-	Raven’s Advanced Progressive Matrices (Short Form, 12 items): Timed visual reasoning task (Appendix X).
Cognitive assessments were conducted either by myself or a trained research assistant after having been trained and deemed competent by Professor Gail Robinson, Head of Neuropsychology at UQ. Participants were permitted to ask clarification questions consistent with each test’s instructions. No adaptations were made for non-native English speakers.
2.2.4	Online Memory Test Platform
Participant recruitment and all post-VR memory testing was conducted via a website I built (https://REMEMVR.com.au) using WordPress and Formidable Forms, a popular online survey plugin. Prospective recruits were directed to the study website via hyperlinks provided in digital advertising materials, or via a QR code in physical advertising materials. Here individuals could read a description of the study, confirm they met all eligibility requirements, and choose a time/day to participate. Upon registration, participants provided their name, email address, phone number, and age. Participant’s personally identifiable information was stored in a securely encrypted spreadsheet.
To complete the four follow-up memory tasks, participants could log in via the study’s participant portal using their email address as a username and their year of birth as the password. Here, participants could click on that day’s prescribed test to begin the recall task. Individual test sections were implemented as discrete online forms, with responses to each section automatically sent to a secure Google Sheets document at the completion of that section. Data were redundantly stored both on the server and in cloud-based spreadsheets. Automated reminders were sent via SMS to each participant on the day prior to their scheduled appointment, and on each scheduled testing day to remind participants to complete that day’s test. Section timing data were logged automatically, although participants were free to complete each section at their own pace. A full copy of all website pages, including recruitment, instructions, and test questions is available in Appendix X.
2.3	PROCEDURE
The following subsections are provided in chronological order.
2.3.1	Initial Laboratory Session
Upon arrival at the Queensland Brain Institute, participants were fully briefed and signed informed consent documents (see Appendix X). They then completed the fixed cognitive battery described above in the following order: 
1.	Rey Auditory Verbal Learning Test (Trials 1-7)
2.	Brief Visuospatial Memory Test - Revised (Trials 1-3)
3.	Virtual Reality Tutorial
4.	National Adult Reading Test
5.	Raven’s Advanced Progressive Matrices
6.	Rey Auditory Verbal Learning Test (Trial 8 and Recognition)
7.	Brief Visuospatial Memory Test - Revised (Trial 4 and Recognition)
All data collected during cognitive testing was physically recorded on a custom designed scoring matrix (See Appendix X). The VR tutorial mentioned above placed participants in a blank virtual room that matched the size and layout of the household rooms. Participants were given ten minutes to familiarise themselves with hand tracking, object pickup and placement, and general VR operation/navigation. Participants could ask questions or request guidance during this tutorial phase. All participants successfully learned the interaction/exploration mechanics without difficulty.
2.3.2	REMEMVR Encoding Task
Participants next completed the REMEMVR encoding task under strict experimenter supervision. Each participant experienced four distinct virtual rooms in a Latin square counterbalanced order, stratified within each age group such that each group had an equal balancing of room/test ordering. Each room session lasted approximately 10 minutes, separated by 5-minute breaks. The full encoding phase took approximately 60 minutes.
At the start of each room, participants were given one minute to freely explore the room environment. Thereafter, the experimenter delivered a fully scripted sequence of verbal instructions unique to each room (See Appendix X). These scripts guided participants through a mixture of observation tasks (e.g., describing paintings, counting doors/windows) and interactive tasks (e.g., picking up, describing, and relocating items). Although the task sequence varied between rooms, all participants completed the same tasks in the same order. Participants could not deviate from the scripted instructions.
The experimenter remained physically present throughout encoding sessions but provided no assistance beyond reading or repeating the scripted instructions. Each room included ambient environmental sounds that were delivered via the headset’s external speakers. Finally, the time taken for each participant to complete each task in each room was physically recorded using the previously mentioned scoring matrix.
2.3.3	Memory Testing Schedule
Memory assessments were administered across four time points:
-	Test 1: Immediately after VR encoding (Day 0, onsite)
-	Test 2: One day later (Day 1, remote)
-	Test 3: Three days later (Day 3, remote)
-	Test 4: Six days later (Day 6, remote)
Each follow-up test targeted one of the four VR rooms, assigned via Latin square counterbalancing. The first test always corresponded to the first room viewed, ensuring equivalent initial delay lengths across participants. Later test orders were counterbalanced to minimise order effects while respecting the temporal structure of the forgetting curve.
Each test contained eight fixed-order sections:
1.	Sleep Hygiene
2.	Room Details Free Recall
3.	Item Details Free Recall
4.	Task Order Cued Recall
5.	Item Cued Recall
6.	Room Recognition
7.	Item Recognition
8.	Memory Strategy Questionnaire
Test instructions were provided at the start of each online session. Once a section was completed, participants could not return to previous sections to view or amend previous answers. Participants could not submit a test section until all items had been answered. They were free to complete tests at their own pace, with completion times automatically recorded for each section. All test questions for each room can be found in Appendix X.
2.3.4	Memory Test Section Content
Sleep Hygiene
This section collected self-reported information related to participant sleep on the night prior to the test. Questions included:
-	Total hours slept the night before
-	Time of waking that day
-	Subjective sleep quality (Likert scale)
-	Fatigue level at time of testing (Likert scale)
-	Use of any intoxicants in the last six hours
Room Details Free Recall
Participants were asked to freely recall and describe features of the room environment they had explored during encoding with no provided cues. 
Questions included:
-	Which order they viewed this room in the context of the four rooms
-	Descriptions of furniture and fixture items and their location
-	Descriptions of the two paintings (portrait and landscape) and their location
-	Descriptions of the unique environmental features such as weather, lighting, and time of day
Item Details Free Recall
Participants were asked to list the six items they interacted with in the room in a free-recall paradigm, the location they picked them up, the location they put them down, and the ordinality of interaction with each item.
Observational Task Order
Participants were asked to indicate the order they completed the seven observational tasks in the room.
Item Verbal Recognition
Participants were shown a schematic diagram of the room that only identified the layout of the walls, which was identical for all rooms, and provided arbitrary labels for spatial locations. The question format was the same as Item Details Free Recall but could select the item from a list of eight multi-choice options, where there was one correct answer and seven semantically similar foils. They then reported where they picked up and put down each item using the labels from the diagram and again reported item interaction ordinality.
Room Visual Recognition
Here participants first were given a similar room layout schematic from the previous section that focused on sections of walls. They were asked to recall the locations of windows, doors, paintings, and strange objects. Following this, participants were shown six images of portraits, landscapes, and strange objects, where one was the correct answer and five were visually similar foils.
Item Visual Recognition
In this section, participants were shown a screenshot of the actual room and adjoining no-context room without any items present. They were then shown six pictures of items and asked to select which item they remember interacting with, where there was one correct answer and five visually similar foils. They also had to identify the closest furniture/fixture where they picked the item up, and put the item down, as well as identify the ordinality of interaction with items.
Memory Strategy Questionnaire
At the end of each test, participants answered a series of questions concerning their subjective experience and memory strategies employed. Questions included:
-	Task difficulty (absolute and relative to prior tests)
-	Whether previous tests helped them recall the current room
-	How frequently they had thought about the room since encoding
-	Self-reported memory strategies for recalling furniture, fixtures, items, locations, and item orders
-	Awareness or application of mnemonic techniques (e.g., method of loci, narrative construction, visual imagery)
-	Open-ended comments or suggestions for the research team
2.3.5	Confidence Ratings
Each test item in actual recollection sections (2-7) required participants to rate how confident they are in their answer using a Likert-style five-star rating (similar to those used in online reviews). Participants were given a diagram on each test page to remind them of the Likert-scale options. Those being:
1.	Guess / No Memory
2.	Not Sure
3.	Mildly Confident
4.	Very Confident
5.	Absolutely Certain
2.3.6	Ancillary Data
At the completion of the first test, participants were asked to complete a demographics questionnaire. This was conducted via a dedicated form on the study website and collected information such as the participant’s age, highest education, previous VR exposure, several health questions, and a 21 item Depression Anxiety and Stress Scale (DASS) questionnaire.
Furthermore, when each test section was completed and synchronized with Google Sheets, a timestamp was included. This allowed a measurement of how much time was spend completing each test section, and the time of day each test was completed.
2.3.7	Scoring and Data Handling
Free-text responses were manually scored by myself following strict pre-specified scoring rules (See Appendix X). Free-text responses were only required to be one or two words in length, allowing misspellings and alternative language terms to be accepted if the response was conceptually correct. Multi-choice responses were automatically scored via a custom formulaic algorithm in Google Sheets. Correct answers were scored with a value of 1, and incorrect answers were scored with a value of 0. Partial score values of 0.5 or 0.25 were given for spatial and ordinal questions according to the following rules:
-	If a participant answered with a spatial location that was located directly adjacent to the correct answer, this was given a score of 0.5
-	If a participant answered with an ordinal answer that was once removed from the correct answer, this was given a score of 0.5
-	If a participant answered with an ordinal answer that was twice removed from the correct answer, this was given a score of 0.25
It’s important to note that partial scores were set to zero for some aspects of statistical analysis due to the mathematical constraints inherent in dichotomous item response theory. This caveat is reiterated where appropriate in Chapter 4.
All data points were individually tagged using an automated custom alphanumeric encoding schema I designed to associate relevant properties of each data point such that data could be temporarily grouped based on any number of characteristics. This labelling system is discussed in more detail in 4.X.X. In total, 1854 unique data points were collected per participant. Each participant’s data was exported from Google Sheets into a master Excel file that could be easily imported into Python for statistical analysis.
Confidence ratings were rescaled to a continuous 0–1 metric. Likert response biases (e.g., participants who only selected extreme or narrow confidence bands) were identified and corrected prior to inclusion in formal Bayesian modelling analyses. Likert response bias correction methodology is discussed in 4.X.X. No data imputation procedures were applied; all questions were compulsory, and no missing responses occurred.
2.3.8	Pilot Testing and Protocol Refinement
Twenty pilot participants across the full age range were tested prior to formal data collection. Pilot results led to substantial refinements, including:
-	Reduction of total rooms from six to four
-	Reduction of items per room from eight to six
-	Simplification and restructuring of certain question formats
-	Improved verbal instructions to reduce participant anxiety and cognitive load
No pilot participants were included in the final sample. Pilot data were extensively analysed to calibrate final task difficulty and structure.
2.3.9	Risk Mitigation and Participant Safety
The entire REMEMVR design prioritised participant safety and comfort by ensuring the following conditions were met:
-	All participants were pre-screened via self-report for susceptibility to VR sickness.
-	1:1 real-world mapped movement eliminated vestibular mismatches associated with VR locomotion.
-	The experimenter was present for all in-person sessions to provide immediate assistance if required.
-	Padded flooring was installed to the VR space to reduce potential injuries in case of a participant falling over.
No participants reported any adverse events, nausea, or safety concerns at any point during their participation.
2.3.10	Ethical Oversight
This study was approved by The University of Queensland Human Research Ethics Committee (ethics reference: 2022/HE001298). Informed consent was obtained prior to participation. Participants were thoroughly briefed that the task was designed to be difficult, and high scores were neither expected nor indicative of poor memory performance. No adverse events were recorded throughout the study period. Ethical oversight during data collection was maintained in accordance with institutional guidelines.
