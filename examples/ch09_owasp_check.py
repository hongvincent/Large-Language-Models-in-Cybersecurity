"""
Chapter 9: OWASP Top 10 Vulnerability Checker
LLM을 활용한 OWASP Top 10 기준 코드 검사
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_owasp_vulnerabilities(code: str, language: str = "Python") -> dict:
    """OWASP Top 10 기준으로 코드 검사"""

    prompt = f"""Analyze this {language} code against OWASP Top 10 2021:

```{language.lower()}
{code}
```

For EACH of the OWASP Top 10 categories, provide:

**A01:2021 – Broken Access Control**
- Finding: Yes/No
- Severity: Critical/High/Medium/Low (if found)
- Location: Line number or code section
- Description: What's wrong
- Remediation: How to fix
- Example: Secure code snippet

**A02:2021 – Cryptographic Failures**
- [Same format]

**A03:2021 – Injection**
- [Same format]

**A04:2021 – Insecure Design**
- [Same format]

**A05:2021 – Security Misconfiguration**
- [Same format]

**A06:2021 – Vulnerable and Outdated Components**
- [Same format]

**A07:2021 – Identification and Authentication Failures**
- [Same format]

**A08:2021 – Software and Data Integrity Failures**
- [Same format]

**A09:2021 – Security Logging and Monitoring Failures**
- [Same format]

**A10:2021 – Server-Side Request Forgery (SSRF)**
- [Same format]

Then provide:
- Overall Risk Score: 0-100
- Priority Remediation List
- Secure Code Rewrite (if major issues found)

Be thorough and specific."""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are an OWASP security expert performing comprehensive application security assessments."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "code": code,
        "language": language,
        "owasp_report": response.choices[0].message.content
    }


def main():
    """메인 함수"""
    print("\n🔒 Chapter 9: OWASP Top 10 Vulnerability Checker\n")
    print("OWASP Top 10 2021 기준 코드 보안 분석\n")

    # 테스트 코드 샘플
    test_samples = [
        # Sample 1: Web Application with Multiple Vulnerabilities
        {
            "name": "User Management API",
            "language": "Python",
            "code": """
from flask import Flask, request, session
import sqlite3
import os
import pickle

app = Flask(__name__)
app.secret_key = "supersecret123"

DATABASE = "users.db"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check credentials
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['is_admin'] = user[3]
        return "Login successful"
    else:
        return "Login failed"

@app.route('/admin/users')
def admin_users():
    # Admin panel
    if session.get('is_admin'):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return str(cursor.fetchall())
    return "Unauthorized"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('/uploads', filename))
    return "File uploaded successfully"

@app.route('/api/user/<user_id>')
def get_user(user_id):
    # Get user data
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id={user_id}"
    cursor.execute(query)
    return str(cursor.fetchone())

@app.route('/download')
def download_file():
    filename = request.args.get('file')
    with open(filename, 'rb') as f:
        return f.read()

@app.route('/deserialize')
def load_session():
    data = request.args.get('session_data')
    obj = pickle.loads(data.encode())
    return str(obj)

if __name__ == '__main__':
    app.run(debug=True)
"""
        },

        # Sample 2: Cryptocurrency Wallet (More focused)
        {
            "name": "Crypto Wallet",
            "language": "Python",
            "code": """
import hashlib
import requests

class CryptoWallet:
    def __init__(self, user_id):
        self.user_id = user_id
        self.api_endpoint = "https://api.crypto-service.com"

    def generate_address(self):
        # Generate new crypto address
        seed = str(self.user_id) + "staticSalt"
        address = hashlib.md5(seed.encode()).hexdigest()
        return address

    def get_balance(self, address):
        # Check balance from external API
        url = f"{self.api_endpoint}/balance?address={address}"
        response = requests.get(url, verify=False)
        return response.json()

    def transfer(self, from_addr, to_addr, amount):
        # Transfer funds
        # No signature verification
        url = f"{self.api_endpoint}/transfer"
        data = {
            'from': from_addr,
            'to': to_addr,
            'amount': amount
        }
        response = requests.post(url, json=data, verify=False)
        return response.json()

    def import_wallet(self, backup_data):
        # Import wallet from backup
        exec(backup_data)  # Execute backup script
        return "Wallet imported"

# Usage
wallet = CryptoWallet(user_id=12345)
address = wallet.generate_address()
print(f"Your address: {address}")
"""
        },

        # Sample 3: IoT Device Controller
        {
            "name": "IoT Device Controller",
            "language": "Python",
            "code": """
import subprocess
import json

class SmartHomeController:
    def __init__(self):
        self.devices = {}
        self.admin_password = "admin123"

    def authenticate(self, password):
        if password == self.admin_password:
            return True
        return False

    def execute_command(self, device_id, command):
        # Execute command on IoT device
        if device_id not in self.devices:
            return "Device not found"

        # Execute system command
        result = subprocess.run(
            f"iot-control {device_id} {command}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout

    def update_firmware(self, device_id, firmware_url):
        # Download and install firmware
        subprocess.run(f"wget {firmware_url} -O /tmp/firmware.bin", shell=True)
        subprocess.run(f"flash-device {device_id} /tmp/firmware.bin", shell=True)
        return "Firmware updated"

    def get_device_logs(self, device_id, log_file):
        # Read device logs
        with open(log_file, 'r') as f:
            logs = f.read()
        return logs

    def save_config(self, config_data):
        # Save configuration
        config = json.loads(config_data)
        with open('device_config.json', 'w') as f:
            json.dump(config, f)
        return "Config saved"

# API endpoint (simplified)
def handle_request(request_data):
    controller = SmartHomeController()

    action = request_data.get('action')
    password = request_data.get('password')

    if not controller.authenticate(password):
        return {"error": "Authentication failed"}

    if action == 'execute':
        return controller.execute_command(
            request_data['device_id'],
            request_data['command']
        )
    elif action == 'update':
        return controller.update_firmware(
            request_data['device_id'],
            request_data['firmware_url']
        )
    elif action == 'logs':
        return controller.get_device_logs(
            request_data['device_id'],
            request_data['log_file']
        )
"""
        },
    ]

    # 각 샘플에 대해 OWASP 검사 수행
    for i, sample in enumerate(test_samples, 1):
        print("="*60)
        print(f"{i}. {sample['name']}")
        print("="*60)
        print(f"Language: {sample['language']}")
        print(f"\nCode:\n{sample['code'][:300]}...\n")

        print("Running OWASP Top 10 Analysis...\n")

        result = check_owasp_vulnerabilities(sample['code'], sample['language'])

        print("="*60)
        print("OWASP Top 10 2021 Assessment Report")
        print("="*60)
        print(result['owasp_report'])
        print("\n\n")

    # OWASP Top 10 교육 자료 생성
    print("="*60)
    print("OWASP Top 10 2021 - Detailed Explanation")
    print("="*60)

    education_prompt = """Provide a comprehensive educational guide on OWASP Top 10 2021:

For each category:

1. **What it is**
   - Clear definition
   - Why it matters
   - Real-world impact

2. **Common Scenarios**
   - Typical vulnerable code patterns
   - Attack examples
   - Exploitation techniques

3. **Detection Methods**
   - Code review checklist
   - Automated tool support
   - Manual testing approaches

4. **Prevention Best Practices**
   - Secure coding patterns
   - Framework-specific guidance
   - Configuration recommendations

5. **Testing & Validation**
   - How to test for it
   - Security test cases
   - Verification methods

Make this practical and actionable for developers."""

    education = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": education_prompt}]
    )

    print(education.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Automated OWASP Checking in CI/CD")
    print("="*60)

    cicd_prompt = """Design a CI/CD pipeline integration for OWASP security checking:

Include:
1. Pipeline stages for security
2. Tool selection and integration
   - SAST tools (Semgrep, SonarQube, Bandit)
   - DAST tools (OWASP ZAP, Burp)
   - Dependency scanning (Snyk, OWASP Dependency-Check)
   - Secret detection (GitGuardian, TruffleHog)

3. Quality gates and thresholds
4. Failure handling
5. Reporting and dashboards
6. Developer feedback loop
7. Exception/waiver process
8. Metrics and KPIs

Provide practical implementation guide."""

    cicd_guide = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": cicd_prompt}]
    )

    print(cicd_guide.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Summary: OWASP Top 10 in LLM Era")
    print("="*60)
    print("""
OWASP Top 10 2021 Quick Reference:

**A01:2021 – Broken Access Control** ⬆️ (moved from #5)
- Missing function level access control
- Insecure direct object references
- IDOR vulnerabilities
- Privilege escalation

**A02:2021 – Cryptographic Failures** (was Sensitive Data Exposure)
- Weak encryption algorithms
- Poor key management
- Transmitting data in clear text
- Weak random number generation

**A03:2021 – Injection** ⬇️ (dropped from #1)
- SQL, NoSQL, OS command injection
- LDAP, XPath injection
- Still critical despite drop in ranking

**A04:2021 – Insecure Design** 🆕
- Missing security controls by design
- Threat modeling failures
- Insecure design patterns
- Focus on pre-code activities

**A05:2021 – Security Misconfiguration**
- Default configurations
- Incomplete configurations
- Open cloud storage
- Verbose error messages

**A06:2021 – Vulnerable and Outdated Components**
- Using components with known vulnerabilities
- Unsupported/outdated software
- Not scanning for vulnerabilities
- Not updating in timely fashion

**A07:2021 – Identification and Authentication Failures**
- Weak password policies
- Credential stuffing
- Session management flaws
- Missing MFA

**A08:2021 – Software and Data Integrity Failures** 🆕
- Insecure CI/CD pipeline
- Auto-update without integrity verification
- Insecure deserialization
- Untrusted data in critical flows

**A09:2021 – Security Logging and Monitoring Failures**
- Insufficient logging
- Logs not monitored
- Inadequate incident response
- Missing detection mechanisms

**A10:2021 – Server-Side Request Forgery (SSRF)** 🆕
- Fetching remote resources without validation
- URL validation bypass
- Cloud metadata access
- Internal service access

**LLM Impact on OWASP Top 10:**

Increased Risk:
- A03: LLMs may generate injection-vulnerable code
- A02: Weak crypto in LLM-generated code
- A07: Insecure auth patterns
- A04: LLMs lack security design context

Mitigation Opportunities:
- LLMs can help identify vulnerabilities
- Automated code review
- Security education
- Pattern recognition

**Security Tools Ecosystem:**

SAST (Static Analysis):
- SonarQube
- Semgrep
- Checkmarx
- Veracode
- Fortify

DAST (Dynamic Analysis):
- OWASP ZAP
- Burp Suite Professional
- Acunetix
- Netsparker

SCA (Composition Analysis):
- Snyk
- Black Duck
- WhiteSource
- OWASP Dependency-Check

IAST (Interactive):
- Contrast Security
- Hdiv Security
- Seeker

**Implementation Roadmap:**

Phase 1: Foundation (Weeks 1-4)
□ Establish security baseline
□ Integrate basic SAST tools
□ Developer training
□ Define quality gates

Phase 2: Enhancement (Weeks 5-12)
□ Add DAST scanning
□ Dependency scanning
□ Secret detection
□ Enhanced reporting

Phase 3: Maturation (Months 4-6)
□ Fine-tune thresholds
□ Custom security rules
□ Advanced testing
□ Metrics and dashboards

Phase 4: Optimization (Ongoing)
□ Continuous improvement
□ Tool updates
□ Process refinement
□ Knowledge sharing

**Success Metrics:**

Leading Indicators:
- Vulnerabilities found in development
- Time to fix vulnerabilities
- Security test coverage
- Developer security training completion

Lagging Indicators:
- Vulnerabilities found in production
- Security incidents
- Time to detect incidents
- Remediation time

**Best Practices:**

✅ Integrate security early (shift-left)
✅ Automate security testing
✅ Provide fast developer feedback
✅ Security as enabler, not blocker
✅ Continuous monitoring and improvement

❌ Security as afterthought
❌ Manual-only testing
❌ Slow feedback loops
❌ Blocking without guidance
❌ Set-and-forget tools

**Resources:**
- OWASP Top 10: https://owasp.org/Top10/
- OWASP ASVS: Application Security Verification Standard
- OWASP Testing Guide
- CWE Top 25
- SANS Top 25

**Next Steps:**
- Chapter 18: Security Awareness Training
- Chapter 24: Red Teaming
- Chapter 25: Security Standards
""")


if __name__ == "__main__":
    main()
