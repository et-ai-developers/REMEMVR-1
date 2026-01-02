#!/usr/bin/env python3
"""
Fix Ch7 status.yaml files to match rq_builder format
"""

from pathlib import Path

# Base directory for results
BASE_DIR = Path("/home/etai/projects/REMEMVR/results/ch7")

# All 28 Ch7 RQs
RQS = [
    "7.1.1", "7.1.2", "7.1.3", "7.1.4",
    "7.2.1", "7.2.2", "7.2.3", "7.2.4",
    "7.3.1", "7.3.2", "7.3.3", "7.3.4", "7.3.5",
    "7.4.1", "7.4.2", "7.4.3",
    "7.5.1", "7.5.2", "7.5.3", "7.5.4",
    "7.6.1", "7.6.2", "7.6.3", "7.6.4",
    "7.7.1", "7.7.2", "7.7.3", "7.7.4",
    "7.8.1", "7.8.2", "7.8.3", "7.8.4"
]

def create_proper_status_yaml(rq_id: str):
    """Create proper status.yaml matching rq_builder format"""
    
    status_content = f'''rq_id: "ch7/{rq_id}"

rq_builder:
  status: success
  context_dump: |
    Created results/ch7/{rq_id}/ with 6 folders
    Folders: docs/, data/, code/, logs/, plots/, results/
    All folders empty, ready for agents
    status.yaml initialized with 10 RQ-specific agents
    Next: rq_concept extracts concept from specs

rq_concept:
  status: pending
  context_dump: ""

rq_scholar:
  status: pending
  context_dump: ""

rq_stats:
  status: pending
  context_dump: ""

rq_planner:
  status: pending
  context_dump: ""

rq_tools:
  status: pending
  context_dump: ""

rq_analysis:
  status: pending
  context_dump: ""

rq_inspect:
  status: pending
  context_dump: ""

rq_plots:
  status: pending
  context_dump: ""

rq_results:
  status: pending
  context_dump: ""

analysis_steps:
  # To be populated during execution

rq_platinum:
  status: pending
  context_dump: ""
'''
    
    status_file = BASE_DIR / rq_id / "status.yaml"
    with open(status_file, "w") as f:
        f.write(status_content)
    
    print(f"✓ Fixed status.yaml for RQ {rq_id}")
    return status_file

def main():
    print(f"Fixing Ch7 status.yaml files in {BASE_DIR}")
    print("-" * 50)
    
    for rq in RQS:
        create_proper_status_yaml(rq)
    
    print("-" * 50)
    print(f"✓ Successfully fixed {len(RQS)} status.yaml files")
    print("\nStatus.yaml format now matches rq_builder standard:")
    print("- rq_id header")
    print("- Agent statuses (rq_builder through rq_platinum)")
    print("- analysis_steps section")
    print("\nReady for rq_concept execution")

if __name__ == "__main__":
    main()