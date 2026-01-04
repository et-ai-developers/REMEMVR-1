#!/usr/bin/env python3
"""
Extract comprehensive status information for all Ch7 RQs.
Collects validation scores, plan status, tool status, and analysis status.
"""

import os
import re
import yaml
import glob
from pathlib import Path

def extract_rq_info_from_concept(concept_file):
    """Extract RQ text from concept file"""
    try:
        with open(concept_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for RQ definition patterns
        patterns = [
            r'RQ\s+[\d\.]+:\s*(.+?)(?:\n\n|\n[A-Z]|\nType:|$)',
            r'Research Question:\s*(.+?)(?:\n\n|\n[A-Z]|\nType:|$)',
            r'Question:\s*(.+?)(?:\n\n|\n[A-Z]|\nType:|$)',
            r'RQ.*?:\s*(.+?)(?:\n\n|\n[A-Z]|\nType:|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                rq_text = match.group(1).strip()
                # Clean up common artifacts
                rq_text = re.sub(r'\*\*.*?\*\*', '', rq_text)  # Remove bold
                rq_text = re.sub(r'\n+', ' ', rq_text)  # Collapse newlines
                rq_text = re.sub(r'\s+', ' ', rq_text)  # Collapse whitespace
                return rq_text
        
        return "RQ text not found in concept file"
    except Exception as e:
        return f"Error reading concept: {e}"

def extract_score(context_dump):
    """Extract numerical score from context dump"""
    if not context_dump:
        return None, "No context"
    
    # Look for score patterns
    patterns = [
        r'(\d+\.?\d*)/10\s+(?:✅\s*)?(?:APPROVED|approved)',
        r'(\d+\.?\d*)/10\s+(?:⚠️\s*)?(?:CONDITIONAL|conditional)',
        r'(\d+\.?\d*)/10\s+(?:❌\s*)?(?:REJECTED|rejected)',
        r'(\d+\.?\d*)/10',
        r'Score:\s*(\d+\.?\d*)',
        r'score.*?(\d+\.?\d*)'
    ]
    
    status_patterns = [
        (r'✅.*?APPROVED|APPROVED.*?✅|approved', 'APPROVED'),
        (r'⚠️.*?CONDITIONAL|CONDITIONAL.*?⚠️|conditional', 'CONDITIONAL'),
        (r'❌.*?REJECTED|REJECTED.*?❌|rejected', 'REJECTED')
    ]
    
    # Extract score
    score = None
    for pattern in patterns:
        match = re.search(pattern, context_dump, re.IGNORECASE)
        if match:
            try:
                score = float(match.group(1))
                break
            except:
                continue
    
    # Extract status
    status = "UNKNOWN"
    for pattern, status_name in status_patterns:
        if re.search(pattern, context_dump, re.IGNORECASE):
            status = status_name
            break
    
    return score, status

def main():
    results_dir = Path("/home/etai/projects/REMEMVR/results/ch7")
    rq_dirs = sorted([d for d in results_dir.iterdir() if d.is_dir() and re.match(r'7\.[1-8]\.[1-5]$', d.name)], key=lambda x: tuple(map(int, x.name.split('.'))))
    
    all_data = []
    
    for rq_dir in rq_dirs:
        rq_id = rq_dir.name
        print(f"Processing {rq_id}...")
        
        # Initialize data structure
        data = {
            'rq_id': rq_id,
            'rq_text': 'Not found',
            'scholar_score': None,
            'scholar_status': 'Not assessed',
            'stats_score': None,
            'stats_status': 'Not assessed',
            'plan_exists': False,
            'tools_status': 'Not started',
            'analysis_status': 'Not started',
            'concept_status': 'Not found'
        }
        
        # Read status.yaml
        status_file = rq_dir / "status.yaml"
        if status_file.exists():
            try:
                with open(status_file, 'r', encoding='utf-8') as f:
                    status_data = yaml.safe_load(f)
                
                # Extract validation scores
                if 'rq_scholar' in status_data and status_data['rq_scholar'].get('context_dump'):
                    data['scholar_score'], data['scholar_status'] = extract_score(status_data['rq_scholar']['context_dump'])
                
                if 'rq_stats' in status_data and status_data['rq_stats'].get('context_dump'):
                    data['stats_score'], data['stats_status'] = extract_score(status_data['rq_stats']['context_dump'])
                
                # Extract other statuses
                if 'rq_concept' in status_data:
                    data['concept_status'] = status_data['rq_concept'].get('status', 'Not found')
                
                if 'rq_tools' in status_data:
                    data['tools_status'] = status_data['rq_tools'].get('status', 'Not started')
                
                if 'rq_analysis' in status_data:
                    data['analysis_status'] = status_data['rq_analysis'].get('status', 'Not started')
                
            except Exception as e:
                print(f"Error reading status.yaml for {rq_id}: {e}")
        
        # Check for plan file
        plan_files = [
            rq_dir / "2_plan.md",
            rq_dir / "docs" / "2_plan.md"
        ]
        for plan_file in plan_files:
            if plan_file.exists():
                data['plan_exists'] = True
                break
        
        # Read RQ text from concept
        concept_files = [
            rq_dir / "docs" / "1_concept.md",
            rq_dir / "1_concept.md"
        ]
        for concept_file in concept_files:
            if concept_file.exists():
                data['rq_text'] = extract_rq_info_from_concept(concept_file)
                break
        
        all_data.append(data)
    
    # Generate comprehensive table
    print(f"\n=== COMPREHENSIVE CH7 STATUS TABLE ===")
    print(f"Generated: {os.popen('date').read().strip()}")
    print(f"Total RQs: {len(all_data)}")
    
    # Summary statistics
    scholar_approved = sum(1 for d in all_data if d['scholar_status'] == 'APPROVED')
    scholar_conditional = sum(1 for d in all_data if d['scholar_status'] == 'CONDITIONAL')
    scholar_rejected = sum(1 for d in all_data if d['scholar_status'] == 'REJECTED')
    scholar_assessed = sum(1 for d in all_data if d['scholar_score'] is not None)
    
    stats_approved = sum(1 for d in all_data if d['stats_status'] == 'APPROVED')
    stats_conditional = sum(1 for d in all_data if d['stats_status'] == 'CONDITIONAL')
    stats_rejected = sum(1 for d in all_data if d['stats_status'] == 'REJECTED')
    stats_assessed = sum(1 for d in all_data if d['stats_score'] is not None)
    
    plans_created = sum(1 for d in all_data if d['plan_exists'])
    tools_success = sum(1 for d in all_data if d['tools_status'] == 'success')
    analysis_success = sum(1 for d in all_data if d['analysis_status'] == 'success')
    
    print(f"\n=== SUMMARY STATISTICS ===")
    print(f"Scholar validation: {scholar_assessed}/32 assessed ({scholar_assessed/32*100:.1f}%)")
    print(f"  - APPROVED: {scholar_approved}, CONDITIONAL: {scholar_conditional}, REJECTED: {scholar_rejected}")
    print(f"Stats validation: {stats_assessed}/32 assessed ({stats_assessed/32*100:.1f}%)")
    print(f"  - APPROVED: {stats_approved}, CONDITIONAL: {stats_conditional}, REJECTED: {stats_rejected}")
    print(f"Plans created: {plans_created}/32 ({plans_created/32*100:.1f}%)")
    print(f"Tools completed: {tools_success}/32 ({tools_success/32*100:.1f}%)")
    print(f"Analysis completed: {analysis_success}/32 ({analysis_success/32*100:.1f}%)")
    
    # Detailed table
    print(f"\n=== DETAILED STATUS TABLE ===")
    print(f"{'RQ':<8} {'RQ Text':<50} {'Scholar':<15} {'Stats':<15} {'Plan':<6} {'Tools':<8} {'Analysis':<10}")
    print("="*130)
    
    for data in all_data:
        rq_text_short = (data['rq_text'][:47] + "...") if len(data['rq_text']) > 50 else data['rq_text']
        
        scholar_col = f"{data['scholar_score'] or 'N/A':.1f}" if data['scholar_score'] else "N/A"
        scholar_col += f" {data['scholar_status'][:3]}"
        
        stats_col = f"{data['stats_score'] or 'N/A':.1f}" if data['stats_score'] else "N/A"
        stats_col += f" {data['stats_status'][:3]}"
        
        plan_col = "✓" if data['plan_exists'] else "✗"
        tools_col = data['tools_status'][:7]
        analysis_col = data['analysis_status'][:8]
        
        print(f"{data['rq_id']:<8} {rq_text_short:<50} {scholar_col:<15} {stats_col:<15} {plan_col:<6} {tools_col:<8} {analysis_col:<10}")
    
    # Export to CSV for further processing
    output_file = "/home/etai/projects/REMEMVR/ch7_comprehensive_status.csv"
    with open(output_file, 'w') as f:
        f.write("RQ_ID,RQ_Text,Scholar_Score,Scholar_Status,Stats_Score,Stats_Status,Plan_Exists,Tools_Status,Analysis_Status,Concept_Status\n")
        for data in all_data:
            rq_text_clean = data['rq_text'].replace('"', '""').replace('\n', ' ')
            f.write(f'"{data["rq_id"]}","{rq_text_clean}",{data["scholar_score"] or ""},"{data["scholar_status"]}",{data["stats_score"] or ""},"{data["stats_status"]}",{data["plan_exists"]},"{data["tools_status"]}","{data["analysis_status"]}","{data["concept_status"]}"\n')
    
    print(f"\nData exported to: {output_file}")

if __name__ == "__main__":
    main()