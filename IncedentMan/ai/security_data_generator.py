import pandas as pd
import numpy as np
import random
import datetime
from typing import List, Dict, Tuple

# Enhanced security-focused taxonomy
SECURITY_TAXONOMY = {
    'SPOOFING': {
        'subcategories': ['IP Spoofing', 'DNS Spoofing', 'ARP Spoofing', 'Email Spoofing', 
                         'MAC Spoofing', 'DHCP Spoofing', 'GPS Spoofing'],
        'common_issues': {
            'IP Spoofing': [
                'source IP address forgery detected', 'IP impersonation attempt',
                'packet with spoofed source IP', 'suspicious IP routing behavior',
                'firewall detected IP spoofing pattern', 'IP packet manipulation detected',
                'illegitimate IP source identified'
            ],
            'DNS Spoofing': [
                'DNS cache poisoning attempt', 'suspicious DNS response',
                'DNS resolver compromise attempt', 'malicious DNS redirection',
                'DNS amplification attack', 'fake DNS records detected',
                'DNS protocol manipulation'
            ],
            'ARP Spoofing': [
                'ARP cache poisoning detected', 'suspicious ARP broadcast',
                'unauthorized ARP reply', 'man-in-the-middle attempt via ARP',
                'gratuitous ARP detected', 'ARP table manipulation',
                'network scanning through ARP'
            ],
            'Email Spoofing': [
                'forged sender address', 'header manipulation detected',
                'SPF verification failure', 'DMARC policy violation',
                'suspicious email origin', 'unauthorized domain use in email',
                'email authentication failure'
            ]
        },
        'priority_weights': {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}
    },
    'MALWARE': {
        'subcategories': ['Ransomware', 'Spyware', 'Trojan', 'Rootkit', 'Keylogger', 
                         'Cryptominer', 'Worm', 'Adware'],
        'common_issues': {
            'Ransomware': [
                'file encryption in progress', 'ransom note detected',
                'mass file extension change', 'suspicious encryption activity',
                'known ransomware signature', 'backup deletion attempt',
                'ransomware communication pattern'
            ],
            'Spyware': [
                'unauthorized data collection', 'suspicious outbound traffic',
                'keystroke logging detected', 'screen capture activity',
                'unauthorized data exfiltration', 'browser history theft',
                'credential harvesting attempt'
            ],
            'Rootkit': [
                'system file manipulation', 'hidden process detected',
                'kernel modification attempt', 'suspicious driver loading',
                'system call hooking', 'rootkit persistence mechanism',
                'hidden file system activity'
            ]
        },
        'priority_weights': {1: 0.0, 2: 0.1, 3: 0.3, 4: 0.6}
    },
    'HIJACKING': {
        'subcategories': ['Session Hijacking', 'Browser Hijacking', 'Network Hijacking', 
                         'Account Hijacking', 'Click Hijacking'],
        'common_issues': {
            'Session Hijacking': [
                'cookie theft detected', 'session token compromise',
                'man-in-the-middle session intercept', 'session replay attack',
                'unauthorized session usage', 'session fixation attempt',
                'session validation failure'
            ],
            'Account Hijacking': [
                'unauthorized account access', 'suspicious password reset',
                'unusual login pattern', 'multiple authentication failures',
                'account takeover attempt', 'credential stuffing attack',
                'password spraying detected'
            ],
            'Network Hijacking': [
                'BGP route hijacking', 'traffic redirection detected',
                'unauthorized gateway change', 'rogue DHCP server',
                'network path manipulation', 'protocol downgrade attempt',
                'SSL strip attack detected'
            ]
        },
        'priority_weights': {1: 0.0, 2: 0.1, 3: 0.3, 4: 0.6}
    },
    'ACCESS_CONTROL': {
        'subcategories': ['Privilege Escalation', 'Access Bypass', 'Authentication Bypass',
                         'Authorization Bypass', 'MFA Compromise'],
        'common_issues': {
            'Privilege Escalation': [
                'unauthorized privilege elevation', 'sudo abuse detected',
                'vertical privilege escalation', 'horizontal privilege escalation',
                'service account compromise', 'admin rights abuse',
                'SYSTEM level escalation'
            ],
            'Authentication Bypass': [
                'authentication mechanism bypass', 'credential bypass attempt',
                'forced browsing detected', 'direct object reference',
                'authentication token manipulation', 'SSO bypass attempt',
                'password hash exploitation'
            ]
        },
        'priority_weights': {1: 0.0, 2: 0.1, 3: 0.4, 4: 0.5}
    }
}

def generate_security_incident() -> Dict:
    """Generate a realistic security incident with detailed attributes."""
    category = random.choice(list(SECURITY_TAXONOMY.keys()))
    category_data = SECURITY_TAXONOMY[category]
    subcategory = random.choice(category_data['subcategories'])
    
    # Get specific issues for the subcategory or use generic ones
    common_issues = category_data['common_issues'].get(
        subcategory, 
        ['suspicious activity', 'security violation', 'potential compromise']
    )
    
    # Base incident description
    issue = random.choice(common_issues)
    
    # Add attack details
    attack_details = []
    if random.random() < 0.7:  # 70% chance to add technical details
        technical_details = {
            'IP Spoofing': [
                f"Source IP: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                f"Packet count: {random.randint(100,10000)}",
                f"Protocol: {random.choice(['TCP', 'UDP', 'ICMP'])}"
            ],
            'Session Hijacking': [
                f"Session ID: {random.randbytes(8).hex()}",
                f"User Agent: Mozilla/{random.randint(1,5)}.0",
                f"Cookie Length: {random.randint(32,256)}"
            ],
            'Ransomware': [
                f"Encrypted Files: {random.randint(100,10000)}",
                f"Extension: .{random.randbytes(4).hex()}",
                f"Bitcoin Address: {random.randbytes(20).hex()}"
            ]
        }
        
        if subcategory in technical_details:
            attack_details.extend(random.sample(technical_details[subcategory], 1))
    
    # Add impact details
    impact = random.choice([
        f"affecting {random.randint(1,100)} systems",
        f"compromising {random.randint(1,50)} user accounts",
        f"impacting {random.choice(['critical', 'sensitive', 'customer', 'financial'])} data",
        f"degrading {random.choice(['network', 'system', 'service', 'application'])} performance"
    ])
    
    # Add detection method
    detection = random.choice([
        "detected by IDS",
        "flagged by SIEM",
        "reported by EDR",
        "identified by SOC",
        "discovered during audit",
        "reported by user",
        "caught by firewall",
        "identified by threat hunting"
    ])
    
    # Construct full description
    description_parts = [issue, impact, detection]
    if attack_details:
        description_parts.extend(attack_details)
    
    description = " - ".join(description_parts)
    
    # Determine priority based on category and subcategory
    priority_weights = category_data['priority_weights']
    priority = random.choices(
        list(priority_weights.keys()),
        weights=list(priority_weights.values())
    )[0]
    
    # Generate timestamp with realistic distribution
    timestamp = (datetime.datetime.now() - 
                datetime.timedelta(days=random.randint(0,30),
                                 hours=random.randint(0,24),
                                 minutes=random.randint(0,60)))
    
    return {
        'ticket_id': f"SEC{random.randint(100000,999999)}",
        'description': description,
        'category': category,
        'subcategory': subcategory,
        'priority': priority,
        'created_timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'status': random.choice(['Open', 'In Progress', 'Escalated', 'Contained', 'Resolved']),
        'requester_type': random.choice(['SOC Analyst', 'Security Engineer', 'System Admin', 'Network Admin', 'Security Tool'])
    }

def generate_security_dataset(num_samples: int = 1000) -> pd.DataFrame:
    """Generate a dataset of security incidents."""
    incidents = [generate_security_incident() for _ in range(num_samples)]
    return pd.DataFrame(incidents)

if __name__ == "__main__":
    # Generate security-focused dataset
    security_df = generate_security_dataset(5000)
    
    # Save to CSV
    security_df.to_csv('data/security_incident_data.csv', index=False)
    
