import os
import re
import boto3
import time
import random
import json
from datetime import datetime, date
import calendar

# Files that had abbreviations corrected (from the fix script output)
CORRECTED_FILES = [
    ('0101', 'january'), ('0102', 'january'), ('0103', 'january'), ('0105', 'january'), ('0106', 'january'), ('0107', 'january'), ('0108', 'january'), ('0109', 'january'), ('0110', 'january'), ('0112', 'january'), ('0113', 'january'), ('0114', 'january'), ('0115', 'january'), ('0116', 'january'), ('0117', 'january'), ('0119', 'january'), ('0120', 'january'), ('0121', 'january'), ('0122', 'january'), ('0123', 'january'), ('0124', 'january'), ('0126', 'january'), ('0127', 'january'), ('0128', 'january'), ('0129', 'january'), ('0130', 'january'), ('0131', 'january'),
    ('0202', 'february'), ('0203', 'february'), ('0204', 'february'), ('0205', 'february'), ('0206', 'february'), ('0207', 'february'), ('0209', 'february'), ('0210', 'february'), ('0211', 'february'), ('0212', 'february'), ('0213', 'february'), ('0214', 'february'), ('0215', 'february'), ('0216', 'february'), ('0217', 'february'), ('0218', 'february'), ('0219', 'february'), ('0220', 'february'), ('0221', 'february'), ('0223', 'february'), ('0224', 'february'), ('0225', 'february'), ('0226', 'february'), ('0227', 'february'), ('0228', 'february'),
    ('0302', 'march'), ('0303', 'march'), ('0304', 'march'), ('0305', 'march'), ('0306', 'march'), ('0307', 'march'), ('0309', 'march'), ('0310', 'march'), ('0311', 'march'), ('0312', 'march'), ('0313', 'march'), ('0314', 'march'), ('0316', 'march'), ('0317', 'march'), ('0318', 'march'), ('0319', 'march'), ('0320', 'march'), ('0321', 'march'), ('0323', 'march'), ('0324', 'march'), ('0325', 'march'), ('0326', 'march'), ('0327', 'march'), ('0328', 'march'), ('0330', 'march'), ('0331', 'march'),
    ('0401', 'april'), ('0402', 'april'), ('0403', 'april'), ('0404', 'april'), ('0406', 'april'), ('0407', 'april'), ('0408', 'april'), ('0409', 'april'), ('0410', 'april'), ('0411', 'april'), ('0413', 'april'), ('0414', 'april'), ('0415', 'april'), ('0416', 'april'), ('0417', 'april'), ('0418', 'april'), ('0420', 'april'), ('0421', 'april'), ('0422', 'april'), ('0423', 'april'), ('0424', 'april'), ('0425', 'april'), ('0427', 'april'), ('0428', 'april'), ('0429', 'april'), ('0430', 'april'),
    ('0501', 'may'), ('0502', 'may'), ('0504', 'may'), ('0505', 'may'), ('0506', 'may'), ('0507', 'may'), ('0508', 'may'), ('0509', 'may'), ('0511', 'may'), ('0512', 'may'), ('0513', 'may'), ('0514', 'may'), ('0515', 'may'), ('0516', 'may'), ('0518', 'may'), ('0519', 'may'), ('0520', 'may'), ('0521', 'may'), ('0522', 'may'), ('0523', 'may'), ('0525', 'may'), ('0526', 'may'), ('0527', 'may'), ('0528', 'may'), ('0529', 'may'), ('0530', 'may'),
    ('0601', 'june'), ('0602', 'june'), ('0603', 'june'), ('0604', 'june'), ('0605', 'june'), ('0606', 'june'), ('0608', 'june'), ('0609', 'june'), ('0610', 'june'), ('0611', 'june'), ('0612', 'june'), ('0613', 'june'), ('0614', 'june'), ('0615', 'june'), ('0616', 'june'), ('0617', 'june'), ('0618', 'june'), ('0619', 'june'), ('0620', 'june'), ('0621', 'june'), ('0622', 'june'), ('0623', 'june'), ('0624', 'june'), ('0625', 'june'), ('0626', 'june'), ('0627', 'june'), ('0628', 'june'), ('0629', 'june'), ('0630', 'june'),
    ('0701', 'july'), ('0702', 'july'), ('0703', 'july'), ('0704', 'july'), ('0705', 'july'), ('0706', 'july'), ('0707', 'july'), ('0708', 'july'), ('0709', 'july'), ('0712', 'july'), ('0713', 'july'), ('0714', 'july'), ('0717', 'july'), ('0718', 'july'), ('0719', 'july'), ('0720', 'july'), ('0723', 'july'), ('0724', 'july'), ('0725', 'july'), ('0727', 'july'), ('0730', 'july'),
    ('0803', 'august'), ('0806', 'august'), ('0807', 'august'), ('0810', 'august'), ('0813', 'august'), ('0815', 'august'), ('0818', 'august'), ('0819', 'august'), ('0821', 'august'), ('0822', 'august'), ('0827', 'august'), ('0828', 'august'), ('0829', 'august'), ('0831', 'august'),
    ('0901', 'september'), ('0902', 'september'), ('0903', 'september'), ('0904', 'september'), ('0905', 'september'), ('0907', 'september'), ('0908', 'september'), ('0909', 'september'), ('0910', 'september'), ('0911', 'september'), ('0914', 'september'), ('0916', 'september'), ('0917', 'september'), ('0919', 'september'), ('0920', 'september'), ('0922', 'september'), ('0924', 'september'), ('0927', 'september'),
    ('1001', 'october'), ('1002', 'october'), ('1003', 'october'), ('1004', 'october'), ('1005', 'october'), ('1006', 'october'), ('1007', 'october'), ('1008', 'october'), ('1009', 'october'), ('1010', 'october'), ('1011', 'october'), ('1012', 'october'), ('1013', 'october'), ('1014', 'october'), ('1015', 'october'), ('1016', 'october'), ('1017', 'october'), ('1018', 'october'), ('1019', 'october'), ('1020', 'october'), ('1021', 'october'), ('1022', 'october'), ('1023', 'october'), ('1024', 'october'), ('1025', 'october'), ('1026', 'october'), ('1027', 'october'), ('1028', 'october'), ('1029', 'october'), ('1030', 'october'), ('1031', 'october'),
    ('1101', 'november'), ('1102', 'november'), ('1103', 'november'), ('1104', 'november'), ('1105', 'november'), ('1106', 'november'), ('1107', 'november'), ('1108', 'november'), ('1109', 'november'), ('1110', 'november'), ('1111', 'november'), ('1112', 'november'), ('1113', 'november'), ('1114', 'november'), ('1115', 'november'), ('1116', 'november'), ('1117', 'november'), ('1118', 'november'), ('1119', 'november'), ('1120', 'november'), ('1121', 'november'), ('1122', 'november'), ('1123', 'november'), ('1124', 'november'), ('1125', 'november'), ('1126', 'november'), ('1127', 'november'), ('1128', 'november'), ('1129', 'november'), ('1130', 'november'),
    ('1201', 'december'), ('1202', 'december'), ('1203', 'december'), ('1204', 'december'), ('1205', 'december'), ('1206', 'december'), ('1207', 'december'), ('1208', 'december'), ('1209', 'december'), ('1210', 'december'), ('1211', 'december'), ('1212', 'december'), ('1213', 'december'), ('1214', 'december'), ('1215', 'december'), ('1216', 'december'), ('1217', 'december'), ('1218', 'december'), ('1219', 'december'), ('1220', 'december'), ('1221', 'december'), ('1222', 'december'), ('1223', 'december'), ('1224', 'december'), ('1225', 'december'), ('1226', 'december'), ('1227', 'december'), ('1228', 'december'), ('1229', 'december'), ('1230', 'december'), ('1231', 'december')
]

# AWS Polly free tier limits (monthly) - CORRECTED FROM YOUR BILL
FREE_TIER_LONGFORM = 500000     # 500K characters per month for long-form
FREE_TIER_NEURAL = 1000000      # 1M characters per month for neural
FREE_TIER_STANDARD = 5000000    # 5M characters per month for standard
FREE_TIER_GENERATIVE = 100000   # 100K characters per month for generative
SAFETY_BUFFER = 50000           # Leave 50k character buFffer

def load_progress():
    """Load progress from file"""
    try:
        with open('correction_progress.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'characters_used': 0,
            'completed_corrections': [],
            'current_month': datetime.now().strftime('%Y-%m'),
            'manual_override': False
        }

def get_aws_polly_costs():
    """Get actual AWS Polly costs from Cost Explorer API"""
    try:
        ce = boto3.client('ce', region_name='us-east-1')
        
        # Get current month date range dynamically
        today = date.today()
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        
        # Handle last day of month - if today is last day, end date is first day of next month
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        if today.day == last_day_of_month:
            # Today is last day, so end date should be first day of next month
            if today.month == 12:
                end_date = date(today.year + 1, 1, 1).strftime('%Y-%m-%d')
            else:
                end_date = date(today.year, today.month + 1, 1).strftime('%Y-%m-%d')
        else:
            # Not last day, use tomorrow as end date
            end_date = date(today.year, today.month, today.day + 1).strftime('%Y-%m-%d')
        
        print(f"\n[CHECKING] Querying AWS Cost Explorer for Polly usage from {start_date} to {end_date}...")
        
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        
        polly_cost = 0
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                service_name = group['Keys'][0]
                if 'Polly' in service_name or 'Amazon Polly' in service_name:
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    polly_cost += cost
        
        if polly_cost > 0:
            # Convert cost to character count (long-form is $100 per 1M characters)
            estimated_chars = int(polly_cost / 100 * 1000000)
            print(f"[SUCCESS] Found AWS Polly charges: ${polly_cost:.2f}")
            print(f"[CALCULATED] Estimated characters used: {estimated_chars:,}")
            return estimated_chars, polly_cost
        else:
            print(f"[INFO] No Polly charges found in Cost Explorer for this month")
            return None, 0
            
    except Exception as e:
        print(f"[ERROR] Could not access Cost Explorer: {e}")
        if 'AccessDenied' in str(e):
            print(f"[INFO] Enable Cost Explorer in AWS Console and ensure IAM permissions")
        elif 'ValidationException' in str(e):
            print(f"[INFO] Cost Explorer may not be enabled or no data available yet")
        return None, 0

def set_actual_usage():
    """Get actual usage from AWS or allow manual setting"""
    print("\n" + "="*50)
    print("REAL AWS USAGE CHECK")
    print("="*50)
    
    # Try to get real AWS costs first
    estimated_chars, actual_cost = get_aws_polly_costs()
    
    if estimated_chars is not None:
        print(f"\n[REAL DATA] AWS Cost Explorer shows:")
        print(f"  Polly charges this month: ${actual_cost:.2f}")
        print(f"  Estimated characters used: {estimated_chars:,}")
        
        while True:
            choice = input("\nUse this real data? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return estimated_chars
            elif choice in ['n', 'no']:
                break
            else:
                print("Please enter 'y' or 'n'")
    
    # Fallback to manual entry
    print("\n[MANUAL ENTRY] Enter usage manually:")
    print("Options:")
    print("1. Enter known dollar amount (will calculate characters)")
    print("2. Enter character count directly")
    print("3. Skip override (use script tracking only)")
    
    while True:
        choice = input("\nChoose option (1/2/3): ").strip()
        
        if choice == '1':
            while True:
                try:
                    cost = float(input("Enter dollar amount charged: $"))
                    chars = int(cost / 100 * 1000000)  # $100 per 1M chars
                    print(f"Calculated: {chars:,} characters")
                    return chars
                except ValueError:
                    print("Please enter a valid dollar amount")
        elif choice == '2':
            while True:
                try:
                    custom = input("Enter character count used this month: ").replace(',', '')
                    return int(custom)
                except ValueError:
                    print("Please enter a valid number")
        elif choice == '3':
            return None
        else:
            print("Please enter 1, 2, or 3")

def save_progress(progress):
    """Save progress to file"""
    with open('correction_progress.json', 'w') as f:
        json.dump(progress, f, indent=2)

def reset_monthly_usage(progress):
    """Reset usage if new month"""
    current_month = datetime.now().strftime('%Y-%m')
    if progress['current_month'] != current_month:
        progress['characters_used'] = 0
        progress['current_month'] = current_month
        print(f"[RESET] New month detected, resetting character usage")
    return progress

def extract_scripture_text(html_file):
    """Extract scripture text from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scripture_pattern = r'<p class="fnb"><span>\d+\s*</span>(.*?)</p>'
    matches = re.findall(scripture_pattern, content, re.DOTALL)
    
    scripture_text = []
    for match in matches:
        clean_text = re.sub(r'<[^>]+>', '', match)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        if clean_text:
            scripture_text.append(clean_text)
    
    return ' '.join(scripture_text)

def get_reading_info(html_file):
    """Extract reading information from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    h4_pattern = r'<h4 class="mt-3">(.*?)</h4>'
    h4_match = re.search(h4_pattern, content)
    
    if h4_match:
        reading_text = h4_match.group(1).strip()
        reading_text = re.sub(r'\s*&\s*$', '', reading_text)
        return reading_text
    
    return "today's reading"

def get_random_intro(reading_info):
    """Get a random intro message for Julia"""
    intros = [
        f"Good morning, my beautiful Julia! It's time for our daily Bible reading together. Today we're reading from {reading_info}. Let's dive into God's Word and see what He has for us today.",
        f"Rise and shine, my love! Another beautiful day to spend time in God's Word together. Today's reading is from {reading_info}. I'm so grateful we can share this spiritual journey together.",
        f"Hello, gorgeous! Ready for our daily dose of divine wisdom? Today we're exploring {reading_info}. Let's see what treasures God has waiting for us in His Word."
    ]
    return random.choice(intros)

def get_random_outro(reading_info):
    """Get a random outro message for Julia"""
    outros = [
        f"That completes today's reading from {reading_info}. I love you so much, Julia, and I pray that God's Word brings you peace, joy, and strength today. Have a wonderful day, my love!",
        f"And that's our beautiful journey through {reading_info} for today. May these words stay with you throughout the day, my precious Julia. You are loved beyond measure - by God and by me!",
        f"What a wonderful time we've had in {reading_info} today! I hope these verses fill your heart with hope and your day with purpose. I love you endlessly, my sweet Julia."
    ]
    return random.choice(outros)

def create_audio_script(date_code, month):
    """Create audio script for a specific date"""
    html_file = f"readings/{month}/{date_code}.html"
    
    if not os.path.exists(html_file):
        return None
    
    scripture_text = extract_scripture_text(html_file)
    reading_info = get_reading_info(html_file)
    
    if not scripture_text:
        return None
    
    random.seed(int(date_code))
    intro = get_random_intro(reading_info)
    outro = get_random_outro(reading_info)
    
    return f"{intro}\n\n{scripture_text}\n\n{outro}"

def generate_longform_audio(script_text, date_code, month):
    """Generate audio using AWS Polly Long-form"""
    try:
        polly = boto3.client('polly', region_name='us-east-1')
        
        response = polly.start_speech_synthesis_task(
            Text=script_text,
            OutputFormat='mp3',
            VoiceId='Danielle',
            Engine='long-form',
            OutputS3BucketName='one-year-bible-ekewaka'
        )
        
        task_id = response['SynthesisTask']['TaskId']
        print(f"  Started long-form task: {task_id}")
        
        wait_time = 0
        while True:
            task_status = polly.get_speech_synthesis_task(TaskId=task_id)
            status = task_status['SynthesisTask']['TaskStatus']
            
            if status == 'completed':
                output_uri = task_status['SynthesisTask']['OutputUri']
                print(f"\n    [COMPLETE] Long-form synthesis completed after {wait_time}s")
                
                s3 = boto3.client('s3')
                uri_parts = output_uri.split('/')
                temp_key = '/'.join(uri_parts[4:]) if len(uri_parts) > 4 else uri_parts[-1]
                final_key = f'2025/{month}/{date_code}.mp3'
                
                try:
                    s3.copy_object(
                        Bucket='one-year-bible-ekewaka',
                        CopySource={'Bucket': 'one-year-bible-ekewaka', 'Key': temp_key},
                        Key=final_key
                    )
                    s3.delete_object(Bucket='one-year-bible-ekewaka', Key=temp_key)
                    print(f"    [SUCCESS] File ready at {final_key}")
                    return True
                except Exception as copy_error:
                    print(f"    [WARNING] Rename failed: {copy_error}")
                    return True
                
            elif status == 'failed':
                print(f"\n    [FAILED] Long-form synthesis failed after {wait_time}s")
                return False
            
            dots = '.' * ((wait_time // 10) % 4)
            print(f"\r    [WAIT] Status: {status}{dots}    ", end='', flush=True)
            time.sleep(10)
            wait_time += 10
            
    except Exception as e:
        print(f"  Error with long-form synthesis: {e}")
        return False

def get_detailed_polly_usage():
    """Get detailed Polly usage by engine type from AWS Cost Explorer"""
    try:
        ce = boto3.client('ce', region_name='us-east-1')
        
        # Get current month date range dynamically
        today = date.today()
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        
        # Handle last day of month - if today is last day, end date is first day of next month
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        if today.day == last_day_of_month:
            # Today is last day, so end date should be first day of next month
            if today.month == 12:
                end_date = date(today.year + 1, 1, 1).strftime('%Y-%m-%d')
            else:
                end_date = date(today.year, today.month + 1, 1).strftime('%Y-%m-%d')
        else:
            # Not last day, use tomorrow as end date
            end_date = date(today.year, today.month, today.day + 1).strftime('%Y-%m-%d')
        
        print(f"\n[CHECKING] Querying AWS for detailed Polly usage from {start_date} to {end_date}...")
        
        # Simple query for Polly costs with usage breakdown
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost', 'UsageQuantity'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'USAGE_TYPE'
                }
            ],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['Amazon Polly']
                }
            }
        )
        
        usage_data = {}
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                usage_type = group['Keys'][0]
                if 'Polly' in usage_type or 'synthesize' in usage_type.lower():
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    usage = float(group['Metrics']['UsageQuantity']['Amount'])
                    if cost > 0 or usage > 0:
                        usage_data[usage_type] = {'cost': cost, 'usage': usage}
        
        return usage_data if usage_data else None
        
    except Exception as e:
        print(f"[ERROR] Could not get detailed usage: {e}")
        if 'AccessDenied' in str(e):
            print("[INFO] Cost Explorer access denied. Enable Cost Explorer in AWS Console.")
        elif 'InvalidNextToken' in str(e) or 'ValidationException' in str(e):
            print("[INFO] Cost Explorer may not be enabled or data not available yet.")
        return None

def show_your_actual_usage():
    """Display your actual AWS bill breakdown from Cost Explorer"""
    print("\n" + "="*70)
    print("YOUR ACTUAL AWS POLLY USAGE THIS MONTH")
    print("="*70)
    
    usage_data = get_detailed_polly_usage()
    
    if not usage_data:
        print("\n[FALLBACK] Could not retrieve detailed usage data from AWS")
        print("Trying basic cost query...")
        
        # Fallback to basic cost query
        estimated_chars, actual_cost = get_aws_polly_costs()
        if estimated_chars:
            print(f"\nTOTAL POLLY USAGE (ESTIMATED):")
            print(f"   Cost: ${actual_cost:.2f}")
            print(f"   Estimated long-form characters: {estimated_chars:,}")
            print(f"   Note: This assumes all usage was long-form ($100/1M chars)")
            return estimated_chars
        else:
            print("\n[MANUAL INPUT REQUIRED] No usage data available from AWS")
            print("This could be because:")
            print("  - Cost Explorer is not enabled")
            print("  - Insufficient permissions")
            print("  - Data is not yet available (24-48 hour delay)")
            print("  - No charges this month")
            
            # Only use September 2025 fallback data if we're in that month
            today = date.today()
            if today.year == 2025 and today.month == 9:
                print(f"\n[USING KNOWN DATA] Based on your $791.96 September 2025 bill:")
                print(f"   Long-form usage: 7,381,580 characters")
                print(f"   Neural usage: 3,362,455 characters")
                print(f"   Standard usage: 58 characters")
                return 7381580  # Your actual long-form usage
            else:
                print(f"\n[NO DATA] No usage data available for current month")
                return 0  # No usage for other months
    
    total_cost = 0
    total_longform_chars = 0
    
    # Map usage types to engines (all regions and patterns)
    engine_mapping = {
        'synthesizeSpeech-characters': ('STANDARD', FREE_TIER_STANDARD, 4),
        'synthesizeSpeechNeural-characters': ('NEURAL', FREE_TIER_NEURAL, 16),
        'synthesizeSpeechLongForm-characters': ('LONG-FORM', FREE_TIER_LONGFORM, 100),
        'synthesizeSpeechGenerative-characters': ('GENERATIVE', FREE_TIER_GENERATIVE, 30)
    }
    
    # AWS regions that might appear in usage types
    aws_regions = ['USE1', 'USE2', 'USW1', 'USW2', 'EUW1', 'EUW2', 'EUW3', 'EUC1', 'APS1', 'APS2', 'APN1', 'APN2', 'SAE1', 'CAC1']
    
    # Add regional patterns to mapping
    for region in aws_regions:
        engine_mapping[f'{region}-SynthesizeSpeech-Characters'] = ('STANDARD', FREE_TIER_STANDARD, 4)
        engine_mapping[f'{region}-SynthesizeSpeechNeural-Characters'] = ('NEURAL', FREE_TIER_NEURAL, 16)
        engine_mapping[f'{region}-SynthesizeSpeechLongForm-Characters'] = ('LONG-FORM', FREE_TIER_LONGFORM, 100)
        engine_mapping[f'{region}-SynthesizeSpeechGenerative-Characters'] = ('GENERATIVE', FREE_TIER_GENERATIVE, 30)
    
    for usage_type, data in usage_data.items():
        cost = data['cost']
        usage_chars = int(data['usage'])
        total_cost += cost
        
        # Find engine info - direct mapping first
        engine_info = engine_mapping.get(usage_type)
        
        # Pattern matching for AWS usage types
        if not engine_info:
            if 'LongForm' in usage_type:
                engine_info = ('LONG-FORM', FREE_TIER_LONGFORM, 100)
            elif 'Neural' in usage_type:
                engine_info = ('NEURAL', FREE_TIER_NEURAL, 16)
            elif 'Generative' in usage_type:
                engine_info = ('GENERATIVE', FREE_TIER_GENERATIVE, 30)
            elif 'SynthesizeSpeech' in usage_type:
                engine_info = ('STANDARD', FREE_TIER_STANDARD, 4)
        
        # Detect engine type by cost-per-character if still not found
        if not engine_info and cost > 0 and usage_chars > 0:
            cost_per_million = (cost / usage_chars) * 1000000
            if cost_per_million > 80:  # Close to $100/1M (long-form)
                engine_info = ('LONG-FORM', FREE_TIER_LONGFORM, 100)
            elif cost_per_million > 25:  # Close to $30/1M (generative)
                engine_info = ('GENERATIVE', FREE_TIER_GENERATIVE, 30)
            elif cost_per_million > 12:  # Close to $16/1M (neural)
                engine_info = ('NEURAL', FREE_TIER_NEURAL, 16)
            else:  # Close to $4/1M (standard)
                engine_info = ('STANDARD', FREE_TIER_STANDARD, 4)
        
        if engine_info:
            engine_name, free_tier, rate_per_million = engine_info
            overage = max(0, usage_chars - free_tier)
            status = "✓ WITHIN FREE TIER" if usage_chars <= free_tier else "✗ EXCEEDED FREE TIER"
            
            print(f"\n{engine_name} ENGINE ({usage_type}):")
            print(f"   Used: {usage_chars:,} characters")
            print(f"   Free Tier: {free_tier:,} characters")
            if overage > 0:
                print(f"   Overage: {overage:,} characters")
            print(f"   Status: {status}")
            print(f"   Cost: ${cost:.2f}")
            
            if engine_name == 'LONG-FORM':
                total_longform_chars += usage_chars
        else:
            print(f"\nUNKNOWN ENGINE ({usage_type}):")
            print(f"   Usage: {usage_chars:,}")
            print(f"   Cost: ${cost:.2f}")
    
    print("\n" + "-"*70)
    print(f"TOTAL BILL: ${total_cost:.2f}")
    if total_longform_chars > FREE_TIER_LONGFORM:
        print(f"MAJOR ISSUE: Long-form free tier is only {FREE_TIER_LONGFORM:,}, not 5M!")
    print("-"*70)
    
    # Only use fallback data if we're querying September 2025 specifically
    today = date.today()
    if today.year == 2025 and today.month == 9 and total_cost < 700:
        print(f"\n[WARNING] API shows ${total_cost:.2f} but expected $791.96 for September 2025")
        print(f"[FALLBACK] Using actual bill data instead of API data")
        print(f"\n[ACTUAL BILL DATA] September 2025:")
        print(f"   Long-form: $738.16 (7,381,600 characters)")
        print(f"   Neural: $53.80 (3,362,500 characters)")
        print(f"   Standard: $0.00 (58 characters)")
        print(f"   Generative: $0.00 (4,539 characters)")
        print(f"   TOTAL: $791.96")
        return 7381600  # Actual long-form usage from bill
    
    return total_longform_chars  # Only return actual long-form usage

def show_polly_pricing_breakdown():
    """Display comprehensive AWS Polly pricing and free tier information"""
    print("\n" + "="*60)
    print("AWS POLLY PRICING & FREE TIER BREAKDOWN (CORRECTED)")
    print("="*60)
    
    print("\n1. STANDARD ENGINE:")
    print("   - Cost: $4.00 per 1M characters")
    print("   - Free Tier: 5M characters/month (first 12 months)")
    print("   - Character Limit: 3,000 per request")
    print("   - Use Case: Basic text-to-speech")
    
    print("\n2. NEURAL ENGINE:")
    print("   - Cost: $16.00 per 1M characters")
    print("   - Free Tier: 1M characters/month (first 12 months)")
    print("   - Character Limit: 3,000 per request")
    print("   - Use Case: Higher quality, more natural speech")
    
    print("\n3. LONG-FORM ENGINE:")
    print("   - Cost: $100.00 per 1M characters")
    print("   - Free Tier: 500K characters/month (ONLY 500K!)")
    print("   - Character Limit: 100,000 per request")
    print("   - Use Case: Long content, news articles, books")
    
    print("\n4. GENERATIVE ENGINE (NEW):")
    print("   - Cost: $30.00 per 1M characters")
    print("   - Free Tier: 100K characters/month")
    print("   - Character Limit: Varies")
    print("   - Use Case: AI-generated conversational speech")
    
    print("\n" + "-"*60)
    print("BILLING USAGE TYPES YOU MIGHT SEE:")
    print("-"*60)
    print("• synthesizeSpeech-characters (Standard)")
    print("• synthesizeSpeechNeural-characters (Neural)")
    print("• synthesizeSpeechLongForm-characters (Long-form)")
    print("• synthesizeSpeechGenerative-characters (Generative)")
    
    print("\n" + "-"*60)
    print("THIS SCRIPT USES: Long-form Engine")
    print("- Best for Bible readings (8K+ characters each)")
    print("- No chunking required")
    print("- Higher quality for long content")
    print("-"*60)

def check_free_tier_status(progress):
    """Check free tier availability and get user confirmation"""
    # Show your actual usage first
    actual_longform_usage = show_your_actual_usage()
    show_polly_pricing_breakdown()
    
    # Set actual usage based on AWS data
    if not progress.get('manual_override', False):
        print("\n[AUTO-SETTING] Using real AWS bill data:")
        progress['characters_used'] = actual_longform_usage
        progress['manual_override'] = True
        print(f"[UPDATED] Set long-form usage to {progress['characters_used']:,} characters")
    
    remaining_budget = FREE_TIER_LONGFORM - progress['characters_used']
    
    print("\n" + "="*50)
    print("LONG-FORM FREE TIER STATUS")
    print("="*50)
    print(f"Monthly limit: {FREE_TIER_LONGFORM:,} characters")
    print(f"Used this month: {progress['characters_used']:,} characters")
    
    # Calculate estimates for both scenarios
    remaining_corrections = [(d, m) for d, m in CORRECTED_FILES if d not in progress['completed_corrections']]
    estimated_chars = len(remaining_corrections) * 8000
    
    if remaining_budget > 0:
        print(f"Remaining budget: {remaining_budget:,} characters")
        print(f"[✓] FREE TIER AVAILABLE")
        
        print(f"\n" + "-"*30)
        print("PROCEED WITH FREE TIER?")
        print("-"*30)
        print(f"Remaining files to process: {len(remaining_corrections)}")
        print(f"Estimated characters needed: {estimated_chars:,}")
        print(f"Cost: FREE (within free tier)")
        
        while True:
            choice = input("\nProceed with free tier usage? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                print("[CONFIRMED] Proceeding with free tier")
                return True, False
            elif choice in ['n', 'no']:
                print("[CANCELLED] Stopping")
                return False, False
            else:
                print("Please enter 'y' or 'n'")
    else:
        print(f"Over budget by: {abs(remaining_budget):,} characters")
        print(f"[✗] LONG-FORM FREE TIER EXHAUSTED")
        print(f"[✗] You've used {progress['characters_used']/FREE_TIER_LONGFORM:.1f}x the free tier limit")
        print(f"[✗] Every additional character costs $0.0001")
        
        polly_cost_per_char = 0.0001
        estimated_cost = estimated_chars * polly_cost_per_char
        
        print(f"\n" + "-"*30)
        print("PAID OPTION AVAILABLE")
        print("-"*30)
        print(f"Remaining files to process: {len(remaining_corrections)}")
        print(f"Estimated characters needed: {estimated_chars:,}")
        print(f"Estimated cost: ${estimated_cost:.2f}")
        print(f"Rate: $100 per 1M characters (Long-form)")
        
        while True:
            choice = input("\nProceed with paid usage? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                print("[CONFIRMED] Proceeding with paid usage")
                return False, True
            elif choice in ['n', 'no']:
                print("[CANCELLED] Stopping to avoid charges")
                return False, False
            else:
                print("Please enter 'y' or 'n'")

def main():
    """Regenerate audio files for corrected abbreviations with budget tracking"""
    print("Regenerating audio for files with corrected abbreviations...")
    
    # Load progress
    progress = load_progress()
    progress = reset_monthly_usage(progress)
    
    # Check free tier status and get user confirmation
    has_free_tier, use_paid = check_free_tier_status(progress)
    
    if not has_free_tier and not use_paid:
        print("\n[STOPPED] Exiting to stay within free tier limits")
        return
    
    # Only process files that need correction and haven't been completed
    remaining_corrections = [(d, m) for d, m in CORRECTED_FILES if d not in progress['completed_corrections']]
    
    print(f"Files needing correction: {len(CORRECTED_FILES)}")
    print(f"Remaining to process: {len(remaining_corrections)}")
    
    os.makedirs("audio-scripts", exist_ok=True)
    
    for date_code, month in remaining_corrections:
        print(f"\n[CORRECTION] Processing {date_code} ({month})...")
        
        # Create script and check character count
        script_text = create_audio_script(date_code, month)
        if not script_text:
            print(f"  [SKIP] No scripture text found")
            continue
        
        script_length = len(script_text)
        projected_usage = progress['characters_used'] + script_length
        
        # Check if this would exceed budget (only if using free tier)
        if has_free_tier and projected_usage > (FREE_TIER_LONGFORM - SAFETY_BUFFER):
            print(f"  [BUDGET LIMIT] Would exceed free tier limit!")
            print(f"  Script length: {script_length:,} characters")
            print(f"  Current usage: {progress['characters_used']:,}")
            print(f"  Projected usage: {projected_usage:,}")
            print(f"\n[STOPPED] Stopping to stay within budget.")
            print(f"Remaining corrections: {len(remaining_corrections) - remaining_corrections.index((date_code, month))}")
            
            # Update script with remaining files
            update_script_with_remaining(remaining_corrections[remaining_corrections.index((date_code, month)):])
            break
        elif use_paid:
            # Show cost for this file when using paid tier
            file_cost = script_length * 0.0001
            print(f"  [PAID] This file will cost: ${file_cost:.4f}")
        
        # Save script
        script_file = f"audio-scripts/{date_code}_corrected.txt"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_text)
        print(f"  [SAVED] Script: {script_length:,} characters")
        
        # Generate audio
        print(f"  [LONGFORM] Regenerating with corrected book names")
        if generate_longform_audio(script_text, date_code, month):
            # Update progress
            progress['characters_used'] += script_length
            progress['completed_corrections'].append(date_code)
            save_progress(progress)
            
            print(f"  [SUCCESS] Audio regenerated with correct book names")
            if has_free_tier:
                print(f"  [BUDGET] Used: {progress['characters_used']:,}/{FREE_TIER_LONGFORM:,} ({progress['characters_used']/FREE_TIER_LONGFORM*100:.1f}%)")
            else:
                total_cost = progress['characters_used'] * 0.0001
                print(f"  [PAID] Total cost so far: ${total_cost:.2f} ({progress['characters_used']:,} characters)")
        else:
            print(f"  [ERROR] Failed to regenerate audio")
    
    print(f"\n[COMPLETE] Correction session finished")
    print(f"Total characters used: {progress['characters_used']:,}")
    print(f"Corrected files: {len(progress['completed_corrections'])}")
    print(f"Remaining corrections: {len(CORRECTED_FILES) - len(progress['completed_corrections'])}")

def update_script_with_remaining(remaining_files):
    """Update the script file to only include remaining files"""
    try:
        # Read current script
        with open(__file__, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Create new CORRECTED_FILES list
        new_files_str = "CORRECTED_FILES = [\n"
        for date_code, month in remaining_files:
            new_files_str += f"    ('{date_code}', '{month}'),\n"
        new_files_str += "]"
        
        # Replace the CORRECTED_FILES section
        pattern = r'CORRECTED_FILES = \[.*?\]'
        updated_content = re.sub(pattern, new_files_str, script_content, flags=re.DOTALL)
        
        # Write updated script
        with open(__file__, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"[UPDATED] Script updated with {len(remaining_files)} remaining files for next month")
        
    except Exception as e:
        print(f"[ERROR] Could not update script: {e}")
        print("You'll need to manually update CORRECTED_FILES for next month")

if __name__ == "__main__":
    main()