import pandas as pd
import random

INCIDENT_TAXONOMY = {
    'SOFTWARE': {
        'subcategories': {
            'Operating System': {
                'issues': [
                    'Windows blue screen error', 'System crash on startup', 'OS update failure',
                    'Boot loop issue', 'Driver compatibility error', 'Kernel panic',
                    'File system corruption', 'OS freezing randomly', 'Login screen not loading',
                    'Windows activation error', 'OS performance degradation', 'System restore failure',
                    'DLL file missing', 'Registry corruption', 'OS not recognizing hardware',
                    'Blue screen after update', 'OS stuck in safe mode', 'Taskbar not responding',
                    'Start menu not working', 'OS not booting after update'
                ],
                'priority_weights': [0.3, 0.3, 0.3, 0.1]  # Higher weights for OS issues
            },
            'Business Applications': {
                'issues': [
                    'Excel not responding', 'Outlook crashes when sending', 'Teams call quality issues',
                    'SAP transaction error', 'Salesforce sync failure', 'SharePoint access denied',
                    'Oracle database timeout', 'Adobe PDF corruption', 'QuickBooks calculation error',
                    'Slack connection issues', 'Zoom audio problems', 'CRM data sync failure',
                    'Power BI refresh error', 'Database connection timeout', 'ERP system locked up'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1]  # Critical for business operations
            },
            
            'Custom Software': {
                'issues': [
                    'Internal app crash', 'API integration failure', 'Database query timeout',
                    'Report generator error', 'Data import failed', 'Custom script exception',
                    'Web service unavailable', 'Legacy system error', 'Batch process stuck',
                    'Dashboard not updating', 'Workflow automation failed', 'Data validation error'
                ],
                'priority_weights': [0.3, 0.4, 0.2, 0.1]  # Based on business impact

            },
            'Core Functionality': {
                'issues': [
                    'Application keeps crashing', 'Unexpected program freeze', 'Feature not working',
                    'System becomes unresponsive', 'Software glitch in main module', 'Critical function failed',
                    'Program crashes during save', 'Memory leak detected', 'Unexpected behavior',
                    'Process hangs indefinitely', 'Data processing error', 'Core module failure'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1]  # Critical functionality
            },
            'Performance': {
                'issues': [
                    'Severe performance degradation', 'High CPU usage', 'Memory consumption spike',
                    'Application running slowly', 'Database query timeout', 'System resource depletion',
                    'Slow response times', 'Poor scalability issues', 'Processing bottleneck',
                    'Network latency problems', 'Resource exhaustion', 'Threading deadlock'
                ],
                'priority_weights': [0.3, 0.4, 0.2, 0.1]  # Based on impact
            },
            'Integration': {
                'issues': [
                    'API integration failure', 'Third-party service down', 'Data sync error',
                    'Authentication service failed', 'Integration point timeout', 'API version mismatch',
                    'Legacy system compatibility', 'Middleware communication error', 'Service discovery failed',
                    'Data format mismatch', 'Integration pipeline broken', 'Interface contract violation'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1]  # Critical for business
            },
            'User Interface': {
                'issues': [
                    'UI elements not responding', 'Screen rendering issue', 'Layout broken',
                    'Button functionality failed', 'Form submission error', 'Display corruption',
                    'Navigation menu broken', 'CSS styling failed', 'Interface not loading',
                    'Accessibility feature broken', 'UI component crash', 'Interactive element failed'
                ],
                'priority_weights': [0.2, 0.3, 0.3, 0.2]  # User-facing issues
            },
            'Data Management': {
                'issues': [
                    'Data corruption detected', 'Database connection lost', 'Data synchronization failed',
                    'Backup process error', 'Data integrity violation', 'Storage capacity critical',
                    'Database deadlock', 'Data migration error', 'Replication lag critical',
                    'Cache invalidation error', 'Data loss reported', 'Storage system failure'
                ],
                'priority_weights': [0.5, 0.3, 0.15, 0.05]  # Data critical
            },
            'Configuration': {
                'issues': [
                    'Environment config error', 'Settings corruption', 'Invalid configuration',
                    'Config sync failure', 'Environment mismatch', 'Deploy config missing',
                    'Parameter validation error', 'Config version conflict', 'Setup process failed',
                    'Configuration override error', 'Settings not persisted', 'Config file corruption',
                    'Package dependency conflicts', 'Conflicting versions and dependencies', 'Library version mismatch',
                    'DLL version conflict', 'Incompatible module versions', 'Package requirement conflicts',
                    'Version resolution failure', 'Dependency tree conflict', 'Framework version incompatibility',
                    'conflicting versions and dependencies'
    
                ],
                'priority_weights': [0.3, 0.3, 0.3, 0.1]
            }
        }
    }
}

def generate_incident() -> dict:
    """Generate a software incident with realistic user-reported descriptions"""
    category = 'SOFTWARE'
    subcat_name = random.choice(list(INCIDENT_TAXONOMY[category]['subcategories'].keys()))
    subcat_data = INCIDENT_TAXONOMY[category]['subcategories'][subcat_name]
    issue = random.choice(subcat_data['issues'])
    
    # User emotion and urgency indicators
    urgency_prefixes = [
        "URGENT: Can't access", "HELP - System down", "CRITICAL: Lost work in",
        "Emergency - Can't continue", "Important: Problems with",
        "System error preventing work", "Immediate assistance needed:",
        "Production blocked by", "Time sensitive issue:",
        "!!Losing work!! -"
        "CRITICAL ALERT:", "PRODUCTION DOWN:", "URGENT - Customer Impact:",
        "HIGH PRIORITY:", "IMMEDIATE ACTION REQUIRED:",
        "SYSTEM ALERT:", "BLOCKING ISSUE:",
        "P1 INCIDENT:", "MAJOR INCIDENT:",
        "EMERGENCY TICKET:"
    ]
    
    # Business impact statements
    impact_statements = [
        "entire team blocked", "client deliverable at risk",
        "can't process customer orders", "meeting starts in 15 minutes",
        "losing billable hours", "deadline approaching",
        "production pipeline stopped", "customer demo affected",
        "revenue impacting issue", "critical path blocked"
        "blocking entire department workflow",
        "multiple teams affected and deadlines at risk",
        "customer-facing services impacted",
        "revenue-generating system affected",
        "critical business process blocked",
        "preventing order processing",
        "impacting customer experience",
        "multiple clients reporting issues",
        "production pipeline completely stopped",
        "business operations severely affected"
    ]
    
    # Technical observations
    tech_observations = [
        "error message attached", "tried clearing cache",
        "happens every time I", "started after update",
        "reproduced on multiple PCs", "rebooted three times",
        "checked system logs", "other users affected too",
        "getting timeout errors", "tried different browser"
        "error logs attached in screenshot",
        "issue reproducible in all environments",
        "multiple users reporting same problem",
        "started after recent deployment",
        "console showing multiple errors",
        "memory usage growing exponentially",
        "all retry attempts failed",
        "system metrics showing anomalies",
        "error rate spiking in monitoring",
        "logs showing cascade of failures",
        "dependency resolution failed", 
        "version conflict detected", "incompatible packages found",
        "libraries clashing with each other", "module version requirements conflict",
    ]
    
    # Software-specific symptoms
    software_symptoms = {
        'Operating System': [
            "screen goes black", "keeps rebooting automatically",
            "extremely slow response", "won't load user profile",
            "stuck at login screen", "showing error code",
            "programs won't launch", "desktop icons missing",
            "task manager not responding", "windows explorer crashing"
        ],
        'Business Applications': [
            "can't save changes", "sync failed multiple times",
            "formula calculation wrong", "report shows errors",
            "data missing from view", "application freezes",
            "can't export data", "dashboard not loading",
            "integration broken", "preview not working"
        ],
        'Custom Software': [
            "process stuck at 99%", "invalid data error",
            "workflow stopped", "script execution failed",
            "memory usage spikes", "constant timeout errors",
            "duplicate entries created", "audit log errors",
            "background job failed", "validation exceptions"
        ],
        'Core Functionality': [
            "application immediately crashes on launch",
            "critical feature completely non-functional",
            "system automatically closing all sessions",
            "core process terminated unexpectedly",
            "main module throwing unhandled exceptions"
        ],
        'Performance': [
            "response time exceeded 30 seconds",
            "CPU usage at 100% across all instances",
            "memory leak causing system slowdown",
            "database queries timing out consistently",
            "application freezing under normal load"
        ],
        'Integration': [
            "API returning 500 errors consistently",
            "third-party integration completely down",
            "data flow between systems broken",
            "authentication service rejecting all requests",
            "middleware dropping connections"
        ],
        'User Interface': [
            "users unable to access main interface",
            "critical buttons non-responsive",
            "forms failing to submit data",
            "UI completely broken in production",
            "user sessions terminating randomly"
        ],
        'Data Management': [
            "database showing corruption markers",
            "critical data missing from records",
            "backup process failing consistently",
            "data inconsistency across services",
            "storage system rejecting writes"
        ],
        'Configuration': [
            "production config completely invalid",
            "environment variables missing critical values",
            "configuration service not responding",
            "deploy pipeline rejected all configs",
            "settings rollback failed"
        ]
    }

    templates = [
        # Urgent format
        f"{random.choice(urgency_prefixes)} {issue} ! {random.choice(impact_statements)}",
        
        # Technical detail format
        f"{issue} ! {random.choice(tech_observations)} - {random.choice(impact_statements)}",
        
        # Symptom format
        f"{issue}: {random.choice(software_symptoms[subcat_name])} - {random.choice(impact_statements)}",
        
        # Combination format
        f"{random.choice(urgency_prefixes)} {issue} - {random.choice(software_symptoms[subcat_name])} - {random.choice(tech_observations)}",
        
        # Time-sensitive format
        f"Time sensitive: {issue} - {random.choice(impact_statements)} - {random.choice(software_symptoms[subcat_name])}",
        
        # Detailed observation format
        f"{issue} ({random.choice(tech_observations)}) ; {random.choice(software_symptoms[subcat_name])} - {random.choice(impact_statements)}",
        f"{random.choice(urgency_prefixes)} {issue} !!! {random.choice(impact_statements)}",
        
        # Technical detail with impact
        f"{issue} - {random.choice(tech_observations)} !{random.choice(impact_statements)}",
        
        # Symptom with technical detail
        f"{issue}: {random.choice(software_symptoms[subcat_name])} - {random.choice(tech_observations)}",
        
        # Comprehensive alert
        f"{random.choice(urgency_prefixes)} {issue} - {random.choice(software_symptoms[subcat_name])} - {random.choice(impact_statements)}",
        
        # Time-critical format
        f"Time-critical alert: {issue} ! {random.choice(impact_statements)} - {random.choice(software_symptoms[subcat_name])}",
        
        # Detailed technical format
        f"{issue} ({random.choice(tech_observations)}) . {random.choice(software_symptoms[subcat_name])} . {random.choice(impact_statements)}"
        f"I can't open my machine. {issue}",
        f"I'm having trouble opening my machine. {issue}",
        
        
    ]
    
    return {
        'description': random.choice(templates),
        'category': category,
        'subcategory': subcat_name,
        'priority': random.choices(
            [1, 2, 3, 4],  # P1 is highest priority
            weights=subcat_data['priority_weights']
        )[0]
    }

def generate_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Generate software incident dataset"""
    data = []
    for _ in range(num_samples):
        data.append(generate_incident())
    
    df = pd.DataFrame(data)
    df.to_csv('data/software_incidents.csv', index=False)
    return df

if __name__ == "__main__":
    generate_dataset()