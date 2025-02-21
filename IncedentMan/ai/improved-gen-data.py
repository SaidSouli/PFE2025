import pandas as pd
import numpy as np
import random
import datetime
from typing import List, Dict, Tuple

# Enhanced categories with subcategories for better classification
INCIDENT_TAXONOMY = {
    'HARDWARE': {
        'subcategories': ['Printer', 'Workstation', 'Server', 'Network Hardware', 'Storage', 'Mobile Device', 
                         'Peripheral', 'IoT Device', 'AV Equipment', 'Point-of-Sale Hardware'],
        'common_issues': {
            'Printer': [
                'paper jam', 'not printing', "doesn't print", 'print quality', 'toner low', 'offline',
                'connection issues', 'configuration error', 'hardware failure', 'maintenance required',
                'error code', 'display malfunction', 'touchscreen unresponsive', 'network printer unavailable'
            ],
            'Workstation': [
                'blue screen', 'won\'t boot', 'slow performance', 'hardware failure', 'display issues',
                'peripheral problems', 'power issues', 'overheating', 'strange noises', 'freezing',
                'USB ports not working', 'battery failure', 'keyboard not responding', 'touchpad malfunction'
            ],
            'Server': [
                'hardware failure', 'disk errors', 'RAID issues', 'memory errors', 'power supply',
                'cooling problems', 'component failure', 'storage capacity', 'performance degradation',
                'fan failure', 'temperature alarm', 'backplane failure', 'SSD wear warning', 'chassis intrusion'
            ],
            'Mobile Device': [
                'screen cracked', 'battery draining', 'won\'t charge', 'app crashes', 'overheating',
                'no signal', 'touchscreen issues', 'camera malfunction', 'audio problems', 'bluetooth failure'
            ],
            'Storage': [
                'disk full', 'slow read/write', 'data corruption', 'array degraded', 'drive failure',
                'controller error', 'cache battery', 'expansion failure', 'LUN unavailable', 'replication error'
            ],
            'Network Hardware': [
                'port failure', 'device offline', 'throughput degradation', 'configuration lost',
                'firmware issues', 'hardware fault', 'overloaded', 'packet loss', 'power cycling'
            ],
            'IoT Device': [
                'offline', 'firmware update failed', 'connectivity issues', 'sensor malfunction',
                'battery depletion', 'data transmission failure', 'integration error', 'unauthorized access'
            ],
            'AV Equipment': [
                'display failure', 'audio cutout', 'projection issues', 'remote control malfunction',
                'connection problems', 'calibration needed', 'resolution mismatch', 'HDMI failure'
            ]
        },
        'priority_weights': {1: 0.3, 2: 0.3, 3: 0.3, 4: 0.1}  # Lower numbers are lower priority
    },
    'SOFTWARE': {
        'subcategories': ['Operating System', 'Application', 'Driver', 'Security Software', 'Custom Software',
                         'Database', 'Cloud Service', 'Virtualization', 'Office Suite', 'Enterprise Software'],
        'common_issues': {
            'Operating System': [
                'blue screen', 'crash', 'update failed', 'slow performance', 'login issues',
                'profile corruption', 'driver conflicts', 'boot problems', 'security patch failed',
                'activation issues', 'compatibility problems', 'resource leaks', 'kernel panic'
            ],
            'Application': [
                'not responding', 'crash', 'performance issues', 'error message', 'data corruption',
                'integration failure', 'version conflict', 'license expired', 'feature not working',
                'plugin failure', 'memory leak', 'installation failed', 'database connection error'
            ],
            'Database': [
                'query timeout', 'deadlock detected', 'corruption', 'index fragmentation',
                'backup failure', 'replication error', 'connection pool exhausted', 'transaction log full'
            ],
            'Cloud Service': [
                'service unavailable', 'API errors', 'quota exceeded', 'authentication failure',
                'data sync issues', 'excessive billing', 'permission problems', 'misconfiguration'
            ],
            'Security Software': [
                'false positives', 'update failure', 'quarantine errors', 'scan hanging',
                'real-time protection disabled', 'firewall issues', 'encryption problems'
            ],
            'Virtualization': [
                'VM not starting', 'snapshot issues', 'hypervisor errors', 'resource contention',
                'migration failed', 'clone error', 'hardware passthrough issues', 'storage overcommit'
            ]
        },
        'priority_weights': {1: 0.3, 2: 0.3, 3: 0.3, 4: 0.1}
    },
    'NETWORK': {
        'subcategories': ['LAN', 'WAN', 'WiFi', 'VPN', 'Internet', 'DNS', 'Firewall', 'Load Balancer',
                         'Router', 'Switch', 'Gateway', 'Proxy'],
        'common_issues': {
            'LAN': [
                'connection lost', 'slow speed', 'intermittent connection', 'packet loss',
                'high latency', 'switch issues', 'cable problems', 'VLAN misconfiguration',
                'broadcast storm', 'duplex mismatch', 'spanning tree loop', 'MAC flooding'
            ],
            'WiFi': [
                'no connection', 'weak signal', 'intermittent connection', 'authentication failed',
                'slow speed', 'coverage issues', 'interference', 'channel congestion',
                'AP offline', 'roaming issues', 'band steering failure', 'client compatibility'
            ],
            'VPN': [
                'connection dropout', 'authentication failure', 'slow performance', 'tunnel collapse',
                'split tunneling issues', 'certificate expired', 'encryption problems', 'client compatibility'
            ],
            'Internet': [
                'service outage', 'intermittent connectivity', 'bandwidth throttling', 'DNS resolution',
                'routing problems', 'ISP gateway issues', 'international traffic slow', 'CDN failures'
            ],
            'Firewall': [
                'blocking legitimate traffic', 'rule conflict', 'high CPU', 'session table full',
                'failover issues', 'inappropriate filtering', 'VPN passthrough problems', 'NAT errors'
            ],
            'DNS': [
                'resolution failure', 'cache poisoning', 'zone transfer issues', 'propagation delay',
                'incorrect records', 'DNSSEC validation', 'forwarding loops', 'timeout errors'
            ]
        },
        'priority_weights': {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.2}
    },
    'SECURITY': {
        'subcategories': ['Malware', 'Phishing', 'Account Compromise', 'Data Breach', 'Insider Threat',
                         'Physical Security', 'Policy Violation', 'Vulnerability'],
        'common_issues': {
            'Malware': [
                'ransomware detected', 'virus outbreak', 'trojan infection', 'suspicious activity',
                'cryptomining detected', 'botnet connection', 'fileless malware', 'rootkit suspected',
                'DNS hijacking malware', 'ARP spoofing tool', 'spyware installation', 'keylogger detected'  
            ],
            'Phishing': [
                'email campaign detected', 'user reported suspicious email', 'clicked phishing link',
                'provided credentials', 'downloaded malicious attachment', 'vishing attempt reported',
                'spoofed email domain', 'CEO fraud attempt'  
            ],
            'Account Compromise': [
                'unusual login location', 'brute force attempt', 'privilege escalation',
                'unauthorized password reset', 'session hijacking', 'API key exposed', 'MFA bypass attempt',
                'credential hijacking', 'browser session hijack', 'cookie hijacking'  
            ],
            'Data Breach': [
                'unauthorized data access', 'data exfiltration detected', 'sensitive information exposed',
                'database dump identified', 'cloud storage misconfiguration', 'third-party breach impact'
            ],
            'Vulnerability': [
                'critical CVE reported', 'zero-day exploit', 'unpatched system', 'misconfiguration',
                'default credentials', 'service exposure', 'weak encryption', 'code injection vulnerability',
                'ARP spoofing detected', 'DNS spoofing attack', 'IP spoofing attempt', 'MAC spoofing detected'  
            ]
        },
        'priority_weights': {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}
    },
    'CLOUD': {
        'subcategories': ['AWS', 'Azure', 'GCP', 'Private Cloud', 'SaaS', 'PaaS', 'IaaS', 'Hybrid Cloud'],
        'common_issues': {
            'AWS': [
                'EC2 instance down', 'S3 bucket accessibility', 'RDS performance', 'Lambda timeout',
                'IAM permission issues', 'CloudFormation failure', 'ELB health check failure', 'cost spike'
            ],
            'Azure': [
                'VM not available', 'App Service down', 'Storage Account issues', 'AD sync failure',
                'ExpressRoute problems', 'Function App errors', 'DevOps pipeline failure', 'resource contention'
            ],
            'SaaS': [
                'service unavailable', 'API rate limiting', 'data sync failure', 'integration broken',
                'feature regression', 'tenant isolation breach', 'authentication issues', 'SSO failure'
            ],
            'Private Cloud': [
                'resource allocation failure', 'orchestration error', 'tenant isolation', 'self-service portal',
                'capacity issues', 'automation failure', 'template error', 'backup failures'
            ]
        },
        'priority_weights': {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.2}
    },
    'IDENTITY': {
        'subcategories': ['Authentication', 'Authorization', 'Directory Services', 'SSO', 'MFA', 'User Management'],
        'common_issues': {
            'Authentication': [
                'login failure', 'password expiration', 'account lockout', 'LDAP connection issue',
                'Kerberos ticket problem', 'certificate expiration', 'token validation error', 'auth provider down'
            ],
            'Directory Services': [
                'replication failure', 'schema issues', 'group policy problem', 'trust relationship',
                'domain controller offline', 'FSMO role unavailable', 'attribute corruption', 'forest connectivity'
            ],
            'MFA': [
                'token synchronization', 'mobile app issues', 'hardware token malfunction', 'SMS delivery failure',
                'bypass code problems', 'enrollment failure', 'authenticator app conflict', 'time drift'
            ],
            'SSO': [
                'assertion failure', 'metadata mismatch', 'certificate expiration', 'IdP unavailable',
                'attribute mapping', 'session timeout', 'redirect loop', 'protocol mismatch'
            ]
        },
        'priority_weights': {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.2}
    },
    'DATA': {
        'subcategories': ['Database', 'Data Loss', 'Backup', 'Recovery', 'Data Quality', 'ETL', 'Storage'],
        'common_issues': {
            'Database': [
                'query performance', 'deadlock', 'corruption detected', 'connection pool exhausted',
                'transaction log full', 'index fragmentation', 'table lock', 'replication lag'
            ],
            'Backup': [
                'backup job failed', 'verification error', 'media failure', 'incomplete backup',
                'retention policy error', 'catalog corruption', 'offsite transfer failed', 'snapshot inconsistency'
            ],
            'Recovery': [
                'restore failure', 'missing backup set', 'incomplete recovery', 'point-in-time failure',
                'inconsistent state', 'application incompatibility', 'storage overwrite', 'media corruption'
            ],
            'Data Quality': [
                'data inconsistency', 'missing records', 'duplicate entries', 'validation failure',
                'transformation error', 'reference integrity', 'schema mismatch', 'encoding problems'
            ]
        },
        'priority_weights': {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.2}
    },
    'COMPLIANCE': {
        'subcategories': ['Audit', 'Regulatory', 'Policy', 'Privacy', 'Legal', 'Documentation'],
        'common_issues': {
            'Audit': [
                'missing controls', 'evidence collection', 'failed audit check', 'logging inadequate',
                'unauthorized action', 'separation of duties', 'access review', 'privileged account usage'
            ],
            'Regulatory': [
                'GDPR violation', 'HIPAA requirement', 'PCI compliance', 'data sovereignty',
                'reporting deadline', 'financial controls', 'consent management', 'retention violation'
            ],
            'Privacy': [
                'data exposure', 'consent violation', 'right to be forgotten request', 'unauthorized disclosure',
                'data subject access request', 'third-party sharing', 'cross-border transfer', 'de-identification failure'
            ],
            'Policy': [
                'acceptable use violation', 'security policy breach', 'unapproved software', 'missing training',
                'procurement violation', 'unauthorized resource', 'change management bypass', 'documentation gap'
            ]
        },
        'priority_weights': {1: 0.1, 2: 0.2, 3: 0.4, 4: 0.3}
    }
}

# Enhanced location and user details for more realistic descriptions
LOCATIONS = {
    'buildings': ['HQ Building', 'Building A', 'Building B', 'Data Center', 'Warehouse', 'Branch Office', 
                'Regional HQ', 'R&D Lab', 'Manufacturing Plant', 'Distribution Center'],
    'floors': ['Ground Floor', '1st Floor', '2nd Floor', 'Basement', 'Mezzanine', 'Executive Floor',
              'IT Floor', 'Operations Center', 'Training Room'],
    'remote': ['Home Office', 'Field Location', 'Customer Site', 'Satellite Office', 'Co-working Space']
}

DEPARTMENTS = [
    'IT', 'Finance', 'HR', 'Marketing', 'Sales', 'Operations', 'Legal', 'Executive', 
    'Customer Support', 'Research', 'Development', 'Engineering', 'Product Management',
    'Supply Chain', 'Facilities', 'Security', 'Compliance', 'Procurement', 'Manufacturing'
]

# Enhanced description generation
def generate_incident_description(category: str, subcategory: str) -> Tuple[str, int]:
    """Generate a realistic incident description with appropriate priority."""
    
    # Get common issues for this category/subcategory or use generic issues if not defined
    common_issues = INCIDENT_TAXONOMY[category]['common_issues'].get(
        subcategory, 
        ['issue', 'problem', 'failure', 'error', 'malfunction', 'outage', 'degradation']
    )
    
    # Location generation with more variety
    if random.random() < 0.2:  # 20% chance for remote location
        location = random.choice(LOCATIONS['remote'])
    else:
        building = random.choice(LOCATIONS['buildings'])
        if random.random() < 0.7:  # 70% chance to include floor
            floor = random.choice(LOCATIONS['floors'])
            location = f"{building}, {floor}"
        else:
            location = building
    
    department = random.choice(DEPARTMENTS)
    
    # More nuanced user impact
    impact_type = random.choice(['users', 'systems', 'services', 'operations'])
    if impact_type == 'users':
        user_count = random.choice([1, 2, 3, 5, 10, 'multiple', 'several'])
        if user_count in [1, 2, 3]:
            user_impact = f"{user_count} user{'s' if user_count > 1 else ''}"
        else:
            user_impact = f"{user_count} users"
        
        if random.random() < 0.4:  # 40% chance to specify department
            user_impact += f" in {department}"
    elif impact_type == 'systems':
        count = random.choice([1, 2, 'multiple', 'several', 'all'])
        systems = random.choice(['servers', 'workstations', 'devices', 'endpoints', 'terminals'])
        user_impact = f"{count} {systems}"
    elif impact_type == 'services':
        scope = random.choice(['critical', 'core', 'business', 'customer-facing', 'internal'])
        user_impact = f"{scope} services"
    else:  # operations
        scope = random.choice(['business', 'critical', 'department', 'team'])
        user_impact = f"{scope} operations"
    
    # Select an issue with more variety
    issue = random.choice(common_issues)
    
    # Add severity indicators for some issues
    if random.random() < 0.3:
        severity = random.choice(['minor', 'major', 'critical', 'intermittent', 'persistent', 'degraded'])
        issue = f"{severity} {issue}"
    
    # Priority determination with more sophistication
    if category == 'SECURITY' and subcategory in ['Malware', 'Data Breach', 'Account Compromise']:
        # Security incidents are higher priority
        priority_weights = {3: 0.3, 4: 0.7}
    elif 'critical' in issue.lower() or 'all' in user_impact or 'business operations' in user_impact:
        priority_weights = {3: 0.4, 4: 0.6}  # High priority
    elif any(high_impact in issue.lower() for high_impact in ['failure', 'outage', 'breach', 'down']):
        priority_weights = {2: 0.3, 3: 0.5, 4: 0.2}  # Medium-high priority
    elif 'department' in user_impact or 'multiple' in user_impact:
        priority_weights = {2: 0.5, 3: 0.4, 1: 0.1}  # Medium priority
    else:
        priority_weights = INCIDENT_TAXONOMY[category]['priority_weights']
    
    priority = random.choices(
        list(priority_weights.keys()), 
        weights=list(priority_weights.values())
    )[0]
    
    # More diverse description templates
    templates = [
        f"{subcategory} {issue} reported by {user_impact} in {location}",
        f"{department} reporting {subcategory} {issue} affecting {user_impact}",
        f"{location} - {subcategory}: {issue} - impacting {user_impact}",
        f"[{department}] {user_impact} affected by {subcategory} {issue}",
        f"Incident: {issue} with {subcategory} reported from {location}",
        f"{issue} in {subcategory} system affecting {user_impact} at {location}",
        f"{department} {location}: {user_impact} experiencing {subcategory} {issue}",
        f"{subcategory} incident - {issue} - {location} - Affecting: {user_impact}",
        f"[{location}] {department} reports {subcategory} {issue} for {user_impact}",
        f"Service alert: {subcategory} {issue} detected, impacting {user_impact}"
    ]
    
    description = random.choice(templates)
    
    # Add time indicators for some incidents
    if random.random() < 0.2:
        time_indicator = random.choice([
            "since this morning", "for the past hour", "intermittently throughout the day",
            "after the recent update", "following maintenance", "recurring issue", 
            "sudden onset", "gradual degradation"
        ])
        description += f" ({time_indicator})"
    
    # Add variation for more realistic text
    word_replacements = {
        'reported': ['noticed', 'observed', 'identified', 'flagged', 'escalated', 'detected'],
        'affecting': ['impacting', 'disrupting', 'hindering', 'preventing access for', 'causing problems for'],
        'experiencing': ['encountering', 'facing', 'struggling with', 'dealing with', 'reporting']
    }
    
    for original, replacements in word_replacements.items():
        if original in description and random.random() < 0.3:
            description = description.replace(original, random.choice(replacements))
    
    # Sometimes add specific details for even more realism
    if random.random() < 0.15:
        details = [
            f"Error code: {random.choice(['E', 'ERR', 'SYS'])}{random.randint(100, 9999)}",
            f"Vendor ticket: {random.choice(['T', 'INC', 'CASE'])}{random.randint(10000, 99999)}",
            f"Asset tag: {random.choice(['IT', 'DEV', 'SRV'])}-{random.randint(1000, 9999)}",
            f"Software version: {random.randint(1, 10)}.{random.randint(0, 20)}.{random.randint(0, 99)}",
            f"IP: 10.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        ]
        description += f" - {random.choice(details)}"
    
    return description, priority

def generate_realistic_timestamp(days_back=180):
    """Generate a timestamp within the specified days back with realistic distribution."""
    # Recent incidents are more common than older ones
    # Log-normal distribution gives more recent timestamps with a tail of older ones
    days_ago = int(random.lognormvariate(0, 1) * (days_back / 5))
    days_ago = min(days_ago, days_back)  # Cap at max days
    
    # Generate a random time of day, with more incidents during business hours
    hour = random.choices(
        range(24),
        weights=[1, 1, 1, 1, 1, 2, 5, 10, 15, 20, 20, 18, 15, 20, 20, 18, 15, 10, 5, 3, 2, 2, 1, 1]
    )[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    timestamp = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    timestamp = timestamp.replace(hour=hour, minute=minute, second=second)
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def generate_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Generate a more diverse and realistic dataset with varied distribution."""
    incidents = []
    
    # Create a realistic distribution across categories (not perfectly balanced)
    category_distribution = {
        'HARDWARE': 0.18,
        'SOFTWARE': 0.22,
        'NETWORK': 0.20,
        'SECURITY': 0.12,
        'CLOUD': 0.10,
        'IDENTITY': 0.08,
        'DATA': 0.06,
        'COMPLIANCE': 0.04
    }
    
    # Generate incidents based on distribution
    for category, percentage in category_distribution.items():
        category_count = int(num_samples * percentage)
        category_details = INCIDENT_TAXONOMY[category]
        
        # Create a slight bias toward certain subcategories
        subcategory_weights = [1.0] * len(category_details['subcategories'])
        
        # Make some subcategories more common than others
        if len(subcategory_weights) > 2:
            subcategory_weights[0] *= 1.5  # First subcategory appears 50% more
            subcategory_weights[1] *= 1.2  # Second subcategory appears 20% more
            
        for _ in range(category_count):
            subcategory = random.choices(
                category_details['subcategories'],
                weights=subcategory_weights[:len(category_details['subcategories'])]
            )[0]
            
            description, priority = generate_incident_description(category, subcategory)
            
            # Add creation timestamp with realistic distribution
            timestamp = generate_realistic_timestamp()
            
            # Add ticket ID with realistic format
            ticket_id = f"INC{random.randint(100000, 999999)}"
            
            # Add additional metadata for more dimensions
            requester_type = random.choice(
                ['Employee', 'Employee', 'Employee', 'Manager', 'Contractor', 'VIP', 'External']
            )
            
            # Generate a realistic resolution time based on priority
            if priority == 4:  # Critical
                resolution_hours = random.uniform(0.5, 12)
            elif priority == 3:  # High
                resolution_hours = random.uniform(2, 48)
            elif priority == 2:  # Medium
                resolution_hours = random.uniform(24, 120)
            else:  # Low
                resolution_hours = random.uniform(72, 240)
                
            # Sometimes incidents remain unresolved
            resolved = random.random() < 0.85  # 85% of incidents are resolved
            
            if resolved:
                resolution_timestamp = (
                    datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") + 
                    datetime.timedelta(hours=resolution_hours)
                ).strftime("%Y-%m-%d %H:%M:%S")
                
                resolution_status = random.choices(
                    ['Resolved', 'Workaround Provided', 'Closed', 'Duplicate', 'Not Reproducible'],
                    weights=[0.6, 0.15, 0.15, 0.05, 0.05]
                )[0]
            else:
                resolution_timestamp = None
                resolution_status = random.choices(
                    ['Open', 'In Progress', 'Pending', 'Awaiting Information', 'Escalated'],
                    weights=[0.2, 0.4, 0.2, 0.1, 0.1]
                )[0]
            
            incidents.append({
                'ticket_id': ticket_id,
                'description': description,
                'category': category,
                'subcategory': subcategory,
                'priority': priority,
                'status': resolution_status,
                'created_timestamp': timestamp,
                'resolved_timestamp': resolution_timestamp,
                'requester_type': requester_type,
                'resolution_hours': resolution_hours if resolved else None
            })
    
    # Convert to DataFrame and add derived features
    df = pd.DataFrame(incidents)
    
    # Add some hijacking examples for security incidents
    security_hijacking = [
        "Account hijacking attempt detected for admin user",
        "Multiple failed login attempts - possible hijacking of service account",
        "Suspected session hijacking from unusual location",
        "Security alert: possible VPN session hijacking detected",
        "User reported suspicious activity - account may have been hijacked",
        "SSH session hijacking attempt blocked by firewall",
        "Web session hijacking detection triggered multiple alarms",
        "Database credentials possibly hijacked - unusual query patterns",
        "API token suspected hijacked - excessive request rate",
        "Email account showing signs of hijacking - unauthorized rules created"
    ]
    
    # Replace some descriptions with hijacking scenarios
    security_indices = df[df['category'] == 'SECURITY'].index
    if len(security_indices) >= 10:
        hijack_indices = random.sample(list(security_indices), 10)
        for i, idx in enumerate(hijack_indices):
            df.at[idx, 'description'] = security_hijacking[i]
            df.at[idx, 'subcategory'] = 'Account Compromise'
            df.at[idx, 'priority'] = 4  # Critical priority
    
    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

# Generate enhanced dataset
if __name__ == "__main__":
    # Generate a large, diverse dataset
    enhanced_df = generate_dataset(10000)
    
    # Save to CSV
    enhanced_df.to_csv('data/enhanced_incident_data.csv', index=False)
    
    