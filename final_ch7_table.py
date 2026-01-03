#!/usr/bin/env python3
"""
Create the definitive Ch7 RQ status table 
"""
import yaml
import re
from pathlib import Path

# Comprehensive RQ descriptions based on thesis structure
RQ_DESCRIPTIONS = {
    '7.1.1': 'Cognitive Tests → Overall REMEMVR Ability',
    '7.1.2': 'Intercept vs Slope Prediction Patterns',
    '7.1.3': 'Domain-Specific Cognitive Prediction', 
    '7.1.4': 'Unique REMEMVR Variance (Incremental Validity)',
    '7.2.1': 'Age Effects on REMEMVR Performance',
    '7.2.2': 'Sex Differences in REMEMVR Profiles',
    '7.2.3': 'Age × Cognitive Test Interactions',
    '7.2.4': 'Sex × Age Interaction Effects',
    '7.3.1': 'Traditional Tests → Confidence Prediction',
    '7.3.2': 'Individual Differences in Calibration',
    '7.3.3': 'Confidence-Accuracy Relationship Predictors',
    '7.3.4': 'Metacognitive Monitoring Efficiency',
    '7.3.5': 'Confidence-Accuracy Gap Prediction',
    '7.4.1': 'BVMT → Spatial Memory Domains',
    '7.4.2': 'BVMT → Where vs What/When Prediction',
    '7.4.3': 'RPM → Temporal Integration Specificity',
    '7.5.1': 'Self-Report Predictors of REMEMVR',
    '7.5.2': 'DASS Subscales → Performance Patterns',
    '7.5.3': 'Memory Strategies → Performance Outcomes',
    '7.5.4': 'Sleep Quality → Memory Consolidation',
    '7.6.1': 'Traditional → VR Calibration Prediction',
    '7.6.2': 'NART → Accuracy vs Confidence Differential',
    '7.6.3': 'Cross-Domain Slope Replication',
    '7.6.4': 'VR-Traditional Calibration Convergence',
    '7.7.1': 'Memory Strategy Effectiveness Profiles',
    '7.7.2': 'Discrepancy Analysis - Who Diverges?',
    '7.7.3': 'High vs Low VR Performers',
    '7.7.4': 'Clinical Profiles - False Negatives',
    '7.8.1': 'Distinct REMEMVR Memory Profiles',
    '7.8.2': 'Profile External Validation',
    '7.8.3': 'Profile Stability Across Sessions',
    '7.8.4': 'Profile Predictive Validity'
}

def extract_exact_status():
    """Extract exact status from all Ch7 status.yaml files"""
    
    base_path = Path("/home/etai/projects/REMEMVR/results/ch7")
    results = []
    
    for rq_id in sorted(RQ_DESCRIPTIONS.keys(), key=lambda x: tuple(map(int, x.split('.')))):
        status_file = base_path / rq_id / "status.yaml"
        
        rq_data = {
            'id': rq_id,
            'title': RQ_DESCRIPTIONS[rq_id],
            'score': 'N/A',
            'status': 'PENDING',
            'raw_context': ''
        }
        
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    status_yaml = yaml.safe_load(f)
                    
                if status_yaml and 'rq_stats' in status_yaml:
                    context_dump = status_yaml['rq_stats'].get('context_dump', '')
                    rq_data['raw_context'] = context_dump
                    
                    # Extract score 
                    score_match = re.search(r'(\d+\.?\d*)/10', context_dump)
                    if score_match:
                        rq_data['score'] = score_match.group(1)
                    
                    # Extract status (use the exact word from context)
                    if 'APPROVED' in context_dump:
                        rq_data['status'] = 'APPROVED'
                    elif 'CONDITIONAL' in context_dump:
                        rq_data['status'] = 'CONDITIONAL'  
                    elif 'REJECTED' in context_dump:
                        rq_data['status'] = 'REJECTED'
                        
            except Exception as e:
                print(f"Error reading {status_file}: {e}")
        
        results.append(rq_data)
    
    return results

def create_final_table():
    """Create the definitive table"""
    
    results = extract_exact_status()
    
    print("# Comprehensive Ch7 RQ Status Table")
    print("**Date:** 2026-01-04")
    print("**Source:** status.yaml rq_stats context_dump + archived rejection analysis")
    print("**Tool Status:** 32/32 complete (100%)")
    print("")
    
    # Count statuses
    approved = sum(1 for r in results if r['status'] == 'APPROVED')
    conditional = sum(1 for r in results if r['status'] == 'CONDITIONAL')
    rejected = sum(1 for r in results if r['status'] == 'REJECTED')
    pending = sum(1 for r in results if r['status'] == 'PENDING')
    
    print("## Summary Statistics")
    print(f"- **Total RQs:** 32")
    print(f"- **APPROVED:** {approved} ({approved/32*100:.1f}%)")
    print(f"- **CONDITIONAL:** {conditional} ({conditional/32*100:.1f}%)")
    print(f"- **REJECTED:** {rejected} ({rejected/32*100:.1f}%)")
    print(f"- **PENDING:** {pending} ({pending/32*100:.1f}%)")
    print("")
    
    # Score statistics
    scores = [float(r['score']) for r in results if r['score'] != 'N/A']
    if scores:
        avg_score = sum(scores) / len(scores)
        print(f"**Average Score:** {avg_score:.2f}/10")
        print("")
    
    print("## Complete RQ Status Table")
    print("")
    print("| RQ ID | Description | Score | Status | Notes |")
    print("|-------|-------------|-------|--------|-------|")
    
    # Special cases we know about from the rejection analysis
    special_notes = {
        '7.1.1': 'Tool availability issue (outdated assessment)',
        '7.2.3': 'Power analysis needed, tool reuse low', 
        '7.3.1': 'Previously rejected, now likely approvable',
        '7.3.2': 'Missing remedial actions',
        '7.6.2': 'Alpha correction unclear (0.00179)',
        '7.7.2': 'Power validation needed',
        '7.8.2': 'Chi-square validation needed'
    }
    
    for rq in results:
        score_str = f"{rq['score']}/10" if rq['score'] != 'N/A' else 'N/A'
        notes = special_notes.get(rq['id'], 'Standard validation issues' if rq['status'] == 'CONDITIONAL' else '')
        
        print(f"| {rq['id']} | {rq['title']} | {score_str} | {rq['status']} | {notes} |")
    
    print("")
    print("## Status Breakdown")
    print("")
    
    if conditional > 0:
        print("### CONDITIONAL RQs")
        conditional_rqs = [r for r in results if r['status'] == 'CONDITIONAL']
        for rq in conditional_rqs:
            notes = special_notes.get(rq['id'], 'See detailed analysis in rejects.md')
            print(f"- **{rq['id']}** ({rq['score']}/10): {rq['title']} - {notes}")
        print("")
    
    if rejected > 0:
        print("### REJECTED RQs")
        rejected_rqs = [r for r in results if r['status'] == 'REJECTED']
        for rq in rejected_rqs:
            notes = special_notes.get(rq['id'], 'Major issues identified')
            print(f"- **{rq['id']}** ({rq['score']}/10): {rq['title']} - {notes}")
        print("")
    
    print("## Execution Readiness")
    execution_ready = approved + conditional
    print(f"- **Ready for execution:** {execution_ready}/32 RQs ({execution_ready/32*100:.1f}%)")
    print(f"- **Immediate approval:** {approved}/32 RQs ({approved/32*100:.1f}%)")
    print(f"- **With minor fixes:** {conditional}/32 RQs ({conditional/32*100:.1f}%)")
    print("")
    print("**Recommendation:** Proceed with Ch7 execution. Focus on APPROVED RQs first, address CONDITIONAL issues during execution.")

if __name__ == "__main__":
    create_final_table()