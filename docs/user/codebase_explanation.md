Here is my explanation of what the codebase is/does currently.

Part 1. Master.xlsx
ALL data that was collected as part of the experiemtn is saved in an excel document called @data/master.xlsx
This data is formatted with each row being a unique datapoint, and pair of columns for each participant.

The first column in the pair has the the participants UID label as the header.
The rows in this column are tags that identify what the data in second column refers to.
This second column is labeled with UID-D

UIDs for participant all start with A then a group number 01-10, and the an incremental counter.

The groups represent what age-bracket that participant belongs to.
A01 = 20-24
A02 = 25-29
...
A09 = 60-65
A10 = 65-70

Each age group has 10 participants in it.
So the participants in age group A01 have the following UIDs:
A010
A011
...
A018
A019

For the following examples of tag usage, I will be using participant A010 as an example, but this can be changed to any participant

The tags in the first column are built with a particular self-made schema and divided into topics
I.e., UID-TOPIC-...
The available topics are as follows
A010-DEM-... = Demographic Data.
A010-COG-... = Cognitive Test Data
A010-RVR-... = REMEMVR Data

Each participant completed four REMEMVR recall tests across 6 days.
The test day forms the next part of the tag sequence (T1, T2, T3, T4). I.e.,
A010-REM-T1-... would be the data collected from their first REMEMVR test.
A010-REM-T4-... would be the data collected from their last REMEMVR test.

Data that was only collected once on day 1 (like demographics and cognitive test scores) are marked with a X in the test number field. I.e.,
A010-DEM-X-... is the demographic data collected from participant A010.
A010-COG-X-... is the cognitive testing data collected from participant A010.

Here is how each topic is built using tags:

Demographic Data:
    General Demographic Info:
        A010-DEM-X-Age = 20-70 "What is your age in years?"
        A010-DEM-X-Sex = 0-3 "What was your assigned sex at birth?" [Female, Male, Other, Prefer not to say] (Note: All participants responded 0 or 1)
        A010-DEM-X-Education = 0-9 "What is your highest completed level of education?" = [High school (Year 9 or lower), High school (Year 10), High school (Year 12), Certificate 1 & 2, Certificate 3 & 4, Diploma / Advanced Diploma, Bachelor’s Degree, Graduate Certificate / Diploma, Master’s Degree, Doctoral Degree]
        A010-DEM-X-VR_Exp = 0-4 "How many hours have you used virtual reality in the past?" = [Never, Less than 1 hour, 1 – 10 hours, 10 – 50 hours, More than 50 hours]
        A010-DEM-X-SLEEP = 0-24 "How many hours do you typically sleep in a night?"
        A010-DEM-X-Tester = 0-1 Which researcher collected the data for this participant? [Jayce, Richard]
        
    
    Health Questionnaire: "Have you ever had any of the following?":
        A010-DEM-X-HQ1 = Yes/No "Had an adverse experience during virtual reality?"
        A010-DEM-X-HQ2 = Yes/No "Had a seizure (convulsion)?"
        A010-DEM-X-HQ3 = Yes/No "Had a stroke?"
        A010-DEM-X-HQ4 = Yes/No "Had a clinical electroencephalogram (EEG)?"
        A010-DEM-X-HQ5 = Yes/No "Had a serious head injury"
        A010-DEM-X-HQ6 = Yes/No "Had any illness that caused brain injury?"
        A010-DEM-X-HQ7 = Yes/No "Had any other brain related condition?"
        A010-DEM-X-HQ8 = Yes/No "Suffer from frequent or severe headaches?"
        A010-DEM-X-HQ9 = Yes/No "Are you taking any medications? (Including contraceptives)?"
        A010-DEM-X-HQTXT = Text "If you answered yes to any of the above, please provide details"
    
    Depression Stress Anxiety Scale (21 Questions):
        A010-DEM-X-DASS1 = 0-3
        A010-DEM-X-DASS2 = 0-3
        ...
        A010-DEM-X-DASS20 = 0-3
        A010-DEM-X-DASS21 = 0-3

        A010-DEM-X-DASS_Dep = Depression Items Total
        A010-DEM-X-DASS_Anx = Anxiety Items Total
        A010-DEM-X-DASS_Str = Stress Items Total

Cognitive Test Data:
    NART (National Adult Reading Test)
        A010-COG-X-NAR-Time = Test duration (s)
        A010-COG-X-NAR-Scor = NART Score 0-50
    
    RPM (Raven's Advanced Progressive Matrices)
        A010-COG-X-RPM-Time = Test duration (s)
        A010-COG-X-RPM-Scor = RPM Score 0-12

        Individual RPM Puzzle Choice
        A010-COG-X-RPM-Tr01 = 0-8 Which answer PX chose for puzzle one
        ...
        A010-COG-X-RPM-Tr12 = 0-8 Which answer PX chose for puzzle twelve

    BVMT-R (Brief Visuospatial Memory Test - Revised) (3 Immediate Recall Trials, 1 delayed recall trial, 1 recognition trial)
        A010-COG-X-BVM-T1Ti = Trial 1 duration (s)
        A010-COG-X-BVM-T1Sc = 0-12 Trial 1 score
        ...
        A010-COG-X-BVM-T3Ti = Trial 3 duration (s)
        A010-COG-X-BVM-T3Sc = 0-12 Trial 3 score

        A010-COG-X-BVM-TDTD = Delay period (s)
        A010-COG-X-BVM-TDTi = Delayed recall trial duration (s)
        A010-COG-X-BVM-TDSc = 0-12 Delayed recall trial score
        
        BVMT-R Computed Scores (These are calculated as per the BVMT-R instructions)
        A010-COG-X-BVM-TotR = Total Recall
        A010-COG-X-BVM-Lear = Learning
        A010-COG-X-BVM-PerR = Percent Retained
        A010-COG-X-BVM-ReHi = Recognition Hits
        A010-COG-X-BVM-ReFA = Recognition False Alarms
        A010-COG-X-BVM-ReDI = Recognition Discrimination Index
        A010-COG-X-BVM-ReRB = Recognition Response Bias
        
    RAVLT (Rey Auditory Verbal Learning Test) (5 Immediate Recall Trials (List A), a distraction trial (List B), a free recall trial (List A), and a delayed recall trial(List A))
        A010-COG-X-RAV-T1Ti = Trial 1 duration (s)
        A010-COG-X-RAV-T1Sc = 0-15 Trial 1 score
        ...
        A010-COG-X-RAV-T5Ti = Trial 5 duration (s)
        A010-COG-X-RAV-T5Sc = 0-15 Trial 5 score
        
        A010-COG-X-RAV-TDTi = Distraction Trial duration (s)
        A010-COG-X-RAV-TDSc = 0-15 Distraction score
        A010-COG-X-RAV-FRTi = Free recall trial duration (s)
        A010-COG-X-RAV-FRSc = 0-15 Free recall trial score
        A010-COG-X-RAV-DRDe = Delay period (s)
        A010-COG-X-RAV-DRTi = Delayed recall trial duration (s)
        A010-COG-X-RAV-DRSc = 0-15 Delayed recall trial score
        
        A010-COG-X-RAV-RXXA = 0-15 Recognition Hits
        A010-COG-X-RAV-RXSA = 0-15 Recognition False Alarms (List A, semantically similar)
        A010-COG-X-RAV-RXPA = 0-15 Recognition False Alarms (List A, phonetically similar)
        A010-COG-X-RAV-RSPA = 0-15 Recognition False Alarms (List A, semantically and phonetically similar)
        A010-COG-X-RAV-RXXB = 0-15 Recognition False Alarms (List B)
        A010-COG-X-RAV-RXSB = 0-15 Recognition False Alarms (List B, semantically similar)
        A010-COG-X-RAV-RXPB = 0-15 Recognition False Alarms (List B, phonetically similar)
        A010-COG-X-RAV-RSPB = 0-15 Recognition False Alarms (List B, semantically and phonetically similar)

REMEMVR Data:
    Tests:
        A010-RVR-T1-... = Data that relates to the 1st test taken by the participant
        A010-RVR-T2-... = Data that relates to the 2nd test taken by the participant
        A010-RVR-T3-... = Data that relates to the 3rd test taken by the participant
        A010-RVR-T4-... = Data that relates to the 4th test taken by the participant
    
    Rooms:
        A010-RVR-T1-BAT-... = This means the participant's 1st test was asking questions about the virtual bathroom
        A010-RVR-T1-BED-... = This means the participant's 1st test was asking questions about the virtual bedroom
        A010-RVR-T1-KIT-... = This means the participant's 1st test was asking questions about the virtual kitchen
        A010-RVR-T1-LIV-... = This means the participant's 1st test was asking questions about the virtual living-room

    Sections:
        SLP = Sleep Hygiene Questionnaire
        RFR = Room Free Recall
        IFR = Items Free Recall
        TCR = Task Cued Recall
        ICR = Items Cued Recall
        RRE = Room Recognition
        ICR = Item Recognition
        STR = Recall Strategies

    General (As the order of tests and vr room viewing was counterbalanced, these variables identify these orders):
        A010-RVR-X-VR1 = The 1st vr room seen [bat, bed, ket, liv]
        A010-RVR-X-VR2 = The 2nd vr room seen [bat, bed, ket, liv]
        A010-RVR-X-VR3 = The 3rd vr room seen [bat, bed, ket, liv]
        A010-RVR-X-VR4 = The 4th vr room seen [bat, bed, ket, liv]
        A010-RVR-T1-Room = What room the 1st test asks about [bat, bed, ket, liv]
        A010-RVR-T2-Room = What room the 2nd test asks about [bat, bed, ket, liv]
        A010-RVR-T3-Room = What room the 3rd test asks about [bat, bed, ket, liv]
        A010-RVR-T4-Room = What room the 4th test asks about [bat, bed, ket, liv]
    
    For the section examples, we will be using the data from participant A010. I.e.,
        A010-RVR-X-VR1 = bat
        A010-RVR-X-VR2 = bed
        A010-RVR-X-VR3 = liv
        A010-RVR-X-VR4 = kit
        A010-RVR-T1-Room = bat
        A010-RVR-T2-Room = bed
        A010-RVR-T3-Room = liv
        A010-RVR-T4-Room = kit
        
    General Stats (These are collected for T1, T2, T3 and T4. I will only show T1 for brevity):
        A010-RVR-T1-STA-X-Date = The date the participant took the test (days since 01/01/1904)
        A010-RVR-T1-STA-X-Time = The time they began that test as a percentage of 24 hours. I.e., 0.5 = 12pm
        A010-RVR-T1-STA-X-TSLt = Hours since their last test
        A010-RVR-T1-STA-X-TSVR = Hours since they saw the room in VR
        A010-RVR-T1-STA-X-TiPS-RFR = Time taken to complete the RFR section (s)
        A010-RVR-T1-STA-X-TiPS-IFR = Time taken to complete the IFR section (s)
        A010-RVR-T1-STA-X-TiPS-TCR = Time taken to complete the TCR section (s)
        A010-RVR-T1-STA-X-TiPS-ICR = Time taken to complete the ICR section (s)
        A010-RVR-T1-STA-X-TiPS-RRE = Time taken to complete the RRE section (s)
        A010-RVR-T1-STA-X-TiPS-IRE = Time taken to complete the IRE section (s)
    
    Sleep Hygiene (T1, T2, T3, T4):
        A010-RVR-T1-SLP-X-AWAK- = How long the participant has been awake that day as a percentage of 24 hours
        A010-RVR-T1-SLP-X-HOUR- = How many hours sleep the participant had the night before
        A010-RVR-T1-SLP-X-WAKE- = What time the participant woke up as a percentage of 24 hours
        A010-RVR-T1-SLP-X-QUAL- = -1 - 1 "How would you rate the quality of your sleep last night compared to a typical night's sleep?" [Much Worse, Slightly Worse, About the same, Slightly Better, Much better]
        A010-RVR-T1-SLP-X-TIRE- = -1 - 1 "How tired do you feel right now?" [Very tired, slightly tired, not tired or energised, slikghtly energised, very energised]
        A010-RVR-T1-SLP-X-CAF1- 0-1 "Have you consumed any caffeine or stimulants in the last six hours?" [no, yes]
        A010-RVR-T1-SLP-X-CAF2- Text "Which stimulant and how many servings?"
        A010-RVR-T1-SLP-X-TOX1- 0-1 "Have you consumed any intoxicating substances in the last six hours?" [no, yes]
        A010-RVR-T1-SLP-X-TOX2- Text "Which substance and how many servings?"
        A010-RVR-T1-SLP-X-HLP1- 0-1 "Is anyone helping you complete this questionnaire?" [no, yes]
        A010-RVR-T1-SLP-X-HLP2- Text "What is your relationship to this person?"

    For the following sections: 
        Answer or confidence? 
            We have end flags of either ...-ANS for the score for that question (0-1) or ...-CON which is their confidence rating for that question (0-1)

        Domains:
            We use domain flags to idenfify which domain is being asked about
            ...-N-... is What questions
            ...-L-... is Where questions for static objects
            ...-U-... is Where questions for where an item was picked up
            ...-D-... is Where questions for where an item was put down
            ...-O-... is When questions for the order in which this item/task was done (1st, 2nd etc)

        Item specific tags
            Each room had 6 items to be interacted with.
            ...-i1CM-... = Common item
            ...-i2CM-... = Common item
            ...-i3CG-... = Congruent item
            ...-i4CG-... = Congruent item
            ...-i5IN-... = Incongruent item
            ...-i6IN-... = Incongruent item

            Each item also has a second tag that identifies more granular item properties.
            ...-n*s**f**-...
            n is the order that item was interacted with. I.e., n1 means that item was picked up 1st
            s is the starting position, so* means it started outside the room, si* means it started inside the room
                Outside the room the item could either be on pillar 1, 2, 3, or 4
                Inside the room the item could either be in corner A, B, C, or D
            f is the finishing position and works the same as s
            Examples:
                ...-n2siCfiD-... means that item was the 2nd item to be picked up (n2), it started inside in corner C (siC), and finished inside in corner D (fiD)
                ...-n6so3fiB-... means that item was the 6th item to be picked up (n6), it started outside on pillar 4 (so3), and finished inside in corner B (fiB)

    Room Free Recall -RFR- (T1, T2, T3, T4):
        ...-OBJ1-... = The largest furniture item [-N-/-L-]
        ...-OBJ2-... = The 2nd largest furniture item [-N-/-L-]
        ...-OBJ3-... = The 3rd largest furniture item [-N-/-L-]
        ...-OBJ4-... = The 4th largest furniture item [-N-/-L-]
        ...-STRA-... = A large strange object that was placed in the room [-N-/-L-]
        ...-LAND-... = The picture of the landscape in the room [-N-/-L-]
        ...-PORT-... = The picture of the portrait in the room [-N-/-L-]
        ...-RORD-... = The order in which they saw this vr room [-O-]
        ...-TMOD-... = The time of day it was in the vr room [-O-]
        ...-WEAT-... = The weather outside of the vr room [-N-]
        ...-DOOR-... = The location of the doors in the room [-L-]
        ...-WIND-... = The location of the windows in the room [-L-]
      
    Item Free Recall -IFR- (T1, T2, T3, T4):
        ...-i1CM-... = What an item from that room was, where it was picked up/put down, and what order it was interacted with [-N-/-U-/-D-/-O-]
        ...-i2CM-... = Same
        ...-i3CG-... = Same
        ...-i4CG-... = Same
        ...-i5IN-... = Same
        ...-i6IN-... = Same

    Task Cued Recall -TCR- (T1, T2, T3, T4):
        ...-TSK1-... = The order they performed this task [-O-]
        ...-TSK2-... = Same
        ...-TSK3-... = Same
        ...-TSK4-... = Same
        ...-TSK5-... = Same
        ...-TSK6-... = Same

    Item Cued Recall -ICR- (T1, T2, T3, T4):
        Same as IFR

    Room Recognition -RRE- (T1, T2, T3, T4): (-N- questions are recognition, the -L- questions are still cued recall)
        ...-DOOR-... = The location of doors in the room [-L-]
        ...-WIND-... = The location of windows in the room [-L-]
        ...-STRA-... = A large strange object that was placed in the room [-N-/-L-]
        ...-LAND-... = The picture of the landscape in the room [-N-/-L-]
        ...-PORT-... = The picture of the portrait in the room [-N-/-L-]
    
    Item Recognition (T1, T2, T3, T4):
        Same as IFR and ICR

    Strategy (T1, T2, T3, T4):
        A010-RVR-T1-STR-X-DIF1- = -1 - 1 "How difficult was your REMEMVR test today?" [very difficult, difficult, moderare, easy, very easy]
        A010-RVR-T1-STR-X-DIF2- = -1 - 1 "How difficult was today's test compared to your previous REMEMVR test?" [very difficult, difficult, moderare, easy, very easy]
        A010-RVR-T1-STR-X-HLP1- = Text "Did completing previous REMEMVR tests help you answer questions about the bedroom?" [Yes, No, Unsure]
        A010-RVR-T1-STR-X-HLP2- = Text "Briefly describe how previous tests helped you answer questions about the bedroom"
        A010-RVR-T1-STR-X-TNK1- = -1 - 1 "How often have you thought about the bedroom since you saw it in virtual reality?" [Never, Once or twice in total, at least once per day, a few times per day, many times per day]
        A010-RVR-T1-STR-X-TNK2- = Text "Since your virtual experience in the bedroom, what kind of elements have you thought about?"
        A010-RVR-T1-STR-X-OBJ1- = Text "Did you use any specific strategies or techniques to remember the furniture/fixtures in the bedroom?"
        A010-RVR-T1-STR-X-ITM1- = Text "Did you use any specific strategies or techniques to remember the items and their locations in the bedroom?"
        A010-RVR-T1-STR-X-MNE1- "Were you aware of any mnemonic techniques (e.g., method of loci, visual imagery) before participating in this study?"
        A010-RVR-T1-STR-X-MNE2- "Did you consciously apply any of these mnemonic techniques during the REMEMVR test?"
        A010-RVR-T1-STR-X-MNE3- "Describe your technique here"
        A010-RVR-T1-STR-X-FEED- "(Optional) Please provide any thoughts, comments, or suggestions related to REMEMVR that you would like to share with the research team."
        
This concludes the section on how data is stored and how their associated tags in the left adjacent cell identifies what the data means.
This is not an exhaustive list but it captures the key variables needed for this analysis.

Part 2. Variables.xlsx
This spreadsheet is how the codebase computes variables for analysis.
It has multiple sheets but only looks at the one called 'variables'.
It has 5 columns:
    Name = The column name I want this variable to have in dfData
    Label = The label I want associated with this variable
    Function = How I want the set to be combined
        sum: add the datapoints up
        mean: calculate the mean
        string: keep it as a string
    Type = What type of data is this?
        dem: demographic data (1 timepoint)
        cog: cognitive testing data (1 timepoint)
        vr: REMEMVR data (4 timepoints)
    Regex = The regex I want to apply to the lists of tags to collect the relevant datapoints per participant and then run the function on.

Currently there are 480 rows as I just kept making new variables as I explored my data and never deleted old variables.

General Files:

    data/data.py
        This is the file that uses master.xlsx and variables.xlsx to create a dfData dataframe to be used for analysis
        To save on iteration time, it looks to see if there are any cached versions of the dataframes that can be loaded much quicker into memory.
        When I change/add variables, I delete data/cache/dfVariables.csv and data/cache/dfData.csv so the program knows to recompute the variables and recreate the cache

    cog/cogtests.py 
        This is used to compare the participant's cognitive test scores against normative data that I have collected.
        This part of the code was built by a research assistant (Jayce) so I'm not 100% sure how it works or if it works correctly.

    tools.py
        This contains some tools that I use to clean/prepare the data

    params.py
        This is where I set up the parameters for various irt analyses I wanted to run.

    irt.py
        This uses params.py to prepare and run various item response theory analyses using the deepirtools library and multi-GPU acceleration

    analysis.py
        This uses the results generated by irt.py to conduct various LMM analyses.

    plots.py
        This is used to create various plots for different types of data

    perplexity.py and perplixity2.py
        This is some code I was using to try and metricise contextual congruence using LLM perplexity instead of just binning items into common, congruent, incongruent.

    del_images.py
        This is a tool I used sometimes to delete certain types of files from the analysis

How I was storing results:

    For irt analyses, I stored the outputs in results/
    These stored various types of information based on the parameters set in params for each analysis.

For LMM results, I stored these in analysis/ and used the same/similar schema as the irt results.


This concludes what the codebase CURRENTLY IS DOING.

REFACTOR INSTRUCTIONS (what I WANT it to do instead):

Currently, the codebase is quite messy. I want to overhaul how it works.
My thesis has three empirical chapters, each with various research questions to be answered.
See thesis/chapters.md and for a more detailed look, see thesis/analyses/ANALYSES_CH5.md thesis/analyses/ANALYSES_CH6.md thesis/analyses/ANALYSES_CH7.md

RESULTS
    We are going to use a schema for running each research question and storing the results.
    It goes as follows:
        results/ This will be the main folder that houses all the results.
        results/ch5/ results/ch6/ results/ch7/ These are the folders for the results for each chapter's RQs
        results/ch5/rq1/ results/ch5/rq2/ ... Each research question will be given its own folder.
        Each folder will have the following:
            info.md All the necessary theoretical/statistical info about the what/how/why of this analysis. A detailed summary of the results, and a scholarly answer to the research question.
            data/input.csv All the data needed to run this analysis
            data/output_1.csv The output after running the 1st step of the analysis
            data/output_n.csv The output after running the nth step of the analysis etc...
            data/output.csv The final output that contains the final results of the analysis
            code/run.py This is the code that runs all the steps of the analysis by calling on various tools from the analysis suite sequentially. It is built by an analysis agent based on the information in its context window about the tools suite and the info.md
            code/terminal.log This is a copy of the terminal session that was generated when the analysis was run by the analysis-executor-agent
            plots/ A folder that contains any generated plots for this analysis. Note, each plot will have an associated csv file so the plot can easily be generated again with a different colourscheme/labels

ANALYSIS TOOLS
    This will be a suite of tools that can run each step of analysis, from the input.csv, through each output_n.csv step, and finally to output.csv
    Instead of the current method of running lots of different analyses in bulk, we will run each RQ's analysis one at a time, one step at a time.
    Changing from bulk to sequence is the best way to make sure that each analysis is 100% bonafide correct and perfect.
    Importanly, each tool in the suite will have a verbose description of how it works such that it can be read by a statistics expert agent.

SUB-AGENTS
    Once the codebase us up and running, the analyses will be run by claude code, employing various agents to ensure it is working correctly.
    We will need the following agents:

    Data-Prep sub-agent:
        Name: data-prep-agent
        Context: Deep knowledge of how master.xlsx and data.py works as well as a full understanding of how UIDs and their data tags work. 
        Master: The main claude code agent.
        TODO: It is given a research question (i.e., results/ch5/rq1) and performs the following tasks in sequential order.
            1. Read info.md
            2. Confirm it understands what data is needed and in what format.
            3. Prepare the necessary regexes for master.xlsx extraction.
            4. Use data.py to export a correctly formatted data/input.csv into the RQ's folder.
            5. Confirm the input.csv is in the correct format.
            6. Update info.md to describe what data has been prepared and how its formatted.
            7. Report back to master and quit.
        Errors: If any steps fail, it reports back what went wrong to the master and quits

    Analysis execution sub-agent:
        Name: analysis-executor-agent
        Context: Deep knowledge of the statistical tools suite, general context of what the PhD is about.
        MCPs: tmux
        Master: The main claude code agent.
        TODO: It is given a research question (i.e., results/ch5/rq1) and performs the following tasks in sequential order.
            1. Read info.md
            2. Confirm it knows what analyses to run, what tools to call, how to call them etc.
            3. Confirm the input data has been prepared correctly
            4. Start a tmux session via the tmux mcp for the analysis so all terminal output can be recorded to file.
            5a. Run each step of the analysis, with each step outputting as data/output_n.csv (nth step)
            5b. Between each step, read the output and make sure there is nothing wrong with it.
            6. Save the final output to data/output.csv
            7. Dump the full terminal output from the tmux session to code/terminal.log
            8. Kill the tmux session
            9. Update the info.md to describe what analyses were run and what the raw results for each step were
            10. Report back to master and quit
        Errors: If any steps fail, it reports back what went wrong to the master and quits

    Results inspector sub-agent:
        Name: results-inspector-agent
        Context: Deep knowledge of the statistical tools suite, indepth context of what the PhD motivation and methodology, and a know what the results schema is supposed to look like.
        MCPs: Context7
        Tools: Web search
        Master: The main claude code agent
        TODO: It is given a research question (i.e., results/ch5/rq1) and performs the following tasks in sequential order.
            1. Read info.md
            2. Confirm it knows what analyses were done and why they were done
            3. Read the output files and terminal log.
            4. Play devils advocate to make sure we can GUARANTEE that the results are 100% statisically valid.
            5. Ensure the results are all beautifully formatted and perfectly aligned with the results schema.
            6. Update the info.md with an exquisitly formatted inspection report and scholarly answer to the research question that could be copy/pasted directly into the PhD thesis.
            7. Report back to master and quit
        Errors: If any steps fail, it reports back what went wrong to the master and quits

    Thesis manager sub-agent:
        Name: thesis-mamager-agent
        Context: Is told to read the LATEST version of the PhD thesis (cloned thesis files), a general context of the results schema
        Master: The main claude code agent
        TODO: It is given a list of research questions (i.e., [results/ch5/rq1, results/ch5/rq2]) and performs the following tasks in sequential order.
            1. Read all the relevant info.mds
            2. Confirms it understands the results of those info.mds, their significance to the thesis.
            3. Lists which parts of the thesis need to be modified based on what's these results say
            4. Modify each cloned chapter based on what it thinks needs to be added/removed/edited
            5. Appends to a thesis changelog that records which parts of the thesis have been changed and how.
            6. Append to each relevant info.md to log that these results have been added to the thesis.
            7. Report back to master and quit
        Errors: If any steps fail, it reports back what went wrong to the master and quits
        
    Code debugger sub-agent:
        Name: debug-agent
        Context: This agent uses context7 mcp and other tools/web searches to deeply understand how code works. Its job is to fix bugs that are identified in the code. These bugs are usually discovered by other agents trying to do things.
        MCPs: Context7, web search.
        
    Plot maker agent:
        Name: plot-maker-agent
        Context: This agent is given a list of RQs and then creates/modifies the plots based on certain colourscheme/parameter/label information.

    Statistics expert sub-agent:
        Name: stats-expert-agent
        Context: This agent is what we use to deeply research and consider various statistical analyses that have been run. It is what prevents this entire codebase from outputting nonsense results or using inappropriate statistical methodology
        


