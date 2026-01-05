# REMEMVR Data Dictionary

**Last Updated:** 2026-01-05
**Purpose:** Comprehensive reference for all variables in dfnonvr.csv and dfvr.csv
**Usage:** Reference this document when selecting variables for Ch7 analyses

---

## 📁 data/dfnonvr.csv
**Description:** Participant-level non-VR data (cognitive tests, demographics, questionnaires)
**Shape:** 100 participants × 235 columns
**Structure:** Wide format (one row per participant)

### Participant Identifier
| Column | Description |
|--------|-------------|
| `UID` | Unique participant identifier (e.g., A010, B023) |

### Cognitive Tests - NART
| Column | Description | Range |
|--------|-------------|-------|
| `nart-time` | Time taken to complete NART (seconds) | Varies |
| `nart-score` | National Adult Reading Test score | 0-50 |

### Cognitive Tests - RPM (Raven's Progressive Matrices)
| Column | Description | Range |
|--------|-------------|-------|
| `rpm-time` | Time taken to complete RPM (seconds) | Varies |
| `rpm-score` | Total RPM score | 0-12 |
| `rpm-tr01-answer` through `rpm-tr12-answer` | Individual item responses for RPM items 1-12 | Varies |

### Cognitive Tests - BVMT (Brief Visuospatial Memory Test)
| Column | Description | Range |
|--------|-------------|-------|
| `bvmt-form-number` | Which form of BVMT was used | 1-6 |
| `bvmt-trial-1-time` | Time for trial 1 (seconds) | Varies |
| `bvmt-trial-1-score` | Trial 1 score | 0-12 |
| `bvmt-trial-2-time` | Time for trial 2 (seconds) | Varies |
| `bvmt-trial-2-score` | Trial 2 score | 0-12 |
| `bvmt-trial-3-time` | Time for trial 3 (seconds) | Varies |
| `bvmt-trial-3-score` | Trial 3 score | 0-12 |
| `bvmt-delayed-recall-delay-period` | Delay before recall (minutes) | ~20-30 |
| `bvmt-delayed-recall-time` | Time for delayed recall (seconds) | Varies |
| `bvmt-delayed-recall-score` | Delayed recall score | 0-12 |
| `bvmt-total-recall` | Sum of trials 1-3 | 0-36 |
| `bvmt-learning` | Learning score (trial 3 - trial 1) | -12 to 12 |
| `bvmt-percent-retained` | % retained (delayed/trial 3 × 100) | 0-100+ |
| `bvmt-recognition-hits` | Recognition hits | 0-6 |
| `bvmt-recognition-falsealarms` | Recognition false alarms | 0-6 |
| `bvmt-recognition-discrimination-index` | Recognition discrimination | Varies |
| `bvmt-recognition-response-bias` | Recognition response bias | Varies |

### Cognitive Tests - RAVLT (Rey Auditory Verbal Learning Test)
| Column | Description | Range |
|--------|-------------|-------|
| `ravlt-trial-1-time` through `ravlt-trial-5-time` | Time for trials 1-5 (seconds) | Varies |
| `ravlt-trial-1-score` through `ravlt-trial-5-score` | Scores for learning trials 1-5 | 0-15 each |
| `ravlt-distraction-trial-time` | Time for List B (seconds) | Varies |
| `ravlt-distraction-trial-score` | List B (distraction) score | 0-15 |
| `ravlt-free-recall-time` | Time for immediate recall (seconds) | Varies |
| `ravlt-free-recall-score` | Immediate free recall score | 0-15 |
| `ravlt-delayed-recall-delay-period` | Delay before recall (minutes) | ~20-30 |
| `ravlt-delayed-recall-time` | Time for delayed recall (seconds) | Varies |
| `ravlt-delayed-recall-score` | Delayed recall score | 0-15 |
| `ravlt-recognition-hits-` | Recognition hits | 0-15 |
| `ravlt-recognition-semantic-misses` | Semantic false positives | Varies |
| `ravlt-recognition-phonetic-misses` | Phonetic false positives | Varies |
| `ravlt-recognition-semantic-phonetic-misses` | Combined semantic+phonetic errors | Varies |
| `ravlt-recognition-distraction-misses` | List B intrusions | Varies |
| `ravlt-recognition-distract-phonetic-misses` | List B phonetic errors | Varies |
| `ravlt-recognition-distract-semantic-misses` | List B semantic errors | Varies |
| `ravlt-recognition-distract-smenaitc-and-pohonetic-misses` | Combined List B errors (note typo in column name) | Varies |

### REMEMVR Task Durations (seconds)
All columns follow pattern: `rememvr-[room]-task-[01-12]-duration`

**Rooms:** bathroom, bedroom, kitchen, livingroom
**Tasks:** 01-12 for each room
**Total:** 48 duration columns (4 rooms × 12 tasks)
**Range:** Typically 5-300 seconds per task

Example columns:
- `rememvr-bathroom-task-01-duration` through `rememvr-bathroom-task-12-duration`
- `rememvr-bedroom-task-01-duration` through `rememvr-bedroom-task-12-duration`
- `rememvr-kitchen-task-01-duration` through `rememvr-kitchen-task-12-duration`
- `rememvr-livingroom-task-01-duration` through `rememvr-livingroom-task-12-duration`

### RAVLT Word Recall Order
Columns 108-227: Individual word recall order for each trial
Pattern: `ravlt-trial-[1-8]-word-[1-15]-(word)-order`

**Trials:** 1-5 (learning), 6 (free recall), 7 (delayed recall), 8 (recognition?)
**Words:** drum, curtain, bell, coffee, school, parent, moon, garden, hat, farmer, nose, turkey, color, house, river
**Values:** Order in which word was recalled (1=first, 15=last, missing=not recalled)

### Demographics
| Column | Description | Values/Range |
|--------|-------------|--------------|
| `age` | Age in years | 18-80 |
| `sex` | Biological sex | 0=female, 1=male |
| `education` | Education level | 1-10 (ordinal scale) |
| `vr-exposure` | Prior VR experience | 0=Never, 1=<1hr, 2=1-10hrs, 3=10-50hrs, 4=>50hrs |
| `typical-sleep-hours` | Usual hours of sleep per night | 4-12 |

### DASS-21 Subscales
| Column | Description | Range |
|--------|-------------|-------|
| `total-dass-anxiety-items` | DASS-21 Anxiety subscale total | 0-21 |
| `total-dass-stress-items` | DASS-21 Stress subscale total | 0-21 |
| `total-dass-depression-items` | DASS-21 Depression subscale total | 0-21 |

---

## 📁 data/dfvr.csv
**Description:** VR episodic memory test data (repeated measures)
**Shape:** 400 rows (100 participants × 4 tests) × 244 columns
**Structure:** Long format (one row per test session)

### Identifiers
| Column | Description | Values |
|--------|-------------|--------|
| `UID` | Participant identifier | Same as dfnonvr.csv |
| `TEST` | Test session number | 1=immediate, 2=1day, 3=1week, 4=4weeks |

### Test Question (TQ) Columns - Accuracy Data
**Naming Convention:** `TQ_[paradigm]-[domain]-[item]`

**Paradigms:**
- `RFR` = Room Free Recall (recall room features without cues)
- `IFR` = Items Free Recall (recall 6 interactive objects without cues)
- `TCR` = Task Cued Recall (recall order of 6 observational tasks with spatial diagram)
- `ICR` = Items Cued Recall (recall items with multichoice + spatial diagram)
- `RRE` = Room Recognition (recognize room features from visual options)
- `IRE` = Items Recognition (recognize items from photos with spatial locations)

**Domains:**
- `N` = Name/What (object identity)
- `L` = Location/Where (spatial location of NON-interactive objects like furniture, doors, windows)
- `O` = Order/When (temporal sequence)
- `U` = Up/Pick-up location (where interactive item was picked up from)
- `D` = Down/Put-down location (where interactive item was placed)

**Items for RFR/RRE (Room features):**
- `OBJ1-4` = Four largest furniture items in room
- `STRA` = Large strange object
- `PORT` = Portrait painting
- `LAND` = Landscape painting
- `DOOR` = Location of doors
- `WIND` = Location of windows
- `WEAT` = Weather outside
- `RORD` = Order this room was viewed (1st, 2nd, 3rd, or 4th)
- `TMOD` = Time of day in VR

**Items for IFR/ICR/IRE (Interactive objects):**
- `i1CM, i2CM` = Common items (e.g., book, mobile phone, keys)
- `i3CG, i4CG` = Congruent items (e.g., toothbrush in bathroom, frying pan in kitchen)
- `i5IN, i6IN` = Incongruent items (e.g., hammer in bathroom, motor oil in bedroom)

**Items for TCR (Tasks):**
- `TSK1-6` = Six observational tasks performed in the room

### Test Confidence (TC) Columns - Confidence Ratings
**Naming Convention:** `TC_[paradigm]-[domain]-[item]`
- Same structure as TQ columns but for confidence ratings
- Values: Confidence scale (likely 1-100 or 1-10)

### Time Since VR Exposure
| Column | Description | Range |
|--------|-------------|-------|
| `TSVR` | Time since VR exposure (hours) | 0-672 |

### Test Completion Times
| Column | Description | Range |
|--------|-------------|-------|
| `seconds-taken-to-complete-rfr` | Time for RFR paradigm (seconds) | Varies |
| `seconds-taken-to-complete-ifr` | Time for IFR paradigm (seconds) | Varies |
| `seconds-taken-to-complete-tcr` | Time for TCR paradigm (seconds) | Varies |
| `seconds-taken-to-complete-icr` | Time for ICR paradigm (seconds) | Varies |
| `seconds-taken-to-complete-rre` | Time for RRE paradigm (seconds) | Varies |
| `seconds-taken-to-complete-ire` | Time for IRE paradigm (seconds) | Varies |

### Sleep and State Variables
| Column | Description | Range/Values |
|--------|-------------|--------------|
| `time-been-awake-today` | Hours awake before test | 0-24 |
| `hours-slept-night-before` | Sleep hours before test | 0-12 |
| `time-woke-up` | Wake time | Time format |
| `sleep-quality--1=bad-1=good` | Sleep quality rating | -1 to 1 |
| `tiredness--1=tired-1=alert` | Alertness rating | -1 to 1 |

### Substance Use
| Column | Description | Values |
|--------|-------------|--------|
| `consumed-stimulants` | Used stimulants before test | Yes/No |
| `what-stimulants` | Which stimulants | Text |
| `consumed-intoxicants` | Used intoxicants before test | Yes/No |
| `what-intoxicants` | Which intoxicants | Text |

### Test Administration
| Column | Description | Values |
|--------|-------------|--------|
| `anyone-helping-you` | Had assistance during test | Yes/No |
| `who-is-helping` | Who provided assistance | Text |

### Strategy Questions
| Column | Description |
|--------|-------------|
| `strategy-1` | How difficult was your REMEMVR test today? |
| `strategy-2` | How difficult was today's test compared to your previous REMEMVR test? |
| `strategy-3` | Did completing previous REMEMVR tests help you answer questions about the [room]? |
| `strategy-4` | Briefly describe how previous tests helped you answer questions about the [room] |
| `strategy-5` | How often have you thought about the [room] since you saw it in virtual reality? |
| `strategy-6` | When you thought about your virtual experience in the [room], what kind of elements did you think about? |
| `strategy-7` | Did you use any specific strategies or techniques to remember the furniture/fixtures in the [room]? |
| `strategy-8` | Describe your strategy here |
| `strategy-9` | Did you use any specific strategies or techniques to remember the items and their locations in the [room]? |
| `strategy-10` | Describe your strategy here |
| `strategy-11` | Were you aware of any mnemonic techniques (e.g., method of loci, visual imagery) before participating in this study? |
| `strategy-12` | Did you consciously apply any of these mnemonic techniques during the REMEMVR test? |
| `strategy-13` | Describe your technique here |
| `strategy-14` | (Optional) Please provide any thoughts, comments, or suggestions related to REMEMVR that you would like to share with the research team |

---

## Important Notes for Ch7 Analyses

### 1. Data Availability
- ✅ ALL DASS subscales now available (Depression, Anxiety, Stress)
- ✅ VR exposure data available as `vr-exposure` in dfnonvr.csv
- ✅ Sleep data available as `typical-sleep-hours` in dfnonvr.csv
- ✅ All cognitive test scores available with detailed trial-level data

### 2. Missing Data
- NART has 3 missing values (participants who couldn't complete)
- Some RAVLT timing data may have missing values
- Check for missing values before analysis

### 3. Variable Naming Conventions
- All column names use lowercase with hyphens (e.g., `total-dass-anxiety-items`)
- No spaces in column names
- Consistent naming patterns for repeated measures

### 4. Test-Retest Structure
- dfvr.csv uses long format with TEST column (1-4)
- Each participant has 4 rows in dfvr.csv
- Link dfnonvr and dfvr using UID column

### 5. Derived Variables to Compute
- RAVLT total: Sum of trials 1-5 scores
- RAVLT learning: Trial 5 - Trial 1
- RAVLT retention: Delayed recall / Trial 5
- BVMT already has computed totals and learning scores

### 6. For Ch7 RQ Analyses
- Use this dictionary to find exact column names
- Never create simulated data - all required data exists
- Check for typos in column names (e.g., "smenaitc" instead of "semantic")
- Reference exact column names from this dictionary in all code

---

**End of Data Dictionary**