import pandas as pd
import random
from datetime import datetime, timedelta

NETWORK_TAXONOMY = {
    'Connectivity': {
        'issues': [
            'Network outage',
            'High latency',
            'Packet loss',
            'Intermittent connectivity',
            'Bandwidth saturation',
            'Network congestion',
            'Link flapping',
            'Interface errors',
            'Network loop',
            'MAC address flooding',
            'Port failure',
            'Switch port error',
            'Network card malfunction',
            'Duplex mismatch',
            'MTU misconfiguration'
        ],
        'priority_weights': [0.15, 0.35, 0.35, 0.15],
        'network_identifiers': [
            'OSI layer 1-3 issue',
            'network pipe',
            'backbone connection',
            'WAN link',
            'transit network',
            'core routing',
            'network fabric'
        ]
    },
    'WiFi': {
        'issues': [
            'Weak signal strength',
            'WiFi interference',
            'Access point failure',
            'Authentication failure',
            'SSID not broadcasting',
            'Channel congestion',
            'WiFi coverage gap',
            'Rogue access point detected',
            'WPA authentication error',
            'WiFi client disconnections',
            'Beacon frame issues',
            'WiFi band interference',
            'Roaming issues',
            'Hidden node problem',
            'WiFi throughput degradation'
        ],
        'priority_weights': [0.2, 0.3, 0.3, 0.2],
        'network_identifiers': [
            'wireless network',
            'RF environment',
            'wireless spectrum',
            '802.11 protocol',
            'WiFi SSID',
            'wireless AP',
            'WiFi channel'
        ]
    },
    'IP Addressing': {
        'issues': [
            'IP address conflict',
            'DHCP pool exhaustion',
            'Invalid IP configuration',
            'DNS resolution failure',
            'Default gateway unreachable',
            'Subnet mask misconfiguration',
            'DHCP server failure',
            'IP allocation failure',
            'Duplicate IP address',
            'DHCP lease expiration',
            'Static IP conflict',
            'DHCP scope depletion',
            'IP routing loop',
            'ARP table corruption',
            'NAT configuration error'
        ],
        'priority_weights': [0.25, 0.35, 0.25, 0.15],
        'network_identifiers': [
            'TCP/IP stack',
            'IP allocation',
            'network addressing',
            'IP schema',
            'address space',
            'CIDR block',
            'subnet topology'
        ]
    },
    'Physical Connectivity': {
        'issues': [
            'Cable disconnection',
            'Fiber optic damage',
            'Bad network cable',
            'Port physical damage',
            'Cross-talk interference',
            'Cable attenuation',
            'Patch panel failure',
            'Connector damage',
            'Physical layer interference',
            'Network jack damage',
            'Cable length exceeded',
            'EMI interference',
            'Ground loop issue',
            'Switch hardware failure',
            'Physical media converter failure'
        ],
        'priority_weights': [0.3, 0.3, 0.25, 0.15],
        'network_identifiers': [
            'physical medium',
            'cabling infrastructure',
            'patch connections',
            'patch panel',
            'physical layer',
            'copper/fiber link',
            'network termination'
        ]
    },
    'Network Performance': {
        'issues': [
            'Slow network response',
            'High network utilization',
            'Bandwidth bottleneck',
            'Application timeout',
            'Network congestion',
            'Slow file transfer',
            'High round-trip time',
            'Buffer overflow',
            'QoS misconfiguration',
            'Traffic shaping issues',
            'Network throttling',
            'Bandwidth saturation',
            'Protocol performance issues',
            'Memory buffer exhaustion',
            'CPU bottleneck on network device'
        ],
        'priority_weights': [0.2, 0.4, 0.3, 0.1],
        'network_identifiers': [
            'network throughput',
            'network metrics',
            'traffic patterns',
            'bandwidth utilization',
            'network QoS',
            'traffic engineering',
            'flow control'
        ]
    },
   'DNS': {
        'issues': [
            'DNS resolution failure',
            'DNSSEC validation error',
            'DNS cache poisoning',
            'Recursive query failure',
            'Zone transfer error',
            'DNS propagation delay',
            'Name server unavailable',
            'DNS record misconfiguration',
            'Split-horizon DNS failure',
            'DNS amplification attack'
        ],
        'priority_weights': [0.2, 0.3, 0.3, 0.2],
        'network_identifiers': [
            'domain name system',
            'name resolution',
            'DNS hierarchy',
            'DNS zone',
            'nameserver configuration',
            'DNS protocol',
            'FQDN resolution'
        ]
    },
    'Enterprise Services': {
        'issues': [
            'Active Directory connectivity failure',
            'Exchange server network issues',
            'SharePoint access problems',
            'Network drive mapping failure',
            'Print server connectivity',
            'File sharing service disruption',
            'Intranet access issues',
            'Remote desktop service failure',
            'VPN capacity overload',
            'SSO service disruption',
            'Cloud service connectivity',
            'Unified communications failure',
            'Video conferencing service down',
            'Application server network issue',
            'Database replication lag'
        ],
        'priority_weights': [0.25, 0.35, 0.25, 0.15],
        'network_identifiers': [
            'enterprise application',
            'network services',
            'business systems',
            'corporate network',
            'enterprise infrastructure',
            'business connectivity',
            'mission-critical applications'
        ]
    }
}

# Network-specific vocabulary for descriptions
NETWORK_VOCABULARY = {
    'verbs': [
        'troubleshoot', 'diagnose', 'route', 'connect', 'ping', 
        'trace', 'resolve', 'configure', 'optimize', 'restart'
    ],
    'adjectives': [
        'slow', 'disconnected', 'intermittent', 'degraded', 'congested',
        'unresponsive', 'saturated', 'unstable', 'laggy', 'misconfigured'
    ],
    'nouns': [
        'router', 'switch', 'gateway', 'connection', 'bandwidth', 
        'throughput', 'latency', 'packet', 'interface', 'link'
    ],
    'action_phrases': [
        'restarting equipment', 'checking cable connections', 'pinging endpoints',
        'running traceroute', 'monitoring traffic', 'updating configurations',
        'testing connectivity', 'measuring bandwidth', 'checking interface stats',
        'validating network routes'
    ]
}

def generate_description(subcategory: str, issue: str, taxonomy_data: dict) -> str:
    """Generate a detailed incident description with distinct network-specific markers"""
    locations = [
        'main office',
        'branch location',
        'remote site',
        'data center',
        'server room',
        'manufacturing floor',
        'warehouse',
        'corporate headquarters',
        'satellite office',
        'client site'
    ]
    
    impacts = [
        'causing service disruption',
        'affecting network performance',
        'impacting user connectivity',
        'causing system slowdown',
        'resulting in connection failures',
        'creating access issues',
        'leading to timeout errors',
        'causing packet drops',
        'affecting multiple users',
        'degrading service quality'
    ]
    
    # Get network-specific identifiers
    network_identifier = random.choice(taxonomy_data['network_identifiers'])
    
    # Get network-specific vocabulary
    verb = random.choice(NETWORK_VOCABULARY['verbs'])
    adj = random.choice(NETWORK_VOCABULARY['adjectives'])
    noun = random.choice(NETWORK_VOCABULARY['nouns'])
    action = random.choice(NETWORK_VOCABULARY['action_phrases'])
    
    # Network-specific templates with clear category markers
    network_templates = [
        f"[NETWORK ALERT] {issue} detected in {random.choice(locations)} {network_identifier}. {verb.capitalize()} required for {adj} {noun}.",
        
        f"[NETOPS] {issue} reported on {network_identifier} at {random.choice(locations)}. Team is {action}.",
        
        f"[NETWORK/{subcategory}] {issue} detected during {network_identifier} monitoring. {noun.capitalize()} is {adj}, needs {verb}ing.",
        
        f"[NETWORK INCIDENT] {issue} related to {network_identifier} {random.choice(impacts)}. {verb.capitalize()}ing {noun} to resolve.",
        
        f"[NET TICKET] {issue} in {network_identifier} at {random.choice(locations)}. {action} to restore connectivity.",
        
        f"[NETWORK MONITOR] {issue} affecting {network_identifier}. {adj.capitalize()} {noun} requires immediate {verb}ing.",
        
        f"[NETOPS BULLETIN] Multiple reports of {issue} with {network_identifier}. Network team {action}.",
        
        f"[NETWORK SUPPORT] {issue} detected on {network_identifier}. Please {verb} the {noun} to restore service.",
        
        f"[NET-{subcategory}] The {network_identifier} is experiencing {adj} issues. Users reporting {issue}.",
        
        f"[NETWORK DIAG] Please help with {network_identifier} problems. {verb.capitalize()}ing shows {issue}.",
        
        f"[NETWORK OUTAGE] {network_identifier} experiencing {issue}. {action} in progress.",
        
        f"[NET SERVICE] Keep losing connection to {network_identifier}. {verb.capitalize()}ing identified {issue}.",
        
        f"[NETWORK OPS] Without {network_identifier}, departments can't work! Identified as {issue}, requires {verb}ing.",
        
        f"[NETOPS PERF] {network_identifier} is {adj}! Investigation shows {issue}. {action} to improve performance.",
        
        f"[NETWORK CONN] Been trying to connect to {network_identifier} for hours. {verb.capitalize()}ed as {issue}.",
        
        f"[NET INTERNAL] Can't load internal sites - {network_identifier} showing signs of {issue}. {verb.capitalize()} required.",
        
        f"[NETWORK STABILITY] {network_identifier} keeps dropping every few minutes. {issue} confirmed by {action}.",
        
        f"[NET-ACCESS] Can't connect to the {network_identifier} - device shows '{adj}' due to {issue}.",
        
        f"[NETWORK FAILURE] No connectivity on all devices connected to {network_identifier}. Root cause: {issue}.",
        
        f"[NETWORK URGENT] The {network_identifier} is down affecting deadlines! {issue} identified through {verb}ing.",
        
        f"[NET PRIORITY] Fix {network_identifier} ASAP - teams can't work due to {issue}. {action} needed immediately.",
        
        f"[NETWORK-911] {network_identifier} is completely non-responsive. Need immediate {verb}ing. Cause: {issue}.",
        
        f"[NETOPS CRITICAL] {network_identifier} connectivity broken - {action} shows {issue} as root cause.",
        
        f"[NETWORK DIAGNOSTIC] {network_identifier} test failure - {verb}ing confirmed {issue} in the {noun}.",
        
        f"[NET DEPARTMENT] Not sure if it's isolated, but the {network_identifier} has {issue} affecting {adj} connections.",
        
        f"[NETWORK CHANGE] {network_identifier} was operational yesterday, now showing {issue}. Needs {verb}ing.",
        
        f"[NET RESOURCE] Can't access shared resources via {network_identifier} - {noun} reports '{adj} error' related to {issue}.",
        
        f"[NETWORK VPN] {network_identifier} keeps disconnecting every few minutes due to {issue}. {action} in progress.",
        
        f"[NET-DNS] Getting 'DNS lookup failed' errors on {network_identifier}. Root cause: {issue}.",
        
        f"[NETWORK STATUS] {network_identifier} says 'connected, no internet' because of {issue}. {verb.capitalize()} needed.",
        
        f"[NETWORK IMPACT] This is affecting productivity - {network_identifier} needs {verb}ing! Issue: {issue}.",
        
        f"[NET LATENCY] Users experiencing delays with {adj} {network_identifier} connection caused by {issue}.",
        
        f"[NETWORK NOTICE] Unusual behavior with {network_identifier} today. Confirmed as {issue} through {action}.",
        
        f"[NET QUERY] What's wrong with the {network_identifier}? {verb.capitalize()}ing shows symptoms of {issue}.",
        
        f"[NETWORK REQUEST] Could IT please check the {network_identifier}? It's very {adj} due to {issue}.",
        
        f"[NET ASSIST] Having trouble connecting to the {network_identifier}. {verb.capitalize()}is shows {issue}.",
        
        f"[NETWORK HELPDESK] Would you mind {verb}ing the {network_identifier} issues? Related to {issue}.",
        
        f"[NET INFO] Wanted to inform you that the {network_identifier} is down because of {issue}. {action} initiated."
    ]
    
    return random.choice(network_templates)

def generate_incident() -> dict:
    """Generate a single network incident record"""
    subcategory = random.choice(list(NETWORK_TAXONOMY.keys()))
    taxonomy = NETWORK_TAXONOMY[subcategory]
    
    issue = random.choice(taxonomy['issues'])
    
    return {
        'description': generate_description(subcategory, issue, taxonomy),
        'category': 'NETWORK',
        'subcategory': subcategory,
        'priority': random.choices(
            [1, 2, 3, 4],
            weights=taxonomy['priority_weights']
        )[0]
    }

def generate_dataset(num_samples: int = 1000) -> pd.DataFrame:
    """Generate network incident dataset"""
    data = [generate_incident() for _ in range(num_samples)]
    df = pd.DataFrame(data)
    
    # Ensure exact column order
    return df[['description', 'category', 'subcategory', 'priority']]

if __name__ == "__main__":
    # Generate and save data
    num_samples = 5000  # Maintained sample size
    df = generate_dataset(num_samples)
    
    # Save to CSV
    df.to_csv('data/network_incidents.csv', index=False)
    
    # Print dataset statistics
    print("\nNetwork Incident Dataset Generated")
    print("-" * 30)
    print(f"Total incidents: {len(df)}")
    print("\nSubcategory Distribution:")
    print(df['subcategory'].value_counts())
    print("\nPriority Distribution:")
    print(df['priority'].value_counts().sort_index())
    
    # Print example records
    print("\nExample Records:")
    print(df.head().to_string())