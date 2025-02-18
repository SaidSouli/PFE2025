import pandas as pd
import numpy as np
import random
import datetime


CATEGORIES = ['NETWORK', 'HARDWARE', 'SOFTWARE', 'DATABASE', 'SECURITY']
PRIORITIES = [1, 2, 3, 4]  
SAMPLES_PER_CATEGORY = 200  
OUTPUT_FILE = "incident_data.csv"



locations = ['Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte', 'Gabès', 'Ariana', 
             'Ben Arous', 'Gafsa', 'Monastir', 'Nabeul', 'Hammamet', 'Djerba', 
             'Tozeur', 'El Kef', 'Mahdia', 'Sidi Bouzid', 'Béja', 'Jendouba', 'Tataouine']
raid_levels = [0, 1, 5, 6, 10]
db_types = ['MySQL', 'PostgreSQL', 'Oracle', 'SQL Server', 'MongoDB', 'Redis', 'Elasticsearch', 'DynamoDB']
app_names = ['ERP', 'CRM', 'HRMS', 'Payroll', 'Inventory', 'Dashboard', 'Customer Portal', 'Mobile App', 'Analytics Platform']
device_types = ['iOS', 'Android', 'Windows', 'macOS', 'Linux', 'Chrome OS', 'Tablet', 'POS Terminal']
events = ['month-end processing', 'year-end closing', 'peak hours', 'holiday season', 'system upgrade', 'data migration', 'scheduled maintenance']
network_devices = ['router', 'switch', 'firewall', 'load balancer', 'VPN concentrator', 'wireless AP', 'proxy server']
server_types = ['web server', 'application server', 'database server', 'file server', 'domain controller', 'virtual host', 'backup server', 'email server']
attackers = ['external threat actors', 'suspicious IPs', 'unauthorized users', 'potential compromise']
severity_words = ['minor', 'moderate', 'significant', 'severe', 'critical', 'potential', 'intermittent', 'recurring', 'persistent']
verbs = ['detected', 'observed', 'reported', 'identified', 'discovered', 'encountered', 'experienced', 'noted']
departments = ['Marketing', 'Finance', 'HR', 'Operations', 'Sales', 'IT', 'Customer Support', 'R&D', 'Executive', 'Legal']
error_codes = ['ERR-1234', 'SYS-5678', 'DB-9012', 'NET-3456', 'SEC-7890', 'APP-2345', 'HW-6789', 'CRIT-0123']
ip_ranges = ['192.168.1', '10.10.20', '172.16.30', '10.0.0', '192.168.0', '172.31.0', '10.1.1']


templates = {
    'NETWORK': [
        (4, [
            "Complete network outage in {location} datacenter affecting all {server_types}",
            "Critical failure of {network_device} in {location} causing total service disruption",
            "Major connectivity loss across all {location} offices - no access to core services",
            "{severity} outage of {location} backbone network affecting {departments} departments",
            "Primary and backup WAN link failure at {location} datacenter - {verb} at {time}"
        ]),
        (3, [
            "VPN connectivity issues for remote employees in {location} - error {error_code}",
            "Intermittent network drops affecting {severity} percentage of users in {location}",
            "{network_device} performance degradation affecting {departments} team workflows",
            "Slowdown in network response times affecting {app_name} services - {verb} by multiple users",
            "Unstable connectivity between {location} and disaster recovery site - started at {time}"
        ]),
        (2, [
            "Intermittent packet loss in {location} office network - {verb} during peak hours",
            "Wi-Fi coverage issues in {location} {departments} area affecting {device_type} devices",
            "{severity} latency reported by users accessing {app_name} from {location} office",
            "Network saturation during {event} affecting {departments} workflows",
            "Degraded performance on {network_device} at {location} - tickets from {departments}"
        ]),
        (1, [
            "DNS resolution delays for internal applications - primarily affecting {app_name}",
            "Minor packet drops on subnet {ip_range}.0/24 in {location} office",
            "Single {network_device} showing early warning signs in {location} facility",
            "Occasional timeout issues reported by {departments} team when accessing {app_name}",
            "Non-critical network alert from monitoring system for {location} guest network"
        ])
    ],
    'HARDWARE': [
        (4, [
            "Server rack failure in {location} datacenter - all {server_types} offline",
            "Critical hardware failure on primary storage array - RAID {raid_level} degraded",
            "UPS failure during power event at {location} - multiple systems affected",
            "Cooling system failure in {location} server room - temperature at critical levels",
            "Multiple blade server failures in chassis at {location} - {verb} during {event}"
        ]),
        (3, [
            "Storage array disk failure in RAID {raid_level} - redundancy compromised",
            "Physical server crash affecting {app_name} in {location} datacenter",
            "Disk subsystem errors on {server_types} in {location} - {verb} multiple errors",
            "Hardware errors on {departments} department's {device_type} devices - {severity} impact",
            "Failing power supply on critical {server_types} at {location} facility"
        ]),
        (2, [
            "Printer fleet connectivity issues in {location} office affecting {departments}",
            "Non-critical disk errors on {server_types} - SMART warnings {verb}",
            "Aging hardware alert for {server_types} supporting {app_name} - replacement needed",
            "Redundant component failure on {network_device} at {location} - still operational",
            "Memory errors {verb} on virtualization host in {location} - some VMs affected"
        ]),
        (1, [
            "Keyboard and mouse malfunction reports from multiple users in {departments}",
            "End-of-life hardware alert for non-critical {server_types} in {location}",
            "Single disk showing early warning signs in RAID {raid_level} array - no data at risk",
            "Projector system issues in {location} conference rooms - {departments} reported",
            "Routine replacement needed for aging workstations in {departments} department"
        ])
    ],
    'SOFTWARE': [
        (4, [
            "Critical application authentication failures for {app_name} - all users affected",
            "Complete system crash of {app_name} affecting all {departments} operations",
            "Major data corruption issue in {app_name} database - service completely down",
            "Catastrophic failure in operating system on {server_types} - {verb} at {time}",
            "Critical bug in production release of {app_name} causing system-wide failures"
        ]),
        (3, [
            "ERP system performance degradation during {event} affecting multiple modules",
            "Application crashes occurring on {app_name} during peak usage hours",
            "Software licensing issue causing service interruption for {app_name} users",
            "Memory leak identified in {app_name} affecting system stability after {time} uptime",
            "Integration failure between {app_name} and third-party services - {verb} after update"
        ]),
        (2, [
            "Mobile app UI rendering issues on {device_type} devices after recent update",
            "Non-critical bug in {app_name} affecting specific workflows in {departments}",
            "Software update problems on {device_type} fleet - {verb} by {departments}",
            "Minor functionality issues in {app_name} reported by {departments} team",
            "Performance slowdown in {app_name} during specific operations - {verb} by users"
        ]),
        (1, [
            "Legacy system printing glitches in {location} office - only affecting {departments}",
            "Cosmetic UI issues in {app_name} on {device_type} platform - no functional impact",
            "Minor alert notifications from monitoring system for {app_name} services",
            "Non-essential module showing errors in {app_name} - doesn't affect core functions",
            "Warning messages appearing in {app_name} logs - no user impact observed"
        ])
    ],
    'DATABASE': [
        (4, [
            "Database corruption detected in {db_type} cluster - data integrity compromised",
            "Complete database outage affecting all {app_name} operations - {verb} at {time}",
            "Critical data loss event in {db_type} production database - immediate attention required",
            "Master database server failure with replication issues to all slaves - {db_type}",
            "Catastrophic query performance issue bringing {db_type} database to a halt"
        ]),
        (3, [
            "SQL deadlock incidents during peak load in {db_type} affecting {app_name}",
            "Database replication lag exceeding thresholds on {db_type} cluster",
            "Significant query performance degradation in {db_type} during {event}",
            "Storage space critical on {db_type} database servers - immediate cleanup needed",
            "Connection pool exhaustion on {db_type} database supporting {app_name}"
        ]),
        (2, [
            "Backup job failures for {db_type} database - {verb} for last {severity} runs",
            "Slow query performance affecting specific reports in {app_name} - {db_type} issue",
            "Intermittent connection drops to {db_type} database during peak hours",
            "Growing transaction logs consuming disk space on {db_type} server",
            "Minor constraint violations {verb} in {db_type} after recent data import"
        ]),
        (1, [
            "Minor index fragmentation issues in {db_type} - scheduled optimization recommended",
            "Gradual growth in database size requiring future capacity planning - {db_type}",
            "Occasional query timeouts for specific reports in {app_name} using {db_type}",
            "Non-critical statistics update failures on {db_type} tables",
            "Historical data archiving required for {db_type} performance optimization"
        ])
    ],
    'SECURITY': [
        (4, [
            "Active data breach detected - unauthorized access to {severity} systems confirmed",
            "Credential stuffing attack successfully compromised multiple user accounts",
            "Ransomware outbreak detected across {location} network - multiple systems affected",
            "Critical zero-day vulnerability exploited on {server_types} - immediate action required",
            "Confirmed data exfiltration from {app_name} database by {attackers}"
        ]),
        (3, [
            "Unauthorized access attempts detected from {location} IP addresses",
            "Suspicious activity detected on privileged account in {app_name} system",
            "Malware detected on multiple endpoints in {departments} department",
            "Potential data leak from {app_name} - unusual access patterns {verb}",
            "Brute force attacks against {app_name} administration interface - {verb} from {ip_range}.x"
        ]),
        (2, [
            "Expired SSL certificates alert for {app_name} - renewal required within 7 days",
            "Unusual login patterns detected for {departments} user accounts - investigation needed",
            "Security patch required for {severity} vulnerability in {server_types}",
            "Phishing campaign targeting {departments} employees - several suspicious emails reported",
            "Anomalous network traffic detected between {location} office and unknown external IPs"
        ]),
        (1, [
            "Low-risk vulnerability detected in {app_name} test environment",
            "Security best-practice violations in {departments} user password selections",
            "Outdated security software on non-critical {device_type} devices",
            "Minor security misconfiguration on {network_device} in {location} office",
            "Security advisory issued for {app_name} - patch available but no active exploits"
        ])
    ]
}


def random_ip():
    return f"{random.choice(ip_ranges)}.{random.randint(1, 254)}"


def random_timestamp():
    now = datetime.datetime.now()
    days_ago = random.randint(0, 90)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    incident_time = now - datetime.timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return incident_time.strftime("%Y-%m-%d %H:%M:%S")


def add_variation(text):
    
    if random.random() <0.1:
        words = text.split()
        if words:
            idx = random.randint(0, len(words) - 1)
            if random.random() <0.5 and len(words[idx]) > 3:
                
                char_pos = random.randint(1, len(words[idx]) - 2)
                words[idx] = words[idx][:char_pos] + random.choice('abcdefghijklmnopqrstuvwxyz') + words[idx][char_pos+1:]
            else:
                
                words[idx] = words[idx].upper() if random.random() < 0.5 else words[idx].lower()
            text = ' '.join(words)
    
    
    if random.random() < 0.15:
        urgency_prefixes = ['URGENT: ', 'PRIORITY: ', 'ATTENTION: ', 'ALERT: ']
        text = random.choice(urgency_prefixes) + text
    
    
    if random.random() < 0.2:
        ticket_refs = [f"[Ticket #{random.randint(10000, 99999)}] ", 
                      f"INC{random.randint(100000, 999999)}: ",
                      f"Ref #{random.randint(1000, 9999)}: "]
        text = random.choice(ticket_refs) + text
    
    return text


incidents = []
for category in CATEGORIES:
    for _ in range(SAMPLES_PER_CATEGORY):
        
        timestamp = random_timestamp()
        
        
        priority_probs = [0.4, 0.3, 0.2, 0.1]  
        priority = np.random.choice(PRIORITIES, p=priority_probs)
        
        
        template_options = templates[category][4 - priority][1]  
        
        
        template_text = random.choice(template_options)
        
        
        try:
            description = template_text.format(
                location=random.choice(locations),
                network_device=random.choice(network_devices) if '{network_device}' in template_text else None,
                server_types=random.choice(server_types) if '{server_types}' in template_text else None,
                raid_level=random.choice(raid_levels) if '{raid_level}' in template_text else None,
                db_type=random.choice(db_types) if '{db_type}' in template_text else None,
                app_name=random.choice(app_names) if '{app_name}' in template_text else None,
                device_type=random.choice(device_types) if '{device_type}' in template_text else None,
                event=random.choice(events) if '{event}' in template_text else None,
                departments=random.choice(departments) if '{departments}' in template_text else None,
                severity=random.choice(severity_words) if '{severity}' in template_text else None,
                verb=random.choice(verbs) if '{verb}' in template_text else None,
                time=timestamp if '{time}' in template_text else None,
                error_code=random.choice(error_codes) if '{error_code}' in template_text else None,
                ip_range=random.choice(ip_ranges) if '{ip_range}' in template_text else None,
                attackers=random.choice(attackers) if '{attackers}' in template_text else None
            )
            
            
            description = add_variation(description)
            
            incidents.append({
                'description': description,
                'category': category,
                'priority': priority,
                'timestamp': timestamp
            })
        except KeyError as e:
            print(f"Error with template: {template_text}, Error: {e}")
            continue


df = pd.DataFrame(incidents)
df = df.sample(frac=1).reset_index(drop=True)  
df.to_csv(OUTPUT_FILE, index=False)
print(f"Generated dataset with {len(df)} incidents at {OUTPUT_FILE}")
print(f"Sample of generated data:")
print(df.head())


print("\nData Statistics:")
print(f"Total incidents: {len(df)}")
print(f"Categories distribution:\n{df['category'].value_counts()}")
print(f"Priorities distribution:\n{df['priority'].value_counts()}")