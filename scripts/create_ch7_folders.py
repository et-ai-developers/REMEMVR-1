#!/usr/bin/env python3
"""
Create Ch7 RQ folder structure for all 28 RQs
Mimics rq_builder behavior to prepare for rq_concept execution
"""

import os
from pathlib import Path

# Base directory for results
BASE_DIR = Path("/home/etai/projects/REMEMVR/results/ch7")

# All 28 Ch7 RQs from specs.md
RQS = [
    # Theme 1: Predictive Validity (Core)
    "7.1.1", "7.1.2", "7.1.3", "7.1.4",
    
    # Theme 2: Age x VR Scaffolding
    "7.2.1", "7.2.2", "7.2.3", "7.2.4",
    
    # Theme 3: Metacognition Predictors
    "7.3.1", "7.3.2", "7.3.3", "7.3.4", "7.3.5",
    
    # Theme 4: Process-Specific Prediction
    "7.4.1", "7.4.2", "7.4.3",
    
    # Theme 5: Self-Report & Contextual
    "7.5.1", "7.5.2", "7.5.3", "7.5.4",
    
    # Theme 6: Individual Differences in Forgetting
    "7.6.1", "7.6.2", "7.6.3", "7.6.4",
    
    # Theme 7: Clinical Utility & Alternative Interpretation
    "7.7.1", "7.7.2", "7.7.3", "7.7.4",
    
    # Theme 8: Latent Profiles & Models
    "7.8.1", "7.8.2", "7.8.3", "7.8.4"
]

def create_rq_structure(rq_id: str):
    """Create standard RQ folder structure"""
    rq_dir = BASE_DIR / rq_id
    
    # Create main RQ directory
    rq_dir.mkdir(parents=True, exist_ok=True)
    
    # Create standard subdirectories
    subdirs = ["data", "plots", "output", "notebooks"]
    for subdir in subdirs:
        (rq_dir / subdir).mkdir(exist_ok=True)
    
    # Create placeholder files that rq_concept expects
    # 1_concept.md will be created by rq_concept
    # 2_plan.md will be created by rq_planner
    # 3_tools.yaml will be created by rq_tools
    # 4_analysis.yaml will be created by rq_analysis
    
    # Create a README to track status
    readme_content = f"""# RQ {rq_id}

## Status
- [ ] 1_concept.md created (rq_concept)
- [ ] 2_plan.md created (rq_planner)  
- [ ] 3_tools.yaml created (rq_tools)
- [ ] 4_analysis.yaml created (rq_analysis)
- [ ] Analysis executed
- [ ] Report generated (rq_report)

## Workflow
1. Run: rq_concept ch7/{rq_id}
2. Run: rq_planner ch7/{rq_id}
3. Run: rq_tools ch7/{rq_id}
4. Run: rq_analysis ch7/{rq_id}
5. Execute analysis pipeline
6. Run: rq_report ch7/{rq_id}
"""
    
    with open(rq_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✓ Created structure for RQ {rq_id}")
    return rq_dir

def main():
    print(f"Creating Ch7 RQ folder structures in {BASE_DIR}")
    print(f"Total RQs to create: {len(RQS)}")
    print("-" * 50)
    
    # Ensure base Ch7 directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create each RQ structure
    created = []
    for rq in RQS:
        rq_dir = create_rq_structure(rq)
        created.append(rq_dir)
    
    print("-" * 50)
    print(f"✓ Successfully created {len(created)} RQ folder structures")
    print("\nFolder structure per RQ:")
    print("  └── [RQ_ID]/")
    print("      ├── README.md (status tracking)")
    print("      ├── data/")
    print("      ├── plots/")
    print("      ├── output/")
    print("      └── notebooks/")
    print("\nNext step: Run rq_concept for each RQ")
    print("Example: Use Task tool with rq_concept agent for ch7/7.1.1")

if __name__ == "__main__":
    main()