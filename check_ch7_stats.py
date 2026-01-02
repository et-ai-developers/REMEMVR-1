#!/usr/bin/env python3
import os
import re
import yaml

ch7_dir = "/home/etai/projects/REMEMVR/results/ch7"

# Collect all RQ stats scores
rq_scores = []
for rq_dir in sorted(os.listdir(ch7_dir)):
    if os.path.isdir(os.path.join(ch7_dir, rq_dir)):
        status_file = os.path.join(ch7_dir, rq_dir, "status.yaml")
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                content = f.read()
                # Find rq_stats context_dump
                match = re.search(r'rq_stats:.*?context_dump:.*?"([^"]+)"', content, re.DOTALL)
                if match:
                    dump = match.group(1)
                    # Extract score
                    score_match = re.search(r'(\d+\.\d+)/10', dump)
                    if score_match:
                        score = float(score_match.group(1))
                        status = "PASS" if score >= 9.0 else "FAIL"
                        rq_scores.append((rq_dir, score, status))

# Print summary
print("Ch7 RQ Stats Scores Summary:")
print("-" * 40)
total = len(rq_scores)
passed = sum(1 for _, _, status in rq_scores if status == "PASS")
failed = sum(1 for _, _, status in rq_scores if status == "FAIL")

print(f"Total RQs with stats scores: {total}")
print(f"PASSED (≥9.0): {passed}")
print(f"FAILED (<9.0): {failed}")
print()

print("Failed RQs that need fixing:")
for rq, score, status in rq_scores:
    if status == "FAIL":
        print(f"  {rq}: {score}/10")

print()
print("Passed RQs (ready for planning):")
for rq, score, status in rq_scores:
    if status == "PASS":
        print(f"  {rq}: {score}/10")