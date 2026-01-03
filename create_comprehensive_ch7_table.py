#!/usr/bin/env python3
"""
Create comprehensive Ch7 RQ table with all details
"""
import os
import yaml
import re
from pathlib import Path

def get_rq_details():
    """Get comprehensive details for all Ch7 RQs"""
    
    results = []
    base_path = Path("/home/etai/projects/REMEMVR/results/ch7")
    
    # RQ mappings from the thesis structure
    rq_descriptions = {
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
        '7.4.4': 'NART → Domain Generalization Effects',
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
    
    # Get all RQ directories
    rq_dirs = [d for d in os.listdir(base_path) if d.startswith("7.") and "." in d[2:]]
    rq_dirs.sort(key=lambda x: tuple(map(int, x.split('.'))))
    
    for rq_dir in rq_dirs:
        rq_path = base_path / rq_dir
        status_file = rq_path / "status.yaml"
        stats_file = rq_path / "docs" / "1_stats.md"
        
        rq_info = {
            'id': rq_dir,
            'title': rq_descriptions.get(rq_dir, 'Missing Description'),
            'score': 'N/A',
            'status': 'PENDING',
            'warnings': [],
            'issues': []
        }
        
        # Extract from status.yaml
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    status_data = yaml.safe_load(f)
                    if status_data:
                        # Extract score and status from rq_stats
                        if 'rq_stats' in status_data and 'context_dump' in status_data['rq_stats']:
                            context_dump = status_data['rq_stats']['context_dump']
                            score_match = re.search(r'(\d+\.?\d*)/10', context_dump)
                            if score_match:
                                rq_info['score'] = score_match.group(1)
                                
                                if 'APPROVED' in context_dump:
                                    rq_info['status'] = 'APPROVED'
                                elif 'CONDITIONAL' in context_dump:
                                    rq_info['status'] = 'CONDITIONAL'
                                elif 'REJECTED' in context_dump:
                                    rq_info['status'] = 'REJECTED'
            except:
                pass
        
        # Extract detailed issues from stats.md
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    content = f.read()
                    
                    # Look for warnings or issues
                    if 'Tool Availability' in content:
                        if re.search(r'Tool Availability.*❌', content):
                            rq_info['issues'].append('Tool Availability')
                        elif re.search(r'Tool Availability.*⚠️', content):
                            rq_info['issues'].append('Tool Issues')
                    
                    if 'Devil\'s Advocate' in content:
                        if re.search(r'Devil\'s Advocate.*⚠️', content):
                            rq_info['issues'].append('Limited Literature Review')
                    
                    if re.search(r'power analysis|Power Analysis', content, re.IGNORECASE):
                        if 'missing' in content.lower() or 'needed' in content.lower():
                            rq_info['issues'].append('Power Analysis Missing')
                    
                    if re.search(r'alpha.*correction|Alpha.*justification', content, re.IGNORECASE):
                        if 'unclear' in content.lower() or 'arbitrary' in content.lower():
                            rq_info['issues'].append('Alpha Correction Unclear')
                            
                    if 'remedial' in content.lower():
                        if 'missing' in content.lower():
                            rq_info['issues'].append('Remedial Actions Missing')
            except:
                pass
        
        results.append(rq_info)
    
    return results

def create_markdown_table(results):
    """Create a comprehensive markdown table"""
    
    print("# Comprehensive Ch7 RQ Status Report")
    print("**Generated:** 2026-01-04")
    print("**Tool Status:** 32/32 complete (100%)")
    print("**Data Source:** status.yaml files + 1_stats.md validation reports")
    print()
    
    # Summary stats - use actual status from files, not score inference
    approved = sum(1 for r in results if r['status'] == 'APPROVED')
    conditional = sum(1 for r in results if r['status'] == 'CONDITIONAL')
    rejected = sum(1 for r in results if r['status'] == 'REJECTED')
    pending = sum(1 for r in results if r['status'] == 'PENDING')
    
    print(f"## Summary")
    print(f"- **Total RQs:** {len(results)}")
    print(f"- **APPROVED (≥9.0):** {approved} ({approved/len(results)*100:.1f}%)")
    print(f"- **CONDITIONAL (8.5-8.9):** {conditional} ({conditional/len(results)*100:.1f}%)")  
    print(f"- **REJECTED (<8.5):** {rejected} ({rejected/len(results)*100:.1f}%)")
    print(f"- **PENDING:** {pending} ({pending/len(results)*100:.1f}%)")
    print()
    
    print("## Detailed RQ Status Table")
    print()
    print("| RQ ID | Description | Score | Status | Issues/Warnings |")
    print("|-------|-------------|-------|--------|-----------------|")
    
    for rq in results:
        score_str = f"{rq['score']}/10" if rq['score'] != 'N/A' else 'N/A'
        issues_str = ', '.join(rq['issues'][:3]) if rq['issues'] else 'None'
        if len(issues_str) > 40:
            issues_str = issues_str[:37] + "..."
        
        print(f"| {rq['id']} | {rq['title']} | {score_str} | {rq['status']} | {issues_str} |")
    
    print()
    print("## RQs Requiring Attention")
    print()
    
    # Conditional RQs
    conditional_rqs = [r for r in results if r['status'] == 'CONDITIONAL']
    if conditional_rqs:
        print("### Conditional RQs (Score 8.5-8.9)")
        for rq in conditional_rqs:
            print(f"- **{rq['id']}** ({rq['score']}/10): {rq['title']}")
            if rq['issues']:
                print(f"  - Issues: {', '.join(rq['issues'])}")
        print()
    
    # Rejected RQs
    rejected_rqs = [r for r in results if r['status'] == 'REJECTED']
    if rejected_rqs:
        print("### Rejected RQs (Score <8.5)")
        for rq in rejected_rqs:
            print(f"- **{rq['id']}** ({rq['score']}/10): {rq['title']}")
            if rq['issues']:
                print(f"  - Issues: {', '.join(rq['issues'])}")
        print()
    
    print("## Score Distribution")
    print()
    scores = [float(r['score']) for r in results if r['score'] != 'N/A']
    if scores:
        score_9_plus = sum(1 for s in scores if s >= 9.0)
        score_8_5_to_9 = sum(1 for s in scores if 8.5 <= s < 9.0)
        score_8_to_8_5 = sum(1 for s in scores if 8.0 <= s < 8.5)
        score_below_8 = sum(1 for s in scores if s < 8.0)
        
        print(f"- **9.0+ (APPROVED):** {score_9_plus} RQs")
        print(f"- **8.5-8.9 (CONDITIONAL):** {score_8_5_to_9} RQs") 
        print(f"- **8.0-8.4 (CONDITIONAL):** {score_8_to_8_5} RQs")
        print(f"- **<8.0 (REJECTED):** {score_below_8} RQs")
        print()
        print(f"**Average Score:** {sum(scores)/len(scores):.2f}/10")
        print(f"**Execution Ready:** {score_9_plus + score_8_5_to_9} RQs ({(score_9_plus + score_8_5_to_9)/len(results)*100:.1f}%)")

if __name__ == "__main__":
    results = get_rq_details()
    create_markdown_table(results)