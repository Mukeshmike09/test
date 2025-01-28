import subprocess
import argparse
import yaml
#test2   tyhfvdfvdvdfhtdgtgrttgtgtggrtgeerd
def run_command(command, *args):

    print("=============================================================".center(100, ' '))
    print(f"Running Command: {command} {' '.join(args)}".center(100, ' '))
    print("=============================================================\n".center(100, ' '))
    process = subprocess.Popen([command] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    print(f"{stdout.strip()} {stderr.strip() }\n")
    return return_code, stdout.strip(), stderr.strip()


def perform_test(test_config, ip_address):
    args = [arg.format(ip_address=ip_address) for arg in test_config['args']]
    return_code, stdout, stderr = run_command(test_config['command'], *args)
    result = "PASS" if return_code == 0 else "FAIL"
    logs = stdout if stdout else stderr
    logs = logs.replace('\n', '<br>')  # Replace newline with HTML line break
    #ip_port = f"{ip_address}/{test_config.get('port', '')}"
    ip_port = f"{ip_address}"
    print("=====================".center(100, ' '))
    print(f"Result = {result}".center(100, ' '))
    print("=====================".center(100, ' '))
    return (result, logs), ip_port, (test_config['command'], *args)

def generate_report(ip_address, tests):
    report = []
    total_tests = 0
    total_pass = 0

    for test_config in tests:
        (result, logs), ip_port, command_args = perform_test(test_config, ip_address)
        report.append((test_config['name'], result, logs, ip_port, command_args, test_config['desc']))
    # Generate HTML report
        total_tests += 1
        if result == "PASS":
            total_pass += 1
    total_fail = total_tests - total_pass
    # Generate HTML report

    html_report = "<html><head><title>Network Test Report</title><style>"
    html_report += "table {border-collapse: collapse; width: 100%;}"
    html_report += "th, td {padding: 8px; text-align: left; border-bottom: 1px solid #ddd;}"
    html_report += "th {background-color: #f2f2f2;}"
    html_report += ".total-header {font-size: 24px; font-weight: bold;}"
    html_report += ".total-table {border-collapse: collapse; width: 50%; margin-top: 20px;}"
    html_report += ".total-table th, .total-table td {padding: 8px; text-align: left;}"
    html_report += ".pass {color: green; font-weight: bold;}"
    html_report += ".fail {color: red; font-weight: bold;}"
    html_report += "</style></head><body>"
    html_report += "<h1>Network Test Report</h1>"

    # Add total tests count
    html_report += "<div class='total-header'>Total Tests</div>"
    html_report += "<table class='total-table'>"
    html_report += "<tr><th>Total Tests</th><th>Total Passed</th><th>Total Failed</th></tr>"
    html_report += f"<tr><td>{total_tests}</td><td class='pass'>{total_pass}</td><td class='fail'>{total_fail}</td></tr>"
    html_report += "</table>"

    html_report += "<html><head><title>Network Test Report</title><style>table {background-color: lightblue;}</style></head><body><table border='1'><tr><th>Action</th><th>Result</th><th>Logs</th><th>TARGET IP</th><th>Command</th><th>Descriptions</th></tr>"
    for idx, (action, result, logs, ip_port, command_args, desc) in enumerate(report, start=1):
        command_args= ' '.join(command_args)
        html_report += f"<tr><td>{idx}) {action}</td><td>{result}</td><td>{logs}</td><td>{ip_port}</td><td>{command_args}</td><td>{desc}</td></tr>"
    html_report += "</table></body></html>"

    return html_report

def main():
    parser = argparse.ArgumentParser(description='Perform network tests using Hping.')
    parser.add_argument('ip_address', type=str, help='IP address to perform tests on')
    parser.add_argument('config_file', type=str, help='Path to YAML config file')
    args = parser.parse_args()

    ip_address = args.ip_address
    config_file = args.config_file

    with open(config_file, 'r') as f:
        tests = yaml.safe_load(f)['tests']

    html_report = generate_report(ip_address, tests)
    with open("network_test_report.html", "w") as f:
        f.write(html_report)

if __name__ == "__main__":
    main()

