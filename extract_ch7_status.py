#!/usr/bin/env python3
"""
Extract comprehensive Ch7 RQ status information
"""
import os
import yaml
import re
from pathlib import Path

def extract_rq_status():
    """Extract status information from all Ch7 RQs"""
    
    results = []
    base_path = Path("/home/etai/projects/REMEMVR/results/ch7")
    
    # Get all RQ directories
    rq_dirs = [d for d in os.listdir(base_path) if d.startswith("7.") and "." in d[2:]]
    rq_dirs.sort(key=lambda x: tuple(map(int, x.split('.'))))
    
    for rq_dir in rq_dirs:
        rq_path = base_path / rq_dir
        status_file = rq_path / "status.yaml" 
        concept_file = rq_path / "docs" / "1_concept.md"
        stats_file = rq_path / "docs" / "1_stats.md"
        
        rq_info = {
            'id': rq_dir,
            'title': '',
            'score': 'N/A',
            'status': 'UNKNOWN',
            'warnings': [],
            'last_updated': 'N/A'
        }
        
        # Extract title from concept.md
        if concept_file.exists():
            try:
                with open(concept_file, 'r') as f:
                    content = f.read()
                    # Look for title in first few lines
                    lines = content.split('\n')[:10]
                    for line in lines:
                        if line.startswith('#') and rq_dir in line:
                            rq_info['title'] = line.replace('#', '').replace(rq_dir, '').strip(' -:')
                            break
                        elif ':' in line and rq_dir in line:
                            rq_info['title'] = line.split(':')[-1].strip()
                            break
            except:
                pass
        
        # Extract status and score from status.yaml
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    status_data = yaml.safe_load(f)
                    if status_data:
                        # Check for scores in rq_stats context_dump
                        if 'rq_stats' in status_data and 'context_dump' in status_data['rq_stats']:
                            context_dump = status_data['rq_stats']['context_dump']
                            # Look for score patterns like "8.2/10" or "9.4/10 APPROVED"
                            score_match = re.search(r'(\d+\.?\d*)/10', context_dump)
                            if score_match:
                                rq_info['score'] = f"{score_match.group(1)}/10"
                                
                                # Extract status from context
                                if 'APPROVED' in context_dump:
                                    rq_info['status'] = 'APPROVED'
                                elif 'CONDITIONAL' in context_dump:
                                    rq_info['status'] = 'CONDITIONAL'
                                elif 'REJECTED' in context_dump:
                                    rq_info['status'] = 'REJECTED'
                        
                        # Extract last updated from any agent that ran successfully
                        for agent in ['rq_stats', 'rq_concept', 'rq_scholar']:
                            if agent in status_data and 'status' in status_data[agent]:
                                if status_data[agent]['status'] == 'success':
                                    rq_info['last_updated'] = '2026-01-03'  # From recent assessment
                                    break
            except:
                pass
        
        # Extract score from stats.md if not found in status.yaml  
        if rq_info['score'] == 'N/A' and stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    content = f.read()
                    # Look for score patterns
                    score_patterns = [
                        r'Overall Score:\s*(\d+\.?\d*)/10',
                        r'Total Score:\s*(\d+\.?\d*)/10',
                        r'Final Score:\s*(\d+\.?\d*)',
                        r'Score:\s*(\d+\.?\d*)/10'
                    ]
                    for pattern in score_patterns:
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            rq_info['score'] = f"{match.group(1)}/10"
                            break
            except:
                pass
        
        results.append(rq_info)
    
    return results

if __name__ == "__main__":
    results = extract_rq_status()
    
    print("# Ch7 RQ Status Summary")
    print("=" * 80)
    print(f"{'RQ ID':<8} {'Title':<40} {'Score':<8} {'Status':<12} {'Warnings'}")
    print("-" * 80)
    
    approved_count = 0
    rejected_count = 0
    conditional_count = 0
    pending_count = 0
    
    for rq in results:
        # Determine status based on score if not explicit
        if rq['score'] != 'N/A':
            try:
                score_val = float(rq['score'].split('/')[0])
                if rq['status'] in ['UNKNOWN', 'pending'] or score_val >= 9.0:
                    if score_val >= 9.0:
                        rq['status'] = 'APPROVED'
                        approved_count += 1
                    elif score_val >= 8.5:
                        rq['status'] = 'CONDITIONAL'
                        conditional_count += 1
                    else:
                        rq['status'] = 'REJECTED'
                        rejected_count += 1
                else:
                    if rq['status'].upper() == 'APPROVED':
                        approved_count += 1
                    elif rq['status'].upper() in ['REJECTED', 'REJECT']:
                        rejected_count += 1
                    elif rq['status'].upper() in ['CONDITIONAL', 'PENDING']:
                        conditional_count += 1
                    else:
                        pending_count += 1
            except:
                pending_count += 1
        else:
            pending_count += 1
        
        warnings_str = ', '.join(rq['warnings'][:2]) if rq['warnings'] else ''
        if len(warnings_str) > 20:
            warnings_str = warnings_str[:17] + "..."
            
        print(f"{rq['id']:<8} {rq['title'][:38]:<40} {rq['score']:<8} {rq['status']:<12} {warnings_str}")
    
    print("=" * 80)
    print(f"SUMMARY: {approved_count} APPROVED | {conditional_count} CONDITIONAL | {rejected_count} REJECTED | {pending_count} PENDING")
    print(f"TOTAL: {len(results)} RQs")
    if len(results) > 0:
        print(f"APPROVAL RATE: {(approved_count/len(results)*100):.1f}%")