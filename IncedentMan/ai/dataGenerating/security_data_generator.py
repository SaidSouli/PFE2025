import pandas as pd
import random

INCIDENT_TAXONOMY = {
    'SECURITY': {
        'subcategories': {
            'Network Attacks': {
                'issues': [
                    'IP spoofing attack', 'ARP poisoning breach', 'TCP session hijacking incident',
                    'Port scanning intrusion', 'Network sniffer breach', 'Man-in-the-Middle intrusion',
                    'SYN flooding breach', 'Suspicious port sweep attack', 'UDP port scan intrusion'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3]
            },
            'Traffic Interception': {
                'issues': [
                    'Unauthorized packet sniffing breach', 'Clear text password interception', 
                    'Network traffic analysis breach', 'Promiscuous mode NIC intrusion',
                    'Suspicious ARP broadcast attack', 'Network eavesdropping breach'
                ],
                'priority_weights': [0.1, 0.3, 0.4, 0.2]
            },
            'Session Attacks': {
                'issues': [
                    'TCP hijacking breach', 'Session token theft', 'Connection sequence prediction attack',
                    'Transparent relay breach', 'Forced session termination attack',
                    'Sequence number prediction breach'
                ],
                'priority_weights': [0.2, 0.3, 0.3, 0.2]
            },
            'Protocol Attacks': {
                'issues': [
                    'ARP cache poisoning attack', 'MAC address spoofing breach', 'DNS poisoning intrusion',
                    'ICMP redirect breach', 'Protocol manipulation attack',
                    'Unauthorized ARP spoofing'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3]
            },
            'Service Interruption': {
                'issues': [
                    'DoS attack breach', 'Security-related service unavailability',
                    'Network flood intrusion', 'Resource exhaustion attack',
                    'Bandwidth saturation breach'
                ],
                'priority_weights': [0.05, 0.1, 0.25, 0.6]
            },
            'Data Manipulation': {
                'issues': [
                    'Packet modification attack', 'Data integrity security breach',
                    'Unauthorized packet injection attack', 'Traffic manipulation intrusion',
                    'Protocol state manipulation breach'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3]
            },
            'Malware': {
                'issues': [
                    'Ransomware infection', 'Virus outbreak attack', 'Trojan infection breach', 'Spyware intrusion', 'Adware infection breach',
                    'Fileless malware infection', 'Cryptojacking breach', 'Polymorphic malware attack', 'Zero-day exploit attack',
                    'Worm propagation breach', 'Bootkit infection attack', 'Rootkit intrusion', 'Backdoor infiltration', 'Keylogger intrusion',
                    'Macro virus infiltration', 'Browser hijacker breach', 'Malicious browser extension attack'
                ],
                'priority_weights': [0.05, 0.1, 0.2, 0.65]
            },
            'Phishing': {
                'issues': [
                    'Suspicious phishing campaign', 'Fake login page attack', 'Credential harvesting breach', 'Spear phishing attack',
                    'Whaling campaign breach', 'Smishing attack intrusion', 'Clone phishing breach', 'Voice phishing attack', 'OAuth phishing infiltration',
                    'Fake browser update attack', 'Pharming attack breach', 'Business email compromise attack', 'Malicious QR code breach',
                    'Typosquatting domain attack', 'Search engine phishing breach', 'Fake security alert attack', 'Social media phishing breach'
                ],
                'priority_weights': [0.2, 0.3, 0.4, 0.1]
            },
            'Unauthorized Access': {
                'issues': [
                    'Brute force attack', 'Privilege escalation breach', 'API key compromise', 'Stolen credentials breach', 'Session hijacking attack',
                    'Password spraying breach', 'Credential stuffing attack', 'MFA bypass breach', 'Kerberoasting attack',
                    'Pass-the-hash intrusion', 'Golden ticket breach', 'Shadow admin infiltration', 'Default credential exploitation',
                    'Lateral movement intrusion', 'VPN security breach', 'Remote access tool exploitation', 'Service account compromise attack'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3]
            },
            'Data Breach': {
                'issues': [
                    'Database security exposure', 'File server security compromise', 'Cloud storage security leak', 'Unencrypted data security transmission',
                    'Improper security access controls', 'S3 bucket security misconfiguration', 'API data security exposure', 'Database dump on dark web',
                    'Exfiltration via DNS tunneling attack', 'Customer PII security exposure', 'Payment information security breach', 'Healthcare data security exposure',
                    'Intellectual property theft attack', 'Data loss via email breach', 'Git repository security leak', 'Sensitive document security disclosure',
                    'Unauthorized data download breach'
                ],
                'priority_weights': [0.05, 0.05, 0.1, 0.8]
            },
            'Network Security': {
                'issues': [
                    'Firewall security breach', 'IDS/IPS security alert', 'Unusual security port scanning', 'DDoS security attack', 'Man-in-the-middle security attempt',
                    'DNS security poisoning', 'BGP security hijacking', 'ARP security spoofing', 'Rogue wireless access point breach', 'SSL stripping security attack',
                    'Network segmentation security failure', 'VPN tunnel security compromise', 'Suspicious security traffic', 'Unusual outbound security connection',
                    'Router security configuration breach', 'IPv6 tunnel security abuse', 'Protocol security anomaly'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3]
            },
            'Insider Threat': {
                'issues': [
                    'Data exfiltration by insider', 'Suspicious admin security activity', 'Unauthorized system security configuration',
                    'Abnormal access security pattern', 'Security policy violation', 'Excessive privilege security usage', 'Off-hours system security access',
                    'Mass file deletion security attempt', 'Contractor credential security misuse', 'Database query security anomaly', 'Unusual printing security activity',
                    'Unauthorized software security installation', 'Departing employee data security access', 'Sabotage security attempt', 'Configuration security tampering',
                    'Unusual remote security access'
                ],
                'priority_weights': [0.1, 0.2, 0.5, 0.2]
            },
            'Application Security': {
                'issues': [
                    'SQL injection attack', 'XSS vulnerability exploitation', 'CSRF security attack', 'Insecure deserialization breach',
                    'Broken authentication security flow', 'Path traversal security attempt', 'File inclusion vulnerability exploitation', 'XML external entity attack',
                    'Server-side request forgery breach', 'API rate limiting security bypass', 'Command injection security attempt', 'Open redirect exploitation',
                    'Prototype pollution attack', 'Memory corruption security exploit', 'Security misconfiguration breach', 'Component with security vulnerability',
                    'CORS security misconfiguration'
                ],
                'priority_weights': [0.1, 0.3, 0.4, 0.2]
            },
            'Physical Security': {
                'issues': [
                    'Unauthorized facility security access', 'Device security theft', 'Tailgating security incident', 'Security camera tampering', 'Server room security breach',
                    'Physical access control security bypass', 'Secured area security intrusion', 'Lost company device security', 'Data center environmental security alert',
                    'HVAC system security tampering', 'Badge cloning security attempt', 'Unauthorized device security connection', 'Lock picking security attempt',
                    'Perimeter security breach', 'Vehicle tailgating security', 'Unauthorized after-hours security access'
                ],
                'priority_weights': [0.3, 0.4, 0.2, 0.1]
            },
            'Social Engineering': {
                'issues': [
                    'Pretexting security call', 'Baiting security incident', 'Quid pro quo security attempt', 'Impersonation of executive security breach', 'Vishing security attack',
                    'Watering hole security attack', 'Fake job offer security scam', 'Vendor impersonation security breach', 'Tech support security scam', 'Scareware security tactics',
                    'Hybrid social engineering attack', 'Physical social engineering breach', 'Dumpster diving security incident', 'Shoulder surfing security breach',
                    'Reverse social engineering attack'
                ],
                'priority_weights': [0.2, 0.4, 0.3, 0.1]
            },
            'Cloud Security': {
                'issues': [
                    'Excessive IAM security permissions', 'Misconfigured security group breach', 'Unencrypted cloud storage security', 'Serverless function security vulnerability',
                    'Container escape security attempt', 'Cloud account security takeover', 'Suspicious API security calls', 'Access key security leaked', 'Instance metadata service security abuse',
                    'Cross-tenant security attack', 'Cloud service security misconfiguration', 'Unauthorized resource security creation', 'Shadow IT cloud security usage',
                    'Third-party integration security exposure'
                ],
                'priority_weights': [0.1, 0.3, 0.4, 0.2]
            },
            'Cryptography': {
                'issues': [
                    'Weak encryption security algorithm', 'Key management security failure', 'Certificate expiration security', 'SSL/TLS downgrade attack',
                    'Hash collision security attack', 'Digital signature security forgery', 'Random number generator security weakness', 'Cryptographic implementation security flaw', 
                    'Certificate authority security compromise', 'Self-signed certificate security usage', 'Padding oracle security attack', 'Key rotation security failure', 
                    'Side-channel security attack'
                ],
                'priority_weights': [0.2, 0.3, 0.4, 0.1]
            },
            'IoT Security': {
                'issues': [
                    'IoT device security compromise', 'Default IoT credentials breach', 'Firmware security vulnerability', 'IoT botnet security activity', 'Smart device security hijacking',
                    'Industrial control system security breach', 'SCADA system security anomaly', 'Medical device security tampering', 'Connected camera security compromise',
                    'Smart building system security breach', 'IoT command injection attack', 'OT network security infiltration', 'Zigbee protocol security exploitation'
                ],
                'priority_weights': [0.1, 0.3, 0.4, 0.2]
            },
            'Mobile Security': {
                'issues': [
                    'Rogue mobile application security', 'Mobile malware security breach', 'Jailbreak/root security detection', 'MDM bypass security attempt', 'SMS-based security attack',
                    'Mobile phishing security (Smishing)', 'App store impersonation security', 'Insecure app data security storage', 'Mobile device security exploitation',
                    'Enterprise app sideloading security', 'Mobile device security loss', 'Unauthorized profile security installation', 'Mobile network security attack'
                ],
                'priority_weights': [0.2, 0.3, 0.4, 0.1]
            },
            'Supply Chain': {
                'issues': [
                    'Vendor security compromise attack', 'Software dependency security attack', 'Counterfeit hardware security', 'Compromised software update security',
                    'Third-party service security breach', 'Supply chain malware attack', 'Hardware backdoor security', 'Code signing certificate security theft',
                    'Vendor remote access security abuse', 'Development pipeline security compromise', 'Open source library security compromise'
                ],
                'priority_weights': [0.1, 0.2, 0.5, 0.2]
            },
            'Port Scanning': {
                'issues': [
                    'TCP SYN scan security attack', 'UDP port scan security breach', 'Port sweep security activity',
                    'Service enumeration security attempt', 'Stealth port scan security breach',
                    'Sequential port probe security attack'
                ],
                'priority_weights': [0.5, 0.3, 0.15, 0.05]
            },
            'Authentication Attacks': {
                'issues': [
                    'Password interception security attempt', 'Credential theft security breach',
                    'Authentication bypass security attempt', 'Token manipulation security attack',
                    'Session credential security compromise'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3]
            }
        }
    }
}

# Security-specific vocabulary for descriptions
SECURITY_VOCABULARY = {
    'verbs': [
        'compromise', 'infiltrate', 'exploit', 'breach', 'attack', 
        'infect', 'exfiltrate', 'hijack', 'intercept', 'penetrate'
    ],
    'adjectives': [
        'malicious', 'unauthorized', 'suspicious', 'compromised', 'vulnerable',
        'targeted', 'fraudulent', 'encrypted', 'sensitive', 'critical'
    ],
    'nouns': [
        'attacker', 'exploit', 'vulnerability', 'breach', 'threat', 
        'malware', 'backdoor', 'payload', 'vector', 'credentials'
    ],
    'action_phrases': [
        'isolating affected systems', 'blocking malicious IPs', 'analyzing malware samples',
        'reviewing log files', 'scanning for backdoors', 'resetting compromised accounts',
        'patching vulnerabilities', 'implementing mitigations', 'deploying countermeasures',
        'conducting forensic analysis'
    ]
}

def generate_incidents_dataframe(num_incidents=100) -> pd.DataFrame:
    """Generate a DataFrame with the specified number of security incidents"""
    incidents = []
    
    for _ in range(num_incidents):
        category = 'SECURITY'
        subcat_name = random.choice(list(INCIDENT_TAXONOMY[category]['subcategories'].keys()))
        subcat_data = INCIDENT_TAXONOMY[category]['subcategories'][subcat_name]
        issue = random.choice(subcat_data['issues'])
        
        # Get security-specific vocabulary
        verb = random.choice(SECURITY_VOCABULARY['verbs'])
        adj = random.choice(SECURITY_VOCABULARY['adjectives'])
        noun = random.choice(SECURITY_VOCABULARY['nouns'])
        action = random.choice(SECURITY_VOCABULARY['action_phrases'])
        
        # Security-specific templates with clear category markers
        templates = [
            # Security alerts with category markers
            f"[SECURITY ALERT] {issue} detected. {noun.capitalize()} attempting to {verb} systems.",
            f"[THREAT DETECTION] {issue} identified by security monitoring. {action} in progress.",
            f"[SIEM ALERT] {issue} signature matched from {adj} source. Security team {verb}ing logs.",
            
            # Security team reports
            f"[SEC-NOTICE] Investigating {issue}. {noun.capitalize()} activity detected from {adj} IP.",
            f"[SOC ALERT] {issue} requiring immediate response. {action} to prevent data {verb}ion.",
            f"[THREAT INTEL] {issue} targeting our infrastructure. {adj.capitalize()} actors using {noun} techniques.",
            
            # Critical security alerts
            f"[SECURITY BREACH] Active {issue} detected. Systems {verb}ed by {adj} {noun}. {action}.",
            f"[INCIDENT RESPONSE] {issue} confirmed. Security team handling {adj} breach of {noun}s. {action}.",
            f"[CRITICAL SECURITY] {issue} in progress. Security operations {verb}ing the {adj} {noun}. {action}.",
            f"can't open my email {issue} in progress. Security operations {verb}ing the {adj} {noun}. {action}.",
            f" i got hacked {issue} ",
            f"password leaked {issue}"
        ]
        
        description = random.choice(templates)
        
        # Choose priority based on weights
        priorities = [1, 2, 3, 4]
        priority = random.choices(priorities, weights=subcat_data['priority_weights'])[0]
        
        incidents.append({
            'description': description,
            'category': category,
            'subcategory': subcat_name,
            'priority': priority
        })
    
    df = pd.DataFrame(incidents)
    return df

if __name__ == "__main__":
   
    incidents_df = generate_incidents_dataframe(5000)
    
    
    incidents_df.to_csv("data/security_incidents.csv", index=False)
    
    print("Data saved to 'security_incidents.csv'")