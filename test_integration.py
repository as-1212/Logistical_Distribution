"""
Integration Tests for Smart Logistics Dashboard
Tests backend API, frontend connectivity, and ML engine integration
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
TIMEOUT = 5

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, message=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"  {status} - {name}")
    if message:
        print(f"           {message}")

def test_backend_health():
    """Test 1: Backend is running"""
    print(f"\n{Colors.BLUE}Test 1: Backend Health Check{Colors.END}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=TIMEOUT)
        passed = response.status_code == 200
        print_test(
            "Backend health check",
            passed,
            f"Status: {response.status_code}"
        )
        return passed
    except Exception as e:
        print_test("Backend health check", False, str(e))
        return False

def test_dashboard_api():
    """Test 2: Dashboard API endpoint"""
    print(f"\n{Colors.BLUE}Test 2: Dashboard API{Colors.END}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/dashboard", timeout=TIMEOUT)
        passed = response.status_code == 200 and 'kpi' in response.json()
        print_test(
            "Dashboard data retrieval",
            passed,
            f"Status: {response.status_code}, Contains KPI: {'kpi' in response.json()}"
        )
        return passed
    except Exception as e:
        print_test("Dashboard data retrieval", False, str(e))
        return False

def test_alerts_api():
    """Test 3: Alerts API endpoint"""
    print(f"\n{Colors.BLUE}Test 3: Alerts API{Colors.END}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/alerts", timeout=TIMEOUT)
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test(
            "Alerts data retrieval",
            passed,
            f"Status: {response.status_code}, Alert count: {len(response.json())}"
        )
        return passed
    except Exception as e:
        print_test("Alerts data retrieval", False, str(e))
        return False

def test_map_api():
    """Test 4: Map data API endpoint"""
    print(f"\n{Colors.BLUE}Test 4: Map Data API{Colors.END}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/map", timeout=TIMEOUT)
        passed = response.status_code == 200
        data = response.json()
        has_states = 'states' in data or isinstance(data, list)
        print_test(
            "Map data retrieval",
            passed and has_states,
            f"Status: {response.status_code}, Has state data: {has_states}"
        )
        return passed and has_states
    except Exception as e:
        print_test("Map data retrieval", False, str(e))
        return False

def test_cors_headers():
    """Test 5: CORS headers are set"""
    print(f"\n{Colors.BLUE}Test 5: CORS Configuration{Colors.END}")
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/health",
            timeout=TIMEOUT,
            headers={'Origin': 'http://localhost:3001'}
        )
        has_cors = 'Access-Control-Allow-Origin' in response.headers
        print_test(
            "CORS headers present",
            has_cors,
            f"CORS origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}"
        )
        return has_cors
    except Exception as e:
        print_test("CORS headers present", False, str(e))
        return False

def test_error_handling():
    """Test 6: Error handling for invalid routes"""
    print(f"\n{Colors.BLUE}Test 6: Error Handling{Colors.END}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/invalid-endpoint", timeout=TIMEOUT)
        passed = response.status_code == 404
        print_test(
            "404 error handling",
            passed,
            f"Status code: {response.status_code} (expected 404)"
        )
        return passed
    except Exception as e:
        print_test("404 error handling", False, str(e))
        return False

def test_json_content_type():
    """Test 7: API returns JSON content"""
    print(f"\n{Colors.BLUE}Test 7: Content Type Check{Colors.END}")
    try:
        response = requests.get(f"{BACKEND_URL}/api/dashboard", timeout=TIMEOUT)
        is_json = 'application/json' in response.headers.get('Content-Type', '')
        print_test(
            "JSON content type",
            is_json,
            f"Content-Type: {response.headers.get('Content-Type', 'Not set')}"
        )
        return is_json
    except Exception as e:
        print_test("JSON content type", False, str(e))
        return False

def run_all_tests():
    """Run all integration tests"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"Smart Logistics Integration Tests")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}{Colors.END}\n")
    
    # Wait for backend to be ready
    print(f"{Colors.YELLOW}Waiting for backend to be ready...{Colors.END}")
    max_retries = 30
    for i in range(max_retries):
        try:
            requests.get(f"{BACKEND_URL}/api/health", timeout=2)
            print(f"{Colors.GREEN}Backend is ready!{Colors.END}\n")
            break
        except:
            if i < max_retries - 1:
                print(f"  Retry {i+1}/{max_retries}...")
                time.sleep(1)
            else:
                print(f"{Colors.RED}Backend not responding after {max_retries} retries{Colors.END}")
                return False
    
    # Run tests
    tests = [
        test_backend_health,
        test_dashboard_api,
        test_alerts_api,
        test_map_api,
        test_cors_headers,
        test_error_handling,
        test_json_content_type
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"{Colors.RED}Error running test: {e}{Colors.END}")
            results.append(False)
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}{Colors.END}")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{Colors.GREEN}✓ All {total} tests passed!{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}✗ {total - passed} out of {total} tests failed{Colors.END}")
        return False

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
