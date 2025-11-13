"""
Automated Test Runner for RISC-V Simulator
Runs all test cases and validates results
"""
import os
import sys
import subprocess
from pathlib import Path
import re
import json
from datetime import datetime


class TestRunner:
    def __init__(self, test_dir="tests"):
        # Adjust path to be relative to project root
        script_dir = Path(__file__).parent.parent
        self.test_dir = script_dir / test_dir
        self.results = []
        self.passed = 0
        self.failed = 0
        self.total = 0
        
    def find_test_files(self):
        """Find all test .asm files"""
        if not self.test_dir.exists():
            print(f"Test directory '{self.test_dir}' not found!")
            return []
        
        test_files = list(self.test_dir.glob("test_*.asm"))
        test_files.sort()
        return test_files
    
    def parse_expected_results(self, test_file):
        """
        Parse expected results from test file comments
        Format: # EXPECT: x1=10, x2=20, x3=30
        """
        expected = {}
        try:
            with open(test_file, 'r') as f:
                content = f.read()
                
            # Look for EXPECT comments
            expect_pattern = r'#\s*EXPECT:\s*(.+?)(?:\n|$)'
            matches = re.findall(expect_pattern, content, re.IGNORECASE)
            
            for match in matches:
                # Parse register expectations: x1=10, x2=20
                reg_pattern = r'([xX]\d+|[a-zA-Z]+\d*)\s*=\s*(-?\d+|0x[0-9a-fA-F]+)'
                for reg, value in re.findall(reg_pattern, match):
                    reg = reg.upper()
                    if value.startswith('0x'):
                        expected[reg] = int(value, 16)
                    else:
                        expected[reg] = int(value)
        except Exception as e:
            print(f"Warning: Could not parse expectations from {test_file}: {e}")
        
        return expected
    
    def run_test_with_main_real(self, test_file):
        """Run test using main_real.py simulator"""
        try:
            # Import simulator components
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from src.main_real import RISCVSimulator
            from src.memory import Memory
            from src.logger import logger
            
            # Create simulator instance
            sim = RISCVSimulator()
            
            # Parse program
            success = sim.load_program(str(test_file))
            if not success:
                return {
                    'success': False,
                    'error': 'Failed to parse test file',
                    'registers': {}
                }
            
            # Run simulation (catch output)
            try:
                # Redirect stdout to capture output
                from io import StringIO
                old_stdout = sys.stdout
                sys.stdout = captured_output = StringIO()
                
                sim.run(max_instructions=1000)
                
                # Restore stdout
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
            except Exception as e:
                sys.stdout = old_stdout
                if "ECALL" not in str(e) and "HALT" not in str(e):
                    raise
            
            # Extract register values
            registers = {}
            if sim.regs:
                for i in range(32):
                    reg_name = f"X{i}"
                    # Access register by name, not index
                    registers[reg_name] = sim.regs[reg_name]
            
            return {
                'success': True,
                'error': None,
                'registers': registers,
                'instructions_executed': len(sim.instructions)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'registers': {}
            }
    
    def validate_results(self, expected, actual_registers):
        """Validate actual results against expected"""
        mismatches = []
        
        for reg, expected_val in expected.items():
            reg = reg.upper()
            actual_val = actual_registers.get(reg, None)
            
            # Convert negative expected values to 32-bit unsigned for comparison
            # RISC-V stores all values as unsigned 32-bit, using two's complement for negatives
            if expected_val < 0:
                expected_val = expected_val & 0xFFFFFFFF
            
            if actual_val is None:
                mismatches.append(f"{reg}: expected={expected_val}, actual=UNDEFINED")
            elif actual_val != expected_val:
                mismatches.append(f"{reg}: expected={expected_val}, actual={actual_val}")
        
        return len(mismatches) == 0, mismatches
    
    def run_single_test(self, test_file):
        """Run a single test file"""
        test_name = test_file.stem
        print(f"\n{'='*80}")
        print(f"Running: {test_name}")
        print(f"{'='*80}")
        
        # Parse expected results
        expected = self.parse_expected_results(test_file)
        
        # Run test
        result = self.run_test_with_main_real(test_file)
        
        # Validate
        if not result['success']:
            status = "FAILED"
            error_msg = result['error']
            validation_passed = False
            mismatches = []
        elif expected:
            validation_passed, mismatches = self.validate_results(expected, result['registers'])
            status = "PASSED" if validation_passed else "FAILED"
            error_msg = None
        else:
            # No expectations, just check if it ran
            status = "PASSED"
            validation_passed = True
            mismatches = []
            error_msg = None
        
        # Print results
        if status == "PASSED":
            print(f"✓ {test_name}: PASSED")
            self.passed += 1
        else:
            print(f"✗ {test_name}: FAILED")
            self.failed += 1
            if error_msg:
                print(f"  Error: {error_msg}")
            if mismatches:
                print(f"  Register mismatches:")
                for mismatch in mismatches:
                    print(f"    {mismatch}")
        
        # Show some register values
        if result['registers']:
            non_zero_regs = {k: v for k, v in result['registers'].items() 
                           if v != 0 and k != 'X0'}
            if non_zero_regs:
                print(f"  Non-zero registers:")
                for reg, val in sorted(non_zero_regs.items())[:10]:
                    print(f"    {reg} = {val} (0x{val:08X})")
        
        self.total += 1
        
        # Store result
        self.results.append({
            'test': test_name,
            'status': status,
            'expected': expected,
            'actual': {k: v for k, v in result['registers'].items() if v != 0},
            'error': error_msg,
            'mismatches': mismatches,
            'instructions_executed': result.get('instructions_executed', 0)
        })
        
        return status == "PASSED"
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("="*80)
        print("RISC-V SIMULATOR - AUTOMATED TEST SUITE")
        print("="*80)
        
        test_files = self.find_test_files()
        
        if not test_files:
            print("No test files found!")
            return
        
        print(f"\nFound {len(test_files)} test files")
        
        # Run each test
        for test_file in test_files:
            try:
                self.run_single_test(test_file)
            except Exception as e:
                print(f"✗ {test_file.stem}: CRASHED - {e}")
                self.failed += 1
                self.total += 1
                self.results.append({
                    'test': test_file.stem,
                    'status': 'CRASHED',
                    'error': str(e)
                })
        
        # Print summary
        self.print_summary()
        
        # Save results
        self.save_results()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {self.total}")
        print(f"Passed: {self.passed} ({100*self.passed/self.total if self.total > 0 else 0:.1f}%)")
        print(f"Failed: {self.failed} ({100*self.failed/self.total if self.total > 0 else 0:.1f}%)")
        print("="*80)
        
        if self.failed > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if result['status'] != 'PASSED':
                    print(f"  - {result['test']}: {result.get('error', 'Validation failed')}")
    
    def save_results(self):
        """Save test results to JSON file"""
        output_file = "test_results.json"
        
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'total': self.total,
            'passed': self.passed,
            'failed': self.failed,
            'tests': self.results
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(results_data, f, indent=2)
            print(f"\nResults saved to: {output_file}")
        except Exception as e:
            print(f"\nWarning: Could not save results: {e}")


def main():
    """Main entry point"""
    runner = TestRunner(test_dir="tests")
    runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()
