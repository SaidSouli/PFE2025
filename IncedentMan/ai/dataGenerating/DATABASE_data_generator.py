import pandas as pd
import random

INCIDENT_TAXONOMY = {
    'DATABASE': {
        'subcategories': {
            'Availability': {
                'issues': [
                    'Database server down', 'Connection pool exhausted', 'Database timeout', 
                    'Instance not responding', 'High wait times', 'Database service crashed',
                    'Replica lag critical', 'Database hung', 'Connection refused', 
                    'Database cluster unavailable', 'Instance terminated unexpectedly', 'Database failover failed'
                ],
                'priority_weights': [0.5, 0.3, 0.15, 0.05]  # Availability is critical
            },
            'Performance': {
                'issues': [
                    'Slow query execution', 'Index scan bottleneck', 'Query timeout', 
                    'Database CPU overload', 'High I/O wait', 'Memory pressure',
                    'Table lock contention', 'Blocking transactions', 'Excessive temp usage', 
                    'Poor query plan', 'Buffer cache thrashing', 'Log write delays'
                ],
                'priority_weights': [0.3, 0.4, 0.2, 0.1]  # Performance affects everyone
            },
            'Data Integrity': {
                'issues': [
                    'Data corruption detected', 'Inconsistent query results', 'Foreign key violation', 
                    'Orphaned records found', 'Duplicate primary keys', 'Constraint error',
                    'Data type mismatch', 'Truncated data values', 'Missing required fields', 
                    'Transaction log corruption', 'Referential integrity failure', 'Data validation error'
                ],
                'priority_weights': [0.5, 0.3, 0.15, 0.05]  # Data integrity is mission critical
            },
            'Capacity': {
                'issues': [
                    'Database storage full', 'Tablespace at capacity', 'Log files filled disk', 
                    'Connection limit reached', 'IOPS limit exceeded', 'Query memory exceeded',
                    'Temp space exhausted', 'Transaction log full', 'Backup space depleted', 
                    'Datafile autoextend failed', 'Rollback segment full', 'Archivelog destination full'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1]  # Capacity issues can be severe
            },
            'Backup & Recovery': {
                'issues': [
                    'Backup job failed', 'Database restore failed', 'Point-in-time recovery error', 
                    'Corrupt backup file', 'Incomplete backup set', 'Transaction log backup failed',
                    'Recovery stuck at rollback', 'Differential backup corrupted', 'Backup validation failed', 
                    'RMAN error', 'Log shipping failure', 'Recovery missing logs'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1]  # Critical for business continuity
            },
            'Configuration': {
                'issues': [
                    'Parameter file corruption', 'Invalid database config', 'Memory settings misconfigured', 
                    'Incompatible parameter values', 'Invalid connection string', 'Character set mismatch',
                    'Listener misconfiguration', 'Instance parameter error', 'Database link failure', 
                    'Authentication method conflict', 'Invalid init parameters', 'Configuration file missing'
                ],
                'priority_weights': [0.3, 0.3, 0.3, 0.1]  # Configuration impacts everything
            },
            'Replication': {
                'issues': [
                    'Replication lag critical', 'Replication stopped', 'Data sync conflict', 
                    'Master-slave desync', 'Replication topology broken', 'CDC process failed',
                    'Logical replication error', 'Publication/subscription error', 'Log reader agent failing', 
                    'Distribution agent stalled', 'Change tracking failed', 'Replication queue overflowed'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1]  # Critical for distributed systems
            },
            'Schema Management': {
                'issues': [
                    'Schema change failed', 'DDL operation hung', 'Invalid object reference', 
                    'Broken view definition', 'Failed stored procedure', 'Function compilation error',
                    'Materialized view refresh failed', 'Index rebuild error', 'Partition operation failed', 
                    'Schema version conflict', 'Sequence generation error', 'Trigger execution failure'
                ],
                'priority_weights': [0.3, 0.3, 0.3, 0.1]  # Schema issues can block work
            },
            'User Access': {
                'issues': [
                    'Permission denied error', 'User account locked', 'Role assignment failed', 
                    'Grant operation failed', 'Invalid credentials', 'Session limit reached',
                    'Password expired', 'Unauthorized schema access', 'Privilege escalation detected', 
                    'User quota exceeded', 'Failed login attempts', 'Resource limit exceeded'
                ],
                'priority_weights': [0.3, 0.3, 0.3, 0.1]  # Access issues block productivity
            },
            'Monitoring & Logging': {
                'issues': [
                    'Alert log filled with errors', 'Monitoring agent disconnected', 'Audit failure', 
                    'Database diagnostics not available', 'Performance metrics missing', 'Query logging failed',
                    'Error log truncation', 'Deadlock detection issues', 'Status dashboard unresponsive', 
                    'Log rotation failure', 'Event notification failure', 'Health check reporting errors'
                ],
                'priority_weights': [0.2, 0.3, 0.4, 0.1]  # Affects visibility but not direct operation
            }
        }
    }
}

def generate_incident() -> dict:
    """Generate a database incident with realistic user-reported descriptions"""
    category = 'DATABASE'
    subcat_name = random.choice(list(INCIDENT_TAXONOMY[category]['subcategories'].keys()))
    subcat_data = INCIDENT_TAXONOMY[category]['subcategories'][subcat_name]
    issue = random.choice(subcat_data['issues'])
    
    # User emotion and urgency indicators
    urgency_prefixes = [
        "URGENT: Database", "HELP - DB down", "CRITICAL: Database error in",
        "Emergency - Can't access", "Important: Problems with database",
        "Database error preventing work", "Immediate database assistance needed:",
        "Production DB blocked by", "Time sensitive DB issue:",
        "!!Data corruption!! -",
        "CRITICAL DB ALERT:", "PRODUCTION DATABASE DOWN:", "URGENT - Database Customer Impact:",
        "HIGH PRIORITY DB ISSUE:", "IMMEDIATE ACTION REQUIRED: Database",
        "DATABASE ALERT:", "BLOCKING DATABASE ISSUE:",
        "P1 DB INCIDENT:", "MAJOR DATABASE INCIDENT:",
        "EMERGENCY DATABASE TICKET:"
    ]
    
    # Business impact statements
    impact_statements = [
        "all queries failing", "transactions not processing",
        "can't process customer orders in database", "entire ERP system down",
        "all data access blocked", "reports not generating",
        "database-dependent services down", "customer data unavailable",
        "finance system can't access data", "business intelligence platform affected",
        "entire company database access affected",
        "multiple teams blocked from data access",
        "customer-facing database services impacted",
        "revenue-generating database down",
        "critical business processes blocked by DB issue",
        "preventing order processing in database",
        "impacting all database-dependent services",
        "multiple clients affected by database outage",
        "production database pipeline completely stopped",
        "business operations severely affected due to database issues"
    ]
    
    # Technical observations
    tech_observations = [
        "error code in logs", "tried restarting instance",
        "happens on all queries", "started after morning maintenance",
        "all attempts to connect fail", "rebooted database server",
        "checked database logs", "multiple instances affected",
        "getting ORA-errors", "tried different connection methods",
        "error logs attached in screenshot",
        "issue reproducible in all database environments",
        "multiple users reporting same database problem",
        "started after recent schema update",
        "database console showing multiple errors",
        "memory usage growing exponentially on DB server",
        "all retry attempts to database failed",
        "database metrics showing anomalies",
        "error rate spiking in DB monitoring",
        "logs showing cascade of database failures"
    ]
    
    # Database-specific symptoms by subcategory
    database_symptoms = {
        'Availability': [
            "connection attempts timing out", "service completely unresponsive",
            "database process not running", "can't establish any connections",
            "database service not listed", "connection string failing",
            "socket connection refused", "database port not responding",
            "listener not accepting connections", "instance crashed with core dump"
        ],
        'Performance': [
            "queries taking 10+ minutes", "timeouts on simple selects",
            "CPU usage at 100 on DB server", "exponential query time increase",
            "deadlocks occurring frequently", "massive I/O wait times",
            "query plans suddenly inefficient", "index not being used",
            "parameter queries failing", "execution plan regression"
        ],
        'Data Integrity': [
            "records missing primary keys", "foreign key violations",
            "query results inconsistent", "checksums failing",
            "unexpected NULL values", "truncated data in fields",
            "record counts don't match", "orphaned relational records",
            "data type conversion errors", "constraint violations"
        ],
        'Capacity': [
            "disk space critical on DB server", "can't extend tablespace",
            "log files filling entire volume", "unable to allocate new blocks",
            "connection pool exhausted", "query memory grants failing",
            "temp tablespace full errors", "no space left for transactions",
            "autoextend failed due to disk full", "max file size reached"
        ],
        'Backup & Recovery': [
            "backup job failing every night", "can't restore from backup set",
            "point-in-time recovery failing", "transaction logs missing",
            "RMAN reporting corrupt blocks", "recovery operation hanging",
            "can't access backup files", "inconsistent backup state",
            "log sequence gap detected", "archive logs missing"
        ],
        'Configuration': [
            "parameter file can't be read", "settings lost after restart",
            "connection string rejected", "incompatible character sets",
            "initialization parameters invalid", "memory settings causing crashes",
            "NLS parameters incorrect", "listener configuration invalid",
            "service registration failed", "SPFILE corruption detected"
        ],
        'Replication': [
            "replica several hours behind master", "replication process terminated",
            "conflicting updates in multi-master", "replication queue backing up",
            "change data capture process failed", "publisher/subscriber mismatch",
            "log reader agent failing", "distribution latency critical",
            "circular replication error", "replication topology broken"
        ],
        'Schema Management': [
            "DDL operation blocked by locks", "invalid object references",
            "stored procedure compilation errors", "broken view definitions",
            "partition operation failed", "index unusable after update",
            "materialized view refresh hanging", "trigger causing exceptions",
            "sequence exhausted available values", "schema validation errors"
        ],
        'User Access': [
            "suddenly can't access any tables", "permissions revoked unexpectedly",
            "role assignments disappeared", "user accounts locked",
            "exceeding resource quotas", "login failures for all users",
            "password verification failing", "proxy authentication errors",
            "grant operations failing", "privileged access revoked"
        ],
        'Monitoring & Logging': [
            "alert log flooded with errors", "no monitoring data available",
            "audit trail missing entries", "diagnostic pack not functioning",
            "wait event statistics unavailable", "AWR reports not generating",
            "metric collection failed", "performance counters reset",
            "deadlock detector not working", "trace files not being created"
        ]
    }

    database_templates = [
        # Urgent format
        f"{random.choice(urgency_prefixes)} {issue} ! {random.choice(impact_statements)}",
        
        # Technical detail format
        f"{issue} ! {random.choice(tech_observations)} - {random.choice(impact_statements)}",
        
        # Symptom format
        f"{issue}: {random.choice(database_symptoms[subcat_name])} - {random.choice(impact_statements)}",
        
        # Combination format
        f"{random.choice(urgency_prefixes)} {issue} - {random.choice(database_symptoms[subcat_name])} - {random.choice(tech_observations)}",
        
        # Time-sensitive format
        f"Time sensitive: {issue} - {random.choice(impact_statements)} - {random.choice(database_symptoms[subcat_name])}",
        
        # Detailed observation format
        f"{issue} ({random.choice(tech_observations)}) ; {random.choice(database_symptoms[subcat_name])} - {random.choice(impact_statements)}",
        
        # Critical alert format
        f"{random.choice(urgency_prefixes)} {issue} !!! {random.choice(impact_statements)}",
        
        # Technical detail with impact
        f"{issue} - {random.choice(tech_observations)} ! {random.choice(impact_statements)}",
        
        # Symptom with technical detail
        f"{issue}: {random.choice(database_symptoms[subcat_name])} - {random.choice(tech_observations)}",
        
        # Comprehensive alert
        f"{random.choice(urgency_prefixes)} {issue} - {random.choice(database_symptoms[subcat_name])} - {random.choice(impact_statements)}",
        
        # Time-critical format
        f"Time-critical alert: {issue} ! {random.choice(impact_statements)} - {random.choice(database_symptoms[subcat_name])}",
        
        # Detailed technical format
        f"{issue} ({random.choice(tech_observations)}) . {random.choice(database_symptoms[subcat_name])} . {random.choice(impact_statements)}"
    ]
    
    return {
        'description': random.choice(database_templates),
        'category': category,
        'subcategory': subcat_name,
        'priority': random.choices(
            [1, 2, 3, 4],  # P1 is highest priority
            weights=subcat_data['priority_weights']
        )[0]
    }

def generate_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Generate database incident dataset"""
    data = []
    for _ in range(num_samples):
        data.append(generate_incident())
    
    df = pd.DataFrame(data)
    df.to_csv('data/database_incidents.csv', index=False)
    return df

if __name__ == "__main__":
    generate_dataset()