import pandas as pd
import random

INCIDENT_TAXONOMY = {
    'HARDWARE': {
        'subcategories': {
            'Storage Failures': {
                'issues': [
                    'Hard drive failure', 'SSD degradation', 'RAID array failure',
                    'Storage controller error', 'Disk corruption', 'Bad sectors detected',
                    'NAS device failure', 'Storage capacity critical', 'Drive overheating',
                    'External HDD not recognized', 'File system corruption', 'Disk I/O errors',
                    'Storage array rebuild failure', 'Disk enclosure fan failure',
                    'Storage device not detected', 'Backup drive failure', 'Storage cable damage',
                    'Storage device ejecting randomly', 'Storage device making clicking noises'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3],  # P1-P4 weights
                'hardware_identifiers': [
                    'storage subsystem',
                    'disk array',
                    'storage medium',
                    'data storage',
                    'RAID configuration',
                    'drive firmware',
                    'mass storage device'
                ]
            },
            'Memory Issues': {
                'issues': [
                    'RAM failure', 'Memory bank error', 'ECC memory alert',
                    'Memory timing failure', 'DIMM degradation', 'Memory temperature critical',
                    'Insufficient memory', 'Memory compatibility issue', 'Memory slot failure',
                    'Memory cache error', 'Memory voltage irregularity', 'Memory overclocking failure',
                    'Memory module not detected', 'Memory leak causing system instability',
                    'Faulty memory causing blue screen errors', 'Memory not recognized after upgrade'
                ],
                'priority_weights': [0.2, 0.3, 0.3, 0.2],
                'hardware_identifiers': [
                    'RAM module',
                    'system memory',
                    'DIMM slot',
                    'memory controller',
                    'memory timing',
                    'memory architecture',
                    'volatile storage'
                ]
            },
            'Processor Problems': {
                'issues': [
                    'CPU overheating', 'Processor throttling', 'CPU fan failure',
                    'Thermal paste degradation', 'Processing core failure', 'CPU socket damage',
                    'BIOS/CPU incompatibility', 'CPU voltage irregularity', 'CPU cache error',
                    'Processor pin damage', 'CPU overclocking failure', 'Processor power delivery issue',
                    'CPU not detected', 'CPU frequency fluctuation', 'CPU temperature sensor failure',
                    'CPU cooler failure', 'CPU performance degradation over time'
                ],
                'priority_weights': [0.1, 0.3, 0.4, 0.2],
                'hardware_identifiers': [
                    'processor core',
                    'CPU die',
                    'processing unit',
                    'CPU architecture',
                    'processor socket',
                    'CPU cooling',
                    'compute engine'
                ]
            },
            'Power Issues': {
                'issues': [
                    'PSU failure', 'Battery degradation', 'UPS malfunction',
                    'Power fluctuation', 'Circuit overload', 'Power connector damage',
                    'Voltage regulation problem', 'Battery swelling', 'Power surge damage',
                    'Inconsistent power delivery', 'AC adapter failure', 'Power supply fan failure',
                    'Battery not charging', 'Power button failure', 'Power cable damage',
                    'Power supply overheating', 'Battery life significantly reduced',
                    'Power supply making buzzing noise', 'Power supply not providing enough wattage'
                ],
                'priority_weights': [0.1, 0.2, 0.4, 0.3],
                'hardware_identifiers': [
                    'power delivery',
                    'electrical system',
                    'power source',
                    'voltage regulator',
                    'battery cell',
                    'power circuitry',
                    'energy source'
                ]
            },
            'Peripheral Failures': {
                'issues': [
                    'Monitor failure', 'Keyboard malfunction', 'Mouse connectivity issue',
                    'Printer hardware error', 'Scanner breakdown', 'USB port failure',
                    'Docking station malfunction', 'External drive failure', 'Paper jam error',
                    'Toner cartridge failure', 'Printer connectivity issue', 'Key stuck',
                    'Wireless keyboard disconnection', 'Screen flickering', 'Dead pixels',
                    'Backlight failure', 'Projector bulb failure', 'Projector focus issue',
                    'HDMI input failure', 'Projector overheating', 'Touchscreen unresponsive',
                    'Printer paper feed error', 'Monitor color calibration issue', 'Printer spooler failure',
                    'Keyboard ghosting issue', 'Monitor bezel damage', 'Projector lens scratch',
                    'Printer roller wear', 'Keyboard LED failure', 'Monitor stand instability'
                ],
                'priority_weights': [0.4, 0.3, 0.2, 0.1],
                'hardware_identifiers': [
                    'external device',
                    'I/O device',
                    'user interface hardware',
                    'output device',
                    'input peripheral',
                    'human interface device',
                    'external accessory'
                ]
            },
            'Network Hardware': {
                'issues': [
                    'NIC firmware corruption', 'Ethernet card physical damage', 'PCIe network card slot damage',
                    'Router hardware component failure', 'Switch physical damage', 'Hardware firewall failure',
                    'Network adapter overheat', 'Physical network adapter bent pins', 'WiFi card component failure',
                    'Network card driver hardware compatibility', 'Network adapter power component failure',
                    'WiFi antenna physical disconnection', 'Network hub physical damage', 'Network bridge component failure',
                    'Network repeater hardware damage', 'Bluetooth adapter failure', 'Network printer interface card damage'
                ],
                'priority_weights': [0.1, 0.3, 0.4, 0.2],
                'hardware_identifiers': [
                    'network adapter hardware',
                    'physical network device',
                    'network hardware component',
                    'network device chassis',
                    'physical network interface',
                    'hardware-level network connection',
                    'network equipment circuit'
                ]
            },
            'Motherboard Issues': {
                'issues': [
                    'Motherboard failure', 'CMOS battery failure', 'PCIe slot damage',
                    'BIOS corruption', 'Chipset failure', 'Board capacitor damage',
                    'Motherboard sensor failure', 'Motherboard trace damage', 'VRM failure',
                    'Motherboard overheating', 'BIOS update failure', 'Motherboard USB port failure',
                    'Motherboard audio jack failure', 'Motherboard RAM slot failure',
                    'Motherboard VRM toroidal transformer issue', 'Motherboard VRM EMI issue', 
                    'Motherboard VRM RFI issue', 'Motherboard VRM noise issue'
                ],
                'priority_weights': [0.1, 0.2, 0.5, 0.2],
                'hardware_identifiers': [
                    'system board',
                    'main board',
                    'logic board',
                    'mainboard chipset',
                    'planar board',
                    'main circuit board',
                    'motherboard PCB'
                ]
            }
        }
    }
}

def generate_incident() -> dict:
    """Generate a hardware incident with realistic user-reported descriptions"""
    category = 'HARDWARE'
    subcat_name = random.choice(list(INCIDENT_TAXONOMY[category]['subcategories'].keys()))
    subcat_data = INCIDENT_TAXONOMY[category]['subcategories'][subcat_name]
    issue = random.choice(subcat_data['issues'])
    
    # Get hardware-specific identifier
    hardware_identifier = random.choice(subcat_data['hardware_identifiers'])

    hardware_templates = [
        # User frustration reports with hardware identifiers
        f"HARDWARE ISSUE: Help! My computer's {hardware_identifier} won't work at all. Diagnosed as: {issue}",
        f"HW: System {hardware_identifier} keeps crashing every few minutes - tech found {issue}",
        f"HARDWARE: {hardware_identifier} was working fine yesterday, but now experiencing {issue}",
        f"HW URGENT: Lost all my work due to {hardware_identifier} having {issue}",

        # Performance complaints with hardware identifiers
        f"HARDWARE SLOWDOWN: My computer's {hardware_identifier} is incredibly slow - IT discovered {issue}",
        f"HW NOISE: Machine {hardware_identifier} making strange noises - related to {issue}",
        f"HARDWARE FREEZE: Computer {hardware_identifier} keeps freezing during meetings due to {issue}",
        f"HW PRODUCTIVITY: Can't get any work done - {hardware_identifier} experiencing {issue}",

        # Equipment status reports with hardware identifiers
        f"HARDWARE ERROR: Blue screen errors from {hardware_identifier} - maintenance found {issue}",
        f"HW DANGER: Smoke coming from {hardware_identifier}! Related to {issue}",
        f"HARDWARE SMELL: Strange burning smell from {hardware_identifier} - technician identified {issue}",
        f"HW FAILURE: Equipment {hardware_identifier} completely dead - caused by {issue}",

        # Work impact reports with hardware identifiers
        f"HARDWARE BLOCKER: Entire team blocked - {hardware_identifier} dealing with {issue}",
        f"HW MEETING: Client meeting interrupted by {hardware_identifier} having {issue}",
        f"HARDWARE DATA: Lost access to critical files due to {hardware_identifier} with {issue}",
        f"HW DEADLINE: Project deadline at risk because of {hardware_identifier} showing {issue}",

        # IT diagnostic reports with hardware identifiers
        f"HARDWARE MAINTENANCE: Routine check of {hardware_identifier} detected: {issue}",
        f"HW DIAGNOSTIC: Hardware diagnostics on {hardware_identifier} alert: {issue}",
        f"HARDWARE MONITORING: System monitoring of {hardware_identifier} warning: {issue}",
        f"HW REPLACEMENT: Emergency {hardware_identifier} replacement needed: {issue}",

        # Specific hardware complaints with hardware identifiers
        f"HARDWARE DISPLAY: Monitor {hardware_identifier} keeps flickering - shows {issue}",
        f"HW INPUT: Keyboard {hardware_identifier} typing random characters - found {issue}",
        f"HARDWARE OUTPUT: Printer {hardware_identifier} making grinding noises - indicates {issue}",
        f"HW POWER: Laptop {hardware_identifier} dying quickly - confirmed {issue}",

        # Environmental impacts with hardware identifiers
        f"HARDWARE ENVIRONMENTAL: After power outage, {hardware_identifier} discovered {issue}",
        f"HW CLIMATE: Post-AC failure, {hardware_identifier} identified with {issue}",
        f"HARDWARE DAMAGE: Coffee spill on {hardware_identifier} resulted in {issue}",
        f"HW RELOCATION: Following office move, {hardware_identifier} found with {issue}",
        
        # More specific hardware issues
        f"HARDWARE PROJECTOR: Urgent: Projector {hardware_identifier} not working before board meeting - identified as {issue}",
        f"HW PRINTER: Printer {hardware_identifier} jams every time I print - caused by {issue}",
        f"HARDWARE DISPLAY: Screen {hardware_identifier} has dead pixels affecting display quality - diagnosed {issue}",
        
        # User report formats
        f"HARDWARE USER: My {hardware_identifier} is making weird clicking sounds. Tech diagnosed: {issue}",
        f"HW COMPLAINT: Computer keeps shutting down randomly. IT found problem with {hardware_identifier}: {issue}",
        f"HARDWARE HELP: Need urgent help with my {hardware_identifier}. Service desk identified {issue}",
        f"HW REQUEST: Please send technician to look at my {hardware_identifier}. Previous diagnosis: {issue}",
        
        # IT staff report formats
        f"HARDWARE IT: During preventative maintenance on {hardware_identifier}, found {issue}",
        f"HW TECH: Technician report: {hardware_identifier} needs replacement due to {issue}",
        f"HARDWARE ANALYSIS: Diagnostic scan of {hardware_identifier} revealed {issue}",
        f"HW INSPECTION: Regular hardware inspection found {hardware_identifier} suffering from {issue}",
        f"It's showing a black screen ,{hardware_identifier} suffers {issue}",
        f"My machine is stuck in a boot loop. {issue}"
    ]

    return {
        'description': random.choice(hardware_templates),
        'category': category,
        'subcategory': subcat_name,
        'priority': random.choices(
            [1, 2, 3, 4],  # P1 is highest priority
            weights=subcat_data['priority_weights']
        )[0]
    }

def generate_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Generate hardware incident dataset"""
    data = []
    for _ in range(num_samples):
        data.append(generate_incident())

    df = pd.DataFrame(data)
    
    # Ensure exact column order
    return df[['description', 'category', 'subcategory', 'priority']]

if __name__ == "__main__":
    # Generate and save data
    num_samples = 5000
    df = generate_dataset(num_samples)
    
    # Save to CSV
    df.to_csv('data/hardware_incidents.csv', index=False)
    
    # Print dataset statistics
    print("\nHardware Incident Dataset Generated")
    print("-" * 30)
    print(f"Total incidents: {len(df)}")
    print("\nSubcategory Distribution:")
    print(df['subcategory'].value_counts())
    print("\nPriority Distribution:")
    print(df['priority'].value_counts().sort_index())
    
    # Print example records
    print("\nExample Records:")
    print(df.head().to_string())